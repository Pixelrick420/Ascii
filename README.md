# ASCII Image/Video Converter

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)](https://github.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red.svg)](https://opencv.org/)
[![PIL](https://img.shields.io/badge/Pillow-8.0+-orange.svg)](https://pillow.readthedocs.io/)

A high-performance, cross-platform ASCII art converter that transforms images and videos into beautiful terminal-based ASCII representations with full color support and intelligent terminal management. This sophisticated tool combines advanced image processing algorithms with platform-specific terminal optimization to deliver exceptional ASCII art conversion capabilities across Windows and Linux.

## Features

### Core Functionality
- Dual Media Support: Convert both static images and dynamic videos to ASCII art
- True Color Support: 24-bit RGB color rendering using ANSI escape sequences
- Intelligent Scaling: Adaptive aspect ratio preservation with configurable maximum dimensions
- Real-time Video Playback: Smooth ASCII video rendering with customizable frame rate control
- Cross-Platform Terminal Integration: Automatic terminal detection and font size optimization

### Advanced Image Processing
- Multi-resampling Algorithm: Utilizes PIL's LANCZOS resampling for high-quality downscaling
- Contrast Enhancement: Dynamic range adjustment using min-max normalization
- Grayscale Conversion: Luminance-based conversion using standard RGB coefficients (0.299, 0.587, 0.114)
- Character Mapping: 12-character density gradient optimized for ASCII representation

### Terminal Management
- Automatic Terminal Detection: Supports 10+ terminal emulators across platforms
- Font Size Optimization: Automatic font size reduction for optimal display
- Window Geometry Calculation: Intelligent terminal sizing based on content requirements
- Process Isolation: Spawns separate terminal instances for non-blocking operation

The application provides comprehensive media-to-ASCII transformation capabilities through both a graphical user interface and command-line interface. True color support is implemented using 24-bit RGB color rendering through ANSI escape sequences, allowing for vibrant and accurate color reproduction in compatible terminals. The intelligent scaling system preserves aspect ratios while adapting content to configurable maximum dimensions, ensuring optimal display quality across different terminal sizes.

For video content, the application provides real-time ASCII video playback with customizable frame rate control, creating smooth animated ASCII sequences. Cross-platform terminal integration automatically detects available terminal emulators and applies optimal font size configurations for the best viewing experience.

## System Requirements

### Minimum Requirements
- Python: 3.7 or higher
- Operating System: Windows 10+, Linux (most distributions)
- Terminal: Any ANSI-compatible terminal emulator
- Memory: Minimum 512MB RAM (2GB+ recommended for large videos)
- Storage: 50MB free space for installation

### Supported File Formats
- Images: JPEG, PNG, BMP, WebP
- Videos: MP4, AVI, MOV, MKV, WebM

### Python Dependencies
- Pillow>=8.0.0: Advanced image processing and manipulation
- opencv-python>=4.5.0: Video capture, processing, and frame extraction
- numpy>=1.19.0: High-performance numerical computations
- tkinter: GUI framework (usually included with Python)

## Installation

The installation process varies depending on your preferred method and operating system. The application can be installed directly from source, within a virtual environment for isolation, or using system package managers for integrated dependency management.

### Direct Installation
```bash
# Clone the repository
git clone https://github.com/Pixelrick420/Ascii.git
cd Ascii

# Run installation
python ascii.py
```

### Virtual Environment (Recommended)
```bash
# Create and activate virtual environment
python -m venv ascii_env

# Windows
ascii_env\Scripts\activate

# Linux
source ascii_env/bin/activate

# Install dependencies
pip install Pillow opencv-python numpy

# Run the application
python main.py
```

Creating a virtual environment isolates the project dependencies from your system Python installation, preventing potential conflicts with other projects. This approach is particularly recommended for development environments or systems with multiple Python projects.

### System Package Installation
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pil python3-opencv python3-numpy python3-tk

# Fedora/RHEL
sudo dnf install python3-pillow python3-opencv python3-numpy tkinter

```

## Usage

The application operates in two distinct modes: a graphical user interface for interactive use and a command-line interface for automation and scripting purposes. Both interfaces provide access to the full feature set while catering to different user preferences and use cases.

### GUI Application
Launch the graphical interface for easy file selection and conversion by running `python main.py`. The GUI provides an intuitive interface with file browser functionality that automatically filters files based on supported formats. Users can toggle color mode support and view real-time system information including platform details and optimization tips.

The interface displays platform-specific usage instructions and provides one-click conversion capabilities with automatic terminal spawning. This approach ensures that the ASCII output appears in an optimally configured terminal window without requiring manual setup.

### Command Line Interface

#### Image Conversion
```bash
# Basic image conversion with colors
python ascii.py image path/to/image.jpg

# Monochrome conversion
python ascii.py image path/to/image.png --no-color
```

#### Video Conversion
```bash
# Basic video conversion with colors
python ascii.py video path/to/video.mp4

# Monochrome video conversion
python ascii.py video path/to/video.avi --no-color
```

The command-line interface supports direct conversion for automation and scripting scenarios. Image conversion processes single static images and outputs the ASCII representation immediately, while video conversion creates an interactive playback experience with frame-by-frame ASCII animation.

#### Advanced CLI Usage
```bash
# Batch processing with shell scripting
for file in *.jpg; do
    python ascii.py image "$file" --no-color
done

# Pipe output to file
python ascii.py image sample.jpg > output.txt

# Background processing
nohup python ascii.py video large_video.mp4 &
```

## Configuration and Optimization

The application automatically configures terminal settings for optimal ASCII display, but advanced users can customize various parameters to suit specific requirements or preferences.

### Terminal Optimization Settings

#### Windows Terminal Configuration
The application automatically configures Windows Terminal with optimal settings including font size reduction to 8 points and selection of the Consolas font family for improved character clarity. Console buffer adjustments ensure proper UTF-8 encoding and appropriate window sizing for ASCII content display.

```powershell
# Font Configuration
--fontSize=8 --fontFace="Consolas"

# Console Buffer Adjustment
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowSize = New-Object System.Management.Automation.Host.Size(120,40)
```

#### Linux Terminal Configuration
Linux systems benefit from automatic font size adjustment using escape sequences and terminal-specific commands. The application attempts to configure popular terminal emulators including KDE Konsole and GNOME Terminal through their respective configuration mechanisms.

```bash
# Universal escape sequence for font size
\033]50;xft:monospace:size=8\007

# KDE Konsole profile switching
qdbus $KONSOLE_DBUS_SERVICE $KONSOLE_DBUS_SESSION setProfile "Small Font"

# GNOME Terminal font configuration
gsettings set org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:default/ font "Monospace 8"
```

### Processing Parameters

Advanced users can modify processing parameters by editing constants in the `ascii.py` file. The maximum width and height parameters control the output dimensions, while the character mapping string defines the density gradient used for ASCII conversion.

```python
MAX_WIDTH = 200      # Maximum character width
MAX_HEIGHT = 100     # Maximum character height
CHARS = "@#Woa+=:~-\" `"  # Character density mapping (dark to light)
```

Video processing optimization can be adjusted through frame sampling rates and playback timing. The step parameter controls how many frames are processed relative to the original frame rate, affecting both processing time and output quality.

```python
# Frame sampling rate (affects processing speed vs quality)
step = max(1, int(fps // 10))  # Process every 10th frame at 30fps

# Playback frame rate
time.sleep(0.1)  # 100ms delay = ~10fps playback
```

## Architecture and Implementation

### Core Components

The application architecture consists of three primary components working in coordination to deliver comprehensive ASCII conversion capabilities. The image processing pipeline handles the core conversion algorithms, while the video processing system manages temporal content and playback functionality. The terminal management system ensures optimal display across different platforms and terminal environments.

#### Image Processing Pipeline
The image processing pipeline transforms input media through a series of carefully orchestrated steps. Initial image loading utilizes PIL's robust format support, followed by RGB color space conversion for consistent processing. The scaling algorithm preserves aspect ratios while fitting content within specified dimensions. Contrast enhancement through min-max normalization optimizes tonal range, while grayscale conversion employs standard luminance coefficients. Character mapping translates pixel intensities to ASCII characters, and color data extraction preserves original color information for ANSI rendering.

#### Video Processing Pipeline
Video processing extends the image pipeline to handle temporal content through OpenCV's video capture capabilities. Frame extraction occurs at configurable intervals to balance processing speed with output quality. Batch processing accumulates frames in memory for smooth playback, while progress tracking provides user feedback during lengthy conversions. The continuous playback loop renders frames sequentially with appropriate timing delays, and keyboard interrupt handling allows graceful termination.

#### Terminal Management System
The terminal management system provides cross-platform compatibility through automatic platform detection and terminal discovery. Font configuration optimization occurs automatically based on detected terminal capabilities. Process spawning creates isolated terminal instances for non-blocking operation, while command construction builds platform-specific execution strings. Comprehensive error handling and fallback mechanisms ensure reliable operation across diverse system configurations.

### Key Algorithms

The aspect ratio preservation algorithm calculates appropriate scaling factors to maintain image proportions while fitting within specified dimensional constraints. The character mapping algorithm translates normalized pixel intensities to appropriate ASCII characters using array indexing operations for optimal performance.

```python
# Aspect ratio preservation
scaleW = maxWidth / width
scaleH = (maxHeight / (height * 0.8))  # Account for character aspect ratio
scale = min(scaleW, scaleH)

# Character mapping optimization
indices = np.clip(pixels * length // 255, 0, length).astype(int)
asciiChars = np.array(list(CHARS))[indices]
```

Color rendering utilizes ANSI escape sequence generation for true color terminal support. The RGB to ANSI conversion function creates appropriate color codes that modern terminals can interpret for accurate color reproduction.

## Screenshots

![image](https://github.com/user-attachments/assets/7bd44b7b-31d3-4bff-87a9-8dcda398f067)

### GUI Interface
- Main application window showing file selection options
- System information display with platform-specific tips
- Color mode toggle and conversion buttons

![image](https://github.com/user-attachments/assets/d1b5fe7e-6d5f-482e-b639-7f45a0c2c4a0)

### ASCII Output
- High-contrast black and white image conversion
- Colorized ASCII art displaying vibrant source imagery
- Video playback sequence showing frame progression
- Terminal window with optimized font sizing


### Cross-Platform Compatibility
- Windows Terminal with ASCII output
- Linux terminal (GNOME/KDE) displaying colored ASCII

## Contributing

Contributions to the ASCII Image/Video Converter project are welcome and encouraged. The project follows standard open-source development practices with clear guidelines for code quality, testing, and documentation standards.

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/yourusername/ascii-converter.git
cd ascii-converter

# Create development environment
python -m venv dev_env
source dev_env/bin/activate  # or dev_env\Scripts\activate on Windows

# Install development dependencies
pip install -e .
pip install pytest black flake8
```

### Code Standards
- Follow PEP 8 style guidelines for Python code formatting
- Maintain comprehensive docstrings for all functions and classes
- Include type hints where appropriate for improved code clarity
- Write unit tests for new functionality using pytest framework
- Ensure cross-platform compatibility for all new features

### Supported Platforms and Testing

The application undergoes testing across multiple operating systems and terminal environments to ensure consistent behavior. Primary testing platforms include Windows 10/11 with Windows Terminal, PowerShell, and Command Prompt. Linux testing covers major distributions including Ubuntu, Fedora, and Arch Linux with various terminal emulators.

## Troubleshooting

### Common Issues and Solutions

**Performance with Large Videos**: Large video files may consume significant memory during processing. Consider reducing the `MAX_WIDTH` and `MAX_HEIGHT` constants or increasing the frame sampling step value to improve performance.

**Terminal Color Support**: If colors appear incorrectly or not at all, verify that your terminal supports 24-bit color (true color). Most modern terminals support this feature, but some older or minimal terminals may require color mode to be disabled using the `--no-color` flag.

**Font Size Issues**: If ASCII output appears too large or too small, the automatic font sizing may not have worked correctly. Manually adjust your terminal font size using keyboard shortcuts (Ctrl+- or Cmd+- depending on platform) or terminal settings.

**Permission Errors on Linux**: Some Linux distributions may require additional permissions for terminal configuration commands. Run the application with appropriate user permissions or manually configure terminal font sizes.

### Platform-Specific Notes

Windows users should ensure that Windows Terminal or a compatible terminal emulator is installed for optimal results. The application supports PowerShell and Command Prompt but provides the best experience with Windows Terminal.

Linux users may need to install additional packages depending on their distribution. The application attempts to configure various terminal emulators automatically, but manual font size adjustment may be necessary in some cases.
