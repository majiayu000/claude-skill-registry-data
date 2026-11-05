---
name: review-round
description: Run a change round for planning units the user reviewed - read the numbered changes in each unit's Review section and have an agent address every one. Use when the user has written review changes into unit files, or says "run the review round".
---

# Review round

1. **Find** every unit file in the current batch whose last `## Review` round says "changes" (a numbered list) and has no later round.
2. **Clarify**: if a change is unclear, ask the user (AskUserQuestion, recommendation first) before any agent starts.
3. **Brief** one agent per unit, on branch `<unit>-rN` (N = the round number): the unit file, the numbered change list, and the `/run-batch` brief lines (timestamps, effort re-check, no extra work, proposed units, tests first, screenshots). The agent addresses every change by its number and reports one line per change: what it did and how to test it.
4. **Run** the agents in parallel, log each round as its own row in the time log, merge, and run the checks.
5. **Update** the unit's section in `REPORT.md` with the round (what changed per number, time, how to test).
6. **Tell the user** which units are ready for the next review, one line each.

A change is part of the unit, not new work. Something new that is not a fix of the reviewed work goes to `proposed/`.
