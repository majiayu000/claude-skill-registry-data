---
name: agent-zero
description: Debug and troubleshoot Agent Zero — ettametta's autonomous production loop. Use when the loop stalls, state recovery fails, renders crash, or the scouting/screening/brainstorming pipeline breaks.
---

# Agent Zero Debugging

Agent Zero is ettametta's autonomous viral content loop: scout trends, screen for virality, brainstorm scripts, render video, publish — then sleep 4h and repeat.

## Quick Diagnostics

```bash
# Agent status
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/zero/status

# State in DB
docker compose exec -T db psql -U ettametta -d ettametta -c "SELECT id, is_running, current_step, last_run_at, next_run_at FROM agent_zero_states ORDER BY id DESC LIMIT 5;"

# Latest insights
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/zero/insights

# KPI file (in-container)
docker compose exec api cat /tmp/agent_zero_kpis.json 2>/dev/null || echo "No KPIs yet"
```

## Architecture

### State Machine

```
IDLE → SCOUTING → SCREENING → BRAINSTORMING → RENDERING → PUBLISHING → WAITING (4h sleep)
  ↑                                                       |
  └───────────────────────────────────────────────────────┘
  On exception: ERROR → 5min backoff → retry from last state
```

### Tools (8 registered)

| Tool | File | Method | Purpose |
|------|------|--------|---------|
| `discovery` | `tools/discovery.py` | HTTP → `/api/v1/discovery/search` | Find trending content |
| `screener` | `tools/market_screener.py` | Groq LLM | Sentiment/monetization scoring |
| `render` | `tools/render.py` | HTTP → `/api/v1/remotion/render` | Trigger Remotion render |
| `remotion` | `tools/remotion_render.py` | `subprocess.run` (npx) | Direct Remotion CLI — bypasses API |
| `publish` | `tools/publish.py` | HTTP → `/api/v1/publish/video` | Multi-platform publish |
| `affiliate` | `tools/affiliate.py` | HTTP → `/api/v1/monetization` | Affiliate link recommendation |
| `paperclip` | `tools/paperclip_kpi.py` | File I/O (`/tmp/agent_zero_kpis.json`) | KPI tracking |
| `interpreter` | `tools/interpreter.py` | Sandboxed exec | Code execution |

### Self-Healing

- **State persistence:** `_persist_state()` writes JSON to `agent_zero_state` DB table (columns: `is_running`, `last_run_at`, `next_run_at`, `current_step`)
- **Startup recovery:** `load_and_resume()` in `src/api/main.py:195` reads DB and auto-restarts the loop if `is_running` was true
- **Error backoff:** Exception → `current_step = "ERROR"` → 300s sleep → retry

### Key Files

| File | Purpose |
|------|---------|
| `src/services/agent_zero/agent.py` | Core `AgentZero` class, `run_iteration()` state machine |
| `src/services/agent_zero/tools/discovery.py` | Discovery API client |
| `src/services/agent_zero/tools/render.py` | Remotion HTTP render client |
| `src/services/agent_zero/tools/remotion_render.py` | Direct Remotion CLI (subprocess) |
| `src/services/agent_zero/tools/publish.py` | Publisher API client |
| `src/services/agent_zero/tools/affiliate.py` | Monetization API client |
| `src/services/agent_zero/tools/market_screener.py` | Groq LLM screener |
| `src/services/agent_zero/tools/paperclip_kpi.py` | KPI file tracker |
| `src/services/agent_zero/tools/interpreter.py` | Sandboxed code execution |
| `src/api/routes/zero.py` | REST API — status, start, stop, insights |
| `src/api/utils/models.py` | `AgentZeroState` DB model |
| `src/services/openclaw/skills/agent_zero.py` | OpenClaw chat skill wrapper |

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/zero/status` | GET | User | Live status (is_running, current_step, integrity) |
| `/zero/start` | POST | User | Launch loop in background task |
| `/zero/stop` | POST | User | Send halt signal |
| `/zero/insights` | GET | User | Latest LLM-generated strategy |

## Common Issues

### Loop stuck at ERROR
Agent caught an exception and is in 5-min backoff. Check logs:
```bash
docker compose logs --tail=100 api 2>&1 | grep -i "agent_zero\|AgentZero\|ERROR"
```
If persistent, check which step failed via `GET /zero/status`.

### State not recovering after restart
`load_and_resume()` only fires if `is_running=true` in DB. Check:
```bash
docker compose exec -T db psql -U ettametta -d ettametta -c "SELECT is_running, current_step FROM agent_zero_states ORDER BY id DESC LIMIT 1;"
```

### Remotion render fails in Agent Zero
Two render paths exist: HTTP API (`tools/render.py`) and direct CLI (`tools/remotion_render.py`). The CLI path uses `subprocess.run` — check if `npx` is available in the container:
```bash
docker compose exec api which npx
```

### KPIs not updating
KPIs are written to `/tmp/agent_zero_kpis.json`. Container restarts wipe `/tmp`. This is by design (ephemeral metrics).

### Screener returns empty
`market_screener.py` calls Groq LLM. Check:
```bash
docker compose exec api python3 -c "from src.api.config import settings; print('GROQ:', 'SET' if settings.GROQ_API_KEY else 'MISSING')"
```

## Integration with OpenClaw

`src/services/openclaw/skills/agent_zero.py` exposes `AgentZeroSkill` — start/stop/status via chat commands. OpenClaw acts as the conversational frontend for Agent Zero.

## Debugging Checklist

1. Is Agent Zero running? `GET /zero/status`
2. What step is it on? `current_step` field
3. DB state: `SELECT * FROM agent_zero_states`
4. Logs: `docker compose logs api | grep -i agent_zero`
5. LLM keys set? Check GROQ_API_KEY, OPENAI_API_KEY
6. Remotion available? `npx remotion --version` in container
7. Discovery service up? `curl http://localhost:8000/api/v1/discovery/search`
