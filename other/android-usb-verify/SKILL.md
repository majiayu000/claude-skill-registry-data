---
name: android-usb-verify
description: "Use when adb, device auth, the Gradle wrapper or AGP 9's built-in Kotlin misbehaves here, or when installing, launching, driving or screenshotting an app via adb, e.g. Ironvellum (formerly Monarch) on the S25 Ultra. Covers USB phones and emulators on this Windows box."
---

# Android device verification (this Windows workstation)

Install, launch, drive and prove an Android app on a USB phone or emulator over adb.
Ironvellum (formerly Monarch, `D:\Monarch`) specifics are at the end.

## Toolchain

- SDK: `%LOCALAPPDATA%\Android\Sdk` (`platform-tools\adb.exe`, `emulator\`, `build-tools\36.0.0`,
  `platforms\android-37.0`); from git-bash, `"$LOCALAPPDATA/Android/Sdk/platform-tools/adb.exe"`.
  Registry `HKLM\SOFTWARE\Android Studio` may have an empty SdkPath — don't trust it.
- JDK: the system Oracle 21 on PATH works; Android Studio's `jbr\bin\java.exe` is flaky from bash.
- Gradle: no gradle CLI is installed. Use the project wrapper from git-bash, `./gradlew.bat <task>`
  or `./gradlew <task>` (both verified 2026-09-24). **Never `cmd //c gradlew.bat`**: it exits 1 and
  prints nothing. A project without wrapper scripts runs
  `java -cp gradle/wrapper/gradle-wrapper.jar org.gradle.wrapper.GradleWrapperMain <task> --console=plain`
  from the project dir (the SDK comes from its `local.properties`); fetch missing wrapper files from
  `raw.githubusercontent.com/gradle/gradle/v<ver>/gradlew{,.bat}` + `gradle/wrapper/gradle-wrapper.jar`.
- AGP 9.x has **built-in Kotlin**: applying `org.jetbrains.kotlin.android` FAILS ("no longer
  required"). Remove it (root + app + catalog); keep `org.jetbrains.kotlin.plugin.compose` + KSP
  (≥2.3.1 for AGP 9). Kotlin DSL: drop `kotlin {}` compilerOptions unless needed.
- Version pins: read `maven-metadata.xml` from dl.google.com / repo1.maven.org for AGP
  (`com/android/tools/build/gradle`), Kotlin, Compose BOM, Room, Navigation, activity-compose,
  lifecycle. Pick the latest STABLE (skip alphas).
- Health Connect (`androidx.health.connect:connect-client` 1.1.0): the record class is
  `BodyFatRecord` (NOT BodyFatMassRecord); permissions in the manifest + rationale intent-filter;
  wrap reads in `runCatching`; gate the connect button on `HealthConnectClient.getSdkStatus`.

## Device choreography (every session)

1. `adb devices` — want `<serial>  device`. `unauthorized` means the RSA prompt is on the phone: the
   user must tap Allow (tick "Always allow"), then poll until it reads `device`. Missing entirely:
   replug. After `adb kill-server` / `start-server` the list can read empty for a moment — poll a
   few times before concluding the device is gone.
2. `adb shell svc power stayon usb` keeps the screen awake while plugged in; without it, screenshots
   come back as the lock screen or all black.
3. Before ANY screencap: `adb shell input keyevent KEYCODE_WAKEUP` + `adb shell wm dismiss-keyguard`.
   A black screenshot = screen off; a lock screen = re-run this step.
4. Install: `adb install -r app.apk`. A fresh state means `adb uninstall` first, which wipes the
   app's data (Room then reseeds cleanly) — never on a device that holds real user data.
5. Launch and check for crashes:
   ```
   adb logcat -c
   adb shell am start -W -n <package>/.MainActivity   # expect Status: ok
   adb logcat -d *:E AndroidRuntime:E | tail -20      # crash history: adb logcat -b crash -d
   ```
   Samsung system noise (minksocket, keystore2, BatteryDump) is normal; only `FATAL EXCEPTION` from
   your package matters. `am start -W` after `force-stop` is a COLD launch; a resumed task reopens on
   its last screen (the user may have navigated), so force-stop for a clean start.

## Driving Compose UIs headlessly

- Dump: `adb shell uiautomator dump /sdcard/ui.xml >/dev/null 2>&1; adb shell cat /sdcard/ui.xml > .tmp/ui.xml`
  (one-line XML).
- Extract tap targets by `text=` (or class) with sed — grep can't slice one-line XML, and some
  harnesses block shell grep:
  `sed 's/></>\n</g' .tmp/ui.xml | sed -n 's/.*text="NAME".*bounds="\[\([0-9]*\),\([0-9]*\)\]\[\([0-9]*\),\([0-9]*\)\]".*/\1 \2 \3 \4/p'`
  → tap the centre `((l+r)/2, (t+b)/2)` with `adb shell input tap X Y`.
- Checkboxes are `checkable="true"` nodes (unchecked = `checked="false"`); buttons are their
  `text=` bounds.
- Do NOT pipe sed output into `while read` — git-bash throws I/O error 87 mid-loop and silently
  skips taps. Write the bounds to a file first (`while read ... done < file`) or loop over
  whitespace-split tokens with a for-loop and a counter.
- Text entry: `input tap <field>`, `sleep 2`, THEN `input text "..."` (typing races focus);
  `input keyevent 111` (ESC) dismisses the IME between fields.
- Dumps often omit Compose field values and can be stale (check the byte size changes) — confirm
  field values with a screenshot, not the dump. Read `enabled`/`selected`/`checked` off the
  clickable ancestor, not the label node: `compose-control-tap-verification`.

## Screenshot proof

`adb exec-out screencap -p > .tmp/shots/<name>.png`, then read the PNG with a vision query (`?q=`)
asking for the specific labels and colours you expect. Trust only what the vision answer confirms.

## Editing and build pitfalls

- Editing source between a background Gradle run's start and finish gives stale or mixed builds —
  land ALL file writes first, then build.
- Edit-tool anchors on a file changed since the last read corrupt it. After any failed or
  mis-anchored edit, and on files edited more than once per session, prefer a full-file rewrite over
  another anchored patch.

## Ironvellum (formerly Monarch) specifics

- Repo `D:\Monarch`; package and applicationId `com.ironvellum.app` in both the `foss` and `play`
  flavours. Standing repo facts (flavour task names, the gate, backups, rename vocabulary) live in
  `monarch-session-context`.
- Devices: the owner's Samsung S25 Ultra `R5GL14GXV3J` (SM-S938B) holds **real training history**;
  the emulator is `emulator-5554` (AVD `IronvellumEmu`, boot it with `python tools/device.py up`).
  With both attached, pin every command with `adb -s <serial>` / `ANDROID_SERIAL`, and do anything
  destructive (uninstall, `pm clear`, instrumented suites) on the emulator. A deliberate reset of the
  phone goes through `monarch-fresh-account-reset`, after the backup in `monarch-session-context`.
- Build and install: `./gradlew.bat :app:installFossDebug`, or
  `adb install -r app/build/outputs/apk/foss/debug/app-foss-debug.apk`.
- Launch: `adb shell am start -W -n com.ironvellum.app/.MainActivity`; only `AndroidRuntime` FATAL
  lines from `com.ironvellum.app` matter.
- Build quirks: AGP 9.4 with built-in Kotlin, KSP 2.3.12. `SectionHeader` lives in
  `com.ironvellum.app.ui.components` (`Common.kt`) — a wrong-package import has bitten repeatedly.
