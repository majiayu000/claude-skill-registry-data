---
name: ask
description: Route a codebase question to the right tool — structural graph, semantic search, or risk analysis. Use when you need to find or understand code without knowing exact file names.
---

# Ask Skill — Codebase Question Router

Answer a question about the codebase by routing to the most effective tool.

> Don't search files manually when a smarter tool exists.

## Routing Rules

### Architecture / flow / how does X work / trace a call
Use `mcp__codebase-memory__trace_path` or `mcp__codebase-memory__get_architecture`.
Zero file reads. 120× fewer tokens than manual exploration.

### Find / search / locate / what file / which function
Use `mcp__cocoindex-code__search` with a semantic query.
Finds code by **meaning**, not exact text — useful when you don't know the exact name.

### Safe to change / impact / blast radius / what breaks / risk score
Use `mcp__code-review-graph__detect_changes_tool` with `base_branch="main"`.
Reports: risk score 0–100, blast radius, breaking changes, dependent modules.

### General code question (narrow, specific file, no plugin fits)
Read the file directly. Grep for the symbol.

## Decision Logic

1. Contains architecture/flow/trace/how/explain → codebase-memory-mcp
2. Contains find/search/locate/where/what file → cocoindex-code
3. Contains safe/impact/blast/breaks/risk/change → code-review-graph
4. None of the above → read directly

## Answer Format

- Tool used and why
- Finding (file path + line if applicable)
- Surprising cross-module connections revealed by the graph (if any)

If no tool gives a clear answer, fall back to reading relevant files.
