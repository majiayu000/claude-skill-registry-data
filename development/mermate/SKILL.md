---
name: mermate
description: Master orchestrator for the Mermate application (mermaid-gpt v5.0.0) — the 5-tab agentic artifact progression Simple Idea → Markdown Spec → Mermaid → TLA+ → TypeScript. Carries the authoritative model of the pipeline state machine, the run-lineage contract, Opseeq stage reporting, and the coordination map to all tab and infrastructure sub-skills. Invoke for ANY work in this repository — coding, debugging, refactoring, extending any tab, route, agent flow, or the MCP bridge.
---

# Mermate

## Binding Persona
Operate under the standards of Leslie Lamport (Turing Award 2013), as established in `specification-master-agent`. The application itself is a state machine; treat it as one. The backend is the single source of truth — the frontend never guesses. Reject cleverness that obscures which state a run is in, and reject any change that lets the UI infer what the server must declare.

## The System (Ground Truth)
Mermate is a Node/Express app (`server/index.js`, port 3333, `npm start`) serving a static frontend (`public/`) with a Python MCP sidecar (`mcp_service/`). Its purpose: refine a raw idea into a verified artifact chain through five tabs, each a state in one progression:

```
idea ──▶ md ──▶ mmd ──▶ tla ──▶ ts        (rust is an optional terminal extension)
```

- Frontend controller: `public/js/mermaid-gpt-app.js` — `STAGE_REGISTRY` (lines 28–130) is the single source of truth for every stage's identity, visuals, input config, wait bands, and IPO contract. Never duplicate stage semantics elsewhere.
- Agent panel: `public/js/mermaid-gpt-agent.js` — two-phase flow (run → pause for notes → finalize), detached sessions surviving refresh via `GET /api/agent/attach/:sessionId`.
- Backend routes: `server/routes/{render,tla,ts,tsx,rust,agent,search,transcribe,specula,openclaw,bundle,trace,runs}.js`, mounted in `server/index.js`.
- Content routing: `server/services/input-router.js` classifies input into `text | md | mmd | hybrid` and selects the pipeline.

## The State Machine (Binding Model)
- **Variables**: current stage, unlocked stage set, run lineage (`run_id`), artifact store (`flows/`, `runs/`, `archs/`).
- **Transitions**: only a stage endpoint may advance the machine, and it declares the new state in its `progressionUpdate` payload:
  ```json
  { "stage": "mmd|tsx|tla|ts|rust",
    "unlockedStages": ["idea","md","mmd", ...],
    "nextRecommended": "tla",
    "confidence": 0.0 }
  ```
- **Invariants** (violations are bugs, report them as such):
  1. **Server-declared readiness**: the frontend renders readiness exclusively from `progressionUpdate`; it never infers unlock state.
  2. **Lineage**: every artifact belongs to a `run_id`; runs are replayable/auditable through `runs/` JSON and `GET /api/mermate/trace/:run_id`.
  3. **Monotonic unlock**: stages unlock, they do not silently re-lock.
  4. **Non-blocking telemetry**: Opseeq reporting (`server/services/opseeq-bridge.js` `reportStage`) is fire-and-forget; it must never stall a pipeline stage.
  5. **Skeleton honesty**: a stage emits failure (`render_failed`, `tla_failed`, `ts_failed`) rather than a fabricated success.

## Skill Coordination (Decision-Point Mapping)
| Decision point | Mandatory sub-skill |
|---|---|
| Tab 1 work — idea intake, enhancement, voice | `mermate-tab-idea` |
| Tab 2 work — markdown spec intake/refinement | `mermate-tab-markdown` |
| Tab 3 work — Mermaid compile, render, depth | `mermate-tab-mermaid` |
| Tab 4 work — TLA+ generation, SANY/TLC | `mermate-tab-tla` |
| Tab 5 work — TypeScript runtime gen/test | `mermate-tab-typescript` |
| Agent sessions, Opseeq, MCP bridge, run lineage, boot/health | `mermate-agentic-infra` |
| MCP tool surface changes | `mermate-openclaw-mcp` (.agents) |
| Opseeq gateway config/troubleshooting | `mermate-opseeq-connect` (.agents) |
| Formal rigor on the TLA+ stage | `specification-master-agent` tree |

Never load more sub-skills than the current tab or decision requires. This master skill remains sole authority on cross-stage invariants.

## Behavioral Doctrine
1. Read the code before changing it: stage semantics live in `STAGE_REGISTRY` and the owning route file — cite them, don't reinvent them.
2. A change touching stage progression must preserve the `progressionUpdate` contract and the five invariants above, or it is refused with the gap named.
3. Telemetry (Opseeq) is optional infrastructure: boot and render must succeed with the gateway down (`fallback_events` in traces prove this).
4. Laziness discipline from `ponytail` applies to all edits: shortest correct diff, reuse existing services, no speculative scaffolding.

## Verification (run what matches the change)
- `npm test` — full suite (`node --test test/test-*.js`)
- `npm run test:fast` — fast unit tests
- `node --test test/test-e2e-tandem.js` — tandem hardening loop: render → TLA+ → TS with trace correlation; self-contained, spawns its own server
- `python3 -m unittest test/test_mermate_mcp_service.py` — MCP bridge
- `curl -s http://localhost:3333/api/health | python3 -m json.tool` — live boot sanity
