---
name: index-management
description: |
  SQLite-backed index over all entity files in the project. The read-side foundation for every other MCP server. Use whenever an agent needs to look up entities by ID, kind, state, or text — instead of grepping the filesystem.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-index-management
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: processkit
    layer: 0
    provides:
      primitives: []
      mcp_tools: [reindex, query_entities, get_entity, search_entities,
            semantic_status, semantic_search_entities, hybrid_search_entities,
            query_events, list_errors, stats]
---

# Index Management

## Intro

`index-management` is the **read-side** foundation. It walks the project's
`context/` directory, parses every entity file, and writes a SQLite
database that other tools query. Its peer at Layer 0 is `id-management`
(the write side, which allocates new IDs). Both are foundational to
every entity-creating skill.

> **MCP server.** This skill ships a self-contained MCP server at
> `mcp/server.py` (PEP 723 script — requires `uv` and Python ≥ 3.10 on
> PATH). Agent harnesses may reach it directly from this skill's
> `mcp/mcp-config.json` or through the processkit gateway. Gateway
> deployments must surface only the processkit servers present in the
> installed/merged MCP configuration; this skill does not imply that
> unrelated processkit tools are available.

## Overview

### What it provides

- **`reindex()`** — rebuild the SQLite index from scratch
- **`query_entities(kind?, state?, limit?)`** — list entities matching filters
- **`get_entity(id)`** — fetch a single entity by ID
- **`search_entities(text, limit?)`** — FTS5 search across titles, bodies, specs
- **`semantic_status()`** — report semantic chunk/vector availability
- **`semantic_search_entities(text, limit?)`** — sqlite-vec semantic search when available
- **`hybrid_search_entities(text, limit?)`** — RRF over FTS5 + semantic results, with FTS-only fallback
- **`query_events(event_type?, subject?, actor?, limit?)`** — query the event log
- **`list_errors(limit?)`** — files that failed to parse during the last reindex
- **`stats()`** — counts of entities/events/errors in the index

List/search tools clamp caller-provided limits before querying the
database. Broad unfiltered event queries are capped more tightly than
filtered event queries, and long event summaries are returned as
previews. Fetch a specific entity by ID when full detail is needed.

### When to use

Agents call the MCP server whenever they need fast lookup. Other MCP
servers (`workitem-management`, `decision-record`, etc.) refresh the
index after writing a new entity to keep reads current. In gateway
deployments, the gateway only routes to index-management if this server
is present in the installed MCP configuration.

### Where the database lives

`<project-root>/context/.cache/processkit/index.sqlite`. Gitignored.
Rebuildable from source files at any time via `reindex()`.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Grepping the filesystem instead of calling `query_entities`.** The
  index is faster, context-cheaper, and reflects parsed semantics
  (state, kind, links) that grep can't see. Reach for `query_entities`
  first; fall back to grep only if the query you need isn't supported.
- **Trusting the index immediately after a hand-edit.** When you edit
  an entity file directly (bypassing the MCP write tools), the index
  is stale until the next `reindex()` call. Either go through the
  write tools, or call `reindex()` yourself before querying.
- **Forgetting to call `reindex` after writing a new entity.** Every
  entity-creating MCP server should call `index_management.reindex`
  (or the lighter `upsert_entity`) after a write. Not doing so means
  the next query won't see the just-created entity.
- **Treating index queries as transactional.** The index is eventually
  consistent. A query immediately after a write may or may not return
  the new row depending on whether reindex completed. If you need
  strict consistency, reindex explicitly first.
- **Trusting `list_errors()` as proof of correctness.** A clean errors
  table means parsing succeeded, not that the entities are
  semantically valid. Schema validation is a separate concern from
  parse success.
- **Using `search_entities` for exact-ID lookup.** `search_entities`
  is ranked FTS5 search over parsed content, with a fallback substring
  search for invalid FTS syntax. Use `get_entity(id)` for exact lookup.
- **Assuming semantic search is always active.** The semantic chunk table
  is always rebuilt, but vector KNN requires the optional `sqlite-vec`
  extension to load. Check `semantic_status()`; use
  `hybrid_search_entities()` when you want an FTS-backed fallback.
- **Re-indexing inside a hot loop.** A full reindex walks the whole
  `context/` tree and is expensive. Batch your writes and reindex
  once at the end, not after every entity.

## Full reference

### Database schema

Three tables — see `src/lib/processkit/index.py` for the DDL.

```sql
entities(id, kind, api_version, path, storage_location, created, updated, title, state, labels_json, spec_json, body)
entities_fts(id, kind, state, title, body, spec_json)
semantic_chunks(rowid, chunk_id, entity_id, kind, state, path, ordinal, text)
entity_vec(embedding)
events(id, timestamp, event_type, actor, subject, subject_kind, summary, details_json, correlation_id, path)
errors(path, message)
```

`spec_json` holds the full `spec` block as JSON for queries we did not
anticipate. `storage_location` is `NULL` for hot-tree files and points at cold
archive payloads for archived entities. `entities` and `events` overlap for
LogEntry rows: a LogEntry appears in both, with the `events` table
denormalizing the event-specific fields for fast filtering.

`entities_fts` is a rebuildable SQLite FTS5 virtual table. It mirrors
the searchable fields from `entities` and is cleared/rebuilt during
`reindex()`. If a stripped-down SQLite build lacks FTS5, the index still
opens and `search_entities` falls back to the previous `LIKE %text%`
behaviour.

`semantic_chunks` is a rebuildable chunk table. When the optional
`sqlite-vec` package can be imported and loaded, `entity_vec` is created
as a `vec0` virtual table containing deterministic local embeddings for
those chunks. The initial embedding strategy is provider-neutral
`local-hashed-bag-of-words`; it gives a stable offline baseline and a
storage contract for later provider/local embedding model upgrades.

### Reindex strategy

`reindex()` is **destructive and atomic** — it deletes all rows and
re-inserts. For typical projects this is fast (sub-second). For very
large projects, an incremental update mode lands later (Phase 4+).

### Errors table

Files that fail to parse get a row in the `errors` table instead of
crashing the reindex. `list_errors(limit?)` returns a bounded window so
the agent can fix them in batches. The errors table is cleared at the
start of each reindex.

### Tools that other servers call

`workitem-management`, `decision-record`, `binding-management`, and
`event-log` all call the shared index library after writing a new file.
This keeps the index in sync without a full reindex on every mutation.
From an MCP-protocol perspective each configured server has its own
process, or is reached through the gateway, and they communicate by
sharing the same SQLite database file.

### Configuration

The index database path is configurable via:

- `processkit.toml` `[index] path = "..."` (relative to project root)
- The `PROCESSKIT_INDEX_DB` environment variable
- Default: `context/.cache/processkit/index.sqlite` (gitignored cache)

### Limitations at v0.3.0

- **WAL mode enabled (v0.4.0+).** Multiple readers and a single writer
  are safe; concurrent writes still serialize via WAL. Typical
  AI-assisted sessions are single-writer anyway.
- **FTS5 search.** Search uses SQLite FTS5 ranking when available and
  falls back to `LIKE %text%` for invalid FTS syntax or unsupported
  SQLite builds.
- **Optional sqlite-vec.** Semantic search uses sqlite-vec only when the
  extension is installed and loadable; otherwise semantic search returns
  no vector results and hybrid search falls back to FTS5.
- **No incremental indexing.** Every reindex is a full sweep.
