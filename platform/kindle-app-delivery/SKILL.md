---
name: kindle-app-delivery
description: Build, sideload, and publish the SCBE Kindle/Fire app using Capacitor, Gradle, ADB, and Amazon Appstore checklist steps.
---

# Kindle App Delivery

Use this skill when shipping the Kindle/Fire app lane end-to-end.

## Preconditions
- Repo path: `C:\Users\issda\SCBE-AETHERMOORE`
- JDK 17 installed and `JAVA_HOME` set
- Android platform-tools (`adb`) installed
- Kindle Fire USB debugging enabled

## Core Commands
1. Build debug APK:
```powershell
Set-Location C:\Users\issda\SCBE-AETHERMOORE
powershell -ExecutionPolicy Bypass -File scripts/system/kindle_build_install.ps1 -BuildType debug
```

2. Build + install to connected Kindle:
```powershell
Set-Location C:\Users\issda\SCBE-AETHERMOORE
powershell -ExecutionPolicy Bypass -File scripts/system/kindle_build_install.ps1 -BuildType debug -Install
```

3. Install to specific device:
```powershell
Set-Location C:\Users\issda\SCBE-AETHERMOORE
powershell -ExecutionPolicy Bypass -File scripts/system/kindle_build_install.ps1 -BuildType debug -Install -DeviceId <adb_serial>
```

## Monitoring
- Kindle lane status:
```powershell
Set-Location C:\Users\issda\SCBE-AETHERMOORE
python scripts/system/monitor_kindle_lane.py
```

## Artifacts
- APK output: `kindle-app/android/app/build/outputs/apk/...`
- Lane status: `artifacts/agent_comm/<day>/kindle-lane-status-*.json`
- Cross-talk bus: `artifacts/agent_comm/github_lanes/cross_talk.jsonl`

## Escalation Rules
- If build fails, emit support packet with exact blocker (`JAVA_HOME`, SDK, signing, ADB).
- Never claim install success without `adb` output.
