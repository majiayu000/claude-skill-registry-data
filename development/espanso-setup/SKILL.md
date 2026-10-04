---
name: espanso-setup
description: Use when setting up Espanso text expansion on macOS, troubleshooting
  the service not starting, or configuring autostart via LaunchAgent.
---

## Purpose

Configure Espanso to run as a background service on macOS (no GUI app).

## Standard Setup

```zsh
espanso service register   # creates LaunchAgent plist
espanso start              # starts the service
```

Verify:
```zsh
espanso status
launchctl print gui/$(id -u)/com.federicoterzi.espanso | grep state
```

Expected: `state = running`.

## If service fails to start

Most common cause: leftover processes from a previous run or the GUI app
interfere with `service register`.

Fix: clean slate before registering.

```zsh
# 1. Remove existing LaunchAgent if present
launchctl bootout gui/$(id -u)/com.federicoterzi.espanso 2>/dev/null
rm ~/Library/LaunchAgents/com.federicoterzi.espanso.plist 2>/dev/null

# 2. Kill all espanso processes
pkill -x espanso

# 3. Verify clean
pgrep -x espanso || echo "clean"

# 4. Re-register and start
espanso service register
espanso start
```

## Notes

- Config lives in `~/Library/Application Support/espanso/` (not XDG)
- `espanso launcher` exits with code 2 when processes are already running — this is normal, not a bug
- Tested on macOS 26.5 (Darwin 25.5.0)
- Do NOT use the GUI app (.app) alongside the service — they conflict
