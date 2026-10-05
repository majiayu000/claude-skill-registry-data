---
name: verify-on-emulator
description: "Boot (or reuse) the TBox-Mock-Play AVD, install the debug APK, drive the launcher, and capture screenshots to verify UI changes on the head-unit geometry."
when_to_use: "Verifying a UI change visually; \"check it on the emulator\", \"screenshot the dashboard\", \"does it look right on the head unit\"."
argument-hint: "[screen-or-area]"
allowed-tools:
  - Bash
  - Read
---

# Verifying on the TBox-Mock-Play emulator

Visual verification on the head-unit geometry. `$ARGUMENTS` names the
screen or area to drive to and screenshot; with no argument, verify
the home dashboard.

## Environment

- **Tools**: resolve `adb` / `emulator` from `PATH` first
  (`command -v adb`; the Bash shell initializes from your profile —
  the committed allowlist covers bare invocations). If not on `PATH`,
  use `$ANDROID_HOME/{platform-tools,emulator}`, else the
  conventional SDK root (`~/Library/Android/sdk` on macOS,
  `~/Android/Sdk` on Linux); absolute-path invocations prompt unless
  mirrored in `.claude/settings.local.json`. `local.properties` and
  `~/Library` may be Read-denied — use `ls`/adb, not `cat`. Gradle
  finds the SDK via `local.properties` regardless.
- **AVD**: `TBox-Mock-Play` — 1280x720 @ 160 dpi (the 800x480 dp
  head-unit geometry) with Google Play, so a signed-in account
  provides real calendar events and media sessions. The definition
  is **committed in this skill directory**: `create-avd.sh` writes
  the AVD registry files directly from `tbox-mock-play.config.ini`
  (no avdmanager / cmdline-tools needed; only the
  `android-33 google_apis_playstore` system image for the host arch
  must be installed). Google sign-in inside the AVD stays a one-time
  manual step per machine — account state is not portable.
- **App id**: the stable flavor is `io.github.seijikohara.femto` (no
  debug suffix); nightly adds `.nightly`
  (`io.github.seijikohara.femto.nightly`). Only the stable flavor has a
  debug variant, so this skill always builds, installs, and grants
  permissions to the stable app id.

## Procedure

1. **Build the debug APK** via the
   [`verify-android-build`](../verify-android-build/SKILL.md) skill
   (the verification-procedure SSOT). The APK lands at
   `app/build/outputs/apk/stable/debug/app-stable-debug.apk`.

2. **Reuse or boot the emulator.** More than one emulator may be
   running, so resolve serials first: `adb devices`, then
   `adb -s <serial> emu avd name` to identify each instance. If a
   `TBox-Mock-Play` is already up, **reuse it** — installing onto the
   instance the user is watching is the point; never touch an
   unrelated instance. If none is running:

   ```bash
   emulator -avd TBox-Mock-Play -no-audio -gpu host
   ```

   Windowed on purpose — the user watches the verification live. In
   a headless context (no display available) add
   `-no-window -gpu swiftshader_indirect` instead of `-gpu host`. If
   the AVD does not exist (`emulator -list-avds`), create it first:

   ```bash
   .claude/skills/verify-on-emulator/create-avd.sh
   ```

   Wait until `adb -s <serial> shell getprop sys.boot_completed`
   reports `1` before installing. With multiple devices attached,
   pass `-s <serial>` to **every** adb call below.

3. **Install the APK**:

   ```bash
   adb -s <serial> install -r app/build/outputs/apk/stable/debug/app-stable-debug.apk
   ```

   Note: `connectedStableDebugAndroidTest` **uninstalls the app afterward** —
   run `:app:installStableDebug` (or `adb install -r`) again before manual
   screenshots. After a reinstall, `am force-stop` + restart the app
   so the running process is the new code.

4. **Pre-grant runtime permissions** — the startup permission dialog
   blocks the dashboard (`MainActivity.requestRuntimePermissions()`
   pops a location dialog on first run; uiautomator shows
   `com.google.android.permissioncontroller`). Pre-grant to skip it:

   ```bash
   adb shell pm grant io.github.seijikohara.femto android.permission.{ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,READ_CALENDAR,READ_PHONE_STATE,BLUETOOTH_CONNECT}
   ```

   then `am force-stop` + restart.

5. **Drive the UI**: `uiautomator dump /sdcard/ui.xml` + `adb pull`,
   grep `content-desc="Settings"` for the dock button bounds (the
   `DashboardDock` component, formerly called the footer), then
   `input tap`. The settings ModalBottomSheet opens **partially
   expanded** — `input swipe` up to fully expand, then swipe to
   scroll.

6. **Capture and inspect**: Compose row text often does not appear as
   discrete `text=` nodes (merged semantics), so confirm with a
   screenshot — `screencap -p` + pull + Read the image:

   ```bash
   adb shell screencap -p /sdcard/shot.png && adb pull /sdcard/shot.png
   ```

## Notes and former limitations

- The LIVE map WebView **renders on the emulator** (verified 2026-07
  under both `-gpu host` and `swiftshader_indirect`); the old "GL
  surface cannot present" limitation no longer reproduces. A blank
  map is NOT expected — check the `-gpu` mode and logcat before
  suspecting a regression.
- The Play system image has no `adb root`; runtime grants via
  `pm grant` still work.

## Report

Report explicitly what was run and what was observed:

- "Ran `adb install -r app-stable-debug.apk` — Success."
- "Pre-granted permissions via `adb shell pm grant ...`."
- "Captured `shot.png` — the calendar card renders the 6-day strip."

Do not claim the UI "looks right" generically; cite the commands and
attach or describe the screenshots.
