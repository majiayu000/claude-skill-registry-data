---
name: orphans
description: Surface articles, capabilities, and functionalities with no inbound graph references — extraction quality + content health checks.
allowed-tools:
  - "mcp__bigweld__find_orphans"
  - "mcp__bigweld__delete_node"
---

# /orphans

Call `find_orphans()` with no label arg (returns all three types: Article without DOCUMENTS/MENTIONS/CITED_BY; Capability without CITED_BY or outbound ENABLES; Functionality without inbound ENABLES). Present a consolidated table grouped by label.

For each orphan Alex wants to integrate, propose `link()` (Tier 0) with the appropriate edge type. For genuine outliers Alex wants gone, propose `delete_node(confirmed=False)` first to show the diff, then `confirmed=True` after his nod.
