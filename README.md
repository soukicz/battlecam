# BattleCam2

A simple, cross-platform desktop application for conference speakers to display their webcam feed in an always-on-top, borderless window alongside their presentation.

## Features

- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Always On Top**: Window stays above your presentation
- **Borderless**: Clean, minimal interface
- **Nickname Overlay**: Display your name on the video
- **Draggable**: Click and drag to reposition
- **Lightweight**: Small window size (320x240 default)
- **Simple CLI**: Easy to use from command line

## Quick Start

### Option 1: Download Pre-Built Executable (Recommended)

**No Python installation required!** Download the latest release for your platform:

👉 **[Download Latest Release](https://github.com/yourusername/battlecam2/releases/latest)**

- **Windows**: `battlecam-windows-x86_64.exe` (~150-250 MB)
- **macOS**: `BattleCam-macos.dmg` (~200-300 MB)
- **Linux**: `battlecam-linux-x86_64` (~150-250 MB)

#### Windows Installation
```bash
# Download and run
battlecam-windows-x86_64.exe --nickname "Your Name" --camera 0

# Windows may show security warning - click "More info" → "Run anyway"
```

#### macOS Installation
```bash
# 1. Open the DMG and drag to Applications
# 2. Right-click → Open (first time only, to bypass Gatekeeper)
# 3. Grant camera permissions when prompted
# 4. Run from Terminal:
/Applications/BattleCam.app/Contents/MacOS/BattleCam --nickname "Your Name" --camera 0
```

#### Linux Installation
```bash
# Make executable and run
chmod +x battlecam-linux-x86_64
./battlecam-linux-x86_64 --nickname "Your Name" --camera 0
```

### Option 2: Run from Source (For Development)

1. **Install Python 3.8+** (if not already installed)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **List available cameras:**
   ```bash
   python battlecam.py --list-cameras
   ```

4. **Run the application:**
   ```bash
   python battlecam.py --nickname "Your Name" --camera 0
   ```

## Usage

### Basic Usage

```bash
battlecam --nickname "Speaker Name" --camera 0
```

### List Available Cameras

```bash
battlecam --list-cameras
```

Output example:
```
Available cameras:
  0: Camera 0 (V4L2, 640x480)
  1: Camera 1 (V4L2, 1280x720)
```

### Custom Window Size

```bash
battlecam --nickname "Speaker" --camera 0 --width 640 --height 480
```

### Show Help

```bash
battlecam --help
```

## Controls

- **ESC** or **Q**: Quit the application
- **Click & Drag**: Move the window around the screen

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--nickname` | `-n` | Your name to display on video | Required |
| `--camera` | `-c` | Camera index (0, 1, 2, ...) | Required |
| `--list-cameras` | | List all available cameras | - |
| `--width` | | Window width in pixels | 320 |
| `--height` | | Window height in pixels | 240 |
| `--help` | `-h` | Show help message | - |

## Building Standalone Executables

### Automated Builds (GitHub Actions)

Pre-built executables are automatically created when you push a version tag:

```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions will automatically:
# 1. Build for Windows, macOS, and Linux
# 2. Create optimized executables
# 3. Publish to GitHub Releases
```

### Local Build

To build locally on your own machine:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **Run the optimized build script:**
   ```bash
   python build.py
   ```

3. **Find your executable:**
   - Windows: `dist/battlecam.exe` (~150-250 MB)
   - macOS: `dist/BattleCam.app` (~200-300 MB)
   - Linux: `dist/battlecam` (~150-250 MB)

### Build Optimizations Applied

The optimized build configuration (`battlecam.spec`) includes:

- ✅ **Headless OpenCV**: Smaller by ~50 MB (no GUI dependencies)
- ✅ **Excluded packages**: Removes matplotlib, scipy, pandas, etc.
- ✅ **UPX compression**: 30-40% size reduction
- ✅ **macOS camera permissions**: Pre-configured Info.plist
- ✅ **Single file**: Easy distribution

### Manual Build (Alternative)

```bash
# Using the optimized spec file
pyinstaller --clean --noconfirm battlecam.spec

# Or basic build without optimizations
pyinstaller --onefile --windowed --name battlecam battlecam.py
```

## Use Cases

- **Conference Presentations**: Show your face while presenting slides in fullscreen
- **Online Webinars**: Keep webcam visible with screen sharing
- **Live Streaming**: Overlay webcam on OBS or other streaming software
- **Remote Teaching**: Display yourself while sharing educational content

## Technical Details

- **Language**: Python 3
- **GUI Framework**: Tkinter (built into Python)
- **Video Capture**: OpenCV (cv2)
- **Image Processing**: PIL/Pillow
- **Platforms**: Windows, macOS, Linux

## Requirements (for Development)

- Python 3.8 or higher
- opencv-python-headless (4.10.0+) - Optimized, no GUI dependencies
- pillow (10.4.0+)

See `requirements.txt` for exact versions.

**Note**: We use `opencv-python-headless` instead of `opencv-python` for smaller distribution size. The headless version excludes Qt/GTK GUI dependencies since we use Tkinter.

## Troubleshooting

### Camera Not Found

```bash
# List cameras to find the correct index
battlecam --list-cameras

# Try different camera indices
battlecam --nickname "Test" --camera 1
```

### Permission Denied (macOS)

On macOS, you may need to grant camera permissions:
1. Go to **System Preferences** → **Security & Privacy** → **Camera**
2. Enable camera access for Terminal or your application

### Permission Denied (Linux)

Add your user to the `video` group:
```bash
sudo usermod -a -G video $USER
# Log out and log back in
```

### Window Not Staying on Top

This is a window manager issue. On some Linux desktop environments, you may need to manually set the window to "Always on Top" from the window menu.

### Build Fails with PyInstaller

Make sure you have the latest version:
```bash
pip install --upgrade pyinstaller
```

## Project Structure

```
battlecam2/
├── .github/
│   └── workflows/
│       └── build.yml           # GitHub Actions CI/CD
├── battlecam.py                # Main application
├── battlecam.spec              # Optimized PyInstaller config
├── requirements.txt            # Python dependencies
├── build.py                    # Local build script
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## Releasing New Versions

To create a new release with automated builds:

```bash
# 1. Update version information in your code
# 2. Commit all changes
git add .
git commit -m "Release v1.0.0: Description of changes"

# 3. Create and push a version tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin main --tags

# 4. GitHub Actions will automatically:
#    - Build executables for all platforms
#    - Create a GitHub Release
#    - Upload all executables
```

## License

This project is released into the public domain. Use it however you like!

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## Support

If you encounter issues, please:
1. Check the Troubleshooting section above
2. Ensure you're using the latest version
3. Run with `--list-cameras` to verify camera availability

## Changelog

### Version 1.0.0 (2025)
- Initial release
- Cross-platform support (Windows, macOS, Linux)
- Borderless, always-on-top window
- Nickname overlay
- Camera listing
- Draggable window
- Standalone executable support
