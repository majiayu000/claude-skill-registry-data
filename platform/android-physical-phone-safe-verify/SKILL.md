---
name: android-physical-phone-safe-verify
description: "Use when a phone with real user data is attached alongside an emulator, before running any Gradle instrumented task with two devices connected, or before changing any setting on the owner's phone. Also when a phone screenshot shows a top card missing."
---

# Verifying on the owner's physical phone

The phone is not a test device. It holds real user data and real settings, and Gradle does not
know the difference.

## 1. Pin instrumented runs to the emulator — always

With two devices attached, `connectedDebugAndroidTest` runs on **both**. The suite typically
calls `pm clear`, `deleteDatabase`, or `DELETE FROM sessions` to seed fixtures. On the owner's
phone that is their training history, gone.

```bash
ANDROID_SERIAL=emulator-5554 ./gradlew :app:connectedDebugAndroidTest
```

Ironvellum is flavoured: its exact task, and the phone backup to pull before installing a
schema-changing build, are in `monarch-session-context`.

Target the phone explicitly, and only for install/launch/screenshot/dump:

```bash
adb -s <PHONE_SERIAL> install -r -t <apk>
```

Never run a Gradle instrumented task while relying on it picking the right device.

## 2. Restore every setting you change

Record before, restore after, and print the readback as proof:

```python
orig = sh("shell","settings","get","system","font_scale").strip()
...                       # sweep
sh("shell","settings","put","system","font_scale",orig)
print("restored:", sh("shell","settings","get","system","font_scale").strip())
```

Same for `cmd locale set-app-locales <pkg> --locales ""`, `wm density`,
`settings put global debug.force_rtl`. A device left at 2.0x font or in RTL is a defect you
introduced.

What to measure while a setting is changed: `android-font-scale-verification` (text scale),
`android-display-size-layout-collapse` (display size), `android-rtl-layout-verification` (RTL).

## 3. Heads-up notifications pollute screenshots

A banner lands exactly where a top card renders. If a screenshot shows a "missing" element at
the top, retake before diagnosing.
