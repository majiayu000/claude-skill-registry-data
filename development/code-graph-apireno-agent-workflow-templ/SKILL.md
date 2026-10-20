---
name: code-graph
description: Cross-repo symbol / dependency query over the project's code-graph engine (ADR-001 NAVIGATION) — navigate object↔object across repos by symbol, not grep, and supply the import edges the RACI-validator + derived-UML consume. INTERFACE skill — it requires the project's code-graph engine to be registered as an MCP server and to expose the fleet-wide cross-repo query contract; until then, it reports the engine is not yet wired.
allowed-tools: Bash(*) Read
argument-hint: <symbol-or-query> [--repo <name>]
---

# Code-graph query: $ARGUMENTS

The NAVIGATION-layer interface of ADR-001. The engine is project-owned and pluggable; this skill is the engine-agnostic query surface. The template names no engine: a project says which MCP server is its code-graph engine in `.claude/code-graph-server` (one line: the server's name in `.mcp.json`), or with `CODE_GRAPH_SERVER`.

**Plug in your engine here.** **codegram** (code graph + doc RAG, exposed as an MCP server) is the reference implementation; it is not open source yet. Until it is, plug in your own RAG / code-graph implementation here — anything that meets the contract below works (Sourcegraph, a language-server index, your own retrieval service). With codegram the file holds `codegram` and its tools are `mcp__codegram__*`.

## Probe the engine

```!
set -uo pipefail
echo "ADR-001 NAVIGATION contract the engine must satisfy (fleet-wide):"
echo "  1. symbol lookup (definition + every cross-repo consumer)"
echo "  2. import/dependency edges, INCLUDING cross-repo (feeds the RACI-validator)"
echo "  3. always-current via async/non-blocking, incremental re-index"
echo ""
R="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SRV="${CODE_GRAPH_SERVER:-}"
[ -z "$SRV" ] && [ -f "$R/.claude/code-graph-server" ] && SRV="$(tr -d '[:space:]' < "$R/.claude/code-graph-server")"
WIRED=0
if [ -z "$SRV" ]; then
  echo "engine: none declared (no .claude/code-graph-server, no CODE_GRAPH_SERVER)."
  echo "  -> a project names its code-graph MCP server there; until then use /lane-check (pattern-based)."
elif grep -q "\"$SRV\"" "$R/.mcp.json" 2>/dev/null; then
  echo "engine: '$SRV' is registered as an MCP server in this repo's .mcp.json."
  echo "  -> query it via its MCP tools (mcp__${SRV}__*). Confirm it indexes more than one repo before"
  echo "     relying on cross-repo answers."
  WIRED=1
else
  echo "engine: '$SRV' is declared but NOT registered in $R/.mcp.json — register it, or fix the name."
fi
echo "WIRED=$WIRED"
```

## Your task

- **If the engine is wired:** use its MCP tools to answer the query — locate the symbol's definition and every cross-repo consumer; surface import edges. Present object↔object across repos (the thing grep misses).
- **If not wired:** report that cleanly — cross-repo navigation, derived UML and RACI validation depend on the project's code-graph engine exposing the ADR-001 contract. Until then, enforcement still works via `/lane-check`; navigation falls back to manual.

Sign `— CTO`.
