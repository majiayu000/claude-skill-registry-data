---
name: flash-the-iphone
description: Build, install, and launch the iOS capture app on a physical iPhone over USB with just flash (sideload, install the app on the phone, re-flash an expired build).
---
# Flash the iPhone

"Flashing" = build the app with `xcodebuild` and install/launch it on a
USB-connected iPhone with `xcrun devicectl`. Target device: iPhone 12 Pro on
iOS 26; bundle id `dev.mbw.BasicEventProducer`. Needs a Mac with Xcode — no
AWS, no backend.

## Read first
- app/README.md — "Building and flashing" (prereqs, WOS_DEVICE, free-vs-paid signing limits).
- docs/GETTING_STARTED.md §6 — the one-time setup walkthrough (signing team, Developer Mode, cert trust).

## Commands
```bash
just flash                     # Release build → install → launch
just flash Debug               # Debug build
WOS_DEVICE=<udid> just flash   # pin a device if auto-detection misfires
xcrun devicectl list devices   # find the UDID
```
One-time: Xcode signed into an Apple ID with a team set under Signing & Capabilities; phone in Developer Mode (Settings → Privacy & Security), USB-connected, "Trust This Computer" accepted. First launch: trust the developer cert under Settings → General → VPN & Device Management.

## Gotchas
- The checked-in project pins the owner's Apple team id in `DEVELOPMENT_TEAM`; building under any other Apple ID means picking your own team once in Signing & Capabilities, or the build fails signing.
- A free personal team's provisioning profile expires after 7 days (the app stops launching mid-trip until re-flashed) and caps at 3 sideloaded apps; the paid program ($99/yr) gives 1-year profiles. Flash close to the trip, not weeks ahead.
- `devicectl` output columns shift between Xcode versions — that is what `WOS_DEVICE` works around.
- Open `app/BasicEventProducer.xcodeproj`, not the repo root (wrong path → "missing its project.pbxproj file").
- No backend needed to test: leave the produce URL blank (captures stay in Outbox) or run `python3 tools/mock_server.py` and point Settings at `http://<Mac-LAN-IP>:8080/produce`.
