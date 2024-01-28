# Screen Flipper

This script vertically flips the screen and touch panel coordinates on linux.
This was designed for use with the following raspberry pi touch screen:

Amazon link: https://amzn.to/3OpChbx
Wisecoco No-Cable-Needed Dual-Speaker with OSD 10.1 inch Raspberry Pi
LCD Touch Screen Portable Monitor IPS 1024 * 600
HDMI Touchscreen Display for RPi 4B 4 3b+ 3 2 Zero B B+

This was ONLY tested on a Raspberry Pi 3b+ running bullseye

# Installation

Copy this script to /usr/local/bin:
```
sudo cp screen_flipper.py /usr/local/bin/
```

Make the script executable:
```
sudo chmod +x /usr/local/bin/screen_flipper.py
```

# Create an app launcher

It can be convenient to create an app launcher that triggers toggling
the screen flip.

Create the launcher file:
```
nano ~/.local/share/applications/screen_flipper.desktop
```

Add the following to the launcher file:
```
[Desktop Entry]
Name=Screen Flipper
Comment=Flips the screen vertically
Exec=/usr/local/bin/screen_flipper.py
Icon=connect_creating.png
Terminal=false
Type=Application
Categories=Utility;
```

Add the launcher to the taskbar:
1. Right click on the task bar
2. Select "Add/Remove panel items"
3. Double click an "Application Launch Bar"
4. Add the "Screen Flipper" app that is under the "Accessories" menu

# Reset on boot

If running this script negatively impacts the touch coordinates after a
reboot, you can add a systemd service that force resets to the normal
orientation:

Create the systemd service:
```
sudo nano /etc/systemd/system/screen_flipper_startup.service
```

Add the following to the service file:
```
[Unit]
Description=Screen Flipper Startup Script
After=graphical.target

[Service]
Type=simple
ExecStart=/usr/local/bin/screen_flipper.py --reset

[Install]
WantedBy=graphical.target
```

Reload systemd:
```
sudo systemctl daemon-reload
```

Enable the service to start on boot
```
sudo systemctl enable screen_flipper_startup.service
```
