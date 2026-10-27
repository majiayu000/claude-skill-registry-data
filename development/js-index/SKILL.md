---
name: js-index
description: Build the interprocedural callgraph + framework detection + tag table for an exploded source tree by calling the tlx MCP js_index_target tool. Run after rag-ingest when status.json.phases.index is missing or stale (sources mtime > index mtime). Writes index/{nodes,edges}.jsonl and frameworks.json into the target dir.
---

# js-index

## Purpose
Run TLX's `js_index_target` against `targets/<name>/sources/` and
persist the resulting graph artifacts inside the target dir so they're
versioned alongside the target's other state.

## Inputs
- `targets/<name>/sources/**` (output of `sourcemap-explode`).

## Steps
1. Call the MCP tool:
   ```
   js_index_target(target_folder="targets/<name>/sources/")
   ```
2. The tool persists the callgraph in TLX's own SQLite/Chroma at
   `~/.tlx/`. We additionally export a copy into the target dir so
   each engagement is self-contained.
3. After success, mirror the artifacts into `targets/<name>/index/`:
   - `index/nodes.jsonl` — `{qname, file, line, kind, framework_tag}`
   - `index/edges.jsonl` — `{caller_qname, callee_qname, edge_kind}`
   - `index/frameworks.json` — detected frameworks + versions
   - `index/tags.jsonl` — source/sink/sanitizer tags
   Use `bin/export_index.py` with a `--db <per-target.db>` flag pointing
   at the snapshot produced by `bin/db-isolate.py snapshot ...` (per
   `CLAUDE.md`). Never let it default to the global `~/.tlx/js_analyzer.db`.
4. **jsluice tag layer (T1.4).** Run:
   ```
   python3 bin/run_jsluice.py targets/<name>
   ```
   Wraps the BishopFox `jsluice` binary (install:
   `go install github.com/BishopFox/jsluice/cmd/jsluice@latest`).
   Extracts URL skeletons (with `EXPR` placeholders flagged
   `severity=medium`, kind `url_skeleton`) and secrets (severity per
   secret kind), maps each finding to the innermost containing node,
   inserts rows into `node_tags` with `source='jsluice'`, writes a raw
   audit trail to `index/jsluice.jsonl`, and drafts a per-secret
   finding stub under `findings/jsluice_secret_<id>/draft.json`
   (`auto_submit: false`, `requires_user_review: true`). If `jsluice`
   is missing, the script writes `status: skipped` and exits 0 — does
   not fail the pipeline.
5. **Build-manifest extractor (T2.3).** Run:
   ```
   python3 bin/build_manifest_extract.py targets/<name>
   ```
   Parses Next.js (`_buildManifest.js`, `routes-manifest.json`), Vite
   (`manifest.json`), Rspack (`rspack.client.json`), and CRA
   (`asset-manifest.json`) build manifests under `raw/` to enumerate
   SPA routes — including hidden admin paths the live crawl missed.
   Writes `index/routes.jsonl` (one route per line). Hand the new
   routes back to `js-harvest` (loop step 1 over each route as a
   navigation seed) to widen the JS asset surface.
6. Stamp `status.json.phases.index` with counts.

## Outputs
- `targets/<name>/index/{nodes,edges,tags}.jsonl`
- `targets/<name>/index/frameworks.json`
- `targets/<name>/index/jsluice.jsonl` (Step 4)
- `targets/<name>/findings/jsluice_secret_<id>/draft.json` (Step 4)
- `targets/<name>/index/routes.jsonl` (Step 5, when implemented)

## Failure modes
- `js_index_target` returns zero nodes → almost always framework
  misdetection. Set
  `session_kv_set("target_<name>:framework_override", "<react|vue|...>")`
  via the TLX UI or a one-off Python call (MCP exposes only
  `session_kv_get` on purpose); re-index.
- AST parser chokes on a file → it's logged inside TLX; we surface
  `index/_skipped.json` so the user knows the coverage gap.
- `run_jsluice.py` reports many `tags_orphan` findings → file paths
  emitted by jsluice don't match `nodes.file` conventions. Inspect
  `result.orphan_files_sample` to see what jsluice produced; usually
  fixed by re-running after `sourcemap-explode` populates `sources/`.
- `run_jsluice.py` exits 3 (per-target DB missing) → run
  `bin/db-isolate.py snapshot targets/<name> <host>/` first.

## Result block
```json
"phases": {
  "index":   { "status": "done", "ts": "<iso>",
    "nodes": N, "edges": E, "tags": T, "frameworks": [...] },
  "jsluice": { "status": "done|skipped", "ts": "<iso>",
    "files_scanned": N, "urls_found": N, "url_skeletons": N,
    "secrets_found": N, "tags_inserted": N, "tags_duplicate": N,
    "tags_orphan": N, "secret_drafts_written": N,
    "audit_file": "index/jsluice.jsonl" }
}
```
