---
name: alternatives-explore
description: Generate materially different approaches to a product, workflow, or system problem, compare them with the conventional approach, and recommend one bounded experiment. Use when the user explicitly asks for bold, contrarian, experimental, or non-incremental alternatives; not for the smallest design that meets stated requirements, which belongs to system-design.
---

# Alternatives Exploration

Find out whether a materially different approach beats the conventional one, and recommend one cheap experiment that can show it.

## Workflow

1. State the problem, the outcome that must stay valuable, the hard constraints, and the assumptions that the obvious approach rests on.
2. Describe the conventional approach in two or three sentences. It is the baseline that every alternative must beat.
3. Generate three to five alternatives. Each alternative must reject a different assumption from step 1, for example who owns the work, when it happens, where it runs, which component is necessary, or whether the problem needs solving at all. Drop an alternative that differs from another only in tools, names, or parameters.
4. Evaluate the baseline and each alternative for user value, feasibility within the constraints, cost to reverse, and cost to test. Name the most likely way each one fails.
5. Recommend the strongest option. If the baseline wins, say so. Do not recommend an alternative only because the user asked for a bold one.
6. Define the smallest experiment for the recommendation: what to build or measure, its cost limit, the result that confirms it, and the result that rejects it. Fix both results before the experiment runs.

Do not settle final architecture, resolve open technical facts, write a plan, or implement the experiment. Use `architecture-refine` to choose between architecture options, `technical-spike` when feasibility depends on an unknown external fact, and `plan-create` to plan accepted work.

## Result

Report the assumptions, the baseline, each alternative with the assumption it rejects and its likely failure, the recommendation and its reason, and the experiment with its cost limit and its confirming and rejecting results. A recommendation does not authorize implementation.
