---
name: design-diagram-data-flow
description: Authors a house-style inline-SVG data-flow diagram for a Tutti design page. Use during the Domain movement (or whenever the argument is about what data moves where) to show entities, stores, and services with directional edges labelled by the data or event that moves between them. Produces a single self-contained inline SVG element in the Sotto vocabulary (svg-node, svg-zone, flowlbl), not Mermaid.
---

# Data-flow diagram

Draw the domain as stores and services with the data moving between them. Each edge is
labelled with the thing that travels it (a payload, an event, a record), not just an arrow.

## Vocabulary

Use the shared Sotto classes so the diagram matches the design page:

- Stores and services: `<rect class="svg-node" ...>` with a `<text class="nodetext">` name and an optional `<text class="nodesub">` type ("store", "service").
- Bounded contexts: group related nodes inside a `<rect class="svg-zone">` with an uppercase `<text class="zonelabel">`.
- Edges: a `<line>` or `<path>` in an accent stroke with an arrowhead, and a `<text class="flowlbl">` naming the data that moves ("audio frames", "change record").
- Accents carry meaning: amber `#ffb454` for the subject store, teal `#5fd3c4` for a safe or persisted path, muted `#97a0ab` for context and boundaries.

## How to lay it out

Place the source on the left, the sink on the right, and label every edge with the concrete
data it carries. Draw only the stores that carry the argument; a diagram of every table is a
schema dump, not a data-flow.

## Output

Emit a single `<svg viewBox="0 0 W H">...</svg>` and nothing else. It must be well-formed
(balanced or self-closing tags, quoted attributes, no XML comments). See example.svg in this
skill for a complete, valid reference.
