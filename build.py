#!/usr/bin/env python3
"""
Build script for BattleCam2
Creates standalone executables using PyInstaller
"""

import subprocess
import sys
import platform
import os


def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False


def install_pyinstaller():
    """Install PyInstaller"""
    print("Installing PyInstaller...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])


def build_executable():
    """Build standalone executable"""
    system = platform.system()
    print(f"Building BattleCam2 for {system}...")
    print("Using optimized .spec file configuration")
    print("This may take 2-5 minutes...\n")

    # Check if spec file exists
    spec_file = 'battlecam.spec'
    if not os.path.exists(spec_file):
        print(f"Error: {spec_file} not found!")
        print("Run PyInstaller to generate it first:")
        print("  pyinstaller --onefile --windowed --name battlecam battlecam.py")
        return 1

    # PyInstaller command using spec file
    cmd = [
        'pyinstaller',
        '--clean',  # Clean build cache
        '--noconfirm',  # Replace output directory without asking
        spec_file
    ]

    # Run PyInstaller
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*60)
        print("Build successful!")
        print("="*60)

        if system == 'Windows':
            executable = "dist\\battlecam.exe"
            print(f"Executable: {executable}")
        elif system == 'Darwin':  # macOS
            executable = "dist/BattleCam.app"
            print(f"Application Bundle: {executable}")
            print(f"To test: open {executable}")
            print("\nTo create DMG for distribution:")
            print("  brew install create-dmg")
            print("  create-dmg dist/BattleCam.app")
        else:  # Linux
            executable = "dist/battlecam"
            print(f"Executable: {executable}")
            print("\nTo make AppImage (optional):")
            print("  # Install appimagetool first")
            print("  # See: https://appimage.github.io/")

        # Get file size
        if system == 'Darwin':
            # For macOS app bundle, get size of the whole directory
            try:
                result = subprocess.run(
                    ['du', '-sh', executable],
                    capture_output=True,
                    text=True
                )
                size = result.stdout.split()[0]
                print(f"Size: {size}")
            except:
                pass
        else:
            # For single file executables
            if os.path.exists(executable):
                size_bytes = os.path.getsize(executable)
                size_mb = size_bytes / (1024 * 1024)
                print(f"Size: {size_mb:.1f} MB")

        print("\nYou can now distribute the executable from the 'dist' folder.")
        print("Users do not need Python installed to run it.")
        print("\nOptimizations applied:")
        print("  - Excluded unnecessary packages")
        print("  - UPX compression enabled")
        print("  - Headless OpenCV (no GUI dependencies)")
        if system == 'Darwin':
            print("  - macOS camera permissions configured")
        print("="*60)

    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return 1

    return 0


def main():
    """Main build function"""
    print("BattleCam2 Build Script")
    print("="*60)

    # Check if PyInstaller is installed
    if not check_pyinstaller():
        print("PyInstaller not found.")
        response = input("Install PyInstaller? (y/n): ")
        if response.lower() == 'y':
            install_pyinstaller()
        else:
            print("PyInstaller is required to build executables.")
            print("Install it with: pip install pyinstaller")
            return 1

    # Build executable
    return build_executable()


if __name__ == '__main__':
    sys.exit(main())
