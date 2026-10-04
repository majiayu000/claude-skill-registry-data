---
name: mobile-boot
description: Boot everything needed to start working with a mobile app in one shot — verify the toolchain is installed, boot/reuse a running iOS Simulator and/or Android Emulator, and confirm the interaction layer (mobile-mcp, or idb/adb) can see the device. Use at the start of any mobile QA/testing/interaction task so `mobile-automation`/`mobile-simulator-interact` never start against a cold environment.
---

# Mobile Environment Auto-Boot

Gets a mobile device from "toolchain installed" to "booted and visible to
the interaction layer" in one pass, so nobody has to manually run boot
commands before every mobile task. Runs the same boot commands
`mobile-simulator-setup` documents, but as a per-session startup check
rather than a one-time install guide.

**Scope boundary** — this skill does NOT install SDKs/toolchains (that's
`mobile-simulator-setup`'s job) and does NOT interact with the app itself
(that's `mobile-automation` / `mobile-simulator-interact`'s job). It only
bridges "toolchain installed" -> "device booted and visible".

## Step 1 — decide platform scope

- If the task names a platform (iOS/Android) or a platform-specific app,
  boot only that platform.
- Otherwise default to whatever's available on this OS: Android is always
  in scope (works on any OS); iOS is only in scope on macOS.
- If both are relevant and it's unclear which the user wants first, boot
  Android first (cross-platform, usually faster to boot), then iOS — don't
  stop to ask unless genuinely blocked (e.g. no toolchain for either
  platform, see Step 2).

## Step 2 — verify toolchain is present (don't install anything here)

```bash
adb version && emulator -version         # Android
xcrun simctl list devices && idb --version   # iOS, macOS only
```

Any of these erroring or missing → **stop**, hand off to
`mobile-simulator-setup` instead. Installing/fixing the toolchain is out
of scope for this skill.

## Step 3 — Android: reuse or boot an emulator

```bash
adb devices
```

- A line other than the header shows `device` (not `offline`) → already
  booted, reuse it, skip to Step 5.
- Nothing listed → boot one:
  ```bash
  emulator -list-avds
  emulator -avd <name> &      # run in background — never block waiting on it
  ```
  Poll boot completion (don't stop at `adb devices` showing the serial —
  that can appear before boot actually finishes):
  ```bash
  adb wait-for-device
  until [ "$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')" = "1" ]; do
    sleep 2
  done
  ```
  First cold boot commonly takes 1-2+ minutes — that's expected, not a hang.

## Step 4 — iOS (macOS only): reuse or boot a simulator

```bash
xcrun simctl list devices | grep -i booted
```

- Already shows a `(Booted)` device → reuse it, skip ahead.
- Nothing booted → boot the first available iPhone runtime:
  ```bash
  DEVICE=$(xcrun simctl list devices available | grep -m1 'iPhone' | grep -oE '[A-F0-9-]{36}')
  xcrun simctl boot "$DEVICE"
  open -a Simulator
  ```
  Re-run the `grep -i booted` check until it confirms — booting isn't
  instant.

## Step 5 — confirm the interaction layer actually sees the device

- **mobile-mcp (preferred)**: `ToolSearch("select:mobile_list_available_devices")`
  if not already loaded, then call it. The device(s) just booted/reused
  must appear in the result. If no `mobile_*` tools are callable at all,
  tell the user to add `"mobile-mcp"` to their own `enabledMcpjsonServers`
  in `.claude/settings.local.json` and reconnect via `/mcp` — don't
  silently fall back to raw commands without saying so.
- **Fallback (mobile-mcp not enabled this session)**: confirm with the raw
  bridge instead — `idb list-targets` should show the UDID as `Booted`;
  `adb -s <serial> shell echo ok` should return `ok`.

## Step 6 — hand off

Once the device is confirmed visible, go straight into `mobile-automation`
(or `mobile-simulator-interact` if `mobile-mcp` isn't enabled) for the
actual task. Don't re-run this whole skill before every subsequent tool
call — only re-enter Step 3/4 if a later call fails with a "no device
found"/"device offline" error mid-task.

## Load this skill when

- Starting any mobile QA/testing/interaction task and it isn't already
  confirmed this session that a simulator/emulator is booted and visible.
- A `mobile_*` (mobile-mcp) or `idb`/`adb` call fails with a "no device"
  error mid-task — re-run the relevant boot step rather than guessing why.

## Skip when

- A simulator/emulator is already confirmed booted and visible earlier
  this same session.
- The toolchain itself isn't installed yet — go straight to
  `mobile-simulator-setup` instead, this skill assumes it's already there.
