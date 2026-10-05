---
name: engram-index
description: Understand a codebase quickly — index it, then get the structural overview (central symbols, communities, bridges, stats). Uses the unified engram MCP. Trigger on "understand this codebase", "what does this repo do", "give me an overview", or first encounter with a new repository.
---

# Engram: Index

Get a structural overview of a codebase — no file reading needed. Uses the
**engram** MCP (which supersedes the old `codegraph` MCP).

## When to use

- "Understand this codebase"
- "What does this repo do?"
- "Give me an overview of this project"
- First encounter with a new repository

## Workflow

1. **Index the repo.** Call `scan_repo` with the absolute path.
   ```
   scan_repo({ "path": "/absolute/path/to/repo" })
   ```

2. **Get the architecture map.** Call `architecture` — one call replaces the old
   `repository_stats` + `central_symbols` + `bridge_symbols` + `call_communities`.
   ```
   architecture({ "limit": 20 })
   ```

3. **Get a context packet (optional).** For a high-level narrative:
   ```
   get_context({ "focus": "main" })
   ```

## How to synthesize

Present a concise narrative:

> This codebase has **N symbols** across **M modules**. The core abstractions are
> **X, Y, Z** (top PageRank). Be careful with **B** — it's a bridge symbol.

Do NOT read individual files unless asked. The graph tells you the structure.

## Tools

| Tool | Purpose |
|---|---|
| `scan_repo` | Index the repo. |
| `architecture` | Central + bridges + communities + stats. |
| `get_context` | Fused context packet. |
| `symbol_context` | Deep-dive a symbol (follow-up). |
