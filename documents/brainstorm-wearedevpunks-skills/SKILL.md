---
name: brainstorm
description: Brainstorm a bounded system with the user as a proposal loop that converges on one shape and a Brainstorm Brief. Use when the user asks to brainstorm a system, shape, or architecture.
---

# Brainstorm

Brainstorm proposes; the user steers. Each turn moves one proposal toward a
shape the user accepts. Question rounds belong to `$requirements-grill`.

## Frame

Bound the system: scope, accepted constraints, available evidence. Name its
real operators: end users, agents, human operators, or a mix. Shape it through
these lenses:

- **Agent legibility**, when agents operate the system: agent-intuitive (clear
  meaning), agent-ergonomic (efficient control), agent-accretive (verified
  knowledge that later runs reuse).
- **`$flow-lenses`**, optional, on your own shapes. Show each finding as a
  tradeoff of the shape it touches.

## Turn

Every turn carries, in order:

1. **Current shape**: the proposed shape, refined by the user's last reaction.
2. **Alternatives**: two or three other shapes, each with its tradeoff against
   the current shape.
3. **Evidence**: an anchor (file, doc, source, user quote) for each claim, or
   an explicit unknown.
4. **Forks**: each open decision as a proposal with a default: "I take X
   unless you steer."
5. **View**: one `$show-me` view of the current shape: a rendered page when
   the host supports it, otherwise `show-me` text views.
6. **Close**: end on the proposal and an invitation to react.

Every open point stays a fork with a default; a turn holds no question round,
no numbered question list, and no `AskUserQuestion` call.

Completion: all six items are present, every claim has an anchor or an
explicit unknown, and the Brief reflects every acceptance, rejection, and
preference so far.

## Exits

Exactly two:

- **Another turn**, when the user steers.
- **`$requirements-grill` with the Brainstorm Brief**, when the user is ready
  to settle requirements.

Brainstorm edits no code, writes no plan, and starts no implementation.

## Brainstorm Brief

The Brief is the only durable write. Write it at
`<wiki-root>/content/docs/project/grilling/<topic>-brainstorm-brief.md` with
the grill artifacts' routed-wiki frontmatter (title
`"<Topic> Brainstorm Brief"`) and its `grilling/meta.json` entry, per the
[Routed Wiki Contract](../requirements-grill/references/artifact-output.md#routed-wiki-contract).

Update it at the end of every turn in which the user accepted or rejected a
shape or stated a preference. It holds:

1. Bounded system and operators.
2. Chosen shape.
3. Rejected shapes, each with the reason.
4. User-stated preferences, quoted verbatim.
5. Open forks, each with the proposed default.
6. Evidence anchors.
