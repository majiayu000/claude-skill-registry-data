---
name: write-diagrams
description: "Use when a document produced in this collection (board, plan, report, analysis, durable doc) could carry a diagram, or when a design question would settle faster shown than said. Picks the diagram that answers the open question and holds the discipline that keeps a diagram readable. Not for decoration: no open question, no diagram."
---

# Write diagrams

**A diagram makes a boundary, an ordering, or a dependency visible early enough to argue about cheaply**, and stays as compressed context for the next reader.

## The catalog

**`diagrams.md` maps each open question to the diagram that answers it.** Read it before drawing. No open question, no diagram.

**Draw while a question is open, not only in the final document**: the container diagram with a `?` on the contested arrow, and ask "which of these two?".

## The discipline

- **One diagram per open question.** A diagram that restates a paragraph is deleted.
- **Every diagram carries a one-line caption right above the fence**: its catalog type and the question it answers, *"Dependency graph: what may import what after this change."*
- **Draw only what one sentence cannot say.**
- **Every arrow is labeled** with what flows and in which direction, **unless the shape carries it**: when every arrow means the same thing and no node has two outgoing arrows, the node names already say it. The moment a node branches, or two arrows mean different things, every arrow gets a label.
- **Real names of real things**: actual service, table and module names, never `Service A`.
- **A box whose responsibility you cannot state in a phrase is deleted.**
- **2–4 diagrams for a feature.** The full C4 set only for a genuinely new system.
- **When the design changes in review, update the diagram in the same edit.**
- **A missing diagram is a finding, not a pass**: when a downstream document depends on a boundary no diagram shows, draw it then.

## Mechanics

- **Mermaid in fenced ```mermaid blocks**, so it renders in aiview and on any git host.
- **C4-style diagrams as `flowchart` with C4 conventions** (`classDef` for person / system / external); Mermaid's native `C4Context` blocks render inconsistently.
- **Colours as eight-digit hex, never `rgba(...)`**; the commas inside `rgba()` split a `classDef` and the definition fails silently.
- **Translucent over opaque** (`#7f7f7f1a`); a translucent fill works in both themes, an opaque light fill burns a white slab into a dark page.
- **Meaning carried by styling is in the label too**, a glyph or a word, so it survives grayscale, dark mode and a colour-blind reader.
- **Run `aiview mermaid-check <file>` after every edit to a diagram.** It parses every block as the viewer will, names the line of each failure, and warns on a fence with no caption and on a branching node with an unlabeled arrow.

## Red flags

| Thought | Reality |
|---|---|
| "The prose already covers the boundary" | A boundary described in a bullet is a boundary nobody checked. "What may import what" is a dependency graph, not a sentence. |
| "I'll invent a hybrid diagram" | The catalog's forms exist because each answers one question. Pick one; two questions get two diagrams. |
