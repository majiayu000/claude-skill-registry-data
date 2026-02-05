---
name: device-screenshot
description: This skill should be used when capturing screenshots from connected devices during development. Use this when users request to capture device screens, take screenshots, analyze device UI, or inspect layout issues on iOS Simulator, physical iOS devices, or Android devices. Typical triggers include "capture screen", "take a screenshot of the device", "show me what's on the device", or "analyze the current screen".
---

# Device Screenshot

## Overview

Capture screenshots from iOS Simulators, physical iOS devices, or Android devices during development. Use this skill to inspect UI layouts, debug rendering issues, verify text/color display, or capture device state for analysis.

## When to Use This Skill

Use this skill when users request to:
- Capture a screenshot from a connected device
- Analyze what's currently displayed on a device screen
- Debug layout rendering issues or UI problems
- Verify how elements are displayed (text, colors, spacing, etc.)
- Take snapshots during development for comparison or documentation

Common user requests that trigger this skill:
- "Capture screen for device"
- "Take a screenshot of the simulator"
- "Show me what's on the device right now"
- "Analyze the current screen"
- "Get a screenshot so we can see the layout issue"

## Quick Start

### iOS Simulator

To capture a screenshot from the currently running iOS Simulator:

```bash
xcrun simctl io booted screenshot $path
```

**Example:**
```bash
xcrun simctl io booted screenshot /tmp/simulator_screenshot.png
```

**Requirements:**
- iOS Simulator must be running (booted)
- Xcode Command Line Tools must be installed

**Common issues:**
- If "No devices are booted" error occurs, ensure the iOS Simulator is running
- The simulator must be the active/focused simulator if multiple are running

### Android Device

To capture a screenshot from a connected Android device or emulator:

```bash
adb shell screencap -p > $path
```

**Example:**
```bash
adb shell screencap -p > /tmp/android_screenshot.png
```

**Requirements:**
- Android device or emulator must be connected
- ADB (Android Debug Bridge) must be installed and in PATH
- USB debugging must be enabled on physical devices

**Common issues:**
- If "device not found" error occurs, run `adb devices` to verify connection
- For multiple devices, specify device with `adb -s <device_id> shell screencap -p > $path`

### Physical iOS Device

To capture a screenshot from a physical iPhone or iPad connected via USB, use the provided script:

```bash
scripts/ios_screenshot.sh $path
```

**Example:**
```bash
scripts/ios_screenshot.sh /tmp/iphone_screenshot.png
```

**Requirements:**
- Physical iOS device must be connected via USB
- Device must be trusted (paired with the Mac)
- Xcode must be installed
- The device should be unlocked

**How it works:**
1. Verifies an iOS device is connected using `xcrun devicectl`
2. Opens Xcode and triggers the screenshot interface (Shift+Cmd+2)
3. Automatically clicks the "Take Screenshot" button
4. Captures the most recent screenshot from Desktop
5. Copies it to the specified output path
6. Cleans up the Desktop screenshot file

**Common issues:**
- If "No connected iOS devices found" error occurs, check USB connection and trust status
- Ensure Xcode has proper permissions to control the system
- The device should be unlocked during screenshot capture

## Workflow

### Standard Screenshot Capture Process

1. **Determine device type** - Identify whether the user wants to capture from iOS Simulator, physical iOS device, or Android device

2. **Verify device status** - Ensure the device is connected and accessible:
   - iOS Simulator: Check if simulator is running
   - Android: Verify with `adb devices`
   - Physical iOS: Check connection with `xcrun devicectl list devices`

3. **Choose output path** - Determine where to save the screenshot:
   - Use `/tmp/` for temporary analysis
   - Use project-specific paths for documentation
   - Default to `/tmp/device_screenshot.png` if not specified

4. **Execute capture command** - Run the appropriate command based on device type

5. **Verify capture success** - Check that the screenshot file was created and is valid

6. **Analyze if requested** - If the user requested analysis, read the screenshot and provide insights about:
   - Layout issues or rendering problems
   - Text display, colors, or spacing concerns
   - UI element positioning or alignment
   - Any visible bugs or inconsistencies

### Example Interaction Flow

**User request:** "Take a screenshot of the simulator and tell me if the button is aligned correctly"

**Process:**
1. Determine device type → iOS Simulator
2. Choose output path → `/tmp/sim_screenshot.png`
3. Execute: `xcrun simctl io booted screenshot /tmp/sim_screenshot.png`
4. Verify file exists
5. Read the screenshot image
6. Analyze button alignment and provide feedback

## Best Practices

- **Always verify device connection** before attempting screenshot capture
- **Use descriptive output paths** to make screenshots easy to identify later
- **Clean up temporary screenshots** after analysis to avoid clutter
- **Default to /tmp/ directory** for temporary analysis screenshots
- **For physical iOS devices**, ensure Xcode has accessibility permissions
- **When analyzing**, be specific about UI issues found (positioning, colors, text, etc.)

## Troubleshooting

### iOS Simulator Issues
- **"No devices are booted"** → Start the iOS Simulator from Xcode
- **Permission denied** → Ensure Xcode Command Line Tools are properly installed

### Android Issues
- **"device not found"** → Run `adb devices` to verify device connection
- **"adb: command not found"** → Install Android SDK Platform Tools and add to PATH
- **Multiple devices connected** → Use `adb -s <device_id>` to specify target device

### Physical iOS Issues
- **"No connected iOS devices found"** → Check USB connection and device trust status
- **AppleScript errors** → Grant Xcode accessibility permissions in System Preferences
- **Screenshot not captured** → Ensure device is unlocked and Xcode is properly installed
- **Button not found** → Update Xcode or check if the UI has changed in recent versions
