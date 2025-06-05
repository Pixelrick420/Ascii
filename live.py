import cv2
import numpy as np
import time
import sys
import os
from ascii import process, getAscii, printImage
import shutil
MAX_WIDTH = 250  
MAX_HEIGHT = 200  

def cleanup():
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__")

class CameraASCII:
    def __init__(self, camera_device=0, width=160, height=80, fpslimit=15):
        self.camera_device = camera_device
        self.max_width = width
        self.max_height = height
        self.fpslimit = fpslimit
        self.cap = None
        
    def setup(self):
        print(f"Initializing camera device {self.camera_device}...")
        self.cap = cv2.VideoCapture(self.camera_device)
        
        if not self.cap.isOpened():
            print(f"Error: Could not open camera device {self.camera_device}")
            return False
            
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("Camera initialized successfully!")
        return True
    
    def getFeed(self, color=True):
        if not self.setup():
            return
            
        print("Starting live ASCII camera feed...")
        print("Press 'q' or Ctrl+C to quit")
        print(f"Color mode: {'ON' if color else 'OFF'}")
        print("Adjusting for live feed in 3 seconds...")
        time.sleep(3)
        
        frameCount = 0
        fpsTimer = time.time()
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Failed to capture frame")
                    break
                
                frame = cv2.flip(frame, 1)
                frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                imageTuple = process(frameRGB, self.max_width, self.max_height, color)
                asciiData = getAscii(imageTuple, color)
            
                sys.stdout.write("\033[2J\033[H")
                printImage(asciiData, imageTuple[0], color)
                
                frameCount += 1
                if frameCount % 30 == 0:  
                    current_time = time.time()
                    actualFPS = 30 / (current_time - fpsTimer)
                    fpsTimer = current_time
                    print(f"\nFPS: {actualFPS:.1f} | Frames: {frameCount} | Press 'q' to quit")
                
                sys.stdout.flush()
                
                time.sleep(1.0 / self.fpslimit)
                
        except KeyboardInterrupt:
            print("\nStopping camera feed...")
        finally:
            self.cleanup()
    
    def capturePhoto(self, filename="camera_capture.jpg", color=True):
        if not self.setup():
            return
            
        print("Capturing photo...")
        ret, frame = self.cap.read()
        
        if ret:
            frame = cv2.flip(frame, 1)
            cv2.imwrite(filename, frame)
            print(f"Photo saved as {filename}")
            
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imageTuple = process(frameRGB, MAX_WIDTH, MAX_HEIGHT, color)
            asciiData = getAscii(imageTuple, color)
            
            print("\nASCII Version:")
            printImage(asciiData, imageTuple[0], color)
        else:
            print("Error: Failed to capture photo")
            
        self.cleanup()
    
    def cleanup(self):
        if self.cap:
            self.cap.release()
            print("Camera resources released")
        cleanup()

def listCameras():
    print("Scanning for available cameras...")
    availableCameras = []
    
    for i in range(5):  
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                availableCameras.append(i)
                print(f"Camera {i}: Available")
            else:
                print(f"Camera {i}: Detected but not working")
            cap.release()
        else:
            print(f"Camera {i}: Not available")
    
    return availableCameras

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python camera_ascii.py live [--no-color] [--device=0] [--fps=15]")
        print("  python camera_ascii.py photo [--no-color] [--device=0] [filename]")
        print("  python camera_ascii.py list")
        print("\nOptions:")
        print("  --no-color    Disable color output")
        print("  --device=N    Use camera device N (default: 0)")
        print("  --fps=N       Set FPS limit for live feed (default: 15)")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    color = "--no-color" not in sys.argv
    device = 0
    fpslimit = 15
    filename = "camera_capture.jpg"
    
    for arg in sys.argv[2:]:
        if arg.startswith("--device="):
            device = int(arg.split("=")[1])
        elif arg.startswith("--fps="):
            fpslimit = int(arg.split("=")[1])
        elif not arg.startswith("--"):
            filename = arg
    
    if mode == "list":
        available = listCameras()
        if not available:
            print("No working cameras found!")
        else:
            print(f"\nWorking cameras: {available}")
            print(f"Use --device={available[0]} to specify a camera")
    
    elif mode == "live":
        camera = CameraASCII(device, fpslimit=fpslimit)
        camera.getFeed(color)
    
    elif mode == "photo":
        camera = CameraASCII(device)
        camera.capturePhoto(filename, color)
    
    else:
        print(f"Invalid mode: {mode}")
        print("Valid modes: live, photo, list")

if __name__ == "__main__":
    main()