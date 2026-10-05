---
name: fresh-eyes
description: >
  Look at a module, config, workflow, or design with fresh eyes: ignore how it
  works today, propose the simplest design that could serve the same purpose,
  and keep the proposals that survive the constraints that shaped the current
  one. Use when the user asks why something is so complicated, wants a
  first-principles or fresh-eyes review, or asks "why don't we just...".
---

# fresh-eyes

<!-- vale Skills.FillerWords = NO -->
<!-- "why don't we just" quotes the reader's hunch; its "just" is the
hunch's voice, not filler. -->

Reproduce the hunch every reader gets: "why don't we just do it like this?" The
discipline is in the order - design from the purpose first, then let the
constraints kill what they can. Reading the current mechanism first anchors you
to it, and every proposal comes out a tweak.

<!-- vale Skills.FillerWords = YES -->
<!-- vale ai-tells.FillerIntensifier = YES -->

## Steps

### 1. State the purpose

Read the target only far enough to write its purpose: what it must provide, to
whom, in one paragraph that doesn't name any part of the current mechanism - inputs,
outputs, and guarantees, never classes, files, or steps. Done when someone who
has never seen the target could design from the paragraph alone.

### 2. Design naively

<!-- vale Skills.FillerWords = NO -->
<!-- vale ai-tells.FillerIntensifier = NO -->
<!-- The naive question is quoted verbatim; its "just" carries the hunch, and
     "single source of truth" is the standard name for the measure. -->

Put the target aside and design from the purpose paragraph: the simplest thing
that could serve it. Ask the naive question of each moving part the purpose
seems to demand - "why don't we just [one obvious move]?" Produce one to three
proposals, each a short sketch: the one move it is built around, and what from
the current shape it deletes. Done when each proposal is simpler than the
current shape by a measure you name, such as fewer parts or a single source of
truth, and any sketch that fails that measure is dropped here.

<!-- vale Skills.FillerWords = YES -->

### 3. Walk the fences

Every difference between a proposal and the current shape is a fence: someone
built that complexity for a reason, live or dead. For each difference, hunt
for the reason - git log and blame on the paths it touches, comments, linked
issues and PRs, tests that only make sense against a hidden constraint such as
scale, compatibility, ordering, failure modes, or policy. Classify each fence:

- **Live** - the constraint still holds and the proposal breaks it. The
  proposal dies, or absorbs the constraint and states the cost of keeping it.
- **Dead** - the constraint no longer holds. Name the evidence: the dependency
  is gone, the scale never came, the API changed.
- **Unknown** - no reason found after the hunt. Say so; only evidence makes a
  fence dead.

Done when every difference is classified and no proposal carries an unexamined
fence.

### 4. Report the survivors

Deliver the proposals that survived, best first. Give each one a short sketch
of the design and what it deletes, then its fence list with verdicts. State
the cost of each live fence the proposal absorbs and the evidence for each
dead fence, and flag each unknown fence as the open risk. When nothing
survives, that is the report: the current shape is
earned, held up by the fences you list. The deliverable is this report; leave
the target untouched.
