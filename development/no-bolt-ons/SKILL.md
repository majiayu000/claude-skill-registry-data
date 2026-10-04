---
name: no-bolt-ons
description: "Use when adding a new requirement to an existing design. Redesign as if the requirement had been there from day one instead of attaching it to the side."
disable-model-invocation: true
kind: principle
---

# No bolt-ons

When a new requirement lands, the easy move is to attach it to whatever's already there. A flag here, a special case there. Don't. Ask what we would have built if we'd known about this requirement on day one, and build that.

## How

- **Read everything the change touches first.** All the affected files, not just the one you were pointed at. You need the whole current design in your head before you can redesign it.
- **Ask the from-scratch question.** "If we were writing this today with this requirement known, what would it look like?" That's the target. The gap between that and what exists is the work.
- **Push the change all the way through.** Types, docs, examples, tests, and any written rationale. A redesign that stops at the code leaves the docs describing the old world.
- **Design it whole, ship it in pieces.** Think through the full redesign, then deliver it as a sequence of small changes that each stand on their own.

## Be bold about it

Don't shrink the redesign to fit what feels safe. With agents doing the work, a rewrite that would have been out of the question a few years ago is often the right call now: rewriting a module, swapping a library, porting something from another language. If the honest from-scratch answer is big, say so and propose it. Patching the existing thing is how designs rot.

## The test

Would someone reading the result be able to tell which part was added later? If yes, it's a bolt-on.
