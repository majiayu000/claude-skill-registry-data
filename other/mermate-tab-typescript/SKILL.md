---
name: mermate-tab-typescript
description: Stage 5 tab (TypeScript) of the Mermate pipeline — TypeScript runtime generation from a verified TLA+ spec, tsc compile, tsx test harness, coverage, and the terminal progressionUpdate. Use when editing TS generation, the test harness, /api/render/ts endpoints, or TS↔TLA+ conformance. Refinement judgments defer to tla-refinement / specification-master-agent.
---

# Mermate Tab 5 · TypeScript (ts)

Operates under `mermate` master invariants; Lamport standards via `specification-master-agent`. The TS runtime is a refinement of the TLA+ spec — conformance claims route through `tla-refinement` discipline, not vibes.

## Stage Identity (from `STAGE_REGISTRY.ts`, public/js/mermaid-gpt-app.js)
- Label: **TypeScript** · reveal: `STAGE 5 · TYPESCRIPT` · color `#34d399`
- Expected duration: ≈20–90s · enhance default: OFF · no upload (runtime is generated)
- **IPO contract**:
  - Input: verified TLA+ spec (mastered run)
  - Process: runtime generation → `tsc` compile → `tsx` test harness + Specula review against the TLA+ spec
  - Output: state-machine implementation, test harness, coverage reports

## Owning Code
- Backend: `server/routes/ts.js` —
  - `POST /api/render/ts` (generate, lines 103–421)
  - `GET /api/render/ts/source/:run_id` (read back without recompile, lines 70–101)
  - `GET /api/render/ts/status`
- Toolchain: `tsc` + `tsx`; Specula LLM reviews generated TS against the TLA+ spec
- Terminal artifacts + bundle: `GET /api/runs/:runId/bundle` (server/routes/bundle.js)
- Tests: `test/test-ts-compiler.js`
- Optional extensions: `/api/render/tsx` (React scaffold, server/routes/tsx.js), `/api/render/rust` (server/routes/rust.js)

## Stage Invariants
1. **Spec precedes code**: TS generation requires a SANY-verified TLA+ artifact from the same `run_id`; never generate TS from a diagram directly.
2. Terminal honesty: outcomes are `ts_complete`, `ts_partial` (compiles, tests incomplete), or `ts_failed` — reported verbatim to Opseeq and in `progressionUpdate` (unlocks all stages incl. `ts`).
3. The generated runtime implements the spec's state machine: same variables, same action boundaries. Divergence is a defect to report, not a feature.
4. `GET /api/render/ts/source/:run_id` must return persisted source — no hidden regeneration.

## Anti-Patterns (Reject)
- Editing generated TS to "fix" behavior that contradicts the TLA+ spec — fix the spec, re-verify, regenerate.
- Swallowing `tsc`/harness failures to present a green tab.
- Adding runtime features with no counterpart in the spec's actions.

## Verification
- `node --test test/test-ts-compiler.js`
- `node --test test/test-e2e-full-pipeline.js` — end-to-end idea→TS
- `curl -s http://localhost:3333/api/render/ts/status`
