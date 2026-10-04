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

## Workflow

1. `rag_search("what you're about to do")` — read the top hits.
2. If you're going to modify a specific file, `rag_query_impact("path/to/file")`.
3. Make the change.

## First call in a brand-new project

The very first query in a project that's never been indexed takes a few
seconds while the index builds. After that, queries are sub-second and
the index stays fresh on its own.
