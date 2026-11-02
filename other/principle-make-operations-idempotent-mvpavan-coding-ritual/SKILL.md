---
name: principle-make-operations-idempotent
description: Apply when designing a command, lifecycle step or loop that may crash, restart or retry.
disable-model-invocation: true
---

# Make operations idempotent

Any run may be a rerun, and any run may stop partway.

- A state-changing operation converges on the same correct end state however
  often it runs and wherever an earlier run stopped.
- Each step works out what to do by comparing the observed current state with
  the goal, and applies only the difference.
- Whatever a run leaves behind (locks, temporary files, partial records,
  claims) is recognisable as stale by the next run, from evidence that holds
  wherever the run stopped.
- Probe an operation with two questions: what happens when it runs twice, and
  what happens when it stops at each point? Wherever the answer depends on
  leftovers, add reconciliation.
