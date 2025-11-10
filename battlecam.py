#!/usr/bin/env python3
"""
BattleCam2 - Conference Webcam Overlay Application
A simple, cross-platform app for displaying webcam feed in an always-on-top window.
"""

import sys
import argparse
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import platform


class BattleCam:
    """Main application class for BattleCam2"""

    def __init__(self, nickname, camera, width=320, height=240):
        self.nickname = nickname
        self.camera_index = self._parse_camera(camera)
        self.width = width
        self.height = height
        self.running = False

        # Initialize video capture
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            print(f"Error: Could not open camera {camera}")
            print("Use --list-cameras to see available cameras")
            sys.exit(1)

        # Set camera resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # Initialize Tkinter window
        self.root = tk.Tk()
        self.root.title(f"BattleCam2 - {nickname}")

        # Make window borderless and always on top
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)

        # Platform-specific window attributes
        if platform.system() == 'Darwin':  # macOS
            try:
                self.root.attributes('-transparentcolor', 'systemTransparent')
            except:
                pass

        # Create label for video display
        self.label = tk.Label(self.root, bg='black')
        self.label.pack()

        # Bind close event (Escape key)
        self.root.bind('<Escape>', lambda e: self.close())
        self.root.bind('<q>', lambda e: self.close())
        self.root.bind('<Q>', lambda e: self.close())

        # Make window draggable
        self.label.bind('<Button-1>', self.start_drag)
        self.label.bind('<B1-Motion>', self.on_drag)
        self._drag_start_x = 0
        self._drag_start_y = 0

        # Center window on screen
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        self.running = True

    def _parse_camera(self, camera):
        """Parse camera argument (try as int first, then as string)"""
        try:
            return int(camera)
        except ValueError:
            # If it's not a number, try to find camera by name
            # For now, just return 0 as default
            print(f"Warning: Could not parse camera '{camera}', using camera 0")
            return 0

    def start_drag(self, event):
        """Start dragging the window"""
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag(self, event):
        """Handle window dragging"""
        x = self.root.winfo_x() + event.x - self._drag_start_x
        y = self.root.winfo_y() + event.y - self._drag_start_y
        self.root.geometry(f'+{x}+{y}')

    def draw_overlay(self, frame):
        """Draw nickname overlay on frame"""
        # Overlay settings
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        font_thickness = 2
        text = self.nickname

        # Get text size
        (text_width, text_height), baseline = cv2.getTextSize(
            text, font, font_scale, font_thickness
        )

        # Position in bottom-left corner with padding
        padding = 10
        x = padding
        y = frame.shape[0] - padding

        # Draw semi-transparent background rectangle
        overlay = frame.copy()
        cv2.rectangle(
            overlay,
            (x - 5, y - text_height - 5),
            (x + text_width + 5, y + baseline + 5),
            (0, 0, 0),
            -1
        )
        # Blend overlay with frame
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

        # Draw text
        cv2.putText(
            frame,
            text,
            (x, y),
            font,
            font_scale,
            (255, 255, 255),
            font_thickness,
            cv2.LINE_AA
        )

        return frame

    def update_frame(self):
        """Capture and display video frame"""
        if not self.running:
            return

        ret, frame = self.cap.read()
        if ret:
            # Draw nickname overlay
            frame = self.draw_overlay(frame)

            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert to PIL Image
            img = Image.fromarray(frame_rgb)

            # Convert to ImageTk
            imgtk = ImageTk.PhotoImage(image=img)

            # Update label
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        # Schedule next update (approximately 30 FPS)
        if self.running:
            self.root.after(33, self.update_frame)

    def run(self):
        """Start the application"""
        print(f"BattleCam2 started - {self.nickname}")
        print(f"Camera: {self.camera_index}")
        print("Press ESC or Q to quit")
        print("Click and drag to move window")

        # Start video update loop
        self.update_frame()

        # Start Tkinter main loop
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.close()

    def close(self):
        """Clean up and close application"""
        self.running = False
        if self.cap:
            self.cap.release()
        if self.root:
            self.root.quit()
            self.root.destroy()


def list_cameras(max_cameras=10):
    """List available cameras"""
    print("Available cameras:")
    found_cameras = []

    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            # Try to read a frame to confirm it works
            ret, _ = cap.read()
            if ret:
                # Try to get camera name (not always available)
                backend = cap.getBackendName()
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                print(f"  {i}: Camera {i} ({backend}, {width}x{height})")
                found_cameras.append(i)
            cap.release()

    if not found_cameras:
        print("  No cameras found")

    return found_cameras


def print_help():
    """Print usage help"""
    help_text = """
BattleCam2 - Conference Webcam Overlay Application

USAGE:
    battlecam --nickname <name> --camera <index>
    battlecam --list-cameras
    battlecam --help

OPTIONS:
    --nickname, -n    Your name/nickname to display on the video
    --camera, -c      Camera index (use --list-cameras to see available)
    --list-cameras    List all available cameras
    --width           Window width in pixels (default: 320)
    --height          Window height in pixels (default: 240)
    --help, -h        Show this help message

EXAMPLES:
    # List available cameras
    battlecam --list-cameras

    # Start with default size (320x240)
    battlecam --nickname "John Doe" --camera 0

    # Start with custom size
    battlecam --nickname "Jane Smith" --camera 1 --width 640 --height 480

CONTROLS:
    ESC or Q          Quit the application
    Click & Drag      Move the window

PURPOSE:
    This app helps conference speakers display their webcam feed in an
    always-on-top, borderless window alongside their presentation.
"""
    print(help_text)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='BattleCam2 - Conference Webcam Overlay',
        add_help=False
    )

    parser.add_argument(
        '--nickname', '-n',
        type=str,
        help='Your name/nickname to display'
    )
    parser.add_argument(
        '--camera', '-c',
        type=str,
        help='Camera index (e.g., 0, 1, 2)'
    )
    parser.add_argument(
        '--list-cameras',
        action='store_true',
        help='List available cameras'
    )
    parser.add_argument(
        '--width',
        type=int,
        default=320,
        help='Window width (default: 320)'
    )
    parser.add_argument(
        '--height',
        type=int,
        default=240,
        help='Window height (default: 240)'
    )
    parser.add_argument(
        '--help', '-h',
        action='store_true',
        help='Show help message'
    )

    # Parse arguments
    args = parser.parse_args()

    # Handle --list-cameras
    if args.list_cameras:
        list_cameras()
        return 0

    # Handle --help or no arguments
    if args.help or (not args.nickname and not args.camera):
        print_help()
        return 0

    # Validate required arguments
    if not args.nickname:
        print("Error: --nickname is required")
        print("Use --help for usage information")
        return 1

    if not args.camera:
        print("Error: --camera is required")
        print("Use --list-cameras to see available cameras")
        return 1

    # Create and run application
    try:
        app = BattleCam(args.nickname, args.camera, args.width, args.height)
        app.run()
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
