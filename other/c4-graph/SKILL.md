---
name: c4-graph
description: "Use when drawing or converting a software architecture diagram following the C4 model — system context, container, or landscape — as a draw.io file rendered in VS Code or draw.io and embedded as .drawio.svg in GitLab, GitHub, or a README, from a text description, a DOT digraph, or a draw.io file or model. Also use when the user mentions C4, draw.io C4 shapes, line jumps, crossing arrows, diagram unreadable on dark theme, or asks to convert a .drawio file or a draw.io SVG export."
---
# C4 graph

## When to use
- User asks for an architecture diagram, a C4 diagram, or a system landscape
- User wants a diagram that opens in VS Code or draw.io and renders as SVG in GitLab, GitHub, or a README
- User provides a DOT digraph, a draw.io file, or a pasted draw.io model to convert
- Arrows cross heavily, or a diagram is unreadable on a dark theme

## Overview

Produce C4 diagrams as `.drawio` files built from the draw.io C4 palette: person, system, container, boundary, and relationship shapes with line jumps where arrows cross. Claude writes the model; the human opens it in VS Code (draw.io extension) or draw.io, runs the Vertical Flow layout, and exports `<name>.drawio.svg` — one file that re-opens in draw.io and renders in GitLab, GitHub, and VS Code.

Reference: [drawio-rules.md](drawio-rules.md). Read it before the first line of diagram code.
Reference: [inputs.md](inputs.md). Read it when converting from a source, validating output, or handing over.

## Rules

1. Read [drawio-rules.md](drawio-rules.md) first; copy its styles, object attributes, and labels verbatim.
2. Never lay out: give vertices distinct, non-overlapping positions and let the human run Arrange > Layout > Vertical Flow in the editor.
3. Respect C4 levels — one level per diagram, 15 elements at most. Level 1 (System Context): persons and systems only, containers collapsed into their owning system. Level 2 (Container): one diagram per in-focus system — its containers plus direct neighbours. Over 15 elements or mixed levels: split per the Levels section of [drawio-rules.md](drawio-rules.md), one file per level, context first.
4. Draw one-way relationships with verb descriptions ("Notifies", "Reads"); two-way traffic is two relationships.
5. In convert mode, extract per [inputs.md](inputs.md); the output edge set must equal the source's. Report dangling edges, never drop them silently.
6. Validate the model before handing over ([inputs.md](inputs.md): parse, edge ids, edge multiset), then give the open-and-export steps and ask for a preview check. Claude never renders.
7. Keep sequence flows out of the C4 diagram — a separate mermaid `sequenceDiagram` block in the markdown.

## Boundaries

This skill never emits mermaid C4 or flowcharts, never renders, and never hand-draws SVG: the `.drawio.svg` comes from the human's export. Commits and MR text belong to [`git-conventions`](../git-conventions/SKILL.md); multi-session planning to [`plan`](../plan/SKILL.md).
