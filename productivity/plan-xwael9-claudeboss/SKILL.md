---
name: plan
description: Delegate architecture/planning work to opencode's dedicated planning agent before any code gets written. Use when the user says "/claudeboss:plan", wants a plan or design reviewed before implementation, or asks for a task to be scoped before building it.
metadata:
  origin: ClaudeBoss
---

# ClaudeBoss — Plan Mode

Opencode ships a dedicated `plan` primary agent, separate from `build`. Use it when the task is "figure out the right approach" rather than "write the code" -- it's a distinct pass from `/claudeboss:team` and `/claudeboss:boss`, meant to run *before* either of them on non-trivial work.

## Prerequisites

`claudeboss install` must have succeeded at least once on this machine.

## Workflow

1. **Delegate the planning question**, not the implementation:
   ```bash
   claudeboss run plan "<the design question: what needs to change, what constraints apply, what are the tradeoffs>"
   ```
   `claudeboss run plan` automatically routes to opencode's `plan` agent (not `build`) and a general-purpose free model.

2. **Review the plan like you'd review a design doc.** Does it account for the actual codebase's conventions and constraints (you may need to check the real code yourself -- the free model has no memory of this specific project beyond what you told it)? Is it missing an edge case, a migration step, a rollback path?

3. **Hand off.** Once the plan is sound, either:
   - implement it yourself,
   - delegate implementation to `/claudeboss:team` (you review + finish), or
   - delegate to `/claudeboss:boss` (you manage, opencode's `build` agent implements, you approve before deploy).

   Tell the user which handoff you're using and why.

4. **If the plan is weak** (vague, ignores a stated constraint, unworkable), don't pass it downstream -- refine the prompt and re-run, or just write the plan yourself and say so. A bad plan compounds into worse code if it flows straight into `/claudeboss:boss`.
