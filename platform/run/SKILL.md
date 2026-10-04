---
name: run
description: Build, install, and run the app on a target device (auto-detects platform)
argument-hint: "[--no-install] [--device <target>] [--variant <variant>]"
---

# Run App

Build, install, and launch the application on a target device. Auto-detects the project platform and build system.

## Arguments

Parse `$ARGUMENTS` for named flags:
- `--no-install` — Skip the install step (assume already installed)
- `--device <target>` — Target device. Values:
  - **Android**: `emulator`, `physical`, or a device serial from `adb devices`
  - **iOS**: `simulator`, `physical`, or a device UDID
  - **Web**: `chrome`, `firefox`, `safari`, `edge`
  - **Flutter**: any `flutter devices` id
- `--variant <variant>` — Build variant (e.g. `debug`, `release`, `demo`). Defaults to `debug`. Passed through to `/skills:install`.

## Platform Detection (Parallel)

Launch parallel agents to detect the project platform:

**Agent 1 — Android**:
Check for: `build.gradle.kts` or `build.gradle` containing `android`, `AndroidManifest.xml`

**Agent 2 — iOS**:
Check for: `*.xcodeproj`, `*.xcworkspace`, `Podfile`, `Package.swift` with iOS platform

**Agent 3 — Web**:
Check for: `package.json` with `dev`/`start` script, `deno.json`, `composer.json`, `Gemfile`

**Agent 4 — Cross-platform**:
Check for: `pubspec.yaml` (Flutter), `build.gradle.kts` with `kotlin("multiplatform")` (KMP)

## Execution

### 1. Install (unless `--no-install`)

Run the `/skills:install` command with the resolved device target. This handles build + install.

### 2. Resolve Device

Determine the target device for launching:

**Android:**
1. `adb devices -l`
2. Match `--device` value:
   - `emulator` → device line containing `emulator`
   - `physical` → device line NOT containing `emulator`
   - Serial string → exact match
   - No value, one device → use it
   - No value, multiple devices → ask the user which to target
3. Extract serial for `adb -s <serial>` commands

**iOS:**
1. `simulator` → `xcrun simctl list devices booted` (boot one if none running)
2. `physical` → `xcrun devicectl list devices`
3. No value, one target → use it
4. No value, multiple targets → ask the user which to target

**Web:**
1. Resolve browser:
   - `chrome` → `open -a "Google Chrome"` (macOS) / `google-chrome` (Linux)
   - `firefox` → `open -a Firefox` / `firefox`
   - `safari` → `open -a Safari`
   - `edge` → `open -a "Microsoft Edge"` / `microsoft-edge`
   - No value → use whatever `open` or `xdg-open` defaults to
2. Dev server URL from framework detection (usually `http://localhost:3000` or `:5173` or `:8080`)

**Flutter:**
1. `flutter devices` to list available
2. Match `--device` value against device id or name
3. No value → first available

### 3. Launch

**Android:**
1. Detect the app package and main activity:
   - Parse `AndroidManifest.xml` for `package` attribute and the activity with `android.intent.action.MAIN`
   - Or parse from `build.gradle.kts`: `applicationId`
2. Launch: `adb -s <serial> shell am start -n <package>/<activity>`

**iOS Simulator:**
1. Detect bundle ID from `Info.plist` or Xcode project
2. Launch: `xcrun simctl launch booted <bundle-id>`

**iOS Device:**
1. `xcrun devicectl device process launch --device <udid> <bundle-id>`

**Web:**
1. Start dev server in background if not running:
   - `package.json` with `dev` script → `<pm> run dev`
   - `package.json` with `start` script → `<pm> run start`
   - `composer.json` (Laravel) → `php artisan serve`
   - `Gemfile` (Rails) → `bin/rails server`
   - `deno.json` → `deno task dev` or `deno task start`
2. Wait for server to be ready (poll localhost)
3. Open browser to the dev URL

**Flutter:**
1. `flutter run -d <device-id>`

### 4. Report

Confirm the app is running with:
- Device name and serial/id
- Package/bundle identifier
- Any relevant URL (for web)

## Error Handling

- **App not installed**: Run `/skills:install` even if `--no-install` was passed, then retry launch
- **Activity not found**: Re-detect from manifest, try alternate activity names
- **Device offline**: Report and suggest reconnecting
- **Port in use (web)**: Find the process on the port, report to user, suggest killing or using alternate port
- **Build failure**: Delegate to `/skills:build` command for diagnosis and fixing
