---
name: design-it-twice
description: "Use when a UI interaction or architecture decision has no precedent in the codebase and the right answer isn't obvious. Build two or three real alternatives, compare them side by side, then commit."
disable-model-invocation: true
kind: principle
---

# Design it twice

When there's no existing pattern to follow and the answer isn't obvious, don't build the first idea. Build two or three and compare. Building the wrong thing costs more than sketching three.

## The rule

- **Two or three real alternatives.** Prototypes or sketches you can look at next to each other. A second flavor of the first idea doesn't count. They have to differ in shape, not in color.
- **One of them is the obvious one.** The version another agent would assume is already there. If the obvious one wins, good. If it doesn't, you now know why, and you can say so.
- **One of them is the bold one.** The version that would have been out of the question before agents did the work. A different library, a different language, a rewrite of the piece instead of a patch. Put it on the table even if it loses. Going with the flow won't get us where we want to be.
- **Let the prototypes decide.** If the question is something you can observe by building it, layout, feel, timing, whether it's even possible, build it and look. Don't ask the human to pick from descriptions. Hand them results to react to.
- **Then commit.** Pick one, delete the others, move on.

## When it applies

- A UI interaction with no prior art in the codebase.
- An architecture choice with more than one workable approach.
- A product decision where the answer depends on how it feels, not on logic.

## When it doesn't

- Mechanical work where the pattern already exists.
- Bug fixes and refactors with a clear target.
- Anything where the constraints leave only one workable option.
