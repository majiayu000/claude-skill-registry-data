---
name: zero-sleep
description: Holds the thread across a big multi-step build without losing the plot — long-haul endurance and context-keeping; invoke via /zero-sleep when a task spans many steps and hours and you need consistency from start to finish.
---

# Zero Sleep

The marathon, not the sprint. This mode is built for long, sprawling builds where the real risk isn't any single step — it's forgetting what you decided three hours ago. It keeps the thread, the goals, and the constraints locked in from step one to step done.

## When to use
- A large, multi-step build that spans many actions or a long session.
- The danger is drift: losing track of earlier decisions, goals, or constraints.

## Behavior
1. Establish and write down the north-star goal, key constraints, and decisions at the start as an anchor.
2. Maintain a living progress ledger: what's done, what's in flight, what's next.
3. Re-read the anchor and ledger before each major step to avoid drifting from the original plan.
4. Keep decisions consistent — when a new step touches an earlier choice, honor it or explicitly revise it on the record.
5. Checkpoint state at natural boundaries so the work can be resumed without re-deriving everything.
6. Watch for contradiction: flag when a new step conflicts with something decided earlier.
7. Periodically summarize progress against the goal so the big picture stays in view.

## Output
Steady end-to-end progress on the build, a maintained progress ledger and decision anchor, and periodic check-ins confirming the work still matches the original goal.
