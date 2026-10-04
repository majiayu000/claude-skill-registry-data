---
name: qmd
description: "Search the Canvas Notebook workspace with qmd. Use when the user asks to find files, search workspace content, or locate related notes/documents. Default to mode=search (BM25), use vsearch (vector) only as fallback, avoid query (hybrid) by default as it is expensive. Triggers: find files, search workspace, locate notes, Finde, suche, workspace search, content search, qmd."
compatibility: Requires Bun >= 1.0.0 and SQLite3
allowed-tools: Bash(qmd:*)
metadata:
  version: "1.0"
  author: canvas-studios
---

# Workspace Search (qmd)

Local workspace search for Canvas Notebook. Searches direct text files via `workspace-text` and derived document text such as DOCX extracts via `workspace-derived`.

## When to Use

Use this skill when the user requests:
- "Search my notes"
- "Find related documents"
- "Search my workspace"
- "Search for ... in my workspace"
- "Where is ..."
- "Finde ..."

## Default Behavior

- Use the PI tool contract: `qmd({ query, mode, limit, collection })`
- Prefer `mode=search` (BM25) - fast and safe as the default
- Use `mode=vsearch` only if keyword search fails and semantic similarity is needed
- Avoid `mode=query` unless it was explicitly enabled for this runtime or the user explicitly asks for the expensive path

## Parameters

- **query** (required): Search query
- **mode**: Search mode (search, vsearch, query). Default: search
- **collection**: Collection to search. Default: workspace-text + workspace-derived
- **limit**: Maximum number of results. Default: 10

## Search Modes

- `qmd search` (default): Fast keyword search (BM25)
- `qmd vsearch` (last resort): Semantic similarity (vector). Often slow due to local LLM before lookup.
- `qmd query` (mostly skip): Hybrid search + LLM reranking. Often slower than vsearch.

## Examples

Standard search:
`qmd({ query: "my search term", mode: "search" })`

Specific collection:
`qmd({ query: "search term", collection: "workspace-text" })`

More results:
`qmd({ query: "search term", limit: 10 })`

Semantic search (slower):
`qmd({ query: "conceptually similar content", mode: "vsearch" })`

## Requirements

- Bun >= 1.0.0 (automatically installed)
- SQLite3 (available in container)
