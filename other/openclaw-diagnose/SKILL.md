---
name: openclaw-diagnose
description: Diagnose and fix OpenClaw gateway and node host issues. Use when openclaw services have warnings, connection failures, pairing errors, or port conflicts.
allowed-tools: Bash Read Grep
---

# OpenClaw Diagnose

When the user asks you to diagnose or fix OpenClaw gateway/node issues, follow this structured investigation.

## Step 1: Gather status

Run these in parallel:

```bash
openclaw gateway status
openclaw node status
openclaw nodes status
openclaw nodes pending
```

## Step 2: Analyze warnings

Look for these common issues:

### Multiple gateway-like services detected
- Check if both `ai.openclaw.gateway` and `ai.openclaw.node` are registered as LaunchAgents
- Use `launchctl print gui/$(id -u)/<label>` to inspect each service
- Use `lsof -iTCP:<port> -sTCP:LISTEN -P` to confirm which process owns the port
- The gateway **listens** on the port; the node host **connects to** the gateway on that port — they do NOT conflict

### Pairing required errors
- Check `~/.openclaw/logs/node.err.log` for `pairing required` or `ECONNREFUSED`
- If the node shows "pairing required", run `openclaw nodes pending` to find the pending request
- Approve with: `openclaw nodes approve <requestId>`
- **Pairing requests expire quickly** — if approval fails with "unknown requestId", restart the node (`openclaw node restart`) and immediately re-check pending + approve

### ECONNREFUSED errors
- The gateway may not be running yet when the node starts
- Check if gateway is listening: `lsof -iTCP:<port> -sTCP:LISTEN -P`
- If gateway is down: `openclaw gateway restart`
- The node has `KeepAlive: true` so it will automatically reconnect once the gateway is up

## Step 3: Verify fix

After taking corrective action, confirm health:

```bash
openclaw nodes status    # Should show: paired · connected
openclaw nodes pending   # Should show: No pending pairing requests
tail -5 ~/.openclaw/logs/node.err.log  # Check for new errors
```

## Key architecture notes

- **Gateway** (`ai.openclaw.gateway`): WebSocket server that listens on a port (default 18789)
- **Node host** (`ai.openclaw.node`): Client that connects to the gateway via WebSocket to register capabilities (browser, system commands)
- The `--host` and `--port` flags on `openclaw node run` specify the **gateway address to connect to**, not a port to bind
- One gateway supports multiple nodes — running both on the same machine is the normal setup
- Node plist is at `~/Library/LaunchAgents/ai.openclaw.node.plist`
- Gateway plist is at `~/Library/LaunchAgents/ai.openclaw.gateway.plist`
- Node logs: `~/.openclaw/logs/node.log` and `~/.openclaw/logs/node.err.log`
