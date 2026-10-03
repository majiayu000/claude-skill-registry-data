---
name: mermate-tab-markdown
description: Stage 2 tab (Markdown Spec) of the Mermate pipeline — markdown architecture spec intake (paste/upload .md/.markdown/.txt), agent planning and spec refinement, and the Markdown → Mermaid unlock. Use when editing md-stage UI, upload handling, or spec refinement behavior.
---

# Mermate Tab 2 · Markdown Spec (md)

Operates under `mermate` master invariants; Lamport standards via `specification-master-agent`.

## Stage Identity (from `STAGE_REGISTRY.md`, public/js/mermaid-gpt-app.js)
- Label: **Markdown Spec** · reveal: `STAGE 2 · MARKDOWN` · color `#38bdf8`
- Expected duration: ≈10–60s · enhance default: ON · upload: `.md,.markdown,.txt`
- **IPO contract**:
  - Input: idea artifact or pasted/uploaded .md
  - Process: agent planning + spec refinement
  - Output: corrected architecture spec, Mermaid unlocked

## Owning Code
- Frontend: `public/js/mermaid-gpt-app.js` (md input config, upload wiring)
- Backend: `server/routes/render.js` `POST /api/render` with `input_mode: 'md'`; multipart via `multer`
- Agent refinement path: `server/routes/agent.js` (`POST /api/agent/run` planning phase)
- Classification: `server/services/input-router.js` → content_state `md` (or `hybrid` when Mermaid signals are present)

## Stage Invariants
1. A successful md render emits `progressionUpdate` unlocking at least `['idea','md','mmd']` — the Mermaid tab unlocks only from this server payload.
2. Uploaded file content is treated as untrusted text: validated, size-bounded, never executed.
3. Hybrid content (markdown + Mermaid-like signals) routes through the provider-backed pipeline when enhance is requested; it must not be misclassified as pure `mmd`.

## Anti-Patterns (Reject)
- Client-side "spec correction" duplicating the agent planning phase.
- Accepting file types beyond the registry's `accept` list without updating `STAGE_REGISTRY.md` first.
- Silently dropping uploaded content on enhance failure — fall back to raw spec, say so.

## Verification
- `npm run test:fast`; pipeline behavior → `node --test test/test-e2e-pipeline.js`
