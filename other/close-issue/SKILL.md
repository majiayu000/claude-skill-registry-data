---
name: close-issue
description: "Verify completion and merge an authorized pull request before confirming its issue is resolved."
metadata:
  category: Delivery
---

# Close Issue

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Completion gate

Resolve the issue, PR, repository, and current head. Determine what the user intends by closing: merging completed work, marking a duplicate, or abandoning an issue. A non-implementation closure should record its actual reason and does not need a fabricated PR.

For an implementation PR:

1. Compare every acceptance criterion with implementation and verification evidence. Read required review, QA, and human-acceptance records under the project's policy. Record missing evidence rather than inventing a pass.
2. Confirm required CI and review checks apply to the current head. Revalidate stale evidence when the code changes. Use the check-ci procedure to distinguish green, pending, failing, absent, and unknown checks.
3. Require a user instruction authorizing the merge, or an established project policy that explicitly delegates merging when its conditions are met. Green CI or a review recommendation by itself is not user authorization. Never approve on the user's behalf or bypass branch protections.
4. Verify the intended base branch, merge strategy, and issue linkage. Follow repository policy rather than assuming squash merge or a particular branch name. Check for a head change immediately before merging; use the service's expected-head protection when available.
5. Merge, then verify the actual merge commit and issue state. If automatic closure did not occur, close the issue only when that is within the authorized request and completion is confirmed.
6. Clean up branches or worktrees only when authorized and safe: do not remove another person's active checkout or uncommitted work. Update an optional project board using its actual terminal state and verify it.

## Deliverable

Report the merge/closure outcome, current issue state, evidence, and any cleanup or follow-up remaining. Do not perform unrelated releases, deployments, or parent-repository pointer updates.
