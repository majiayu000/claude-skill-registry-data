---
name: git-branching
description: "Branching strategy and lifecycle: GitHub Flow default, trunk-based criteria, release branches, worktrees, PR preparation."
---

# git-branching

One feature, one branch, one short life. Strategy follows release reality, not habit.
## Inspection

Check team size, release cadence, parallel supported versions, and current branch lifetimes before prescribing a model.

## Decision rules

GitHub Flow default; trunk-based only with CI + flags; long-lived branches only for parallel releases; delete after merge.


## Activate when

- Choosing a branching model, managing branch lifecycle, working across parallel streams, preparing PRs.

## Do NOT activate for

- Daily commit/push mechanics (git-workflow) or releases (git-release).

## Procedure

1. Model: GitHub Flow default (short `feature/*` → PR → merge → deploy). Trunk-based only with strong CI + flags. Long-lived release branches only for parallel supported versions.
2. Lifecycle: branch from current main, keep alive for days not weeks, rebase or merge to stay current, delete after merge.
3. Parallel streams: one branch per worktree; worktrees share refs/stash; `git worktree prune` after manual deletions.
4. Wrong-branch commits: move with `checkout -b` + reset/cherry-pick (see git-recovery), don't drag unrelated work along.
5. PR prep: atomic commits, protection requirements checked, `gh` PR if available (see github/pr-workflow).
6. Verify: default branch deployable, stale branches pruned, protection active.

## Failure modes

GitFlow overhead for continuous-deploy SaaS; branches living for weeks; stale branches nobody owns; protection missing on main.

## Escalation

Daily mechanics → git/git-workflow; release branches → git/git-release.
