---
name: UI Screenshot
description: Instructions for capturing and retrieving high-quality UI screenshots from Android devices.
---

# UI Screenshot

This skill standardizes the process of capturing, retrieving, and organizing screenshots from Android devices for visual verification and documentation.

## Workflow

### 1. Capture Screenshot
Use `screencap` on the device to save the framebuffer to a file.
```bash
adb shell screencap -p /sdcard/screenshot.png
```

### 2. Retrieval
Pull the screenshot file from the device to your local machine.
```bash
adb pull /sdcard/screenshot.png <local_destination_path>
```
*Suggestion*: Use a descriptive filename locally, e.g., `login_screen_v2.png`.

### 3. Cleanup
Delete the temporary file from the device to save space and keep it clean.
```bash
adb shell rm /sdcard/screenshot.png
```

## One-Liner (PowerShell)
To capture, pull, and clean up in one go (replace `local_filename.png`):
```powershell
adb shell screencap -p /sdcard/s.png; adb pull /sdcard/s.png ./local_filename.png; adb shell rm /sdcard/s.png
```

## Verification Tips
- Ensure the device screen is on and displaying the target UI.
- Use `adb shell input keyevent 82` to unlock screen if needed (depends on security settings).
- For automated UI testing screenshots, consider using instrumented tests (Espresso/UiAutomator), but for ad-hoc agent verification, this ADB method is fastest.
