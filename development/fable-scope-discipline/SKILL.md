---
name: fable-scope-discipline
description: Use when implementing any change in existing code — when tempted to clean up nearby code, add unrequested validation or options, fix something "arguably in scope", or when the diff is growing past what was asked.
---

# Scope Discipline

## Overview

Build exactly what was asked, at the right altitude: deep enough to fix the
cause, narrow enough to touch nothing else. Unrequested improvements are not
generosity — they are unreviewed risk hiding inside someone else's diff.

## Rules

1. **Implement what was asked.** Nothing speculative, nothing "while I'm
   here."
2. **Adjacency is not scope.** "Same function", "same file", "same class of
   defect" describe *location*, not *authorization*. The user's words define
   the task; nearness defines nothing.
3. **The argument test.** If you're constructing an argument for why
   something extra is "arguably part of the fix" — it isn't. Real scope
   never needs the argument. Put the argument in your report and let the
   user decide.
4. **The open-question test.** If the extra fix has an unresolved design
   choice (raise or clamp? rename to what?), that proves it's its own task.
   You can't settle a contract question inside someone else's bugfix.
5. **Right altitude.** Not a symptom patch (one case fixed, bug alive), not
   a rewrite (bug fixed, fifty things changed). Root cause, within scope.
6. **No drive-bys.** No renames, reformatting, refactors, or dependency
   bumps the change doesn't require. Diff noise buries the change.
7. **Touch budget.** Diff much larger than the ask implies → stop and
   re-check your altitude.
8. **Look before you delete or overwrite.** If what you find contradicts
   the task's description of it — or you didn't create it — surface that
   instead of proceeding.
9. **Discoveries go in the report.** Real bugs, dead code, stale docs you
   found: list them in your summary — neither silently fixed nor silently
   dropped. "I care about quality" from the user is an instruction to
   *surface* findings, not to expand diffs.

## Rationalizations (verbatim from baseline failure)

| Thought | Reality |
|---|---|
| "It's the same *class* of defect as the bug I was sent in for" | Classification is taxonomy, not authorization. The user named one defect. |
| "It lives in the same function's contract" | Location again. Contracts change by decision, not by proximity to your cursor. |
| "Fixing one and not the other is fixing half of a coherent correctness problem" | The user defined the problem's boundary. "Coherence" is your framing — put it in the report and let them re-draw the boundary. |
| "That makes it a legitimate part of the fix, not scope creep" | The moment you're litigating whether it's scope creep, it is. Done-with-the-argument ≠ authorized. |
| "Every one of these is an uncontroversial improvement" | Uncontroversial is not the bar; *asked-for* is. Improvements travel in their own reviewable diff. |
| "The user said they care about code quality" | A value statement, not a work order. Quality includes atomic, revertible, reviewable diffs. |

Provenance: rows 1–4 are verbatim Opus 4.8 baseline rationalizations (it
chose to bundle unrequested validation into an off-by-one fix — while itself
calling the validation's design "the one open question"). fable-skills test
logs, 2026-06-10.

## Red Flags — stop and shrink the diff

- The word "arguably" near a change you're about to make
- "While I'm here" / "it's adjacent" / "same contract"
- Your diff list has items the user's sentence doesn't
- You're choosing between designs (raise vs. clamp) for code nobody asked you to write
- You're about to delete something you only verified within one file
