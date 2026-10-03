---
name: mermate-agentic-infra
description: Core agentic infrastructure of the Mermate application — detached agent sessions (run/finalize/attach/stop), agent modes, depth scoring and role caps, Opseeq stage-event bridge with heartbeat lifecycle, run lineage and trace store, boot/health gates, and the Python MCP bridge. Use when working on server/routes/agent.js, opseeq-bridge.js, run tracking, server boot/health, mcp_service/, or cross-cutting pipeline behavior rather than a single tab.
---

# Mermate Agentic Infrastructure

Operates under `mermate` master invariants; Lamport standards via `specification-master-agent`. This skill owns the machinery *between* the tabs; tab-specific work belongs to the `mermate-tab-*` skills.

## 1. Agent Sessions (server/routes/agent.js, public/js/mermaid-gpt-agent.js)
- Two-phase flow: **Phase 1** `POST /api/agent/run` (planning → refinement → preview render → pause for notes) → **Phase 2** `POST /api/agent/finalize` (apply notes → final Max render).
- **Detached sessions**: owned by session, not SSE connection; events buffered for replay. Reattach `GET /api/agent/attach/:sessionId`, stop `POST /api/agent/stop/:sessionId`, list `GET /api/agent/active`, modes `GET /api/agent/modes`.
- Grace: 300s no-listener timeout (`MERMATE_AGENT_GRACE`); sessions retained 10 min after completion; frontend persists session id in localStorage (`MermaidAgent.SESSION_KEY`).
- Agent modes: `code-review`, `thinking`, `optimize-mmd`, `tla-verify`, `tla-optimize`, `ts-generate`, `ts-optimize`, `full-build`.

**Invariants**
1. A session's event stream is replayable: reattach after refresh delivers buffered events in order; no event is lost to a dropped SSE connection.
2. Terminal SSE events are never dropped: `preview_ready`, `final_render`, `done`, `error`.
3. Depth scoring gates fan-out: `depthScore` (0–1) → tier shallow/medium/deep → role cap 2/3/4, reported as `agent_depth_score` to Opseeq.

## 2. Opseeq Bridge (server/services/opseeq-bridge.js)
- `OPSEEQ_URL` default `http://localhost:9090`; `reportStage(runId, stageEvent)` is **fire-and-forget** — WebSocket first, HTTP fallback (at-least-once), local persistence via `traceStore.append()`. Opseeq dedupes on `(run_id, stage, ts)`.
- Stage events: `render_start/complete/failed`, `agent_depth_score/planning/preview/finalize`, `tla_complete/failed`, `ts_complete/partial/failed`.
- Heartbeat lifecycle (server/index.js): frontend pings `POST /api/opseeq/heartbeat`; >60s silence (`OPSEEQ_HEARTBEAT_TIMEOUT_MS`) stops the container; boot gate polls ≤30s; warm-up failure is non-fatal.

**Invariants**
4. The pipeline never blocks on Opseeq: gateway down → `fallback_events` in the trace, render still succeeds.
5. Boot waits are bounded (server 30s gate; frontend 4×2s warm poll + 20s heartbeat badge) — no unbounded stall on optional infrastructure.

## 3. Run Lineage & Traces
- Every run: `run_id` + JSON lineage in `runs/`, artifacts in `flows/`, archived sources in `archs/`.
- Read paths: `GET /api/runs`, `GET /api/artifacts/:run_id`, `GET /api/runs/:runId/bundle`, `GET /api/mermate/trace/:run_id` (server/routes/trace.js).
- Search/projects: server/routes/search.js over DuckDB (`server/backend/query`).

**Invariant**
6. Lineage is append-only and auditable: a trace read back via `/api/mermate/trace/:run_id` reconstructs the run's stage order without gaps.

## 4. MCP Bridge (mcp_service/ — Python)
- `server.py` (tools, stage map) / `client.py` (HTTP+SSE transport); thin layer over Express — no synthetic workflows. Stage map: render, tla, ts, rust, tsx, agent_preview, agent_finalize, agent_session, runs, artifacts, bundle, guide, specula, trace, tla_harness.
- Config: `.mcp.json` → `.venv-mcp/bin/python -m mcp_service`, `MERMATE_URL=http://127.0.0.1:3333`, `OPENCLAW_URL=http://127.0.0.1:8787`. External servers: `opseeq` (SSE, :9090/mcp), `synth` (`synthesis-mcp`, stdio — external, not in this repo).
- Authoring discipline: see `mermate-openclaw-mcp` (.agents) — maintained under `ponytail`.

## 5. Boot & Health
- `npm start` → `server/index.js` :3333; `GET /api/health` reports copilot, Opseeq (healthy/warming), toolchain status.
- Setup: `docs/installation.md` (`./mermaid.sh start`, optional Ollama/OpenAI providers, `.env`).

## Anti-Patterns (Reject)
- Coupling a stage's success path to Opseeq availability.
- Session state keyed to SSE connection instead of session id.
- New MCP tools that don't map to a real Express route.
- Unbounded waits/retries anywhere in boot, heartbeat, or telemetry.

## Verification
- `node --test test/test-e2e-tandem.js` — full tandem loop incl. trace correlation + `fallback_events`
- `node --test test/test-e2e-agent.js` — agent workflow
- `python3 -m unittest test/test_mermate_mcp_service.py` — MCP bridge
- `curl -s http://localhost:3333/api/health | python3 -m json.tool`
