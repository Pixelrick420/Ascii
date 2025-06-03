from PIL import Image
import cv2
import numpy as np
import time
import sys
import os


MAX_WIDTH  = 200
MAX_HEIGHT = 100
CHARS = "@#Woa+=:~-\" `"


def rgbToAnsi(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def resetColor():
    return "\033[0m"


def process(image, maxWidth, maxHeight, color=True):
    if isinstance(image, np.ndarray):
        height, width = image.shape[:2]
        image = Image.fromarray(image)
    else:
        width, height = image.size


    scaleW = maxWidth / width
    scaleH = (maxHeight / (height * 0.8))
    scale  = min(scaleW, scaleH)

    newCols = int(width  * scale)
    newRows = int(height * scale * 0.5)

    newCols = max(1, newCols)
    newRows = max(1, newRows)

    resized = image.resize((newCols, newRows), Image.Resampling.LANCZOS)
    resizedArr = np.array(resized)

    if resizedArr.ndim == 3:
        if color:
            colorData = resizedArr
        else:
            colorData = None
        grayscale = np.dot(resizedArr, [0.299, 0.587, 0.114])
    else:
        colorData = None
        grayscale = resizedArr.astype(float)

    minval = grayscale.min()
    maxval = grayscale.max()
    if maxval != minval:
        contrasted = ((grayscale - minval) * 255 / (maxval - minval)).astype(int)
    else:
        contrasted = grayscale.astype(int)

    return newCols, newRows, contrasted, colorData

def getAscii(imageTuple, color=True):
    pixels    = imageTuple[2]
    colorData = imageTuple[3] if len(imageTuple) > 3 else None

    length = len(CHARS) - 1
    indices = np.clip(pixels * length // 255, 0, length).astype(int)
    asciiChars = np.array(list(CHARS))[indices]

    if color and (colorData is not None):
        flatChars  = asciiChars.flatten()
        flatColors = colorData.reshape(-1, 3)
        return flatChars, flatColors
    else:
        return ''.join(asciiChars.flatten()), None

def printImage(asciiData, widthChars, color=True):
    if color and isinstance(asciiData, tuple):
        chars, colors = asciiData
        total = len(chars)
        rows = total // widthChars

        for r in range(rows):
            line = ""
            for c in range(widthChars):
                idx = r * widthChars + c
                r_, g_, b_ = colors[idx]
                ch = chars[idx]
                line += f"{rgbToAnsi(r_, g_, b_)}{ch}{resetColor()}"
            print(line)
    else:
        asciiStr = asciiData if isinstance(asciiData, str) else asciiData[0]
        lines = [asciiStr[i:i + widthChars] for i in range(0, len(asciiStr), widthChars)]
        print('\n'.join(lines))

    sys.stdout.flush()

def imageToAscii(path, color=True):
    print("Starting ASCII conversion for:", path)
    print(f"Color mode: {'ON' if color else 'OFF'}")
    sys.stdout.flush()

    try:
        image = Image.open(path).convert("RGB")
        print(f"Image loaded successfully: {image.size}")
        sys.stdout.flush()
    except Exception as e:
        print("Error while opening image:", e)
        return

    newCols, newRows, contrasted, colorData = process(image, MAX_WIDTH, MAX_HEIGHT, color)
    asciiData = getAscii((newCols, newRows, contrasted, colorData), color)

    if color and isinstance(asciiData, tuple):
        print(f"ASCII conversion complete, total chars: {len(asciiData[0])}")
    else:
        print(f"ASCII conversion complete, total chars: {len(asciiData)}")
    sys.stdout.flush()

    printImage(asciiData, newCols, color)


def videoToAscii(path, color=True):
    print("Starting ASCII conversion for:", path)
    print(f"Color mode: {'ON' if color else 'OFF'}")
    sys.stdout.flush()

    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print("Could not open video.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30.0

    totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, int(fps // 10))

    frames = []
    readFrames = 0
    barLen = 40

    print(f"Video info: FPS={fps}, Total frames={totalFrames}, Step={step}")
    sys.stdout.flush()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if readFrames % step == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imageTuple = process(frame_rgb, MAX_WIDTH, MAX_HEIGHT, color)
            asciiData  = getAscii(imageTuple, color)
            frames.append((asciiData, imageTuple[0])) 

            progress = min(readFrames / max(1, totalFrames), 1.0)
            filled   = int(progress * barLen)
            sys.stdout.write(
                "\rProgress: [{}{}] {:.1f}%".format(
                    "=" * filled, " " * (barLen - filled), progress * 100
                )
            )
            sys.stdout.flush()

        readFrames += 1

    cap.release()
    print(f"\nProcessed {len(frames)} frames")
    sys.stdout.flush()

    try:
        while True:
            for asciiData, widthChars in frames:
                sys.stdout.write("\033[2J\033[H")
                printImage(asciiData, widthChars, color)
                sys.stdout.write(
                    "Progress: [{}{}] 100.0%\n".format("=" * barLen, "")
                )
                sys.stdout.flush()
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ascii.py <image|video> <filepath> [--no-color]")
        sys.exit(1)

    mode, path = sys.argv[1], sys.argv[2]
    color       = "--no-color" not in sys.argv

    print(f"Mode: {mode}, Path: {path}")
    print(f"File exists: {os.path.exists(path)}")
    print(f"Color enabled: {color}")
    sys.stdout.flush()

    if mode == "image":
        imageToAscii(path, color=color)
    elif mode == "video":
        videoToAscii(path, color=color)
    else:
        print(f"Invalid mode: {mode}")
        sys.exit(1)