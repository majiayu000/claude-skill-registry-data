---
name: power-debug
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing any fix
---

# Find the Root Cause First

## The iron law

**No fix without root cause investigation first.**

A fix applied to a symptom you have not explained is a guess. Guesses that happen to work are
worse than guesses that fail, because they hide the real defect until it returns somewhere
more expensive.

## Phase 0 — Has this already been documented?

If `.planning/power/context/pitfalls.md` exists, read it before anything else. It is where
previously observed failure modes were recorded with evidence, and the cheapest possible
investigation is discovering that someone already did it.

A match there is a lead, not a verdict: confirm it against the current failure before acting on
it.

## Phase 1 — Root cause

1. **Read the entire error.** All of it — the message, the type, every frame of the stack, the
   lines before it. The answer is in there more often than not.
2. **Reproduce it consistently.** An intermittent failure you cannot trigger is not yet
   understood. Find the condition that makes it deterministic.
3. **Check what changed recently.** `git log`, `git diff`. Most breakage is recent.
4. **In a multi-component system, instrument every boundary before proposing anything.** Add
   logging at each hand-off — caller, transport, handler, storage — and run once to learn
   *where* it breaks. Guessing which layer is wrong and fixing that layer is how three fixes
   go by without touching the defect.
5. **Trace the data backwards** from where it is wrong to where it was right. The bug is
   between those two points.

## Phase 2 — Pattern analysis

Find something in this same codebase that works and does the same kind of thing. Read it
**completely** — not a skim, not the parts you expect to matter. List every difference between
it and the broken path, including the ones that look irrelevant. The irrelevant-looking one is
frequently the answer.

## Phase 3 — One hypothesis at a time

Write it down: "I think X is the cause, because Y." Design the smallest test that would prove
it wrong. Change **one** variable.

If the hypothesis was wrong, form a **new** one. Do not stack another fix on top of the
previous attempt — a codebase with three speculative fixes in it is harder to debug than the
original bug.

## Phase 4 — Fix

1. Write the failing test first (`pwdev-power:power-tdd`).
2. Fix the **root cause**, once. No "while I'm here" — an unrelated improvement in a bugfix
   commit makes the bisect useless.
3. Verify with `pwdev-power:power-verify`.

## Three strikes

**If three fixes have failed, stop.** The problem is not where you are looking, and the
architecture is now the suspect. Bring it to your human partner with what you tried and what
each attempt ruled out. Continuing costs more than asking.

## Signals you have already gone wrong

When your human partner says any of these, they are telling you that you skipped Phase 1:

- "Is that actually happening?"
- "Stop guessing."
- "Think about this properly."

Go back to reading the error.
