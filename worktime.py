import os
import sys
import subprocess
from pathlib import Path

# --- Configuration Section ---
# Set the time zones and labels here
TIME_ZONE_1 = 'US/Eastern'  # Time zone for the first location
TIME_ZONE_2 = 'US/Pacific'  # Time zone for the second location
LABEL_1 = 'EST'  # Label for the first time zone
LABEL_2 = 'PST'  # Label for the second time zone
SHORTCUT_NAME = "WorkTime.lnk"  # Name of the shortcut to be created on the desktop
ICON_PATH = "worktime.ico"  # Path to the icon file (must be .ico format)
# --- End of Configuration Section ---

def check_and_install(package):
    """
    Check if a Python package is installed; if not, install it.

    :param package: The name of the package to check/install.
    """
    try:
        __import__(package)
    except ImportError:
        print(f"Package '{package}' not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure required packages are installed
check_and_install("pytz")
check_and_install("pywin32")
check_and_install("winshell")  # Added winshell check

import pytz
import tkinter as tk
from datetime import datetime, timedelta
import winshell
from win32com.client import Dispatch

def create_desktop_shortcut():
    """
    Create a shortcut on the desktop to this Python script.
    """
    desktop = winshell.desktop()
    shortcut_path = os.path.join(desktop, SHORTCUT_NAME)
    
    if not os.path.exists(shortcut_path):
        python_executable = sys.executable.replace("python.exe", "pythonw.exe")  # Use pythonw.exe to avoid cmd window
        target = python_executable  # The executable to run
        script_path = os.path.join(os.getcwd(), sys.argv[0])  # The script to run

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target  # This should be the Python executable (pythonw.exe)
        shortcut.Arguments = f'"{script_path}"'  # The Python script as an argument
        shortcut.WorkingDirectory = os.path.dirname(script_path)

        # Set the icon if it exists
        if os.path.exists(ICON_PATH):
            shortcut.IconLocation = os.path.join(os.getcwd(), ICON_PATH)

        shortcut.save()
        print(f"Shortcut created at {shortcut_path}")

# Create the shortcut if it's the first run
create_desktop_shortcut()

TIME_ZONES = {
    LABEL_1: TIME_ZONE_1,
    LABEL_2: TIME_ZONE_2
}

class WorkTimeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{LABEL_1}/{LABEL_2} WorkTime")
        self.geometry("240x160")
        self.configure(bg='#2E2E2E')
        self.overrideredirect(True)  # Remove the title bar for a clean look

        # Add a close button
        self.add_close_button()

        # Enable dragging of the window
        self.enable_dragging()

        # Set up fonts
        self.time_font = ('Helvetica', 20, 'bold')
        self.label_font = ('Helvetica', 14, 'bold')

        # Initialize the UI components
        self.initialize_ui()

        # Start updating the clock
        self.update_clock()

    def add_close_button(self):
        """
        Add a close button to the top right corner of the window.
        """
        close_button = tk.Button(self, text="X", command=self.destroy, bg='#2E2E2E', fg='white', bd=0)
        close_button.pack(side='top', anchor='ne')

    def enable_dragging(self):
        """
        Enable the window to be moved by dragging.
        """
        self.bind('<Button-1>', self.start_move)
        self.bind('<B1-Motion>', self.do_move)

    def initialize_ui(self):
        """
        Initialize the user interface components.
        """
        self.time_label_1 = tk.Label(self, text="", font=self.time_font, fg='#FFFFFF', bg='#2E2E2E')
        self.time_label_1.pack(pady=5)

        self.time_label_2 = tk.Label(self, text="", font=self.time_font, fg='#FFFFFF', bg='#2E2E2E')
        self.time_label_2.pack(pady=5)

        input_frame = tk.Frame(self, bg='#2E2E2E')
        input_frame.pack(pady=10)

        self.input_time = tk.Entry(input_frame, font=self.label_font, width=10, fg='#A9A9A9', bg='#4E4E4E', justify='center')
        self.input_time.pack(side='left', padx=5)

        self.placeholder = f"{LABEL_1} to {LABEL_2}"
        self.input_time.insert(0, self.placeholder)
        self.input_time.bind("<FocusIn>", self.clear_placeholder)
        self.input_time.bind("<FocusOut>", self.add_placeholder)

        self.output_label = tk.Label(input_frame, text="", font=self.label_font, fg='#FFFFFF', bg='#2E2E2E')
        self.output_label.pack(side='left', padx=10)

        self.input_time.bind("<KeyRelease>", self.real_time_conversion)

    def start_move(self, event):
        """
        Initialize the window move process by capturing the starting position.
        """
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        """
        Move the window based on mouse drag.
        """
        x = (event.x_root - self.x)
        y = (event.y_root - self.y)
        self.geometry(f"+{x}+{y}")

    def update_clock(self):
        """
        Update the displayed times for both time zones.
        """
        now_zone_1 = datetime.now(pytz.timezone(TIME_ZONES[LABEL_1]))
        now_zone_2 = now_zone_1.astimezone(pytz.timezone(TIME_ZONES[LABEL_2]))
        self.time_label_1.config(text=f"{now_zone_1.strftime('%I:%M %p')} {LABEL_1}")
        self.time_label_2.config(text=f"{now_zone_2.strftime('%I:%M %p')} {LABEL_2}")
        self.after(5000, self.update_clock)

    def parse_time_input(self, user_time):
        """
        Parse user input time in multiple formats to handle both 12-hour and 24-hour formats.

        :param user_time: The time input string provided by the user.
        :return: A datetime object if the format is correct, else None.
        """
        formats = [
            '%I %p',        # e.g., "5 PM"
            '%I:%M %p',     # e.g., "5:30 PM"
            '%H',           # e.g., "15" (24-hour format)
            '%H:%M',        # e.g., "15:30" (24-hour format)
        ]
        for time_format in formats:
            try:
                parsed_time = datetime.strptime(user_time, time_format)
                return parsed_time
            except ValueError:
                continue
        return None

    def convert_time(self):
        """
        Convert the user-provided time from the first time zone to the second.
        """
        user_time = self.input_time.get().strip()
        if user_time == "" or user_time == self.placeholder:
            self.output_label.config(text="Invalid format")
            return

        user_time_dt = self.parse_time_input(user_time)
        
        if user_time_dt:
            # Convert the input time to the appropriate time zone
            now_zone_1 = datetime.now(pytz.timezone(TIME_ZONES[LABEL_1]))
            user_time_dt = now_zone_1.replace(hour=user_time_dt.hour, minute=user_time_dt.minute)
            converted_time = user_time_dt.astimezone(pytz.timezone(TIME_ZONES[LABEL_2]))
            
            # Display the converted time in the correct format
            self.output_label.config(text=f"{converted_time.strftime('%I:%M %p')}")
            self.after(10000, self.reset_app)  # Auto-reset after 10 seconds
        else:
            self.output_label.config(text="Invalid format")
            self.after(10000, self.reset_app)  # Auto-reset after 10 seconds

    def real_time_conversion(self, event=None):
        """
        Trigger the conversion process when the user enters a time.
        """
        if self.input_time.get() != self.placeholder:
            self.convert_time()

    def clear_placeholder(self, event):
        """
        Clear the placeholder text when the user clicks into the input field.
        """
        if self.input_time.get() == self.placeholder:
            self.input_time.delete(0, tk.END)
            self.input_time.config(fg='#FFFFFF')

    def add_placeholder(self, event):
        """
        Restore the placeholder text if the input field is empty.
        """
        if self.input_time.get() == "":
            self.input_time.insert(0, self.placeholder)
            self.input_time.config(fg='#A9A9A9')

    def reset_app(self):
        """
        Reset the app to its initial state, clearing the input field and result.
        """
        self.input_time.delete(0, tk.END)
        self.output_label.config(text="")
        self.add_placeholder(None)

if __name__ == "__main__":
    app = WorkTimeApp()
    app.mainloop()
