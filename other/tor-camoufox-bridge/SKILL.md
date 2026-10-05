---
name: tor-camoufox-bridge
version: 1.0.0
author: Hermes Agent
license: MIT
description: Unified browser bridge that routes through Tor Browser (primary) with Camoufox fallback for sites that block Marionette/geckodriver
metadata:
  hermes:
    tags: [tor, camoufox, bridge, browser-automation, anti-detection, proxy]
    triggers:
      - tor-camoufox bridge
      - camouflage extension
      - browser bridge
      - tor fallback
      - anti-detection routing
      - marionette bypass
    related_skills: [tor-browser-mcp, firefox-stealth-ops, tor-circuit-rotation]
---

## Overview

The Tor-Camoufox Bridge provides a unified MCP tool surface that:
1. Routes requests through **Tor Browser** (via torbrowser-mcp) by default — full anonymity properties preserved
2. Falls back to **Camoufox** (anti-detection browser) when sites detect Marionette automation
3. Supports manual engine switching via `bridge_switch`

## Components

| Component | Location | Description |
|-----------|----------|-------------|
| Tor Browser MCP | `${MY_REPOS}/Documents/github/tor-browser-mcp` | Hardened fork with 74 tools |
| Camoufox Engine | `${MY_REPOS}/Documents/github/camofox-browser` | Anti-detection browser (REST API on :9377) |
| Camoufox MCP (Enhanced) | `camofox-browser/enhanced_mcp_server.py` | Full 35-endpoint REST → MCP bridge |
| Tor-Camoufox Bridge | `~/.hermes/scripts/tor_camoufox_bridge.py` | Unified orchestrator MCP server |
| Start Script | `~/.hermes/scripts/start-camoufox.sh` | Auto-starts Camoufox on boot |

## Scheduled Jobs

| Job | Schedule | Purpose |
|-----|----------|---------|
| `hermes-nightly-watchdog` | Daily 3 AM ET | Update Hermes + Gateway, check repos, restart gateway |
| `tor-circuit-rotation` | Every 6 hours | Request fresh Tor circuit, verify IP change |

## Nightly Watchdog

The watchdog at `~/.hermes/scripts/hermes-nightly-watchdog.py` runs these phases:

1. **Hermes Agent Update** — `hermes update --check` then `hermes update -y`
2. **Pip Package Check** — `pip list --outdated`
3. **Git Repos** — Pull, commit, push 4 repos
4. **AI News Scan** — Upstream Hermes releases, commits
5. **PIM Check** — PIM DB size, recent activity
6. **Camoufox Check** — Health check, auto-start if down
7. **Gateway Restart** — Stop, verify, start, verify
8. **System Health** — Disk, memory, uptime
9. **Report** — Markdown to `~/.hermes/nightly-reports/`
10. **Commit** — Reports committed to hermes-config repo

## Bridge Tools

| Category | Tools |
|----------|-------|
| **Tor Browser** | `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_new_identity` |
| **Camoufox Fallback** | `camoufox_navigate`, `camoufox_snapshot`, `camoufox_screenshot`, `camoufox_status`, `camoufox_start`, `camoufox_stop` |
| **Diagnostics** | `bridge_status`, `bridge_switch` |

## Circuit Rotation

`tor-circuit-rotation` fires every 6 hours, calls NEWNYM, verifies exit IP change, and reports the result.

## Config Entries

```yaml
mcp_servers:
  tor-browser-mcp:
    args: [-m, torbrowser_mcp, --tbb-root, ${USER_HOME}/TorBrowser, ...]
    command: ${USER_HOME}/.../python.exe
    workdir: ${MY_REPOS}/Documents/github/tor-browser-mcp
    timeout: 300
  camoufox-enhanced:
    args: [enhanced_mcp_server.py]
    command: python
    workdir: ${MY_REPOS}/Documents/github/camofox-browser
    timeout: 300
  tor-camoufox-bridge:
    args: [${USER_HOME}/.hermes/scripts/tor_camoufox_bridge.py]
    command: python
    timeout: 300
```
