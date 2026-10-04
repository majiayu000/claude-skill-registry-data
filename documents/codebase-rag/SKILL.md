---
name: codebase-rag
description: Always-on semantic search over the current project. Use it before editing unfamiliar code, when looking for callers/callees, when checking how a similar feature is already implemented, or when you need to know what depends on a file before changing it.
---

# Codebase RAG

Semantic search over whatever project you're currently working in. The
server detects the project root, keeps an index in a per-machine cache,
and watches the filesystem so the index stays current as files change.

## When to use it

- Before editing unfamiliar code: search for related implementations.
- When looking for callers, callees, or similar patterns.
- When the user's instruction doesn't say which file to touch.
- Before modifying a file: check what depends on it.

## Tools

### `rag_search(query, num_results=5, source_type="all")`

Semantic search across constraints, patterns, and code. Returns ranked
results with file paths and relevance scores.

`source_type` is one of `"all"` (default), `"docs"` (constraints +
patterns), `"code"` (source only), or `"constraints"` (rules only).

### `rag_query_impact(file_path, num_similar=5)`

Show what depends on a file: its exports, the files that import it, and
semantically similar files that may need coordinated changes. Pass the
path relative to the project root, with forward slashes.

## Choosing `source_type`

The default `"all"` is correct most of the time. Narrow it when:

- `"constraints"` — checking what rules govern an area before designing
  a change. Returns only architecture / constraints / `CLAUDE.md`-style
  files.
- `"docs"` — understanding intent and patterns before reading code.
  Returns constraints plus `docs/patterns/` style documentation.
- `"code"` — finding existing implementations to copy or call. Filters
  out docs so examples aren't drowned out by prose.

A useful two-step for non-trivial changes: search `"docs"` first to
learn the rules, then `"code"` to find concrete implementations.

## Workflow

1. `rag_search("what you're about to do")` — read the top hits.
2. If you're going to modify a specific file, `rag_query_impact("path/to/file")`.
3. Make the change.

## How retrieval is weighted

The server gives higher retrieval weight to files it treats as
constraints or patterns, so they outrank random source matches:

- `ARCHITECTURE.yml` / `ARCHITECTURE.yaml` — 10×
- `CONSTRAINTS.md` — 10×
- `CLAUDE.md` — 10×
- Anything under `docs/patterns/` — 8×
- Everything else — 1×

If the project has rules or patterns worth surfacing first, putting them
in one of these files (or under `docs/patterns/`) is the simplest way to
make them appear at the top of search results. No config needed.

## Adding custom sources

To index ADRs, OpenAPI specs, style guides, RFCs, or any other docs the
project already maintains, edit `customSources` in the per-project
`config.json` (see "Where state lives" below):

```json
{
  "customSources": [
    { "pattern": "docs/adr/*.md",        "sourceType": "docs",        "weight": 9.0 },
    { "pattern": "openapi.yaml",         "sourceType": "constraints", "weight": 10.0 },
    { "pattern": "docs/guides/**/*.md",  "sourceType": "docs",        "weight": 8.0 }
  ]
}
```

- `pattern` — glob relative to the project root.
- `sourceType` — `"constraints"`, `"docs"`, or `"code"`. Determines
  which collection the files index into and which `source_type` filter
  surfaces them.
- `weight` — retrieval weight. Built-in constraints use 10.0, patterns
  use 8.0, code uses 1.0.

The next `rag_search` call rebuilds the index to pick up the change.

## Where state lives

The index and config live in a per-machine cache directory keyed by
project root, **not** inside the project tree:

- Windows: `%LOCALAPPDATA%\codebase-rag\<hash>\`
- macOS: `~/Library/Caches/codebase-rag/<hash>/`
- Linux: `$XDG_CACHE_HOME/codebase-rag/<hash>/` or `~/.cache/codebase-rag/<hash>/`

Inside that directory: `config.json` (project config + custom sources)
and `collections/` (ChromaDB on-disk store). Deleting the directory
forces a fresh index on next query.

## Status responses

Both tools return a `status` field. Handle the non-success cases:

- `"success"` — results are valid.
- `"indexing"` — first-run index is still building. Wait a few seconds
  and retry the same call. Result lists are empty until ready.
- `"no_project"` — no project root detected (no `.git`, `package.json`,
  `pyproject.toml`, `Cargo.toml`, or `go.mod` walking up from cwd).
  Tell the user; the server can't operate without a project root.
- `"index_failed"` — bootstrap failed. The `summary` field has the
  reason. Surface it; don't retry blindly.

## First call in a brand-new project

The very first query in a project that's never been indexed takes a few
seconds while the index builds (you'll see `status: "indexing"`). After
that, queries are sub-second and the index stays fresh on its own via
the filesystem watcher.
