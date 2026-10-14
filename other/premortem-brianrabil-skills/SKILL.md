---
name: plan-mode-premortem
description: Assume failure and work backward to causes. Use when a plan is about to be committed and the risks must be surfaced before, not after, delivery.
license: MIT
---

# Premortem

A plan reviewed for what could go wrong is more robust than one reviewed for what will go right. Assume it already failed and find out why.

1. State the plan and its success criteria. Assume it has failed at delivery — the outcome was not achieved.
2. Generate the most plausible causes of failure, ordered by likelihood. For each, name the specific mechanism: a dependency that was assumed, a step that was skipped, a constraint that was unknown, a stakeholder who was not consulted.
3. For each cause, state the earliest point it could have been detected and the signal that would have revealed it.
4. Report the causes with their detection points, and propose the smallest change to the plan that would catch the most likely ones earliest.

A premortem is a planning exercise, not a critique of the people. It does not authorize changing the plan without the owner's agreement.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
