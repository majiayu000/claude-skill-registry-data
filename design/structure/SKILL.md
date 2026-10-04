---
name: design-structure
description: Facilitates the Structure movement of a Tutti design session. Use after the Decide movement to work out how the pieces fit at each zoom level (context, then containers, then components) and to record the irreversible choices as ADRs. Asks one question at a time, may invoke the architecture and network diagram skills when a zoom level reads better as a picture, and emits the movement artifact section once the context, the containers, and the recorded irreversible choices are covered.
---

# Structure movement

Lay out how the pieces fit. The guiding question is: how do the pieces fit at each zoom level?
Work outside in, one zoom level at a time (the system in its context, then the containers
inside it, then components where it matters), and pin the choices you cannot cheaply undo.

## What to cover

- **Context drawn**: the system as one box among the people and systems it talks to.
- **Containers drawn**: the deployable or runnable pieces inside the system and how they talk.
- **Irreversible choices recorded as ADRs**: the decisions that are expensive to reverse (a
  datastore, a protocol, a trust boundary), each with the context and the consequence.

## How to facilitate

Ask ONE question at a time, zooming from context to containers rather than diving straight to
components. When a choice would be costly to walk back, stop and record it as an ADR before
moving on. Go deeper on a boundary that carries trust or data across a seam from the Domain
movement.

## Diagrams

When a zoom level reads better as a picture, invoke the `architecture` diagram skill for the
container fit and the `network` diagram skill for how the pieces reach each other, and embed
the inline SVG in the artifact section.

## When you are done

Once the context, the containers, and the irreversible choices (as ADRs) are covered, emit the
tagged complete reply with the artifact section as markdown: a `## Structure` heading, the
context, the containers, and the ADRs for the irreversible choices.
