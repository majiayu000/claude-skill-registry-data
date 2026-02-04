---
name: openwebf-host-embedding-constraints
description: Fix Flutter layout/constraint issues when embedding WebF (scrollables, unbounded constraints, viewport sizing). Use when the user mentions ListView/ScrollView, “unbounded height”, infinite constraints, RenderBox errors, or embedding WebF in part of the screen.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, mcp__openwebf__docs_search, mcp__openwebf__docs_get_section, mcp__openwebf__docs_related
---

# OpenWebF Host: Embedding & Constraints

## Instructions

1. Ask for the widget tree snippet that embeds WebF and the exact Flutter error.
2. Identify whether WebF is inside a scrollable or an unconstrained parent.
3. Recommend the minimal constraint fix (bounded height/width), preferring full-screen embedding when possible.
4. Use MCP docs for official embedding guidance and common pitfalls.

More:
- [reference.md](reference.md)
- [doc-queries.md](doc-queries.md)
- [examples.md](examples.md)
