# -*- mode: python ; coding: utf-8 -*-
"""
BattleCam2 PyInstaller Specification File
Optimized build configuration for cross-platform distribution
"""

import sys
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Collect any data files if needed
datas = []

# Hidden imports (modules that PyInstaller might miss)
hiddenimports = [
    'PIL._tkinter_finder',
]

a = Analysis(
    ['battlecam.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude large unnecessary packages
        'matplotlib',
        'scipy',
        'pandas',
        'pytest',
        'setuptools',
        'distutils',
        'numpy.distutils',
        # Documentation and testing
        'test',
        'unittest',
        'doctest',
        'pydoc',
        'pdb',
        # Network modules (if not needed)
        'email',
        'html',
        'http',
        'urllib3',
        'ftplib',
        'smtplib',
        # XML processing
        'xml',
        'xmlrpc',
        # Other
        'IPython',
        'jupyter',
        'notebook',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove unnecessary binaries to reduce size
# Filter out Qt, PySide, and other GUI frameworks we don't use
a.binaries = [
    x for x in a.binaries
    if not x[0].startswith((
        'Qt',
        'PySide',
        'PyQt',
        'scipy',
        'matplotlib',
    ))
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Platform-specific configurations
if sys.platform == 'darwin':  # macOS
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='BattleCam',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,  # Compress with UPX
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,  # No console window
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )

    # Create macOS app bundle
    app = BUNDLE(
        exe,
        name='BattleCam.app',
        icon=None,  # Add icon path here if you have one: 'icon.icns'
        bundle_identifier='com.battlecam.app',
        info_plist={
            # CRITICAL: Camera permission description for macOS
            'NSCameraUsageDescription': 'BattleCam needs access to your camera to display video feed for conference presentations',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'CFBundleName': 'BattleCam2',
            'CFBundleDisplayName': 'BattleCam2',
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '10.13.0',  # macOS High Sierra or later
        },
    )

elif sys.platform == 'win32':  # Windows
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='battlecam',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,  # Compress with UPX
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,  # No console window
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=None,  # Add icon path here if you have one: 'icon.ico'
    )

else:  # Linux and other platforms
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='battlecam',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,  # Compress with UPX
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,  # No console window
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )
