---
name: plan-mode-brainstorm
description: Brainstorm distinct possibilities for an open-ended problem. Use when the user asks for ideas, directions, or ways to approach a goal before choosing a solution.
license: MIT
---

# Brainstorm

Open the option space while keeping the user's goal and constraints in view.

1. State the goal, known constraints, and the dimension that is still open. Use the context already provided; ask a question only when a missing constraint would make the ideas unusable.
2. Produce several materially different approaches. Vary the mechanism or underlying assumption, not just the wording. Include a less obvious approach when it is plausible.
3. For each approach, give its core idea, why it could work, the main cost or failure mode, and a small way to test it. Do not present unverified claims as facts.
4. End with a compact map of the options and the choice that would distinguish them. Recommend one only if the user supplied selection criteria or asked for a recommendation.

The brainstorm is complete when every option addresses the same goal, respects the stated constraints, and differs in substance from the others. Deliver ideas, not an implementation or a project plan.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
