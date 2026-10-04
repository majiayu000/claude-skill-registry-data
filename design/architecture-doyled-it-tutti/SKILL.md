---
name: design-diagram-architecture
description: Authors a house-style inline-SVG architecture diagram for a Tutti design page. Use during the Structure movement to show the system's shape as nested C4-ish zones (a context holding containers, a container holding components) with the pieces inside. Produces a single self-contained inline SVG element in the Sotto vocabulary (svg-zone, svg-node, zonelabel), not Mermaid.
---

# Architecture diagram

Draw the system's structure as nested boundaries: an outer context zone that holds one or two
container nodes, each a real deployable piece. This is the C4-ish view, boxes inside boxes.

## Vocabulary

Use the shared Sotto classes so the diagram matches the design page:

- Boundaries: `<rect class="svg-zone">` with an uppercase `<text class="zonelabel">` (a system context, a container). Nest a smaller zone inside a larger one for a container-holds-components view.
- Containers and components: `<rect class="svg-node" ...>` with a `<text class="nodetext">` name and an optional `<text class="nodesub">` role ("FastAPI", "Rust").
- Relations: a `<line>` or `<path>` in an accent stroke with an arrowhead when one piece calls another, with an optional `<text class="flowlbl">`.
- Accents carry meaning: amber `#ffb454` for the subject system, teal `#5fd3c4` for a trusted or safe container, muted `#97a0ab` for boundaries and context.

## How to lay it out

Draw the outer zone first, then place the containers inside with room around them. Nest at
most two levels; a diagram that shows every class is a call graph, not an architecture. Label
each zone in uppercase.

## Output

Emit a single `<svg viewBox="0 0 W H">...</svg>` and nothing else. It must be well-formed
(balanced or self-closing tags, quoted attributes, no XML comments). See example.svg in this
skill for a complete, valid reference.
