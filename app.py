import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import shutil
import sys
import platform

def getGeometry(size):
    maxWidth, _ = shutil.get_terminal_size()
    termWidth = size if size < maxWidth else maxWidth
    termHeight = int(termWidth * 0.5)
    return (termWidth, termHeight)

def getFontSizeCommands(system):
    if system == "windows":
        return {
            "wt_profile": '--fontSize=8 --fontFace="Consolas"',
            "powershell": '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8;',
            "cmd": '',
        }
    elif system == "linux":
        return {
            "escapeSeq": '\033]50;xft:monospace:size=8\007', 
            "konsole": 'qdbus $KONSOLE_DBUS_SERVICE $KONSOLE_DBUS_SESSION setProfile "Small Font" 2>/dev/null || ',
            "gnome": 'gsettings set org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:default/ font "Monospace 8" 2>/dev/null || '
        }
    return {}

def launch(scriptPath, mode, filePath, cols, lines, color=True, device=0, fps=15):
    isColor = "" if color else " --no-color"
    
    system = platform.system().lower()
    fontCmds = getFontSizeCommands(system)
    
    pythonAlias = sys.executable
    
    if mode == "live":
        baseCmd = f'"{pythonAlias}" "{scriptPath}" live{isColor} --device={device} --fps={fps}'
    elif mode == "photo":
        baseCmd = f'"{pythonAlias}" "{scriptPath}" photo{isColor} --device={device}'
    else:
        baseCmd = f'"{pythonAlias}" "{scriptPath}" "{mode}" "{filePath}"{isColor}'

    print(f"Launching command: {baseCmd}")
    print(f"System: {system}")
    
    if system == "windows":
        return launchWindows(baseCmd, fontCmds)
    elif system == "linux":
        return launchLinux(baseCmd, fontCmds)
    else:
        print(f"Unsupported operating system: {system}")
        return runDirectly(scriptPath, mode, filePath, color, device, fps)

def launchWindows(command, fontCmds):
    terminals = [
        ("wt", "Windows Terminal"),
        ("powershell", "PowerShell"),
        ("cmd", "Command Prompt")
    ]
    
    for terminal, name in terminals:
        try:
            if terminal == "wt":
                wt_args = [
                    "wt",
                    "--profile", "Command Prompt",
                    "--startingDirectory", os.getcwd(),
                    "cmd", "/k"
                ]
                fullCmd = f"{fontCmds.get('cmd', '')}{command}"
                wt_args.append(fullCmd)
                subprocess.Popen(wt_args)
                print(f"Launched with {name} (font size: 8)")
                return True
            
            elif terminal == "powershell":
                psSetup = fontCmds.get('powershell', '')
                escaped = command.replace("'", "''")  
                fullCmd = f"cd '{os.getcwd()}'; {psSetup} & cmd /c \"{escaped}\""
                
                subprocess.Popen([
                    "powershell",
                    "-NoProfile"
                    "-NoExit",
                    "-Command", fullCmd
                ])
                print(f"Launched with {name} (console adjusted)")
                return True
            
            
            elif terminal == "cmd":
                modeCmd = fontCmds.get('cmd', '')
                fullCmd = f"cd /d \"{os.getcwd()}\" && {modeCmd}{command}"
                subprocess.Popen(["cmd", "/k", fullCmd])
                print(f"Launched with {name} (size adjusted)")
                return True
            
        except FileNotFoundError:
            print(f"{name} not found, trying next...")
            continue

        except Exception as e:
            print(f"Error launching {name}: {e}")
            continue
    
    return False

def launchLinux(command, fontCmds):
    terminals = [
        ("konsole", ["konsole", "--hold", "--workdir", os.getcwd()]),
        ("gnome-terminal", ["gnome-terminal", f"--working-directory={os.getcwd()}"]),
        ("xfce4-terminal", ["xfce4-terminal", "--working-directory", os.getcwd(), "--hold"]),
        ("mate-terminal", ["mate-terminal", "--working-directory", os.getcwd()]),
        ("xterm", ["xterm", "-hold", "-fs", "8"]),
        ("x-terminal-emulator", ["x-terminal-emulator"])
    ]
    
    for terminalName, baseCmd in terminals:
        try:
            if terminalName == "konsole":
                fontSetup = fontCmds.get('konsole', '')
                fullCmd = f"{fontSetup}printf '{fontCmds.get('escapeSeq', '')}' && {command}"
                cmd = baseCmd + ["-e", "bash", "-c", fullCmd]
                subprocess.Popen(cmd)

            elif terminalName == "gnome-terminal":
                fontSetup = fontCmds.get('gnome', '')
                escapeSeq = fontCmds.get('escapeSeq', '')
                fullCmd = f"{fontSetup}printf '{escapeSeq}' && {command}; read -p 'Press Enter to close...'"
                cmd = baseCmd + ["--", "bash", "-c", fullCmd]
                subprocess.Popen(cmd)

            elif terminalName == "xterm":
                escapeSeq = fontCmds.get('escapeSeq', '')
                fullCmd = f"printf '{escapeSeq}' && {command}"
                cmd = baseCmd + ["-e", "bash", "-c", fullCmd]
                subprocess.Popen(cmd)
            else:
                escapeSeq = fontCmds.get('escapeSeq', '')
                if "hold" in baseCmd:
                    fullCmd = f"printf '{escapeSeq}' && {command}"
                    cmd = baseCmd + ["-e", "bash", "-c", fullCmd]
                else:
                    fullCmd = f"printf '{escapeSeq}' && {command}; read -p 'Press Enter to close...'"
                    cmd = baseCmd + ["-e", "bash", "-c", fullCmd]
                subprocess.Popen(cmd)
            
            print(f"Launched with {terminalName} (font adjusted)")
            return True
        
        except FileNotFoundError:
            print(f"{terminalName} not found, trying next...")
            continue

        except Exception as e:
            print(f"Error launching {terminalName}: {e}")
            continue
    
    return False

def runDirectly(scriptPath, mode, filePath, color, device=0, fps=15):
    print("No suitable terminal found, running directly...")
    try:
        if mode == "live":
            args = [sys.executable, scriptPath, "live", f"--device={device}", f"--fps={fps}"]
        elif mode == "photo":
            args = [sys.executable, scriptPath, "photo", f"--device={device}"]
        else:
            args = [sys.executable, scriptPath, mode, filePath]
        
        if not color:
            args.append("--no-color")
        subprocess.run(args)
        return True
    
    except Exception as e:
        messagebox.showerror("Error", f"Could not run script: {e}")
        return False

def openFile(mode, color=True):
    filetypes = [
        ("Image files", "*.jpg *.jpeg *.png *.bmp *.webp") if mode == "image" else
        ("Video files", "*.mp4 *.avi *.mov *.mkv *.webm")
    ]

    filepath = filedialog.askopenfilename(title="Select a file", filetypes=filetypes)
    if not filepath:
        return

    if not os.path.exists(filepath):
        messagebox.showerror("Error", "Selected file doesn't exist.")
        return

    scriptPath = os.path.abspath("ascii.py")
    
    if not os.path.exists(scriptPath):
        messagebox.showerror("Error", f"ascii.py not found at {scriptPath}")
        return

    print(f"File selected: {filepath}")
    print(f"Script path: {scriptPath}")
    print(f"Color enabled: {color}")
    print(f"Operating System: {platform.system()}")
    
    success = launch(scriptPath, mode, filepath, 0, 0, color)
    if not success:
        runDirectly(scriptPath, mode, filepath, color)

def launchCamera(mode, color=True, device=0, fps=15):
    scriptPath = os.path.abspath("live.py")
    
    if not os.path.exists(scriptPath):
        messagebox.showerror("Error", f"live.py not found at {scriptPath}")
        return

    print(f"Camera mode: {mode}")
    print(f"Script path: {scriptPath}")
    print(f"Color enabled: {color}")
    print(f"Device: {device}, FPS: {fps}")
    print(f"Operating System: {platform.system()}")
    
    success = launch(scriptPath, mode, "", 0, 0, color, device, fps)
    if not success:
        runDirectly(scriptPath, mode, "", color, device, fps)

def build():
    root = tk.Tk()
    root.title("ASCII Media Converter")
    root.geometry("500x400")
    root.resizable(False, False)

    title = tk.Label(root, text="ASCII Converter", font=("Arial", 16, "bold"))
    title.pack(pady=10)

    sysLabel = tk.Label(root, text=f"System: {platform.system()} {platform.release()}", 
                       font=("Arial", 9), fg="gray")
    sysLabel.pack(pady=2)

    optionsFrame = tk.LabelFrame(root, text="Options", font=("Arial", 10))
    optionsFrame.pack(pady=10, padx=20, fill="x")

    colorVar = tk.BooleanVar(value=True)
    colorCheck = tk.Checkbutton(optionsFrame, text="Enable Colors", variable=colorVar, 
                               font=("Arial", 10))
    colorCheck.pack(anchor="w", padx=10, pady=5)

    cameraFrame = tk.Frame(optionsFrame)
    cameraFrame.pack(fill="x", padx=10, pady=5)

    tk.Label(cameraFrame, text="Camera Device:", font=("Arial", 9)).pack(side="left")
    deviceVar = tk.StringVar(value="0")
    deviceEntry = tk.Entry(cameraFrame, textvariable=deviceVar, width=5)
    deviceEntry.pack(side="left", padx=5)

    tk.Label(cameraFrame, text="FPS:", font=("Arial", 9)).pack(side="left", padx=(20,0))
    fpsVar = tk.StringVar(value="15")
    fpsEntry = tk.Entry(cameraFrame, textvariable=fpsVar, width=5)
    fpsEntry.pack(side="left", padx=5)

    mainFrame = tk.LabelFrame(root, text="File Conversion", font=("Arial", 10))
    mainFrame.pack(pady=10, padx=20, fill="x")

    buttonFrame1 = tk.Frame(mainFrame)
    buttonFrame1.pack(pady=10)

    imgButton = tk.Button(buttonFrame1, text="Convert Image", width=15, height=2, command=lambda: openFile("image", colorVar.get()))
    imgButton.pack(side=tk.LEFT, padx=5)

    vidButton = tk.Button(buttonFrame1, text="Convert Video", width=15, height=2, command=lambda: openFile("video", colorVar.get()))
    vidButton.pack(side=tk.RIGHT, padx=5)

    cameraMainFrame = tk.LabelFrame(root, text="Live Camera", font=("Arial", 10))
    cameraMainFrame.pack(pady=10, padx=20, fill="x")

    buttonFrame2 = tk.Frame(cameraMainFrame)
    buttonFrame2.pack(pady=10)

    def getCamParams():
        try:
            device = int(deviceVar.get())
            fps = int(fpsVar.get())
            return device, fps
        except ValueError:
            messagebox.showerror("Error", "Invalid device or FPS value")
            return 0, 15

    liveButton = tk.Button(buttonFrame2, text="Live Camera Feed", width=15, height=2, command=lambda: launchCamera("live", colorVar.get(), *getCamParams()))
    liveButton.pack(side=tk.LEFT, padx=5)

    photoButton = tk.Button(buttonFrame2, text="Take Photo", width=15, height=2, command=lambda: launchCamera("photo", colorVar.get(), getCamParams()[0], 15))
    photoButton.pack(side=tk.RIGHT, padx=5)

    tipFrame = tk.Frame(root)
    tipFrame.pack(pady=10)

    tip1 = tk.Label(tipFrame, text="Tips:", font=("Arial", 10, "bold"), fg="blue")
    tip1.pack()

    tip2 = tk.Label(tipFrame, text="• Decrease terminal font size for better display", font=("Arial", 8), fg="blue")
    tip2.pack()

    tip3 = tk.Label(tipFrame, text="• Use Ctrl+C to stop live camera feed", font=("Arial", 8), fg="blue")
    tip3.pack()

    system = platform.system().lower()
    if system == "windows":
        tip4 = tk.Label(tipFrame, text="• Windows: Use Ctrl+Mouse Wheel to resize terminal", font=("Arial", 8), fg="gray")
    else:
        tip4 = tk.Label(tipFrame, text="• Linux: Use Ctrl+- to decrease font size", font=("Arial", 8), fg="gray")
    tip4.pack()

    root.mainloop()

if __name__ == "__main__":
    build()