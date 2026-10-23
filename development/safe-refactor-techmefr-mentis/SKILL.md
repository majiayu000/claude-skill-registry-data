---
name: safe-refactor
description: "Use when restructuring code that already works (extracting, consolidating, moving an ownership boundary, splitting a file) and behaviour must stay the same: fix the proof before the first edit, move one boundary per step, replay the same proof after."
---

# safe-refactor

A support block for step 6 (`code`) and step 9 (`simplify`) of `WORKFLOW.md`, for the change whose whole point is that
nothing observable changes. `simplify` cleans a diff that is already correct; `archi` decides where code
should live; this block is the protocol for moving it there without breaking it.

## When
A structural edit with no intended behaviour change: extracting a function or a class, merging duplicates,
moving logic to the layer that owns it, splitting an oversized file, replacing a hand-rolled piece with a
library call. Not for a bug fix (`references/01-surgical-patch.md`) and not for a data or schema transition
(`skills/deprecation-migration`).

## Steps
1. **Draw the boundary of what must not change.** Write down, before reading further: the public signatures
   others call, the failure behaviour (which errors, with which types and messages callers match on), the order
   of side effects, the output formats, the compatibility windows. Anything outside that list is allowed to move.
   A feature or a fix riding along is outside the refactor and gets its own change.
2. **Fix the proof before touching structure.** Run the tests that cover the code you will move and see them
   pass. If they do not exist, pin the current behaviour first (`references/02-pinning-behaviour.md`); if you
   cannot pin it, say so and narrow the refactor to what can be proven, or stop. A refactor with no proof
   is a rewrite with a different name.
3. **Move one ownership boundary per step.** One concern changes owner at a time: a function leaves a class, a
   query leaves a controller, a duplicate collapses into its twin. Each step leaves the code building and the
   proof passing, so any step can be the last one you ship.
4. **Keep the surface still.** Public signatures, error behaviour, ordering and compatibility stay as step 1
   wrote them, unless the task scoped a change and named it. No new dependency, configuration key or
   abstraction unless correctness needs it; a refactor that grows the surface has become a design change.
5. **Replay the identical proof after every step.** The same commands, the same scope. Red means undo that
   step (revert it) and look again at the boundary; fixing forward with a second idea is how a refactor turns
   into a bug hunt in code you just rearranged.
6. **Stop when behaviour matches and the requested structure exists.** No extra renames, no tidying of the
   next file over. What you noticed and did not touch goes in the closing message, once.

## Output / checkpoint
The structure asked for, the proof from step 2 re-run green on the final state with its output read, and a list
of what you noticed but left. A commit per boundary moved, so a reviewer can follow the moves one at a time.

## Guardrails
- **The same proof before and after, or it was not a refactor.** A proof you changed in the same step you
  changed the code proves nothing; an assertion adjusted to match new output is a behaviour change you chose
  not to look at (`skills/tdd`).
- Never combine a refactor with a behaviour change in one commit; a reviewer cannot tell which line is which.
- Never refactor code you have not been asked to touch (`skills/code-baseline` §0): leave it and report it.
- A split made only to satisfy a size count, or a layer added only to be consistent, is not a structure the
  code needed (`skills/over-engineering-review`).
- Blocked on proof, or on a boundary you cannot draw? Escalate rather than refactor on hope.

| Thought | What to do instead |
|---|---|
| "The tests are slow, I will run them at the end" | Step 5. A red at the end names a dozen suspects. |
| "I will fix this bug while I am in here" | A second change in the same diff. Note it, finish the move, fix it next. |
| "The old test is wrong, I will update it with the move" | Then it was a behaviour change. Stop and say which behaviour. |
| "It is only moving code, no test needed" | Moving code changes load order, scope and import cycles. That is what the proof is for. |

Predicted, not recorded: replace with verbatim sentences from a `skills/testing-blocks` run when one exists.

## Origin
The `safe-refactor`, `surgical-patch` and `verify-and-stop` skills of `caveman` (Apache-2.0, MIT-licensed
lineage, read 2026-10-02): bracketing a structural edit with the same proof, one ownership boundary at a time,
the narrowest-layer fix. Rewritten in our own words; no text copied, so its NOTICE obligations do not apply.
The "lean build" and "migration" skills of the same repo are already covered by `skills/code` step 0 and
`skills/deprecation-migration`; nothing was added for them. Pinning behaviour is our own addition.
