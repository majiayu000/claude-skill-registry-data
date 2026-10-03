---
name: unmapped
description: SFDC capabilities still needing SNOW pairing — the daily migration query.
allowed-tools:
  - "mcp__bigweld__find_unmapped_capabilities"
  - "mcp__bigweld__pair"
  - "mcp__bigweld__get_node"
---

# /unmapped

Call `find_unmapped_capabilities(system="sfdc")` to get the current list of SFDC capabilities with no outbound `MAPS_TO` edge. Present results numbered, sorted by name.

For any capability Alex wants to pair, ask for the SNOW target slug (or use `find_nodes(label="Capability", filters={"system": "snow"})` to surface candidates). Then call `pair(sfdc_slug, snow_slug, confirmed=False)` first to show the dry-run diff (creates MAPS_TO + bumps both Capabilities to `confidence='verified'` + sets `verified_at`). After Alex's explicit nod, call `pair(..., confirmed=True)`.

If Alex wants the full body of a candidate before pairing, use `get_node(slug, label="Capability")`.
