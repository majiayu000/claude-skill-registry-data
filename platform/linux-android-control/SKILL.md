---
name: linux-android-control
emoji: 📱
description: Control Android devices from Linux using ADB (Android Debug Bridge). Send texts, make calls, take screenshots, install apps, control media, navigate UI, and more. Use when a user asks FRIDAY to control their Android phone.
when: User asks FRIDAY to control Android phone, send SMS, make calls, take phone screenshot, install APK, open app on phone, or interact with mobile device.
requirements:
  binaries:
    - adb
---

# Android Control Skill

Control your Android device from FRIDAY using ADB (Android Debug Bridge).

## Prerequisites

1. **Enable USB Debugging** on your Android phone:
   - Go to Settings → About Phone → Tap "Build Number" 7 times
   - Go to Settings → Developer Options → Enable "USB Debugging"
   
2. **Connect phone via USB** or set up **Wireless ADB**:
   - For wireless: `adb tcpip 5555` then `adb connect <phone-ip>:5555`

3. **Authorize the connection** when prompted on your phone

## Commands Reference

### Device Management
```bash
# List connected devices
adb devices

# Get device info
adb shell getprop ro.product.model
adb shell getprop ro.build.version.release

# Reboot device
adb reboot

# Check battery status
adb shell dumpsys battery
```

### Send SMS Message
```bash
# Open SMS app with pre-filled message
adb shell am start -a android.intent.action.SENDTO -d "sms:<phone_number>" --es sms_body "<message>"

# Example: Send message to 9876543210
adb shell am start -a android.intent.action.SENDTO -d "sms:9876543210" --es sms_body "Hello from FRIDAY!"
```

### Make Phone Calls
```bash
# Initiate a call
adb shell am start -a android.intent.action.CALL -d "tel:<phone_number>"

# Example: Call 9876543210
adb shell am start -a android.intent.action.CALL -d "tel:9876543210"

# End call (hang up)
adb shell input keyevent KEYCODE_ENDCALL
```

### Open Apps
```bash
# Open specific app by package name
adb shell monkey -p <package_name> -c android.intent.category.LAUNCHER 1

# Common apps:
adb shell monkey -p com.whatsapp -c android.intent.category.LAUNCHER 1          # WhatsApp
adb shell monkey -p com.spotify.music -c android.intent.category.LAUNCHER 1     # Spotify
adb shell monkey -p com.google.android.youtube -c android.intent.category.LAUNCHER 1  # YouTube
adb shell monkey -p com.instagram.android -c android.intent.category.LAUNCHER 1  # Instagram
adb shell monkey -p com.google.android.gm -c android.intent.category.LAUNCHER 1  # Gmail
adb shell monkey -p com.android.chrome -c android.intent.category.LAUNCHER 1     # Chrome
adb shell monkey -p com.google.android.apps.maps -c android.intent.category.LAUNCHER 1  # Maps

# List all installed packages
adb shell pm list packages

# Search for app package
adb shell pm list packages | grep -i spotify
```

### Take Screenshot on Phone
```bash
# Capture screenshot and save to phone
adb shell screencap -p /sdcard/screenshot.png

# Pull screenshot to computer
adb pull /sdcard/screenshot.png ~/Pictures/phone_screenshot.png

# One-liner: Screenshot and pull
adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png ~/Pictures/phone_$(date +%Y%m%d_%H%M%S).png
```

### Screen Recording
```bash
# Record screen for 10 seconds
adb shell screenrecord --time-limit 10 /sdcard/recording.mp4

# Pull recording to computer
adb pull /sdcard/recording.mp4 ~/Videos/phone_recording.mp4
```

### Media Control
```bash
# Play/Pause media
adb shell input keyevent KEYCODE_MEDIA_PLAY_PAUSE

# Next track
adb shell input keyevent KEYCODE_MEDIA_NEXT

# Previous track
adb shell input keyevent KEYCODE_MEDIA_PREVIOUS

# Volume up/down
adb shell input keyevent KEYCODE_VOLUME_UP
adb shell input keyevent KEYCODE_VOLUME_DOWN

# Mute
adb shell input keyevent KEYCODE_VOLUME_MUTE
```

### Navigation & Input
```bash
# Tap at coordinates (x, y)
adb shell input tap 500 1000

# Swipe from (x1,y1) to (x2,y2)
adb shell input swipe 500 1500 500 500    # Swipe up
adb shell input swipe 500 500 500 1500    # Swipe down
adb shell input swipe 100 500 900 500     # Swipe right
adb shell input swipe 900 500 100 500     # Swipe left

# Type text
adb shell input text "Hello World"

# Press keys
adb shell input keyevent KEYCODE_HOME        # Home button
adb shell input keyevent KEYCODE_BACK        # Back button
adb shell input keyevent KEYCODE_APP_SWITCH  # Recent apps
adb shell input keyevent KEYCODE_POWER       # Power button
adb shell input keyevent KEYCODE_ENTER       # Enter key
adb shell input keyevent KEYCODE_DEL         # Backspace
```

### Screen Control
```bash
# Turn screen on/off
adb shell input keyevent KEYCODE_POWER

# Wake up screen
adb shell input keyevent KEYCODE_WAKEUP

# Lock screen
adb shell input keyevent KEYCODE_SLEEP

# Get screen state
adb shell dumpsys power | grep "Display Power"
```

### File Transfer
```bash
# Push file to phone
adb push ~/file.txt /sdcard/Download/

# Pull file from phone
adb pull /sdcard/Download/file.txt ~/

# List files
adb shell ls /sdcard/
```

### Install/Uninstall Apps
```bash
# Install APK
adb install ~/Downloads/app.apk

# Uninstall app
adb uninstall com.package.name

# Install and replace existing
adb install -r ~/Downloads/app.apk
```

### Notifications
```bash
# Open notification shade
adb shell cmd statusbar expand-notifications

# Close notification shade
adb shell cmd statusbar collapse

# Clear all notifications
adb shell service call notification 1
```

### Clipboard
```bash
# Set clipboard text (Android 10+)
adb shell am broadcast -a clipper.set -e text "Text to copy"

# Note: Reading clipboard requires special app like Clipper
```

### Open URLs
```bash
# Open URL in browser
adb shell am start -a android.intent.action.VIEW -d "https://google.com"

# Open YouTube video
adb shell am start -a android.intent.action.VIEW -d "https://youtube.com/watch?v=VIDEO_ID"
```

### Wireless ADB Setup
```bash
# With phone connected via USB:
adb tcpip 5555

# Then disconnect USB and connect wirelessly:
adb connect <phone_ip_address>:5555

# Find phone IP: Settings → About Phone → Status → IP Address
# Or: adb shell ip addr show wlan0

# Disconnect wireless
adb disconnect
```

### Screen Mirroring (requires scrcpy)
```bash
# Mirror phone screen to computer
scrcpy

# Mirror with specific settings
scrcpy --max-size 1024 --bit-rate 2M

# Record while mirroring
scrcpy --record ~/Videos/phone_mirror.mp4
```

## Common Use Cases

### "Send a text to Mom saying I'll be late"
```bash
adb shell am start -a android.intent.action.SENDTO -d "sms:+919876543210" --es sms_body "I'll be late"
```

### "Open Spotify on my phone"
```bash
adb shell monkey -p com.spotify.music -c android.intent.category.LAUNCHER 1
```

### "Take a screenshot of my phone"
```bash
adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png ~/Pictures/phone_screenshot.png
```

### "Play/pause music on my phone"
```bash
adb shell input keyevent KEYCODE_MEDIA_PLAY_PAUSE
```

### "Go back on my phone"
```bash
adb shell input keyevent KEYCODE_BACK
```

### "Open YouTube video"
```bash
adb shell am start -a android.intent.action.VIEW -d "https://youtube.com/watch?v=dQw4w9WgXcQ"
```
