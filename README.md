# ASCII Media Converter

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)](https://github.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red.svg)](https://opencv.org/)

A high-performance ASCII art converter that transforms images, videos, and live camera feeds into terminal-based ASCII representations with full color support and intelligent terminal management.

## Features

**Media Support**: Convert static images, dynamic videos, and live camera feeds to ASCII art with true 24-bit RGB color rendering using ANSI escape sequences.

**Advanced Processing**: Utilizes LANCZOS resampling for high-quality scaling, dynamic contrast enhancement, and luminance-based grayscale conversion with optimized 12-character density mapping.

**Real-time Performance**: Smooth ASCII video playback and live camera streaming with customizable frame rate control and automatic terminal optimization.

**Cross-Platform**: Automatic terminal detection across 10+ terminal emulators with font size optimization and process isolation for non-blocking operation.

## System Requirements

**Python**: 3.7+ with dependencies:
- `Pillow>=8.0.0` - Image processing
- `opencv-python>=4.5.0` - Video/camera capture
- `numpy>=1.19.0` - Numerical computations
- `tkinter` - GUI framework

**Supported Formats**:
- Images: JPEG, PNG, BMP, WebP
- Videos: MP4, AVI, MOV, MKV, WebM
- Cameras: USB webcams, built-in cameras

**Hardware**: 512MB RAM minimum (2GB+ recommended for large videos), 50MB storage space.

## Installation

### Quick Start
```bash
git clone https://github.com/Pixelrick420/Ascii.git
cd Ascii
python ascii.py
```

### Virtual Environment (Recommended)
```bash
python -m venv ascii_env
source ascii_env/bin/activate  # Windows: ascii_env\Scripts\activate
pip install Pillow opencv-python numpy
python ascii.py
```

Virtual environments prevent dependency conflicts and provide isolated project spaces for cleaner development workflows.

## Usage

### GUI Application
Launch the graphical interface with `python app.py` for intuitive file selection and one-click conversion with automatic terminal spawning and optimal display configuration.

### Command Line Interface

**Image Conversion**:
```bash
python ascii.py image path/to/image.jpg
python ascii.py image path/to/image.png --no-color
```

**Video Conversion**:
```bash
python ascii.py video path/to/video.mp4
python ascii.py video path/to/video.avi --no-color
```

**Live Camera Feed**:
```bash
python camera_ascii.py live                    # Default camera, color
python camera_ascii.py live --device=1 --fps=20
python camera_ascii.py live --no-color
```

**Camera Photo Capture**:
```bash
python camera_ascii.py photo                   # Save as camera_capture.jpg
python camera_ascii.py photo custom_name.jpg --device=1
```

**Camera Management**:
```bash
python camera_ascii.py list                    # List available cameras
```

### Camera Features

The camera module provides real-time ASCII conversion with live FPS monitoring, frame flipping for mirror effect, and automatic camera initialization with optimized capture settings.

Live feed supports keyboard interrupt (Ctrl+C) for graceful termination and displays real-time performance metrics including FPS and frame count.

## Configuration

### Processing Parameters
Edit constants in `ascii.py` for custom output dimensions and character mapping:
```python
MAX_WIDTH = 200      # Maximum character width
MAX_HEIGHT = 100     # Maximum character height
CHARS = "`'\"-~:;=+aow#W@" # Density gradient (dark to light)
```

### Terminal Optimization
The application automatically configures terminal settings including font size reduction and UTF-8 encoding. Manual adjustment may be required on some systems using terminal-specific keyboard shortcuts (Ctrl+- or Cmd+-).

### Camera Settings
Camera parameters can be adjusted in `camera_ascii.py`:
```python
# Default camera resolution: 640x480
# Default ASCII dimensions: 160x80
# Default FPS limit: 15
```

## Architecture

**Image Pipeline**: PIL-based loading → RGB conversion → aspect-ratio scaling → contrast enhancement → character mapping → ANSI color rendering.

**Video Pipeline**: OpenCV frame extraction → batch processing → continuous playback with timing control → keyboard interrupt handling.

**Camera Pipeline**: Real-time capture → frame flipping → live ASCII conversion → FPS monitoring → resource cleanup.

**Terminal Management**: Cross-platform detection → font optimization → process spawning → error handling with fallback mechanisms.

## Screenshots

![GUI Interface](https://github.com/user-attachments/assets/a64e9b73-afe8-45b8-a953-c2e4233a2943)

*Main application window with file selection and system information*

![ASCII Output](https://github.com/user-attachments/assets/d1b5fe7e-6d5f-482e-b639-7f45a0c2c4a0)

*High-contrast ASCII conversion with color support*

## Troubleshooting

**Large File Performance**: Reduce `MAX_WIDTH`/`MAX_HEIGHT` constants or increase frame sampling for better performance with large videos.

**Color Display Issues**: Verify terminal supports 24-bit color (true color). Use `--no-color` flag for compatibility with older terminals.

**Camera Access**: Run `python camera_ascii.py list` to identify available camera devices. Use `--device=N` to specify alternative cameras.

**Font Size**: Manual terminal font adjustment may be needed if automatic sizing fails. Use Ctrl+- (or Cmd+-) keyboard shortcuts.

## Contributing

Development follows PEP 8 standards with comprehensive docstrings and type hints. Testing covers Windows 10/11 and major Linux distributions with various terminal emulators.

```bash
# Development setup
git clone https://github.com/yourusername/ascii-converter.git
python -m venv dev_env
source dev_env/bin/activate
pip install -e . && pip install pytest black flake8
```
