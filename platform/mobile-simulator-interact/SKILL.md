---
name: mobile-simulator-interact
description: Give Claude real interaction control (tap/swipe/type/screenshot) and log-reading over a running mobile simulator/emulator — idb for iOS Simulator (macOS only), adb for Android Emulator (any OS) — so Claude can drive a mobile app under test the same way claude-in-chrome drives a browser tab. Use when a teammate wants Claude to actually interact with a mobile app (navigate a flow, fill a form, verify a screen) or read its logs, not just watch it run manually.
---

# Mobile Simulator/Emulator Interaction Control

This skill is the interaction layer: **screenshot/inspect → decide →
tap/swipe/type → screenshot/inspect again**, plus log reading for crashes
and errors — the mobile equivalent of `claude-in-chrome`'s `computer` tool
loop. It assumes the simulator/emulator is already booted and the app
under test is already installed and running (see the
`mobile-simulator-setup` skill for that one-time environment setup, and
whatever run/install step gets the specific app onto the device).

Pick the section for the platform in play. Always confirm the target
device explicitly (`--udid` for idb, `-s <serial>` for adb) once more than
one device/emulator could be running — an implicit "current" target is a
common source of commands silently hitting the wrong device.

## iOS Simulator (idb) — macOS only

### Finding what to tap

**Preferred — accessibility tree, no vision guesswork:**

```bash
idb ui describe-all --udid <UDID> --json
```

Returns every visible accessible element with `AXLabel`, `type`, and a
`frame` (`{x, y, width, height}` in **points**, not pixels). Tap target =
frame center: `(x + width/2, y + height/2)`.

```bash
idb ui describe-point <x> <y> --udid <UDID>   # what's at a known point
```

Works cleanly for standard UIKit/Material-style widgets. Custom-painted
views (canvas/chart widgets, Flutter widgets without semantics enabled)
may show up unlabeled or not at all — fall back to screenshots for those.

**Fallback — screenshot + pixel coordinates:**

```bash
idb screenshot /tmp/sim.png --udid <UDID>
```

Read the PNG with the `Read` tool to visually locate the target.

**Coordinate scale gotcha**: `idb screenshot` captures at the device's
native **pixel** resolution (often `@3x`), but `idb ui tap` takes **point**
coordinates (the same space `describe-*` uses). Divide screenshot pixel
coordinates by the device's scale factor (2 or 3) before tapping, or taps
will land 2-3x off from where they should.

### Acting

```bash
idb ui tap <x> <y> --udid <UDID>                     # point coordinates
idb ui swipe <x1> <y1> <x2> <y2> --udid <UDID>
idb ui text "some text" --udid <UDID>                # types into the focused field
idb ui key <keycode> --udid <UDID>                   # e.g. 40=return, 42=backspace
idb screenshot /tmp/sim.png --udid <UDID>            # verify the result
```

Text fields must be tapped (focused) before `idb ui text` — it sends to
whatever currently has keyboard focus, not to a specific field.

### Reading logs

```bash
xcrun simctl spawn booted log stream --predicate 'processImagePath CONTAINS "<AppBinaryName>"'
```

Pipe through a focused filter so only actionable lines surface:

```bash
xcrun simctl spawn booted log stream --predicate 'processImagePath CONTAINS "<AppBinaryName>"' \
  | grep -E --line-buffered "EXCEPTION|Error|ERROR|FAILED|StackTrace|assert|RenderFlex|overflow|40[134]|50[023]"
```

`--line-buffered` is mandatory on the `grep` — without it, output is
delayed by minutes due to pipe buffering. If the app is a Flutter build
launched via `flutter run`, its own stdout (Dart exceptions, `debugPrint`)
is a separate, often more useful, stream than the native `log stream`
output.

## Android Emulator (adb) — any OS

### Finding what to tap

**Preferred — view hierarchy dump, no vision guesswork:**

```bash
adb -s <serial> shell uiautomator dump /sdcard/window_dump.xml
adb -s <serial> pull /sdcard/window_dump.xml
```

The XML has `bounds="[x1,y1][x2,y2]"`, `text`, `resource-id`, and
`content-desc` for every element — works even on a closed-source APK,
since it queries the live view tree, not the app's source. Tap target =
bounds center.

**Fallback — screenshot + pixel coordinates:**

```bash
adb -s <serial> exec-out screencap -p > /tmp/emu.png
```

Read with the `Read` tool. Unlike iOS, adb screenshot pixels and adb tap
coordinates are in the **same** space — no scale-factor conversion needed.

**Flutter/canvas-renderer caveat**: if the APK itself is a Flutter (or
Unity/React Native canvas-based) build, `uiautomator dump` will likely see
one opaque view with no children — same problem as iOS's semantics tree.
Fall back to screenshot + pixel tap for those apps.

### Acting

```bash
adb -s <serial> shell input tap <x> <y>
adb -s <serial> shell input swipe <x1> <y1> <x2> <y2> [duration_ms]
adb -s <serial> shell input text "some_text"          # no spaces — use %s for a space
adb -s <serial> shell input keyevent <keycode>         # e.g. 66=enter, 67=backspace, 4=back
adb -s <serial> exec-out screencap -p > /tmp/emu.png   # verify the result
```

Tap the target field first to focus it before `input text`, same as iOS.

### Reading logs

```bash
adb -s <serial> logcat --pid=$(adb -s <serial> shell pidof -s <package>)
```

Or filter by severity across the whole log if you don't have the package
name handy:

```bash
adb -s <serial> logcat *:E    # errors and above only
```

**R8/ProGuard caveat**: a minified release APK (the common case for a
handed-over build with no source) shows obfuscated class/method names in
stack traces (e.g. `a.b.c.onCreate` instead of the real class) unless you
also have the matching `mapping.txt` to deobfuscate. Exception type and
message are still visible either way.

## Practical loop (either platform)

1. Inspect current state — accessibility tree/uiautomator dump preferred,
   screenshot when you need to actually *see* rendered output (layout,
   colors, images) or the tree comes back empty.
2. Identify the target element/coordinates.
3. Act — tap / swipe / type.
4. Inspect again to confirm the action had the expected effect. Don't
   assume a tap landed correctly — verify it.
5. Watch the log stream in parallel so a crash or exception triggered by
   your action is caught, not silently missed.

## Load this skill when

- A teammate wants Claude to actually interact with a mobile app under
  test — tap something, fill a form, navigate a multi-step flow, verify a
  screen visually — not just watch logs or read code.
- A teammate wants Claude to read/monitor a running app's logs for
  crashes, exceptions, or HTTP errors.
- Triggers: "test this on the simulator/emulator", "tap the button", "fill
  in this field", "navigate to X and check", "check the app logs", "does
  this screen look right".

## Skip when

- The simulator/emulator or toolchain isn't set up yet — use
  `mobile-simulator-setup` first.
- Pure source-code review with no device involved.
