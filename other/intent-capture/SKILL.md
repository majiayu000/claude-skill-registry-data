---
name: intent-capture
description: Restate a request as goal + constraints + done-when before planning or editing. Trigger when a request is vague, has two+ plausible readings, or names no acceptance criterion.
---

# Intent Capture — Pin the Ask Before Acting

A plan built on a misread request fails regardless of execution quality. This skill forces the read to become explicit and checkable before `plan-first` or any edit runs.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — a misread this caught, or a case where it fired on an already-clear request and wasted a turn. Merge instead of duplicating; delete disproven bullets.

## When it applies
Same threshold as `plan-first`, so the two compose instead of double-gating every turn:
- The request has **two or more plausible readings**, OR
- It names **no observable success condition** ("make it better," "clean this up"), OR
- It's the first ask in a new thread of work with no prior context to anchor it.

Below that: skip this and go straight to the work (or straight to `plan-first` if the file-count/destructiveness threshold applies instead).

## The format (3 lines, no more)
```
Goal: <one sentence, the outcome — not the method>
Constraints: <only what was stated or confirmed — never invented (see AI-12)>
Done-when: <one observable check that proves it's finished>
```

Then proceed — this is not a pause for approval unless a genuine fork exists (present it as 2 options with a recommendation, per the project's plan-first convention).

## Rules
- **Constraints come from the request or a direct confirmation, never from assumption.** If a needed constraint is missing, ask one specific question rather than guessing — a wrong guess here poisons every downstream step.
- **Done-when must be checkable by someone else**, not just "it works" — a command that passes, a screen that renders, a file that exists.
- **This is not `plan-first`.** `plan-first` breaks approved intent into files/approach; this skill exists one step earlier, to pin down *what* before `plan-first` decides *how*. On a task that already has a clear goal, skip straight to `plan-first`.
- **Three lines, not a document.** Padding this into paragraphs defeats its purpose — it's a fast anchor, not a spec.

## Failure mode this prevents
Executing a full multi-file change against the wrong reading of the request, discovered only after the work is done — the cost of that redo dwarfs the cost of three lines up front.
