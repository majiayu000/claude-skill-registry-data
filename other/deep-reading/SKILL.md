---
name: deep-reading
description: >-
  Reads an entire file and produces a structured content map showing sections,
  entities, claims, and gaps. Use when needing to understand a file before editing,
  checking conversion completeness, or when user says "what is in this file",
  "content map", "deep read", "read the whole thing", or "check completeness".
  Does NOT modify files — read-only analysis only.
model: sonnet
effort: medium
context: fork
---

# Deep Reading

Read a file completely and produce a structured content map.

## Process

1. Read the ENTIRE file (no cutoff)
2. Produce content map: sections, named entities, standalone content
3. Gap analysis: compare against repo for missing files/entries

## Output

```
## Content Map: [filename]
### Sections
1. [Heading] (lines X-Y) — [one-line summary]
### Named Entities
- Characters: [list]
- Locations: [list]
- Concepts: [list]
### Gaps
[Missing entries, truncated content, orphaned sections]
```

## Out of Scope

Does NOT modify files. Read-only analysis.
Does NOT audit for contradictions (use /auditing-physics).
