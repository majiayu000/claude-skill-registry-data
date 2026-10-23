---
name: when-stuck
description: "Use when the work has stalled and more effort in the same direction is not helping: pick the technique matching the kind of stuck. Distinct from debug, where the cause is findable."
---

# when-stuck

Cross-cutting (`WORKFLOW.md` §2). `debug` handles a bug: something behaves wrongly and there's a cause
to trace. This block handles the other kind of stuck, where nothing is failing exactly, the approach
just isn't working, and the instinct is to try the same thing with more determination.

The first move is diagnosis: **which kind of stuck is this**. Applying the wrong technique is how you
spend an afternoon being creative about a problem that needed a measurement.

| Symptom | Technique |
|---|---|
| Special cases multiplying, several near-identical implementations | §1 unify, or delete |
| "It has to be done this way" and nobody can say why | §2 invert the assumptions |
| Works here, unclear whether it survives production | §3 push the scale to the extremes |
| The same problem keeps reappearing in different places | §4 name the pattern once |
| The same action keeps failing, findings are being lost, or work resumes after a gap | §5 [`references/05-repeated-failure.md`](./references/05-repeated-failure.md) |
| A task too vague or too big to say what the first move is | §6 [`references/06-unblock-card.md`](./references/06-unblock-card.md) |
| Something behaves wrongly, with a traceable cause | not here → `debug` |
| Blocked on information only a human has | not a technique → ask |

## When
As soon as the same approach has been retried without progress — a spec that won't settle, a design
decision that keeps reversing, a bug whose cause moves every time you look, a task that has been "almost
done" for hours. **Not** for a wrong behaviour with a findable cause: that is `debug`.

## Steps

### 1. Unify, or delete: the simplification cascade
When you have four things doing almost the same job:
1. **Inventory the variations** honestly, all of them.
2. **Find the sentence that unifies them** — the "if this is true, we don't need X, Y and Z". That
   sentence is the whole technique; without it you're just planning a refactor. Treat it as a
   hypothesis, not a result: it's easy to sound right before anything is written down, and step 4 is
   what actually tests it.
3. **Check every existing case fits** the unified model, including the awkward one. The awkward one is
   usually why there were four. If making it fit means fixing something that was independently wrong
   (a check in the wrong place, a guard applied per-item when it isn't per-item), separate that fix
   from the unification — don't credit the abstraction with a fit it only reached because a bug got
   fixed along the way, and don't let that fix's line count hide inside step 4's comparison.
4. **Count the lines it deletes against the lines it adds.** A cascade that unifies four things into
   one abstraction and removes nothing is over-abstraction wearing the costume of simplification.
   That's the `over-engineering-review` test, and it applies here in full: if the complexity moved
   rather than disappeared, don't do it. Do this by actually writing the unified version, not by
   estimating: a unifying sentence that felt obviously right at step 2 can still net-add lines once the
   shared machinery (a config object, optional-callback plumbing) is written out, and when it does the
   verdict is to keep the duplication, not to unify.

### 2. Invert the assumptions
When you feel boxed into the only possible approach:
1. **List what must be true** for the current approach to be the right one. Write the assumptions
   down; unwritten ones don't get questioned.
2. **State the opposite of each**, even when it sounds absurd.
3. **Follow the implications**: what would change if the opposite held?
4. **Keep the inversions that survive contact with reality.** Most won't. The one that does is usually
   the thing you couldn't see: "faster is always better" inverts into a deliberate debounce, which is
   both slower per keystroke and better overall.

### 3. Push the scale to the extremes
When "will this hold?" is vague:
1. **Pick the dimension** that worries you: volume, users, duration, failure rate, latency.
2. **Run it mentally at a thousand times more, and a thousand times less.** Not double, not half:
   extremes are what expose the assumption.
3. **Name what breaks first.** An in-memory cache that's fine for hours is unbounded growth over
   years. A synchronous call that's fine locally is unusable across a continent. An error handler
   that's fine for occasional failures collapses at a constant rate.
4. This converts "will it scale" into a specific failure you can decide to accept or prevent.

### 4. Name the pattern once
When the same shape keeps reappearing:
1. **Require three occurrences** in genuinely different places before generalising. Two is a
   coincidence, and generalising from two is how a bad abstraction gets born.
2. **Strip the domain vocabulary** and state what's actually happening underneath.
3. **List what varies** between the occurrences: that's what the general form has to parameterise, and
   if the list is long, they weren't the same problem.
4. Then apply §1's line count before building anything.

### 5 and 6. In `references/`
§5 holds the rules around any attempt (never repeat a failed action, escalate after three, write findings to disk,
the reboot checkpoint); §6 holds the unblock card for a task too vague to start. Read them from the table at the top.

## Output / checkpoint
No checkpoint of its own: it feeds back into whichever step was stuck. What it owes is a decision —
the technique applied, what it revealed, and what changes — not a page of exploration.

## Guardrails
- **Timebox it.** This block exists to break a stall, not to become the afternoon. If no technique has
  produced a decision, that's the signal to ask a human, not to try a fifth angle.
- **Don't reach for a technique when the blocker is information.** If the answer lives in someone's
  head or in the business's rules, no amount of inversion produces it. Ask.
- **A technique that produces an insight but no change produced nothing.** Interesting is not the bar.
- §1 and §4 both propose generalising, and both are net-negative if they add more than they remove.
  The line count isn't a formality, it's the check that keeps this block from becoming a licence to
  abstract.

## Origin
Rewrite of the `problem-solving/` category from a market skills repository (the companion of the
upstream this framework responds to): `when-stuck` as a dispatch, plus `simplification-cascades`,
`inversion-exercise`, `scale-game` and `meta-pattern-recognition`.

Two deliberate departures. **Merged into one block instead of six**: these are techniques you reach
for rarely, and six separate files is six files nobody opens — the symptom→technique table at the top
is how the thing actually gets used, so it's the block, not an index pointing elsewhere.
**`collision-zone-thinking` was not taken**: forcing two unrelated domains together (code as biology)
generates metaphors reliably and decisions rarely, and this framework already errs toward too much
material rather than too little. Also added: the three-occurrence threshold before generalising, and
the requirement that §1 and §4 pass the `over-engineering-review` line count — the source presents
unification as straightforwardly good, which collides with our standing preference for less logic to
maintain.

**Dogfooded, 2026-09-10.** Real stuck scenario, not a pre-known answer: in `/tmp/dogfood-nestjs`
(scratch files, isolated from the rest of that project), wrote four near-identical notification
dispatch functions (welcome, password-reset, invite, digest) that had grown one at a time, matching
the table's first row ("special cases multiplying"). Applied §1 step by step. Step 2 produced a
unifying sentence that sounded right — a `dispatch(recipient, config)` core with per-type guard and
subject-builder callbacks. Step 3 surfaced a real, independent bug in the awkward case (the digest
function's "nothing to digest" check was written per-recipient even though it depends on a
call-level count, not on the recipient) — genuinely matching "the awkward one is usually why there
were four." Step 4, done by actually writing the unified version rather than estimating, gave 59
lines before and 70 after: the abstraction net-added lines. Per the method's own rule, the correct
call was **not to unify** — keep the four functions, fix the digest bug on its own.

The method worked: step 4's guardrail caught exactly the trap step 2's optimism walked into, which is
the scenario the guardrail describes in the abstract but this is the first time it was checked against
real written-out code instead of asserted. One real gap found and fixed above: step 3 didn't say what
to do when the awkward case's "fit" comes from fixing an unrelated bug rather than from the
abstraction itself — without separating the two, the bugfix's line savings get silently absorbed into
step 4's count, making a non-viable unification look better than it is. No other step needed
correction; §2/§3/§4 were not exercised in this pass.

Sections 5 and 6 (`references/05-repeated-failure.md`, `references/06-unblock-card.md`) were added 2026-10-19; their sources, the choices that are ours and what was not read are in [`references/origin.md`](./references/origin.md).
