---
name: plan-mode-plan
description: Make an executable plan for an agreed goal. Use when the user asks for an implementation plan, a sequence of work, or a way to decide what done means before execution.
license: MIT
---

# Plan

Make the next move clear. A plan is ready when its first step is actionable and its last has a success check.

1. State the goal in the user's terms. Capture constraints, existing authorization, work already completed, and the decision that prompted planning. Ask only about a choice that blocks a useful route; label other unknowns as assumptions.
2. Inspect the relevant current state and authoritative sources. Separate observed facts from assumptions. Treat a proposed feature, catalog entry, or passing typecheck as different from a working capability.
3. Write the shortest dependency-ordered route. For each step, name its deliverable, prerequisite, and observable completion check. Include a recovery point for a change that could disrupt existing work. Leave out speculative infrastructure.
4. Define acceptance evidence for the user's actual outcome, including integration or runtime behavior where it matters. Say which checks can run now and which need a later environment or decision.
5. Present the route, its first action, and any unresolved decision. If the user also asked for implementation, move into the first authorized step once the route is usable.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
