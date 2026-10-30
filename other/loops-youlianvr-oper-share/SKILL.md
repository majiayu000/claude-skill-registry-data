---
name: loops
description: >-
  Repeating / autonomous work cycles: bounded loop mode ("loop 10 30m
  <prompt>"), unattended night-shift or heartbeat work with one-task-at-a-
  time focus, and a library of proven loop prompts. Use when the user asks
  for autonomous repeated execution — "keep going until done", "work in
  cycles", "[HEARTBEAT]", "while I sleep", cron-style self-runs. One
  contract; the parts under parts/ carry the mechanics.
---

# loops — autonomous cycles

> Home branch in Memora: `root/skill/loops`.
>
> Every loop must have a stopping condition and a verification step per
> iteration. A loop without a verify step is a way to burn tokens, not work.

## Choosing a part

| Situation | Part |
|---|---|
| Run a bounded repeating cycle from a user prompt | `parts/loop/` |
| Finish an assigned unattended goal with checkpoints and valid stops | `parts/autonomous-work/` |
| Ready-made loop prompt patterns to pick from | `parts/loop-library/` |

## Rules

- **The stop condition belongs to the owner.** Iteration cap and exit condition
  come from the invocation; the agent may propose one, never widen or replace it.
- **Night shift may**: read, test, edit code in its own branch, prepare the
  report. It may not deploy, spend money, or take external actions — those wait
  for the owner, one authorization each.
- **Heartbeat stays silent** when nothing changed: write only on a change or a
  blocker. No progress chatter, no forced "still working" lines.
- Verify changed work and save checkpoints (Memora node + short chat line) so a
  resumed session continues instead of repeating.
- Destructive or irreversible actions inside a loop always pause for the owner;
  autonomy never outranks Never Destroy.
- One-off persona/style modes (`godmode`, `bro`) are separate top-level skills,
  not loops.

## Related

`autonomous-work`, `task-cycle`, `planning`, `ship` (deploy needs the owner).
