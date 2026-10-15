---
name: full-picture
argument-hint: "[the system, issue, or decision to map]"
description: Map a system, an issue, or a decision as one rendered page — the parts, how they connect, what exists over time, and what a change touches. Use on "I don't have the full picture", "show me a visual", "what does each of these do", "map this out".
---

Produce ONE self-contained HTML file (Mermaid via CDN) and deliver it rendered in the side panel
(`SendUserFile` with `display: render`; where that tool is absent, name the path). Put it beside the
session's other docs written for the user.

Sections, in this order:

1. **The parts** — one table: part · what it is · where it comes from · who uses it · does the user
   see it.
2. **How they connect** — a Mermaid diagram per state. When a change is on the table (§4 exists),
   ALWAYS draw two under this heading — **before** first, then **after** — with the same node names
   in both so the eye can diff them; otherwise one. One note under them naming the surprising edge.
3. **Over time** — a grid: rows = moments, columns = the parts; cells colored real / thin / empty.
   The first row-group is always "today". Add one row-group per option when options exist.
4. **What changes** — only when a change is on the table: surface → change, then "not touched".
5. **Sources** — the `file:line` list. The only place a citation appears; the body carries none.

Rules:

- Read the code that produces each part before drawing it. A doc's description is not a source.
- Plain words in the body; repo names only where the user already uses them.
- The chat reply is a four-line reading order plus the next action. No ASCII diagram in chat, no
  `.md` fallback.
