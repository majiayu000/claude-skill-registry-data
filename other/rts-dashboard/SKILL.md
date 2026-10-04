---
name: rts-dashboard
description: "RTS (Real-Time Strategy) style monitoring dashboard for OpenClaw. Provides a browser-based tactical command center with real-time visualization of agents, skills, sessions, cron jobs, and system vitals. Features include a tactical map with active agents, radar scan animation, agent/skill detail panels, and chat messaging via Gateway WebSocket (chat.send). Use when the user wants to monitor OpenClaw status visually, launch a dashboard, or view agents/sessions/skills in a game-style UI."
---

# RTS Dashboard

A StarCraft/C&C-inspired tactical command center for OpenClaw monitoring.

## Agent Actions

### Start Dashboard

When the user wants to open/view/launch the dashboard, or when visiting `127.0.0.1:4320` fails:

1. **Check if already running:**
   ```powershell
   Get-NetTCPConnection -LocalPort 4320 -ErrorAction SilentlyContinue
   ```
2. **If not running, start it in background:**
   ```powershell
   cd "<skill_dir>"; node server.js
   ```
   Use `exec` with `background: true` and `yieldMs: 3000`, then check logs to confirm `⚡ Online` message.
3. **If `node_modules/` is missing**, run `npm install` first.
4. Tell the user: `http://127.0.0.1:4320` is ready.

### Stop Dashboard

```powershell
Get-NetTCPConnection -LocalPort 4320 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
```

## Quick Start (Manual)

```bash
cd rts-dashboard
npm install
node server.js
```

Open `http://127.0.0.1:4320` in browser.

## Requirements

- Node.js 18+
- OpenClaw Gateway running (default port 18789)
- `ws` npm package (auto-installed via `npm install`)

## Features

- **Tactical map**: Active agents as diamond nodes with orbiting skill dots and trail animation
- **Left panel**: Full agent list + skill library with search
- **Right panel**: System vitals (CPU/RAM), gateway status, event logs, selected target details
- **Agent detail**: Model, current task, deployed skills, recent conversation
- **Skill detail**: Description, use cases, related agents
- **Chat bar**: Send messages to agents via Gateway WebSocket `chat.send` RPC
- **Cron jobs**: Display scheduled tasks with status on the map
- **5-min cooldown**: Agents remain visible for 5 minutes after going offline (amber blink + countdown)
- **CRT scan line + radar sweep + grid**: Full military-UI aesthetic

## Configuration

Environment variables (all optional):

| Variable | Default | Description |
|----------|---------|-------------|
| `RTS_PORT` | `4320` | Dashboard HTTP port |
| `OPENCLAW_GATEWAY_PORT` | `18789` | Gateway port |
| `OPENCLAW_HOME` | `~/.openclaw` | OpenClaw home directory |
| `OPENCLAW_GATEWAY_TOKEN` | (from config) | Gateway auth token |

## Authentication

The dashboard implements Ed25519 device signing for Gateway WebSocket authentication:

- On first launch, generates a keypair and saves to `.device-keys.json`
- Signs each `connect.challenge` nonce using v3 protocol
- Gateway token is auto-discovered from `OPENCLAW_GATEWAY_TOKEN` env var or `gateway.auth.token` in `openclaw.json`
- Localhost connections are auto-approved by Gateway (no manual pairing needed)
- **No `dangerouslyDisableDeviceAuth` or `allowInsecureAuth` required**

## Cross-Platform

- OpenClaw installation path auto-detected via `require.resolve` → `which/where` → `npm root -g` → fallback paths
- Skill directories: `~/.agents/skills/` (user) + `{openclaw}/skills/` (built-in) + `{openclaw}/extensions/*/skills/` (extensions)
- Agent/skill config parsed via `JSON.parse` (robust, no regex)
- Works on Windows, macOS, and Linux

## Gateway Requirements

The dashboard needs the Gateway to allow its WebSocket origin:

```json5
{
  gateway: {
    controlUi: {
      allowedOrigins: ["http://127.0.0.1:4320"]
    }
  }
}
```

This is the only Gateway config change needed. Apply with `openclaw config set gateway.controlUi.allowedOrigins '["http://127.0.0.1:4320"]'` or via the Control UI config panel.

## Data Sources (refreshed every 3 seconds)

- **Agents**: `~/.openclaw/openclaw.json` → `agents.list`
- **Skills**: Filesystem scan of skill directories
- **Active sessions**: `.jsonl.lock` files in `~/.openclaw/agents/*/sessions/`
- **System vitals**: Node.js `os` module (CPU delta sampling every 2s)
- **Gateway status**: HTTP GET to gateway root
- **Cron jobs**: `~/.openclaw/cron/jobs.json`

## File Structure

```
rts-dashboard/
├── SKILL.md          # This file
├── server.js         # Node.js server (HTTP + WebSocket)
├── package.json      # Dependencies (ws only)
└── public/
    └── index.html    # Single-file dashboard (HTML + CSS + Canvas JS)
```
