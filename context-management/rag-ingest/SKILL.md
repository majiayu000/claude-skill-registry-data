---
name: rag-ingest
description: Embed every file under targets/<name>/sources/ into a ChromaDB collection named target_<name> via the TLX rag module (Google text-embedding-004). Run after sourcemap-explode when status.json.rag.collection is missing. Enables docs_query(collection="target_<name>", query=...) for retrieval during static + dynamic analysis.
---

# rag-ingest

## Purpose
Build a per-target retrieval index over the exploded source tree so
Claude (and Opus during audit) can fetch only the relevant code chunks
instead of stuffing the entire app into context.

## Inputs
- `targets/<name>/sources/**`
- env: `GOOGLE_API_KEY` for the embedder.

## Steps
1. Verify env. If missing, halt with `memory.md > Failure-mode reminders`
   pointer to fix.
2. Resolve TLX rag module entry point. Since this folder vendors TLX
   in `./tlx/`, invoke via the `tlx` MCP. The MCP exposes `docs_query`
   but not `docs_ingest` directly — we ingest by calling the underlying
   module function through a tiny helper at
   `bin/rag_ingest.py target_<name> targets/<name>/sources/`.
3. The helper does:
   - `from kernel import Kernel`
   - `await kernel.boot(surface="mcp")` then resolve the rag module's
     `ingest()` function via `kernel.services.get("rag")` (falls back
     to legacy service names `docs` / `docs_module`).
   - Walk `sources/`, batch-embed files (chunk size ~1000 tokens with
     ~100-token overlap), persist to `~/.tlx/chroma/target_<name>`.
4. Write count + model to `status.json.rag`.

## Outputs
- `~/.tlx/chroma/target_<name>` collection.
- updated `status.json.phases.rag`.

## Failure modes
- `PERMISSION_DENIED` on embedder → bad `GOOGLE_API_KEY` or missing
  Generative Language API enablement on the GCP project.
- Disk full at `~/.tlx/chroma/` → free space; rerun (idempotent).
- File too large to embed → split into smaller chunks; if individual
  chunk exceeds embedder token limit, log skip.

## Result block
```json
"phases": { "rag": { "status": "done", "ts": "<iso>",
  "collection": "target_<name>", "chunks": N, "model": "text-embedding-004" } }
```
