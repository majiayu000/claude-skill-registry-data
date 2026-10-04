---
name: codegram
description: Cross-repo symbol / dependency query over the project's code-graph engine (ADR-001 NAVIGATION) — navigate object↔object across repos by symbol, not grep, and supply the import edges the RACI-validator + derived-UML consume. INTERFACE skill — it requires the project's code-graph engine (e.g. codegram) to be running and exposing the fleet-wide cross-repo query contract; until that Phase-2 retrieval extension lands, it reports the engine is not yet wired.
allowed-tools: Bash(*) Read
argument-hint: <symbol-or-query> [--repo <name>]
---

# Codegram query: $ARGUMENTS

The NAVIGATION-layer interface of ADR-001. The engine is project-owned + pluggable; this skill is the engine-agnostic query surface.

## Probe the engine

```!
set -uo pipefail
echo "ADR-001 NAVIGATION contract the engine must satisfy (fleet-wide):"
echo "  1. symbol lookup (definition + every cross-repo consumer)"
echo "  2. import/dependency edges, INCLUDING cross-repo (feeds the RACI-validator)"
echo "  3. always-current via async/non-blocking, incremental re-index"
echo ""
# Is a code-graph engine reachable? (codegram is one impl — MCP server.)
WIRED=0
if grep -q '"codegram"' "$(git rev-parse --show-toplevel 2>/dev/null || pwd)/.mcp.json" 2>/dev/null; then
  echo "engine: codegram is registered as an MCP server in this repo's .mcp.json."
  echo "  -> query it via its MCP tools (mcp__codegram__*). NOTE: fleet-wide CROSS-REPO query is the"
  echo "     Phase-2 retrieval extension (per-repo today) — confirm it indexes >1 repo before relying on cross-repo answers."
  WIRED=1
else
  echo "engine: NO code-graph engine wired (no codegram in .mcp.json)."
  echo "  -> this is the project-side Phase-2 work: a minimal fleet-wide + cross-repo retrieval extension"
  echo "     satisfying the contract above. Until then, fall back to /lane-check (pattern-based) for enforcement."
fi
echo "WIRED=$WIRED"
```

## Your task

- **If the engine is wired:** use its MCP tools to answer the query — locate the symbol's definition and every cross-repo consumer; surface import edges. Present object↔object across repos (the thing grep misses).
- **If not wired:** report that cleanly — the cross-repo navigation + derived-UML + RACI-validation depend on the project's code-graph engine exposing the ADR-001 contract (the project's code-graph engine retrieval extension). Until then, enforcement still works via `/lane-check`; navigation falls back to manual.

Sign `— CTO`.
