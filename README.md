WorkTime is a simple yet powerful Python application that helps users convert time between two configurable time zones. The application provides a graphical user interface (GUI) where the current time is displayed for both time zones, and users can easily input a time in one zone and convert it to the other.

Features
Real-time Time Display: Automatically updates the current time for both time zones.
Time Conversion: Allows users to input a time in one zone and instantly see the converted time in the other zone.
Customizable Time Zones: Easily configure the time zones to match your needs.
Desktop Shortcut: Creates a desktop shortcut with a custom icon for quick access.
No Command Prompt Window: Runs without opening a command prompt window.

Installation
Prerequisites
Python 3.6 or higher
Pip (Python package installer)

Step-by-Step Installation
Clone the Repository:
git clone https://github.com/blisspixel/WorkTime.git
cd worktime

Install Required Packages:
The script automatically checks for and installs required packages. However, you can manually install them using:
pip install pytz pywin32 winshell

Place the Icon File:
If you want to use a custom icon for the desktop shortcut, place your .ico file in the project directory and name it worktime.ico. Alternatively, update the ICON_PATH variable in the script to point to your icon.

Run the Script:
python worktime.py

The first time you run the script, it will create a desktop shortcut for easy access.

Configuration
The application can be easily customized by modifying the configuration section at the top of the worktime.py script:

# --- Configuration Section ---
TIME_ZONE_1 = 'US/Eastern'  # Time zone for the first location
TIME_ZONE_2 = 'US/Pacific'  # Time zone for the second location
LABEL_1 = 'EST'  # Label for the first time zone
LABEL_2 = 'PST'  # Label for the second time zone
SHORTCUT_NAME = "WorkTime.lnk"  # Name of the shortcut to be created on the desktop
ICON_PATH = "worktime.ico"  # Path to the icon file (must be .ico format)
# --- End of Configuration Section ---

TIME_ZONE_1 / TIME_ZONE_2: Set the time zones you want to display and convert between.
LABEL_1 / LABEL_2: Set the labels for the time zones.
SHORTCUT_NAME: The name of the desktop shortcut.
ICON_PATH: The path to your custom icon file.

Usage
Launch the Application: Use the desktop shortcut or run the script to launch the WorkTime application.

Time Conversion: Enter a time in the input field, and it will automatically convert to the other time zone.

Reset: The application automatically resets the input field after 10 seconds of inactivity.
