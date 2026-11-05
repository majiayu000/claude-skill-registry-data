---
name: image-scoring-mcp
description: Driftara Gallery MCP — one driftara server (search → resolve → execute over local, ipc, cdp, api and system actions); backend work goes to the sibling vexlum (is-be-mcp).
---

# Gallery MCP (driftara)

Catalog: [`mcp-server/driftara/catalog.json`](../../../mcp-server/driftara/catalog.json). Contract: [DRIFTARA_MCP.md](../../../docs/technical/DRIFTARA_MCP.md). Quick reference: [mcp_tools_reference.md](../../mcp_tools_reference.md).

## Server keys

| Key | Tools |
|-----|-------|
| **`driftara`** | **`search`**, **`resolve`**, **`execute`**; `dispatch` and `sse_status` are deprecated aliases |
| **`is-be-mcp`** (sibling backend, vexlum) | Same three tools for backend REST, SQL, jobs and diagnostics |

The old gallery keys (`is-ui-mcp`, `is-ui-router`, `is-ui-local`, `is-ui-api`) still start but warn and serve driftara. Do not use `imgscore-el-*`, `image-scoring-gallery-*`, `image-scoring-pipeline-*`.

## Workflows

### Gallery startup / backend connection

1. `execute("system.status")`: catalog, live server, CDP and backend reachability.
2. `execute("local.gallery_status")`, then `execute("api.api_health")`.
3. Backend deep dive → vexlum: `search("scoring errors")` → `execute("diagnostics.get_error_summary", {})`.

### Anything in the running app (IPC, renderer)

1. Start the app with `npm run dev` (or `ENABLE_GALLERY_MCP_SSE=1`); `ipc.*` and `live.*` otherwise return `live_unavailable`.
2. `search("image count")` → `resolve("ipc.db.get-image-count")` → `execute(...)`.
3. Renderer: `live.cdp_screenshot`, `live.cdp_console_logs`, `live.cdp_click`.

### Unknown action

`search(query)` ranks ids, aliases and intent examples. A miss returns suggestions, and a vexlum hint when the intent is backend work.

## Writes and destructive actions

- `write` needs `confirmed=true`.
- `destructive` needs three things:
  - `DRIFTARA_ALLOW_ELEVATED=1` in the **gallery app's** environment;
  - a `dry_run=true` call that returns `confirm_token`;
  - `confirmed=true` plus that token, with the same arguments.

  Destructive actions are deletes, import, sync, backup, config save and `live.cdp_evaluate`.

Dry-run first. Keep elevation off in automated profiles.
