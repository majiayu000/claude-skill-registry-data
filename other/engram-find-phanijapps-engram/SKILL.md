---
name: engram-find
description: Onboard a new developer to a codebase — map the architecture, identify key abstractions and critical paths. Uses the unified engram MCP. Trigger on "I'm new to this codebase", "how does this work", "explain the architecture", "where do I start".
---

# Engram: Find

Map the architecture and trace the code graph for a new developer. Uses the
**engram** MCP (which supersedes the old `codegraph` MCP).

## When to use

- "I'm new to this codebase"
- "How does this project work?"
- "Explain the architecture"
- "Where do I start reading code?"

## Prerequisites

Index first if needed: `scan_repo({ "path": "..." })`.

## Workflow

1. **Get the architecture map.** Call `architecture`.
   Returns: central symbols, bridges, communities, stats — one call.

2. **Deep-dive the top symbol.** Call `symbol_context` on the highest-ranked
   central symbol.
   Returns: callers, callees, community — the "understand this = understand the system" symbol.

3. **Assess critical paths.** For bridge symbols, call `change_impact`.
   Returns: blast radius + dependency paths.

4. **Get a context packet.** Call `get_context` for a fused overview.
   Returns: recall (docs + memories) + code neighborhood (+ `[Graph]` links).

## How to synthesize

Present a narrative onboarding guide with: module count, core abstractions
(central symbols), critical paths (bridges), and where to start reading
(the top symbol's context).

## Tools

| Tool | Purpose |
|---|---|
| `scan_repo` | Index the repo. |
| `architecture` | Central + bridges + communities + stats. |
| `symbol_context` | Deep-dive one symbol. |
| `change_impact` | Blast radius of a change. |
| `get_context` | Fused context packet. |
