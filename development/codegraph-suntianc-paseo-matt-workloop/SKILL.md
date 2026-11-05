---
name: codegraph
description: Pre-indexed code knowledge graph for codebase exploration, symbol navigation, call chains, and change-impact analysis. Use when exploring an unfamiliar repo, tracing callers/callees, or assessing blast radius before a change — replaces grep+Read loops with one query.
---

# CodeGraph

SQLite knowledge graph of a codebase's symbols, edges, and files (30+ languages), served over MCP. One `codegraph_explore` call returns the verbatim, line-numbered source of the relevant symbols plus the call paths between them and a blast-radius summary.

## Setup (per project)

```bash
codegraph init     # builds .codegraph/ index in cwd (needed before MCP tools work there)
codegraph status   # index health; pending-sync files are listed
```

Auto-sync keeps the index fresh: the OS-native file watcher + 2s debounce, per-file staleness banners, and catch-up reconciliation on MCP reconnect. Manual `codegraph sync` is only needed with `CODEGRAPH_NO_DAEMON=1` or CI pre-flight.

## MCP tools

| Intent | Tool |
|---|---|
| Almost any question — architecture, flow, bug, investigation | `codegraph_explore` ⭐ (primary; usually the only call needed) |
| Locate symbol by name | `codegraph_search` |
| Call chain | `codegraph_callers` / `codegraph_callees` |
| Change impact | `codegraph_impact` |
| Single symbol full source / overload disambiguation | `codegraph_node` |
| File structure | `codegraph_files` |
| Index health | `codegraph_status` |

## Principles

- `codegraph_explore` first — it groups source by file with line numbers and links the call paths.
- Answer directly from the graph; do NOT delegate exploration to file-reading subagents — that defeats the index.
- One `explore` beats `search` + `node` chained calls.
- Never use grep to verify codegraph results — AST edges are stronger evidence than text matches.
- Graph edges are proven, not complete: a missing edge does not prove a reference is absent.
- After edits, watch the staleness banner (⚠️ names a pending file) — Read that file directly for live content.
