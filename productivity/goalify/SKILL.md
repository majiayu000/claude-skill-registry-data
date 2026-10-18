---
name: goalify
description: Goalify messy intent by generating and activating one lean goal immediately, then continuing work under it.
---

# Goalify

`goalify` generates and activates the goal in one move, immediately. Invocation
is permission to create the active goal now and continue the user's task under
it.

## Workflow

1. Read supplied handoffs, specs, issues, logs, examples, and scoped repo
   guidance.
2. Reduce the request to one durable objective with proof and stop conditions.
3. Write the smallest `/goal` contract that can run without re-asking.
4. Activate that goal immediately, then keep working under the active goal.
5. Report only progress, blockers, and final proof relevant to that active goal.

## Contract

Include only:

- objective: one outcome
- context: exact paths, issues, URLs, logs, artifacts, and constraints
- workflow: terse checkpoints with named skills, tools, or phases from context
- proof: commands, scenarios, artifacts, logs, or other done evidence
- stop: done condition, early-stop blocker, and final report expectation

Keep it pointer-heavy, no secrets, no vague "make it work", and <= 4,000
characters after `/goal`.
