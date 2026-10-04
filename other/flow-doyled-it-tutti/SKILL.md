---
name: design-diagram-flow
description: Authors a house-style inline-SVG flow diagram for a Tutti design page. Use during the Impact movement (or any movement whose artifact is clearer as a sequence of steps or states) to show a left-to-right or top-down flow with labelled edges. Produces a single self-contained inline SVG element in the Sotto vocabulary (svg-node, nodetext, flowlbl), not Mermaid.
---

# Flow diagram

Draw a flow: a small number of steps or states connected by labelled, directional edges.
Left-to-right for a pipeline, top-down for a decision or state flow.

## Vocabulary

Use the shared Sotto classes so the diagram matches the design page:

- Nodes: `<rect class="svg-node" x=".." y=".." width=".." height=".." rx="10" fill="<accent .10 rgba>" stroke="<accent hex>" stroke-width="1.4"/>` with a centered `<text class="nodetext" text-anchor="middle" fill="<accent text>">Title</text>` and an optional `<text class="nodesub" ...>subtitle</text>`.
- Edges: a `<line>` or `<path>` in an accent stroke with an arrowhead, and an optional `<text class="flowlbl">` label near its midpoint.
- Accents carry meaning: amber `#ffb454` for the primary path, teal `#5fd3c4` for a safe or confirmed branch, coral `#ff8c6b` for an error or abort branch, muted `#97a0ab` for context.

## How to lay it out

Give each node room (about 150x54), space them roughly 90px apart on the flow axis, and label
every edge with the action or condition. Keep it to the few steps that carry the argument;
a flow with fifteen boxes is a failure of framing, not a thorough diagram.

## Output

Emit a single `<svg viewBox="0 0 W H">...</svg>` and nothing else. It must be well-formed
(balanced or self-closing tags, quoted attributes, no XML comments). See example.svg in this
skill for a complete, valid reference.
