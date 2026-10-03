---
name: mermate-tab-mermaid
description: Stage 3 tab (Mermaid) of the Mermate pipeline — Mermaid source compile/render to mastered PNG/SVG diagrams, depth scoring, and the run artifacts that TLA+ and TypeScript build from. Use when editing render pipeline, mermaid-cli integration, depth scoring, diagram output, or /api/render behavior.
---

# Mermate Tab 3 · Mermaid (mmd)

Operates under `mermate` master invariants; Lamport standards via `specification-master-agent`.

## Stage Identity (from `STAGE_REGISTRY.mmd`, public/js/mermaid-gpt-app.js)
- Label: **Mermaid** · reveal: `STAGE 3 · DIAGRAM` · color `#818cf8`
- Expected duration: ≈5–30s · enhance default: OFF · upload: `.mmd`
- **IPO contract**:
  - Input: markdown spec or raw .mmd source
  - Process: compile + repair + depth scoring
  - Output: mastered diagram (PNG/SVG) — **the run TLA+/TS build from**

## Owning Code
- Frontend: `public/js/mermaid-gpt-app.js` — `renderMermaid()` (line ~2287), depth badge, result display
- Backend: `server/routes/render.js` `POST /api/render` (lines 495–1047) — mermaid-cli (`@mermaid-js/mermaid-cli`), Python enhancer bridge (`MERMAID_ENHANCER_URL`, default localhost:8100), inference provider
- Depth scoring: `depth_score`/`depth_tier` (shallow|medium|deep), surfaced in response and reported to Opseeq
- Artifacts: `flows/` (rendered output), `archs/` (archived sources), `runs/` (lineage JSON with `run_id`)

## Stage Invariants
1. **The mastered run is the anchor**: `run_id` returned here is the input contract for `/api/render/tla` and `/api/render/ts`. Never regenerate a diagram implicitly in a later stage.
2. Success payload carries `paths`, `diagram_name`, `run_id`, `metrics`, and `progressionUpdate` unlocking `['idea','md','mmd','tsx','tla']` with `nextRecommended` set.
3. Compile failure emits `render_failed` stage event and a structured error — never a fabricated diagram.
4. Opseeq events `render_start`/`render_complete`/`render_failed` are fire-and-forget; render succeeds with Opseeq down.

## Anti-Patterns (Reject)
- Bypassing mermaid-cli with a hand-rolled renderer or "fixing" diagrams client-side.
- Losing `run_id` lineage (e.g. rendering without persisting to `runs/`).
- Duplicating depth-score semantics outside the single scoring path in the render route.

## Verification
- `node --test test/test-compiler.js`; render regression → `npm run test:regression`
- Live: render from each input_mode and confirm `flows/` + `runs/` artifacts and `progressionUpdate` payload
