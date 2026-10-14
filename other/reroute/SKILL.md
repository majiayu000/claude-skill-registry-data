---
name: plan-mode-reroute
description: Revise a plan after a failed assumption, blocker, or changed constraint. Use when an accepted path is stale or failing and the user still wants the original goal achieved.
license: MIT
---

# Reroute

Change the route without losing the destination. Start with the first observed point where the accepted path stopped working.

1. Capture what was attempted, observed, and expected. Check the source or runtime seam that produced the failure before proposing a remedy.
2. Preserve the original goal, accepted constraints, authorization, and completed work. Identify which plan assumption failed and which later steps depend on it. Do not restart finished work or discard unrelated changes.
3. Compare the smallest viable alternatives against evidence, effort, reversibility, and effect on acceptance criteria. Prefer a supported path that uses existing tools and contracts over custom infrastructure whose maintenance cost the user did not request.
4. Replace the affected steps and their checks. State the new first action, what changed, and any remaining risk. When a materially different tradeoff belongs to the user, present concrete choices with consequences; continue independent work meanwhile.
5. Execute the revised next step when already authorized, then verify its result. If every route depends on missing input or an external change, report the exact blocker and the smallest action that would unblock it.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
