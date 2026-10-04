---
name: design-slice
description: Facilitates the Slice movement of a Tutti design session. Use after the Structure movement to map the backbone of the journey, name the walking skeleton (the first end-to-end increment), and sequence the entire remaining scope into an ordered build plan. Tutti builds the whole design autonomously, so this movement sets the ORDER of the full build, never an MVP subset. Asks one question at a time, may invoke the story-map diagram skill when the backbone reads better as a picture, and emits the movement artifact section once the backbone, the walking skeleton, and the full ordered scope are covered.
---

# Slice movement

Set the order in which the whole app gets built. Tutti builds the entire ratified design
autonomously, increment by increment, for as long as it takes. This movement is NOT about
choosing a minimal product to ship or picking what to cut. Everything in the design gets built.
The only question is sequence: what order makes each increment coherent, independently testable,
and safe to build on.

The guiding question is: in what order is the whole app built, walking skeleton first?

## What to cover

- **Backbone mapped**: the sequence of activities the user moves through, left to right, across
  the full app.
- **Walking skeleton**: the first end-to-end increment, a thin path that touches every part of
  the system while doing almost nothing, so the whole architecture is proven before it is
  fleshed out. It is the first thing built, never the last, and never the product itself.
- **Remaining scope sequenced**: every other increment (the ribs), ordered by dependency and
  value, from right after the skeleton all the way to the complete design. Nothing is dropped or
  deferred to a human; the order is the whole point.

## How to facilitate

Ask ONE question at a time. Map the backbone first, then name the walking skeleton (the thinnest
end-to-end increment that proves the path), then sequence the rest of the scope into an ordered
build plan. Order by what unblocks what and by value, so an autonomous builder always has a
running, testable app and each step layers cleanly on the last.

Do NOT ask "what would you ship first," "what is the MVP," or "what could we cut." The design is
built in full; the walking skeleton is only the first step of building all of it. If the human
frames something as out of scope, that belongs in the design's non-goals (the Frame movement),
not here. Here, in-scope work is only ever sequenced, never trimmed.

## Diagrams

When the backbone and its build order read better as a picture, invoke the `story_map` diagram
skill and embed its inline SVG in the artifact section.

## When you are done

Once the backbone, the walking skeleton, and the full ordered scope are covered, emit the tagged
complete reply with the artifact section as markdown: a `## Slice` heading, the backbone, the
walking-skeleton increment, and the remaining increments in build order (every part of the
design accounted for).
