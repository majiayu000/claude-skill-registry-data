---
name: aether-phone-lane-ops
description: Boot, recover, tune, and verify the SCBE Android emulator phone lane for AetherCode and Polly Pad. Use when Codex needs to operate the `SCBE_Pixel_6_API35` emulator, repair stale lock state, resize the phone surface, or prove the current lane state from local artifacts.
---

# Aether Phone Lane Ops

Use this skill for Android emulator work around `SCBE_Pixel_6_API35`, `AetherCode`, and Polly Pad.

## Truth Boundary

- This skill does not bypass sandbox or approval rules.
- It reduces friction by pointing Codex at the repo scripts, existing status artifacts, and already-approved launcher prefixes.
- Treat `artifacts/kindle/emulator/*.json` and `artifacts/system/aether_phone_mode_pids.json` as the canonical local evidence surface.

## Quick Start

Run from `C:\Users\issda\SCBE-AETHERMOORE`.

Preview the lane without launching anything:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/system/start_polly_pad_emulator.ps1 -PreviewOnly
```

Summarize the latest local state from artifacts:

```powershell
python C:\Users\issda\.codex\skills\aether-phone-lane-ops\scripts\phone_lane_status.py
```

## Packet Order

### A. Discover

Check the emulator lane in this order:

1. `python C:\Users\issda\.codex\skills\aether-phone-lane-ops\scripts\phone_lane_status.py`
2. `& "C:\Users\issda\AppData\Local\Android\Sdk\platform-tools\adb.exe" devices -l`
3. `powershell -ExecutionPolicy Bypass -File scripts/system/start_polly_pad_emulator.ps1 -PreviewOnly`

If the status script says phone mode is live and `adb devices -l` shows `emulator-5554`, prefer attach or direct ADB follow-up over a fresh launch.

### B. Recover

If the emulator is stale, invisible to ADB, or showing `.protobuf.lock` / `multiinstance.lock` noise:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/system/stop_polly_pad_emulator.ps1 -StopPhoneMode -StopAdbServer
```

Then relaunch:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/system/start_polly_pad_emulator.ps1
```

### C. Launch Or Attach

Default launch:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/system/start_polly_pad_emulator.ps1
```

Reading-friendly launch:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/system/start_polly_pad_emulator.ps1 `
  -ScreenPreset reading `
  -RuntimeDensity 340 `
  -FontScale 1.12
```

If the emulator is already booted and only device setup remains:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/system/start_polly_pad_emulator.ps1 -SkipEmulatorLaunch
```

Read [references/launcher-matrix.md](./references/launcher-matrix.md) only when launch flags or failure modes matter.

### D. Operate The Phone Lane

Canonical emulator browser base:

- `http://10.0.2.2:8088/`

Canonical routes:

- `http://10.0.2.2:8088/polly-pad.html`
- `http://10.0.2.2:8088/chat.html`

Repo scripts to prefer:

- `scripts/system/start_polly_pad_emulator.ps1`
- `scripts/system/stop_polly_pad_emulator.ps1`
- `scripts/system/start_aether_phone_mode.ps1`
- `scripts/system/stop_aether_phone_mode.ps1`
- `scripts/system/kindle_device_diagnostics.ps1`

If direct Polly Pad launch lands in Chrome `FirstRunActivity`, complete the one-time Chrome setup and rerun the route launch. Do not claim Polly Pad browser launch is clean until that gate is cleared.

### E. Verify

The run is only complete when local evidence proves it:

- `adb devices -l` shows a live emulator serial, or the latest emulator status JSON records `ok=true`
- the phone-mode PID snapshot exists and the local web lane responds on `127.0.0.1:8088`
- the latest status JSON includes the routes or notes needed for the current run

Use the status script again at the end to summarize the local truth surface.

## Guardrails

- Do not claim the emulator is dead only because one launcher timed out; check raw `adb devices -l` and latest artifacts.
- Do not start a second emulator instance against the same AVD if `emulator` or `qemu-system-x86_64` is already holding the lock.
- Prefer recovery before rebuild.
- Keep the skill focused on emulator and phone-lane operations. Use other skills for publishing, research, or content generation.
