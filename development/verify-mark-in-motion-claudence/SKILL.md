---
name: verify
description: Build, relaunch, and observe the Claudence menu bar app to verify a change end-to-end.
---

# Verifying Claudence changes

Claudence is a macOS menu bar app (SwiftUI, Xcode project + SwiftPM package in the same repo).

## Build

- Unit-test/compile loop: `swift build` and `swift test` from the repo root (fast, seconds).
- Real app bundle: `xcodebuild -scheme Claudence -configuration Debug build`
  (single scheme `Claudence`; output lands in
  `~/Library/Developer/Xcode/DerivedData/Claudence-*/Build/Products/Debug/Claudence.app`).

## Relaunch

The user usually has a Debug instance running from DerivedData. To swap in a new build:

```bash
pkill -x Claudence; sleep 1; open ~/Library/Developer/Xcode/DerivedData/Claudence-*/Build/Products/Debug/Claudence.app
```

Keychain session key (`com.claudence.session` / `default`) survives relaunch; the app fetches live usage within seconds of launch.

## Observe (no accessibility access needed)

The popover can't be opened programmatically (osascript lacks assistive access), but the app persists everything it renders:

- Current snapshot: `~/Library/Application Support/Claudence/Snapshots/current_snapshot.json`
  (also `last_known_good_snapshot.json`; check `fetchedAt` to confirm a fresh live fetch happened after relaunch)
- History: `~/Library/Application Support/Claudence/History/usage_history.json` (appended on each live fetch)
- Diagnostics/errors: `~/Library/Application Support/Claudence/diagnostics.json`
- Settings: `~/Library/Application Support/Claudence/settings.json` (session key is NOT here, it's in the Keychain)

For UI-only changes, ask the user to click the menu bar icon and screenshot — programmatic capture is blocked without accessibility + screen-recording permissions.

## Gotchas

- `grep --include=*.swift` fails under zsh globbing; quote it or use `-r ... --include "*.swift"`.
- Reading the keychain item from a script triggers a blocking permission dialog — don't; let the app do the fetch and read its output files instead.
