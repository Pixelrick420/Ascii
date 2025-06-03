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
    """Get font size reduction commands for different systems"""
    if system == "windows":
        return {
            "wt_profile": '--fontSize=8 --fontFace="Consolas"',
            "powershell": '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; $Host.UI.RawUI.WindowSize = New-Object System.Management.Automation.Host.Size(120,40);',
            "cmd": 'mode con: cols=120 lines=40 && '
        }
    elif system == "linux":
        return {
            "escapeSeq": '\033]50;xft:monospace:size=8\007', 
            "konsole": 'qdbus $KONSOLE_DBUS_SERVICE $KONSOLE_DBUS_SESSION setProfile "Small Font" 2>/dev/null || ',
            "gnome": 'gsettings set org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:default/ font "Monospace 8" 2>/dev/null || '
        }
    return {}

def launch(scriptPath, mode, filePath, cols, lines, color=True):
    isColor = "" if color else " --no-color"
    
    system = platform.system().lower()
    fontCmds = getFontSizeCommands(system)
    
    base_command = f'python3 "{scriptPath}" "{mode}" "{filePath}"{isColor}'
    
    print(f"Launching command: {base_command}")
    print(f"System: {system}")
    
    if system == "windows":
        return launchWindows(base_command, fontCmds)
    elif system == "linux":
        return launchLinux(base_command, fontCmds)
    else:
        print(f"Unsupported operating system: {system}")
        return runDirectly(scriptPath, mode, filePath, color)

def launchWindows(command, fontCmds):
    """Launch on Windows with font size adjustments"""
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
                    "--fontSize", "8",
                    "--fontFace", "Consolas",
                    "cmd", "/k"
                ]
                fullCmd = f"{fontCmds.get('cmd', '')}{command}"
                wt_args.append(fullCmd)
                subprocess.Popen(wt_args)
                print(f"Launched with {name} (font size: 8)")
                return True
            elif terminal == "powershell":
                psSetup = fontCmds.get('powershell', '')
                fullCmd = f"cd '{os.getcwd()}'; {psSetup} {command}"
                subprocess.Popen([
                    "powershell",
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
    """Launch on Linux with font size adjustments"""
    terminals = [
        ("konsole", ["konsole", "--hold", "--workdir", os.getcwd()]),
        ("gnome-terminal", ["gnome-terminal", f"--working-directory={os.getcwd()}"]),
        ("xfce4-terminal", ["xfce4-terminal", "--working-directory", os.getcwd(), "--hold"]),
        ("mate-terminal", ["mate-terminal", "--working-directory", os.getcwd()]),
        ("xterm", ["xterm", "-hold", "-fs", "8"]),  # Font size for xterm
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

def runDirectly(scriptPath, mode, filePath, color):
    """Run the script directly without terminal"""
    print("No suitable terminal found, running directly...")
    print("Note: For better display, consider decreasing your terminal font size manually")
    try:
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

    cols, lines = getGeometry(150)
    scriptPath = os.path.abspath("ascii.py")
    
    if not os.path.exists(scriptPath):
        messagebox.showerror("Error", f"ascii.py not found at {scriptPath}")
        return

    print(f"File selected: {filepath}")
    print(f"Script path: {scriptPath}")
    print(f"Color enabled: {color}")
    print(f"Operating System: {platform.system()}")
    
    success = launch(scriptPath, mode, filepath, cols, lines, color)
    if not success:
        runDirectly(scriptPath, mode, filepath, color)

def build():
    root = tk.Tk()
    root.title("ASCII Image/Video Converter")
    root.geometry("400x250")
    root.resizable(False, False)

    title = tk.Label(root, text="ASCII Image/Video Converter", font=("Arial", 16, "bold"))
    title.pack(pady=10)

    sysLabel = tk.Label(root, text=f"System: {platform.system()} {platform.release()}", font=("Arial", 9), fg="gray")
    sysLabel.pack(pady=2)

    label = tk.Label(root, text="Choose an option:", font=("Arial", 12))
    label.pack(pady=10)

    colorVar = tk.BooleanVar(value=True)
    colorCheck = tk.Checkbutton(root, text="Enable Colors", variable=colorVar, font=("Arial", 10))
    colorCheck.pack(pady=5)

    buttonFrame = tk.Frame(root)
    buttonFrame.pack(pady=10)

    imgButton = tk.Button(buttonFrame, text="Convert Image", width=15, height=2,
                         command=lambda: openFile("image", colorVar.get()))
    imgButton.pack(side=tk.LEFT, padx=5)

    vidButton = tk.Button(buttonFrame, text="Convert Video", width=15, height=2,
                         command=lambda: openFile("video", colorVar.get()))
    vidButton.pack(side=tk.RIGHT, padx=5)

    tipFrame = tk.Frame(root)
    tipFrame.pack(pady=10)

    tip1 = tk.Label(tipFrame, text="Tip: Decrease terminal font size for better display", font=("Arial", 8), fg="blue")
    tip1.pack()

    system = platform.system().lower()
    if system == "windows":
        tip2 = tk.Label(tipFrame, text="Windows: Use Ctrl+Mouse Wheel or Ctrl+- to resize", 
                       font=("Arial", 8), fg="gray")
    elif system == "darwin":
        tip2 = tk.Label(tipFrame, text="macOS: Use Cmd+- to decrease font size", 
                       font=("Arial", 8), fg="gray")
    else:
        tip2 = tk.Label(tipFrame, text="Linux: Use Ctrl+- to decrease font size", 
                       font=("Arial", 8), fg="gray")
    tip2.pack()

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        mode, path = sys.argv[1], sys.argv[2]
        color = "--no-color" not in sys.argv

        try:
            from ascii import imageToAscii, videoToAscii
            if mode == "image":
                imageToAscii(path, color=color)
            elif mode == "video":
                videoToAscii(path, color=color)
            else:
                print(f"Invalid mode: {mode}")
                sys.exit(1)
        except ImportError as e:
            print(f"Error importing ascii module: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error running conversion: {e}")
            sys.exit(1)
    else:
        build()