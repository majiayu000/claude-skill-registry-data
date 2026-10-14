---
name: plan-mode-to-epic
description: Shape a multi-part product or engineering outcome into one epic. Use when the user needs a coordinated delivery boundary, workstreams, dependencies, and completion criteria before splitting work into tickets.
license: MIT
---

# To Epic

An **epic** coordinates one outcome across several workstreams. Make its finish line and dependencies visible.

1. Read the PRD, spec, discussion, and existing issues. Identify the outcome, its users or consumers, and why coordination is needed. If the source contains separate outcomes, call out the split.
2. Write a title and body covering the problem, target outcome, success evidence, included and excluded scope, constraints, and risks. Group work into deliverable workstreams or milestones. State what becomes usable or verifiable at each.
3. Show only real dependencies and sequencing constraints. Name owners and dates only when supplied or verified; otherwise leave them open. Link decisions and source material that a ticket author will need.
4. Check that workstreams cover scope, dependency order is possible, and the done condition can be observed without reading ticket status.

Deliver a reviewable epic draft. Leave ticket-sized acceptance criteria to `plan-mode-to-tickets`. Create or update an external epic only with explicit authorization.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
