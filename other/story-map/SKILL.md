---
name: design-diagram-story-map
description: Authors a house-style inline-SVG user-story map for a Tutti design page. Use during the Slice movement to show activities across the top and the tasks or stories in columns beneath each, with an optional line marking the walking-skeleton slice. Produces a single self-contained inline SVG element in the Sotto vocabulary (svg-node, flowlbl), not Mermaid.
---

# Story-map diagram

Draw a user-story map: a row of activities across the top (the backbone of what the user
does), and beneath each activity a column of the tasks or stories that realise it. A dashed
line across the columns marks the walking-skeleton slice, the thinnest end-to-end release.

## Vocabulary

Use the shared Sotto classes so the diagram matches the design page:

- Activities: `<rect class="svg-node" ...>` across the top in the amber accent with a `<text class="nodetext">` name.
- Stories: `<rect class="svg-node" ...>` in the muted accent, stacked in a column under their activity.
- Slice marker: a dashed horizontal `<line>` (`stroke-dasharray`) across the columns with a `<text class="flowlbl">` labelling the release ("walking skeleton").
- Accents carry meaning: amber `#ffb454` for the activity backbone, muted `#97a0ab` for the stories beneath, teal `#5fd3c4` to highlight a story that is in the first slice.

## How to lay it out

Put the activities in reading order left to right, stack each activity's stories directly
beneath it in priority order (most essential at the top), and draw the slice line under the
first release's stories. Map the activities that carry the argument, not the whole backlog.

## Output

Emit a single `<svg viewBox="0 0 W H">...</svg>` and nothing else. It must be well-formed
(balanced or self-closing tags, quoted attributes, no XML comments). See example.svg in this
skill for a complete, valid reference.
