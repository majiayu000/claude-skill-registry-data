---
name: firefox-cdp-bridge
description: CDP↔BiDi bridge plugin for routing Hermes browser_* tools through Firefox
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [firefox, cdp, bidi, browser, bridge]
    triggers: [firefox-cdp, browser-engine, browser-firefox, browser-provider, cdp-bridge, bidi-proxy]
    related_skills: [firefox-stealth-automation, firefox-remote-control]
---

# Firefox CDP↔BiDi Bridge

## Problem
Firefox 151+ uses **BiDi** (not Chrome CDP) for remote debugging. The Hermes `browser_*` tools call `agent-browser` (a Node.js CLI built on Playwright), which is a **Chrome CDP client** — it can't speak BiDi.

Setting `browser.cdp_url: http://localhost:9222` does NOT work because:
- Firefox 151 serves BiDi on port 9222, not Chrome CDP
- `/json/version` and `/json/list` Chrome endpoints return 404
- `agent-browser` expects Chrome CDP WebSocket protocol

## Architecture
```
Hermes → browser_navigate → agent-browser --cdp ws://127.0.0.1:19222
                                          ↓
                    FirefoxBridge (port 19222)
                      ├── HTTP: /json/version, /json/list (Chrome CDP compat)
                      └── WebSocket: translates CDP → BiDi for Firefox
                                           ↓
                    Firefox BiDi WebSocket (port 9222)
```

## Plugin Location
`~/.hermes/plugins/browser/firefox/` contains:
- `__init__.py` — package marker
- `provider.py` — FirefoxBrowserProvider + FirefoxBridge

## Prerequisites
1. Firefox must be running with `--remote-debugging-port 9222`
2. Hermes must have the plugin loaded

## Usage
```yaml
# In config.yaml:
browser:
  cloud_provider: firefox
```

## Current Limitations
- WebSocket forwarding is echo-only (no CDP↔BiDi translation)
- To fully support all `agent-browser` CDP commands, the WebSocket needs a proper `run_translation_loop()` that maps:
  - `Page.navigate` → `browsingContext.navigate`
  - `Runtime.evaluate` → `script.evaluate`
  - `Input.dispatchMouseEvent` → `input.performActions`
  - `Page.captureScreenshot` → `browsingContext.captureScreenshot`
  - and 15+ other CDP methods to their BiDi equivalents
- See `__init__.py` `_TRANSLATION_MAP` for the starting point

## Alternative: Use MCP Firefox Tools Directly
The `ultimate-firefox-mcp`, `git-stars`, and `personal-intelligence` MCP servers already provide Firefox-based navigate/click/type/screenshot tools. Until the CDP bridge is complete, use those MCP tools for Firefox operations.
