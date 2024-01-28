#!/usr/bin/env python3

import os
import re
import sys
import subprocess
from argparse import ArgumentParser
from subprocess import call

"""
Screen Flipper

This script vertically flips a screen and touch panel coordinates on linux.
This was designed for use with the following raspberry pi touch screen:

Amazon link: https://amzn.to/3OpChbx
wisecoco No-Cable-Needed Dual-Speaker with OSD 10.1 inch Raspberry Pi
LCD Touch Screen Portable Monitor IPS 1024 * 600
HDMI Touchscreen Display for RPi 4B 4 3b+ 3 2 Zero B B+

This was tested on a Raspberry Pi 3b+ running bullseye

If running this negatively impacts the touch coordinates after a reboot,
you can add a systemd service that force resets to the normal orientation.
"""

# This assumes that Display ID 0 + HDMI-1 is what should be flipped
DISPLAY_ID = "0"
XRANDR_DEVICE = "HDMI-1"

# Regex to find touch device: "wch.cn CH57x"
# This will probably be different for different touch screens
TOUCH_DEVICE_REGEX = r'wch\.cn CH57x\s+id=(\d+)'

# An empty file that is created to store the current
# flipped state
STATE_FILE_PATH = "/tmp/screen_flipper_state"

class ScreenFlipper():
    def __init__(self):
        super().__init__()

    def execute_normal_orientation(self):
        device_id = self.find_touchscreen_id()
        if device_id is None:
            print("Faled to obtain touch screen ID")
            exit(1)
        env = {"DISPLAY": f":{DISPLAY_ID}"}
        call(["xrandr", "--output", XRANDR_DEVICE, "--rotate", "normal"], env=env)
        call(["xinput", "--set-prop", str(device_id), "libinput Calibration Matrix", "1", "0", "0", "0", "1", "0", "0", "0", "1"], env=env)

    def execute_inverted_orientation(self):
        device_id = self.find_touchscreen_id()
        if device_id is None:
            print("Faled to obtain touch screen ID")
            exit(1)
        env = {"DISPLAY": f":{DISPLAY_ID}"}
        call(["xrandr", "--output", XRANDR_DEVICE, "--rotate", "inverted"], env=env)
        call(["xinput", "--set-prop", str(device_id), "libinput Calibration Matrix", "-1", "0", "1", "0", "-1", "1", "0", "0", "1"], env=env)

    def toggle_screen_flip(self):
        if os.path.exists(STATE_FILE_PATH):
            # File exists, so the screen is flipped already
            # Delete the file and flip the screen back to the normal orientation
            os.remove(STATE_FILE_PATH)
            self.execute_normal_orientation()
        else:
            # File does not exist, so the screen is not flipped
            # Create the file and flip the screen to the inverted orientation
            with open(STATE_FILE_PATH, "w") as state_file:
                state_file.write("")
            self.execute_inverted_orientation()

    def find_touchscreen_id(self):
        try:
            # Run `xinput list` to find the devices that are available
            output = subprocess.check_output(['xinput', 'list'], universal_newlines=True)

            # Use regex to find the line containing 'wch.cn CH57x'
            # This will probably be different for different touch screens
            match = re.search(TOUCH_DEVICE_REGEX, output)

            if match:
                # Extract and return the touch device ID from the regex match
                return int(match.group(1))
            else:
                print("Touchscreen not found in xinput list.")
                return None

        except subprocess.CalledProcessError as e:
            print(f"Error executing xinput list: {e}")
            return None

def main(force_reset):
    screen_flipper = ScreenFlipper()

    if force_reset:
        screen_flipper.execute_normal_orientation()
        sys.exit(0)

    screen_flipper.toggle_screen_flip()
    sys.exit()

if __name__ == '__main__':
    parser = ArgumentParser(description='Screen Flipper')
    parser.add_argument('--reset', '-r', action='store_true', help='Force reset')
    args = parser.parse_args()
    main(args.reset)
