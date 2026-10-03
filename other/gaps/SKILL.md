---
name: gaps
description: Migration gap surface — Capabilities with migration_state='gap' (no SNOW equivalent yet) plus Capabilities still unmapped to SNOW.
allowed-tools:
  - "mcp__bigweld__find_capabilities_by_state"
---

# /gaps

Call `find_capabilities_by_state(state="gap")` to surface explicit migration gaps — Capabilities flagged as having no SNOW equivalent yet. Present results with name + system + description.

Note: the broader "what's not yet paired to SNOW" view is the Tier 0 `find_unmapped_capabilities()` tool, which is always available without invoking this skill. Use this skill when Alex specifically wants the gap-flagged subset; use the Tier 0 tool when he wants the full unmapped sweep.
