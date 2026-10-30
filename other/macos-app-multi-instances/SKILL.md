---
name: macos-app-multi-instances
description: Run several simultaneous instances of one macOS app (e.g. two or three accounts logged into WeChat at once) by duplicating and re-signing its .app bundle. Use when an app refuses to open a second window and just refocuses the running one, when `open -n -a <App>` launches no new process, or when a second independent login session for the same app is needed without a second macOS user account or VM.
---

# Run several instances of a macOS app

Duplicate and re-sign a macOS app bundle so each copy runs as a separate process the OS treats as a different app: its own sandbox container, its own login session, running alongside the original. Verified on WeChat 4.1.15 (Tencent, App Store, sandboxed): two accounts logged in at once, each in its own container, on 2026-10-25.

## Facts every step rests on

- **`open -n -a` is not the fix.** It forces a new *launch request*, but an app with its own single-instance IPC check (most chat/IM apps) just detects the sibling and refocuses it — no new process shows up in `pgrep`.
- **The container follows the bundle ID, not the code signature.** A sandboxed app's data lives at `~/Library/Containers/<CFBundleIdentifier>/`. Change the identifier in a copy and macOS hands it a fresh, empty container at launch.
- **A plain ad-hoc re-sign drops the sandbox.** `codesign --force --deep --sign -` keeps no entitlements, so the copy runs unsandboxed. WeChat still builds its data path under `~/Library/Containers/<id>/`, but other apps may not.
- **Keeping the sandbox needs care.** An ad-hoc signature cannot carry `com.apple.application-identifier` or `com.apple.developer.team-identifier`; drop them. Keep `com.apple.security.application-groups`, renamed to match the copy (`5A4RE8SF68.com.tencent.xinWeChat` → `…xinWeChat2`): sandboxed WeChat registers Mach services under that name and dies 1 s after launch (`deny mach-register …MachPortRendezvousServer`) without it.
- **The copy is a snapshot, not a mirror.** It doesn't track vendor updates. Rebuild it from the updated original; the data stays in the container, so the login survives.

## Use the script

`scripts/multi_app.py` does it all:

```bash
python3 <skill-dir>/scripts/multi_app.py            # next copy: /Applications/WeChat2.app, then WeChat3.app, …
python3 <skill-dir>/scripts/multi_app.py /Applications/Foo.app
python3 <skill-dir>/scripts/multi_app.py --refresh  # after the original updates: rebuild every copy
```

Each copy N gets bundle ID `<original>N`, `CFBundleName`/`CFBundleDisplayName` `<App>N` (and `<localized name>N` in every `*.lproj/InfoPlist.strings`, which is what Finder, Spotlight and the Dock show: `WeChat2`, `微信2`), and no `Contents/PlugIns` (the Share and FileProvider extensions would register twice under the original's IDs). The script signs it sandboxed first, launches it, and checks the main process is alive after 3 s; if not, it re-signs plain, launches again and says the copy runs without a sandbox. The copy is left running. `--refresh` skips a running copy, and warns when a once-sandboxed copy falls back to plain, since it then no longer sees its old data. `python3 scripts/test_multi_app.py` checks the numbering.

`du -sh` the original first: WeChat is about 700 MB per copy.

## Verify

`pgrep -fl 'MacOS/WeChat$'` lists one process per instance. `codesign -d --entitlements - --xml /Applications/WeChat2.app | plutil -p -` shows `app-sandbox` and the renamed group. `lsof -p <pid>` of the copy's main process shows files only under `~/Library/Containers/<original>N`. Log a second account into the copy; the original stays logged in.
