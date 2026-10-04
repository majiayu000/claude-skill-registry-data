---
name: install
description: Install the app on a device or emulator (auto-detects platform and build system)
argument-hint: "[--device <target>] [--variant <variant>]"
---

# Install App

Install the built application onto a target device, emulator, or simulator. Auto-detects the project platform and build system.

## Arguments

Parse `$ARGUMENTS` for named flags:
- `--device <target>` — Device target: `emulator`, `physical`, `simulator`, or a specific serial/UDID. Defaults to first available.
- `--variant <variant>` — Build variant (e.g. `debug`, `release`, `demo`). Defaults to `debug`.

## Platform Detection (Parallel)

Launch parallel agents to detect the project platform:

**Agent 1 — Android**:
Check for: `build.gradle.kts` or `build.gradle` containing `android`, `AndroidManifest.xml`
- Gradle wrapper: `./gradlew installDebug`
- Flutter: `flutter install`

**Agent 2 — iOS**:
Check for: `*.xcodeproj`, `*.xcworkspace`, `Podfile`, `Package.swift` with iOS platform
- Xcode: `xcodebuild -destination <dest> install` or via `xcrun simctl install`
- Flutter: `flutter install -d <device>`

**Agent 3 — Web**:
Check for: `package.json` with `dev`/`start` script, `deno.json`, `composer.json`
- Not applicable for install — skip (install is a no-op for web; `run` handles it)

**Agent 4 — Cross-platform**:
Check for: `pubspec.yaml` (Flutter), `build.gradle.kts` with `kotlin("multiplatform")` (KMP)
- Flutter: `flutter install -d <device>`
- KMP: detect target platform from connected devices, then use appropriate install

## Device Selection

### Android
1. Run `adb devices -l` to list connected devices
2. If `--device emulator`: target the emulator device (name contains `emulator`)
3. If `--device physical`: target the non-emulator device
4. If `--device <serial>`: target that specific serial
5. If no `--device` and exactly one device: use it
6. If no `--device` and multiple devices: ask the user which to target
7. If no devices: report error and suggest `adb start-server` or launching an emulator

### iOS
1. If `--device simulator`: use `xcrun simctl list devices booted` to find a running simulator
2. If `--device physical`: use `xcrun devicectl list devices` for physical devices
3. If `--device <udid>`: target that specific UDID
4. If no `--device` and exactly one target (booted sim or physical): use it
5. If no `--device` and multiple targets: ask the user which to target

## Execution

1. **Detect** platform via parallel agents above
2. **Build** the installable artifact if not already built:
   - Android: `./gradlew assembleDebug` (or `installDebug` which builds + installs)
   - iOS: `xcodebuild build` then install
   - Flutter: `flutter build` then `flutter install`
3. **Install**:
   - Android: `./gradlew install<Variant>` (e.g. `installDebug`, `installRelease`) or `adb -s <serial> install -r <apk-path>`
   - iOS Simulator: `xcrun simctl install booted <app-path>`
   - iOS Device: `xcrun devicectl device install app --device <udid> <app-path>`
   - Flutter: `flutter install -d <device-id>`
4. **Report**: Confirm installation with device name and app identifier

## Error Handling

If installation fails:
- **Android "INSTALL_FAILED_UPDATE_INCOMPATIBLE"**: Run `adb uninstall <package>` then retry
- **Android no device**: Check `adb devices`, suggest starting emulator
- **iOS signing error**: Report and suggest checking signing configuration
- **Build failure**: Fall back to the `/skills:build` command, fix errors, then retry install
