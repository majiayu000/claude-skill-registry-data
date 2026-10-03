---
name: atrisk
description: Functionalities at risk if a Capability is deprecated or gapped — impact analysis for migration retirement decisions.
allowed-tools:
  - "mcp__bigweld__find_functionalities_at_risk"
  - "mcp__bigweld__walk_dependency_chain"
  - "mcp__bigweld__get_node"
---

# /atrisk <capability_slug>

Ask Alex which Capability slug he's considering retiring or moving to `migration_state='deprecated'`/`'gap'`. Then:

1. Call `find_functionalities_at_risk(capability_slug)` — Functionalities with inbound ENABLES from this Capability (i.e., user-facing workflows that break if this Capability goes away).
2. Call `walk_dependency_chain(capability_slug, depth=3)` — Capabilities downstream that DEPENDS_ON this one transitively (the broader blast radius).

Present both results: "deprecating X breaks N user-facing workflows + M downstream capabilities." Offer to drill into any specific node via `get_node()` for context.
