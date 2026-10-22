---
name: ADB & Logcat Expert
description: Expert instructions for using ADB and analyzing Android logs.
---

# ADB & Logcat Expert

This skill encapsulates mastery over the Android Debug Bridge (ADB) and Logcat for debugging and device management.

## ADB Essentials

### 1. Device Management
Check connected devices:
```bash
adb devices
```
If multiple devices are connected, use `-s <serial_number>` to target a specific one.

### 2. Installation & Uninstallation
Install an APK (retaining data if updating):
```bash
adb install -r path/to/app.apk
```
Uninstall an app:
```bash
adb uninstall com.package.name
```

### 3. Shell Access
Enter device shell:
```bash
adb shell
```
Execute a single command:
```bash
adb shell [command]
```

## Logcat Mastery

### 1. Basic Logging
View logs in real-time:
```bash
adb logcat
```

### 2. Cleaning Buffer
Clear previous logs before starting a test run:
```bash
adb logcat -c
```

### 3. Filtering
**By Tag:**
Only show logs with tag `MyApp`:
```bash
adb logcat -s MyApp
```

**By Priority:**
Show Warning level and above (V, D, I, W, E, F):
```bash
adb logcat *:W
```

**By Process ID (PID):**
First, find the PID of your app:
```bash
adb shell pidof -s com.package.name
```
Then filter by PID (Linux/Mac/Windows PowerShell with grep equivalent):
```bash
adb logcat --pid=<PID>
```

### 4. Format Output
Show time, PID, TID, and Tag:
```bash
adb logcat -v threadtime
```
Colorful output for easier reading:
```bash
adb logcat -v color
```

## Debugging Crashes
When an app crashes, look for the `AndroidRuntime` tag or fatal exceptions.
Search for:
```bash
adb logcat -s AndroidRuntime
```
key phrases: `FATAL EXCEPTION`, `Caused by`.
