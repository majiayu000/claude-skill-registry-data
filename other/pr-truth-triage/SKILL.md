---
name: pr-truth-triage
description: "Classify stale branches by their actual integration diff, conflicts and current requirements; preserve work and separate remaining content from readiness."
---
# Branch truth triage

Inspect live refs, PR state, related commits and the current requirement. Branch names, `git cherry`, ancestor checks and merged-PR titles are useful evidence, not sufficient proof that the current content is already present or still wanted. A three-dot diff shows changes from the merge base; it does not count commits.

1. Fetch the verified remote and record full base/candidate SHAs. Check failures explicitly. An unavailable ref is unknown, not an empty branch.
2. Create a fresh disposable worktree at the current base with a unique temporary branch. Use `git worktree add -b`, never `-B` on an existing branch. Preserve other writers' worktrees and refs.
3. Attempt a no-commit integration of the candidate in that worktree. If conflicts occur, record conflicting paths and requirements; abort only your own attempt. Do not automatically cherry-pick a whole history or resolve toward an outdated implementation.
4. Inspect the staged integration diff against the pinned base. `git diff --cached --quiet` exits 0 for empty, 1 for differences, and higher values for errors. Handle all three separately.
5. Classify:
   - **EMPTY:** this integration contributes no content change; no new implementation PR is needed on that evidence.
   - **NONEMPTY:** content remains to assess. Review requirements, regressions, deletions and tests before proposing it.
   - **CONFLICT:** requires contextual investigation; do not call it redundant or shippable.
   - **UNKNOWN:** missing refs, tool errors or incomplete evidence.
6. If useful work remains, create an owned review branch and run applicable tests/reviews. A nonempty diff is not permission to ship. Never force-push another contributor's branch to publish a trial integration.

Report repository, refs, classification, evidence, current applicability and owner/next action. Preserve ambiguous branches. Clean up only your own clean test worktree through `git worktree remove`; retain dirty evidence for review.
