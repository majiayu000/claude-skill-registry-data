---
name: headless-chrome-cdp
description: >
  Launch and troubleshoot Chrome with CDP (remote debugging) on headless Linux servers without X11/display.
  Use when browser_navigate fails with "Connection refused" on the CDP port, or when launching Chrome for browser automation on a headless machine.
---

# Headless Chrome CDP Setup

## Problem
`browser_navigate` or `browser_cdp` fails with `Connection refused` on port 9222 (or configured CDP port). Config has `cdp_url` set but Chrome isn't exposing it.

## Root Cause
Chrome requires an X server or display environment to run GUI mode. On headless Linux (no desktop, no `$DISPLAY`), Chrome crashes with:
```
ERROR: ui/ozone/platform/x11/ozone_platform_x11.cc:256] Missing X server or $DISPLAY
ERROR: ui/aura/env.cc:246] The platform failed to initialize. Exiting.
```

## Solution

### Step 1: Kill existing Chrome instances
```bash
pkill -f chrome 2>/dev/null
sleep 1
```

### Step 2: Launch headless Chrome with CDP
```bash
/opt/google/chrome/chrome \
  --headless=new \
  --remote-debugging-port=9222 \
  --no-first-run \
  --no-default-browser-check \
  --no-sandbox \
  --disable-gpu
```
Run in background with `terminal(background=true)`.

### Step 3: Verify CDP is reachable
```bash
sleep 5 && curl -s http://127.0.0.1:9222/json/version
```
Should return a JSON object with `"Browser"`, `"Protocol-Version"`, and `"webSocketDebuggerUrl"`.

### Step 4: Use browser tools
Navigate normally — `browser_navigate` will now connect via CDP.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Connection refused` after launch | Chrome crashed or didn't bind port | Check `process(action="log")` for X server errors |
| Port 9222 already in use | Previous Chrome instance still running | `fuser -k 9222/tcp` then relaunch |
| `Missing X server` in logs | Not using `--headless=new` | Add `--headless=new` flag |
| Permission denied | Running as root without sandbox | Add `--no-sandbox` flag |
| CDP returns version but `browser_navigate` still fails | Config `cdp_url` mismatch | Verify `~/.hermes/config.yaml` has `cdp_url: http://127.0.0.1:9222` |

## Notes
- `--headless=new` is the modern headless mode (Chrome 109+). Avoid legacy `--headless` without `/new`.
- `--no-sandbox` is required when running as root or in containers.
- After relaunching Chrome, browser sessions reset — any open tabs are gone.
- This is a general infrastructure issue, not specific to any single tool or skill.