---
name: kindle-app-ops
description: Build, sideload, and validate the SCBE Kindle/Fire OS app loop with Capacitor, ADB, and release-readiness checks.
---

# Kindle App Ops

Use this skill when working on Kindle Fire app packaging, installation testing, and release checks.

## Scope
- Build/update Capacitor Android shell from `kindle-app/`
- Install APK to Kindle with ADB (USB or wireless)
- Validate app boot + network/offline behavior
- Prepare for Amazon Appstore submission

## Commands

Run from `C:\Users\issda\SCBE-AETHERMOORE`.

### Build APK (debug)
```powershell
Set-Location kindle-app
npm run build
npx cap sync android
Set-Location android
./gradlew assembleDebug
```

### Install on Kindle with ADB
```powershell
adb devices
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

### Optional wireless ADB
```powershell
adb connect <kindle-ip>:5555
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

## Validation Checklist
1. App launches without white screen.
2. Home UI renders at 7in and 10in tablet widths.
3. Connection state is visible (online/offline).
4. Core actions fail gracefully when offline.
5. API target host is correct for deployed environment.

## Artifacts to reference
- `kindle-app/capacitor.config.ts`
- `kindle-app/scripts/copy-pwa-assets.js`
- `kindle-app/store-listing.md`
- `docs/research/2026-03-04-kindle-dev-and-virtual-upload-brief.md`
