# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BattleCam2 is a cross-platform desktop application for conference speakers to display their webcam feed in an always-on-top, borderless window. It's a single-file Python application with PyInstaller-based distribution.

**Tech Stack:**
- Python 3.8+ with Tkinter (GUI)
- OpenCV (`opencv-python-headless`) for webcam capture
- PIL/Pillow for image processing
- PyInstaller for executable distribution

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Test the application
python battlecam.py --list-cameras
python battlecam.py --nickname "Test" --camera 0
```

**Important:** Always use `opencv-python-headless` (not `opencv-python`) to keep distribution size small.

## Building Executables

```bash
# Install build tools
pip install pyinstaller

# Build optimized executable using spec file
python build.py

# Or manually:
pyinstaller --clean --noconfirm battlecam.spec
```

**Output locations:**
- Linux: `dist/battlecam`
- Windows: `dist/battlecam.exe`
- macOS: `dist/BattleCam.app`

The `battlecam.spec` file contains critical optimizations (package exclusions, UPX compression, macOS permissions).

## Architecture

**Single-class design:** The `BattleCam` class in `battlecam.py` handles everything:
- `__init__`: Sets up OpenCV capture, Tkinter window (borderless, always-on-top), and event bindings
- `update_frame()`: 30 FPS loop that captures frames, draws nickname overlay, and updates display
- `draw_overlay()`: Renders nickname text with semi-transparent background using OpenCV
- Window dragging: Implemented via Tkinter mouse event bindings (`start_drag`, `on_drag`)

**Key implementation details:**
- Window is borderless via `root.overrideredirect(True)` and stays on top via `root.attributes('-topmost', True)`
- macOS requires special `Info.plist` configuration in `battlecam.spec` for camera permissions
- Frame updates use `root.after(33, ...)` for ~30 FPS without blocking Tkinter mainloop

## CI/CD and Releases

GitHub Actions workflow (`.github/workflows/build.yml`) automatically builds executables on:
- Version tags: `v*` (v1.0.0, v2.0.0) or numeric tags (`0.0.1`, `1.0.0`)
- Manual trigger via GitHub UI

**Creating a release:**
```bash
git tag 0.0.2  # or v0.0.2
git push origin 0.0.2
# GitHub Actions builds and publishes to Releases automatically
```

**Important:** The workflow pattern `'[0-9]*.*'` matches numeric version tags without the "v" prefix.

## Distribution Optimizations

The `battlecam.spec` file is critical for keeping executable size reasonable (~150-250 MB):
- Excludes unnecessary packages (matplotlib, scipy, pandas, etc.)
- Uses UPX compression (30-40% size reduction)
- Filters out unused GUI framework binaries (Qt, PySide, PyQt)
- macOS-specific: Includes `NSCameraUsageDescription` in Info.plist (required for camera access)

**Never modify `requirements.txt` without updating `battlecam.spec` excludes accordingly.**

## Repository URL

GitHub: `https://github.com/soukicz/battlecam`

## Testing Camera Access

Camera enumeration is handled by `list_cameras()` function which iterates through indices 0-9. On Linux, ensure user is in `video` group. On macOS, app must request camera permissions (handled by Info.plist).

## File Structure

- `battlecam.py` - Main application (single-file architecture)
- `battlecam.spec` - PyInstaller configuration with optimizations
- `build.py` - Wrapper script for local builds
- `requirements.txt` - Runtime dependencies (used by developers and CI/CD)
- `.github/workflows/build.yml` - Automated multi-platform builds
