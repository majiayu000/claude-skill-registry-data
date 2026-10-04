---
name: scbe-pocket-phone
description: "Treat the SCBE Android emulator as Codex's daily-driver pocket phone for browsing, messaging, workflow capture, mobile testing, and app handoff. Use when Codex should operate `SCBE_Pixel_6_API35` like a real personal phone: boot or recover the lane, open Polly Pad or AetherCode routes, browse in Chrome, bridge secrets, hand off to browser research skills, capture notes, or coordinate document and image work through a mobile-first flow."
---

# SCBE Pocket Phone

Use this skill when the emulator should behave like a phone in your pocket instead of a one-off test device.

## Quick Start

Run from `C:\Users\issda\SCBE-AETHERMOORE`.

1. Establish phone truth with `$aether-phone-lane-ops`.
```powershell
python C:\Users\issda\.codex\skills\aether-phone-lane-ops\scripts\phone_lane_status.py
& "C:\Users\issda\AppData\Local\Android\Sdk\platform-tools\adb.exe" devices -l
powershell -ExecutionPolicy Bypass -File scripts/system/start_polly_pad_emulator.ps1 -PreviewOnly
```

2. Recover or launch only if needed.
```powershell
powershell -ExecutionPolicy Bypass -File scripts/system/stop_polly_pad_emulator.ps1 -StopPhoneMode -StopAdbServer
powershell -ExecutionPolicy Bypass -File scripts/system/start_polly_pad_emulator.ps1
```

3. Open the phone surfaces.
- `http://10.0.2.2:8088/polly-pad.html`
- `http://10.0.2.2:8088/chat.html`
- Chrome or another browser tab for external web workflows

4. If the task needs credentials, resolve them just-in-time with `$scbe-api-key-local-mirror`.

Read [references/integration-matrix.md](./references/integration-matrix.md) only when selecting companion skills or app connectors.

## Modes

### Developer

- Use for ADB checks, local app routes, emulator launch and recovery, browser lane testing, and mobile QA.
- Prefer attach or repair over a fresh launch when `emulator-5554` is already live.

### User

- Use for browsing, reading, messaging-style web flows, note capture, search, and cloud handoff work.
- Treat calling and messaging as browser or app workflows unless a real telephony path is explicitly provisioned.

### Modder

- Use for density and font tuning, browser session cleanup, first-run Chrome repair, sync experiments, and route customization.
- Keep evidence in the emulator status artifacts before claiming the mod worked.

## Core Workflow

1. Verify the lane.
- Start with the status script, `adb devices -l`, and preview mode.
- Do not claim the phone is usable until local artifacts and ADB agree.

2. Choose the phone surface.
- Use Polly Pad or chat routes for SCBE-native flows.
- Use Chrome when the phone is acting as a portable browser terminal.
- Use reading-friendly launch settings when the task is long-form review or research.

3. Bring in the right companion lane.
- Use `$aether-phone-lane-ops` for boot, repair, density, and route truth.
- Use `$scbe-api-key-local-mirror` for secret-backed app or web sessions.
- Use `$aetherbrowser-arxiv-nav`, `$aetherbrowser-github-nav`, and `$aetherbrowser-notion-nav` when the phone session needs a destination-specific browser workflow.
- Use `$scbe-universal-synthesis` when the phone becomes one lane in a larger multi-skill run.
- Use `$obsidian` when the phone session should leave behind notes, links, or capture artifacts.
- Use Adobe Acrobat and Adobe Photoshop connectors from the host when documents or images need deterministic processing while the phone lane acts as the mobile surface or sync target.

4. Finish with evidence.
```powershell
python C:\Users\issda\.codex\skills\aether-phone-lane-ops\scripts\phone_lane_status.py
& "C:\Users\issda\AppData\Local\Android\Sdk\platform-tools\adb.exe" devices -l
```

## Guardrails

- Do not claim the emulator is live without ADB or the latest status artifact.
- Do not launch a second instance against the same AVD lock.
- Do not store keys in plaintext; resolve them just-in-time.
- Do not present browser-based calling or messaging as real cellular service.
- Do not duplicate other skills inside this one; route to them.
