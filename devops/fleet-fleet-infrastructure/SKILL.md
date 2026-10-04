---
name: fleet-fleet-infrastructure
description: Understanding the fleet's own infrastructure — MC, gateway, LocalAI, IRC, Plane, daemons. What each service does, how they connect, and how to diagnose issues. Maps to devops_infrastructure_health.
---

# Fleet Infrastructure — DevOps Domain Knowledge

The fleet runs on 6+ services. When something breaks, you need to know what talks to what, what logs to check, and how to restart without losing state.

## The Service Map

| Service | Port | What It Does | Config |
|---------|------|-------------|--------|
| Gateway (OpenArms) | 18789 (WS), 9400 (HTTP) | Agent sessions, heartbeats, MCP, CRONs | Gateway config |
| Mission Control | 8000 | Tasks, agents, board memory, approvals | Docker + env |
| MC Frontend | 3000 | Web dashboard for PO | Docker |
| LocalAI | 8090 | Local LLM inference, embeddings | AICP project |
| IRC (miniircd) | 6667 | Real-time agent communication | scripts/setup-irc.sh |
| The Lounge | 9000 | Web IRC client for PO | scripts/setup-lounge.sh |
| ntfy | external | Push notifications to PO mobile | 3 topics |

## How They Connect

```
PO → MC Frontend (3000) → MC Backend (8000) ← Orchestrator (30s cycle)
                                              ↓
Gateway (18789) ← Agent Sessions ← MCP Server ← fleet/mcp/tools.py
     ↓                                          ↓
IRC (6667) ← The Lounge (9000) ← PO       Events → Board Memory
     ↓                                          ↓
ntfy (external) → PO mobile                Plane (optional)
```

The orchestrator is the brain — it reads from MC, writes context files, dispatches tasks, wakes agents, monitors health. It runs as a daemon (`fleet/cli/orchestrator.py`), not as a service.

## Health Check Protocol

When you call `devops_infrastructure_health()`:

### 1. MC Backend
```
Check: curl -s http://localhost:8000/api/v1/agents
Healthy: returns JSON array of agents
Unhealthy: connection refused, timeout, or 5xx error
```

### 2. Agent Status
```
Check: count agents where status = "online"
Healthy: 10/10 online (or expected count)
Warning: <8 online (some offline)
Critical: <5 online (fleet degraded)
```

### 3. Gateway
```
Check: gateway process running (PID file or ps)
Healthy: process exists, WebSocket accepting connections
Unhealthy: process dead, OOM killed, config error
```

### 4. IRC
```
Check: nc -z localhost 6667
Healthy: port responding
Unhealthy: miniircd not running
```

## Common Issues and Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Gateway OOM | Too many concurrent sessions, NODE_OPTIONS too low | Increase heap: `NODE_OPTIONS="--max-old-space-size=4096"` |
| Agents stuck "provisioning" | last_seen_at not set on provision | Patch: set last_seen_at when status=online |
| MC returns 500 | Database migration needed or Docker restart | `docker compose restart mc-backend` |
| IRC not connecting | miniircd not started | `scripts/setup-irc.sh` |
| Heartbeats not firing | Gateway config stale or agent session pruned | `scripts/clean-gateway-config.sh` |
| Orchestrator crash | Missing import or config | Check `fleet orchestrator` logs |

## The Daemon Ecosystem

4 daemons run alongside the gateway:

| Daemon | Interval | What It Does |
|--------|---------|-------------|
| Orchestrator | 30s | 13-step brain cycle: context → dispatch → health |
| Sync | 60s | Board sync, Plane sync |
| Monitor | 300s | Budget monitoring, storm detection |
| Auth | 120s | OAuth token refresh |

Start all: `fleet daemon start`
Check: `fleet daemon status`
Logs: `fleet logs` (combined) or `fleet logs orchestrator`

## IaC Principle

Everything is scripted. No manual steps after checkout:
- `scripts/setup.sh` — zero to running fleet
- `scripts/start-fleet.sh` — gateway startup
- `scripts/setup-mc.sh` — MC Docker setup
- `make status` — fleet overview
- `make gateway` — start gateway
- `make mc-up` — start MC

When you fix an infrastructure issue, the fix goes in a script — not in a "run this command" instruction. The next `setup.sh` run should produce the same result.
