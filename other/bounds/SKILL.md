---
name: plan-mode-bounds
description: Surface hard resource limits before planning. Use when a goal must be checked against time, budget, rate limits, permissions, or capacity before a route is chosen.
license: MIT
---

# Bounds

A plan that ignores a constraint is not a plan. Find the limits that would invalidate the work before committing to a route.

1. Name the goal and the deliverable. Identify the limits that could invalidate it: time, budget, money, rate limits, quotas, permissions, data volume, latency, team capacity, and external deadlines.
2. For each limit, state the actual number or threshold, not a category. Distinguish a hard limit from a soft preference. If a limit is unknown, name the owner who knows and the cheapest way to find out.
3. Check the goal against the tightest limits. If the goal cannot fit, say so and propose the largest version that does, rather than planning around a limit you have not confirmed.
4. Record the bounds the plan must respect, with the source of each. Mark any bound that is an assumption.

Bounds are read-only findings. Surfacing a limit does not authorize changing it; escalate to the owner if a limit must move.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
