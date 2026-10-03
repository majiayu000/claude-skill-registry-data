---
name: pr-ready
description: Drive an existing pull request or merge request from current branch state to merge-ready by reconciling its base, CI/checks, review threads, requested changes, and revision-specific evidence without expanding feature scope.
---
# PR Ready

Use when a PR/MR already exists and the remaining job is to make that exact change mergeable.

## Procedure
1. Identify the repository, PR/MR, head branch, target base, current head SHA, required checks, and review policy from current forge/repository state.
2. Inspect the complete base-to-head diff and unresolved reviews before changing anything so the remaining work is understood as one revision, not isolated comments.
3. Refresh the target base according to repository policy. Rebase or merge only when appropriate, preserve intent during conflicts, and never rewrite shared history casually.
4. Re-run or inspect required CI/checks for the current head revision. Classify failures as branch-caused, base/upstream, flaky, environmental, or unrelated before editing code.
5. Address valid review findings with the smallest scoped change. For incorrect, stale, or already-resolved feedback, reply or resolve according to forge/repository policy rather than changing correct code to satisfy a stale comment.
6. Preserve author/contributor credit and unrelated branch work. Do not turn PR readiness into a refactor, redesign, or new feature pass.
7. Push changes safely, using force-with-lease only when authorized history rewriting actually requires it.
8. Re-query the forge after every material update. Do not assume a push made checks green or that a reply resolved a review thread.
9. If the PR premise is invalid or the change needs substantial replacement rather than readiness work, stop and hand off to contribution/code review rather than silently rebuilding it under the same scope.
10. Report the final head SHA, base, required-check state, unresolved/waived review state, and exact PR/MR reference.

## Decision rules
- Merge readiness is revision-specific; stale green checks are not evidence for a new head SHA.
- Fix failures caused by the PR, not unrelated repository problems unless separately assigned.
- An approved exception or intentionally deferred thread must be explicit; do not manufacture “all clear.”
- Repository policy determines merge/rebase/review mechanics, not this skill.

## Quality gate
The PR/MR is ready when the intended current revision is based appropriately, every required check is green or explicitly accepted by authorized policy, blocking review feedback is resolved or formally waived, the full diff still matches scope, and the forge confirms the exact head/base state being reported.