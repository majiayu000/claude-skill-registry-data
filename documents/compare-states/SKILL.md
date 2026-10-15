---
name: compare-states
argument-hint: "[the mechanism, and the states to compare]"
description: Build one self-contained HTML page that sets two or more states of the same mechanism side by side at full identifier-level detail.
---

Produce ONE self-contained HTML file (Mermaid via CDN) and deliver it rendered in the side panel
(`SendUserFile` with `display: render`; where that tool is absent, name the path). Put it beside the
session's other docs written for the user.

Three regions, left to right:

1. **Shared** — spans every row, split into two panels of its own. Left: the problem in three
   sentences, then a table of every object the diagrams name. Right: a glossary of every label,
   grouped tables · functions · columns · arguments, one plain sentence each.
2. **Diagrams** — one Mermaid diagram per state, stacked. The same boxes and the same layer count in
   every one, so they overlay.
3. **Reading** — one panel per diagram, in the same grid row so the tops align: the state's name, a
   numbered list that walks the arrows, and one coloured verdict box.

Rules:

- Read the code that produces each box before drawing it. A doc's description is not a source. Every
  line number comes from a file opened this session.
- Real identifiers inside a diagram — table, id argument, columns. Plain words live in the glossary
  and the reading. Never paraphrase inside a box.
- `useMaxWidth: false`, so every diagram renders at one scale. When one overflows, widen the page.
  Never drop a box to make it fit.
- A numbered arrow is one statement the code runs, in order. An unnumbered arrow is a pointer that
  exists once the statements have run. Colour only the row under discussion.
- The chat reply is a four-line reading order plus the next action. No ASCII diagram in chat, no
  `.md` fallback.
