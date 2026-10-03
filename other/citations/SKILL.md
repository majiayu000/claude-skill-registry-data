---
name: citations
description: Most-traversed articles around a topic — graph-walked citation count, surfaces canonical references.
allowed-tools:
  - "mcp__bigweld__find_citations"
  - "mcp__bigweld__get_node"
---

# /citations <topic>

Call `find_citations(topic)` with the user's topic argument. Present results as a numbered list with citation counts. Offer to drill into the top result via `get_node()` if Alex wants the full body.
