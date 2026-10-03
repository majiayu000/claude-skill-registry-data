---
name: mermate-opseeq-connect
description: Use when configuring, troubleshooting, or verifying the connection between Mermate and the Opseeq runtime gateway, including stage event reporting and pipeline orchestration.
---

# Mermate-Opseeq Connection

## Required Configuration

### .env
```
OPENAI_BASE_URL=http://localhost:9090/v1
OPSEEQ_URL=http://localhost:9090
```

Do NOT include `/v1` in `OPSEEQ_URL` — each module appends path segments as needed.

### .mcp.json
```json
{
  "mcpServers": {
    "opseeq": { "url": "http://localhost:9090/mcp", "transport": "sse" },
    "synth": { "command": "synthesis-mcp", "transport": "stdio" }
  }
}
```

## Pipeline Stage Reporting

Mermate reports stage events to Opseeq via `opseeq-bridge.js`:
- `reportStage(runId, stageEvent)` — POST to `OPSEEQ_URL/api/mermate/stage`
- `getTrace(runId)` — GET from `OPSEEQ_URL/api/mermate/trace/:run_id`

Stage flow: `render -> tla -> ts -> rust -> desktop`

## Opseeq MCP Tools for Mermate

Available via Opseeq MCP at `http://localhost:9090/mcp`:
- `mermate_status` — copilot health, TLA+, TS, agent availability
- `mermate_agent_modes` — list agent modes
- `mermate_render` — send source for compilation
- `mermate_generate_tla` — generate TLA+ from run
- `mermate_generate_ts` — generate TypeScript from run
- `pipeline_orchestrate` — full multi-stage pipeline with review
- `artifact_verify` — verify pipeline artifacts

## Docker

Image tag: `mermate:v5`
Build: `docker build -t mermate:v5 .`
Opseeq rebuild from Mermate: `npm run opseeq:docker:build`

## Health Verification

1. Mermate: `curl http://localhost:3333/api/copilot/health`
2. Opseeq: `curl http://localhost:9090/health`
3. Cross-check: `curl http://localhost:9090/api/status` — verify `mermate.running = true`
