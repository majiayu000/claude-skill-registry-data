---
name: design-diagram-sequence
description: Authors a house-style inline-SVG sequence diagram for a Tutti design page. Use during the Decide movement (or any data-transport argument) to show actors or components as columns with vertical lifelines and the ordered messages that pass between them over time. Produces a single self-contained inline SVG element in the Sotto vocabulary (svg-node, flowlbl), not Mermaid.
---

# Sequence diagram

Draw the actors or components as columns across the top, drop a vertical lifeline from each,
and lay the messages between them top to bottom in the order they happen. Time runs downward.

## Vocabulary

Use the shared Sotto classes so the diagram matches the design page:

- Actor heads: `<rect class="svg-node" ...>` at the top of each column with a `<text class="nodetext">` name.
- Lifelines: a thin vertical `<line>` in the muted accent dropping from each actor head.
- Messages: a horizontal `<line>` in an accent with an arrowhead, ordered top to bottom, each carrying a `<text class="flowlbl">` naming the message ("dial", "hello", "stream reply").
- Accents carry meaning: amber `#ffb454` for the initiating actor, teal `#5fd3c4` for a confirmed or safe reply, coral `#ff8c6b` for a failure, muted `#97a0ab` for lifelines.

## How to lay it out

Space the columns evenly, keep each message on its own row about 34px apart, and read the
sequence top to bottom. Show the handful of messages that make the decision, not a full
protocol trace.

## Output

Emit a single `<svg viewBox="0 0 W H">...</svg>` and nothing else. It must be well-formed
(balanced or self-closing tags, quoted attributes, no XML comments). See example.svg in this
skill for a complete, valid reference.
