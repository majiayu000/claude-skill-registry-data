---
name: macos-dual-instance
description: Run two simultaneous instances of one macOS app (e.g. two accounts logged into the same chat app) by duplicating and re-signing its .app bundle. Use when an app refuses to open a second window and just refocuses the running one, when `open -n -a <App>` launches no new process, or when a second independent login session for the same app is needed without a second macOS user account or VM.
---

# Run two instances of a macOS app

Duplicate and re-sign a macOS app bundle so it runs as a second, independent process the OS treats as a different app: its own sandbox container, its own login session, running alongside the original. Verified on WeChat.app (Tencent, sandboxed, container under `~/Library/Containers/`) 2026-09-19.

## Facts every step rests on

- **`open -n -a` is not the fix.** It forces a new *launch request*, but an app with its own single-instance IPC check (most chat/IM apps) just detects the sibling and refocuses it — no new process shows up in `pgrep`. `LSMultipleInstancesProhibited` in Info.plist is a separate, OS-level flag; its absence doesn't mean the app allows a second copy of itself.
- **The container follows the bundle ID, not the code signature.** A sandboxed app's data lives at `~/Library/Containers/<CFBundleIdentifier>/`. Change the identifier in a copy of the bundle and macOS hands the copy a fresh, empty container at launch — an independent login session with no shared state.
- **Ad-hoc signing is enough to launch, not enough to trust.** `codesign --force --deep --sign -` replaces the vendor's signature so the copy can execute, but it strips notarization: a Finder double-click gets Gatekeeper-blocked (launch with `open` from Terminal, or right-click → Open once, instead). Some apps also run their own anti-tamper checks independent of the OS signature and refuse to start, or crash, after re-signing — a per-app roll of the dice, not guaranteed to work.
- **The copy is a snapshot, not a mirror.** It doesn't track vendor updates. When the original updates itself, redo the copy from the freshly updated `.app` to keep the clone current.

## Steps

### 1. Confirm the block is app-level, not OS-level

`defaults read /Applications/<App>.app/Contents/Info.plist LSMultipleInstancesProhibited` (usually errors "not found" — that's not the blocker). Then compare `pgrep -fl "<App>.app/Contents/MacOS/<App>"` before and after `open -n -a /Applications/<App>.app`.

Done when the process count doesn't grow from `open -n` alone — that's the signal this technique is needed.

### 2. Copy and re-identify

```bash
cp -R /Applications/<App>.app /Applications/<App>2.app
/usr/libexec/PlistBuddy -c "Set :CFBundleIdentifier <original-id>.dup" /Applications/<App>2.app/Contents/Info.plist
/usr/libexec/PlistBuddy -c "Set :CFBundleName <App>2" /Applications/<App>2.app/Contents/Info.plist
```

`Set` fails on a missing key — use `Add :CFBundleDisplayName string <App>2` instead if that key isn't present. `du -sh` the original first: Electron/Chromium-based apps run several hundred MB per copy.

Done when the copy's `CFBundleIdentifier` and name are unique from the original.

### 3. Re-sign and launch

```bash
codesign --force --deep --sign - /Applications/<App>2.app
open /Applications/<App>2.app
```

Done when `codesign -dv` on the copy shows the new identifier with `Signature=adhoc`, and it launches without a Gatekeeper dialog.

### 4. Verify independence

`pgrep -fl "MacOS/<App>$"` should list two PIDs (original + copy). `ls ~/Library/Containers/ | grep <original-id>` should show both the original identifier and the `.dup` one, each with its own `Data/Documents/`.

Done when both processes run simultaneously and the copy's container is separate and freshly created — ready to log a second, independent account into.
