---
name: branch-hygiene
description: Keep Git branches and worktrees understandable and safe by maintaining clear base/upstream relationships, bounded purpose, current integration state, clean ownership, and deliberate cleanup.
---
# Branch Hygiene

Use when creating, inspecting, updating, or cleaning branches/worktrees during collaborative or multi-agent development.

## Procedure
1. Identify the repository's branching convention and the exact base/upstream before creating or moving a branch. Do not assume `main`, `master`, or origin are the correct targets.
2. Give each branch a bounded purpose that can be described independently. Avoid using one long-lived branch as a dumping ground for unrelated work unless the repository intentionally follows that model.
3. Record/inspect upstream tracking and divergence. Know whether local history is ahead, behind, or has diverged before pulling, rebasing, merging, or pushing.
4. Keep worktrees and branches paired deliberately in multi-agent work. Verify which worktree owns which branch and do not delete or reuse a branch still checked out or containing unintegrated work.
5. Incorporate base changes using the repository's accepted strategy. Rebase for a clean unpublished/authorized series or merge when history/shared-branch policy requires it; do not rewrite shared history casually.
6. Before switching, deleting, resetting, or cleaning, inspect uncommitted/untracked state and commits not reachable from a safe reference. Preserve recoverable work before destructive operations.
7. Remove merged/obsolete branches and worktrees when their purpose is complete and recovery is no longer needed, but verify the integration target actually contains the intended commits first.
8. Keep temporary experiment branches distinguishable from deliverable branches and avoid publishing them as canonical work without review.
9. When automations/agents create branches, use deterministic collision-resistant naming appropriate to the project and report the exact branch/commit used in handoffs.

## Decision rules
- A branch name is coordination metadata; it should help a human understand ownership/purpose.
- Divergence must be inspected before choosing pull/rebase/merge behavior.
- Never delete a branch simply because its PR is closed without verifying whether its commits are integrated or intentionally abandoned.
- Worktree cleanup should not become source-code cleanup.
- Shared branch policy and repository protection rules override personal preference.

## Quality gate
Branch state is healthy when purpose and upstream/base are clear, divergence is understood, no work is stranded in disposable branches/worktrees, history changes respect collaboration policy, obsolete references are removed only after verification, and another contributor can tell where active work belongs.