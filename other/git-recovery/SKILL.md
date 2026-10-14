---
name: git-recovery
description: "Recover lost work: reflog, deleted branches/commits, bad merge/rebase, corrupted tree, leaked secrets. Diagnose first, smallest safe recovery."
---

# git-recovery

Stop, diagnose, then recover with the least destructive tool that works.

## Activate when

- Lost commits, deleted branches, bad merge/rebase, corrupted working tree, accidental force-push, leaked secret.

## Do NOT activate for

- Planned history edits (git-rebase) or routine flows (git-workflow).

## Procedure

1. Freeze: stop new commits; capture `git status`, `git log --oneline -10`, `git reflog -20`, `git fsck --lost-found` output.
2. Choose the smallest tool: `git reset --keep`/`--merge` for index messes; `checkout -b` + cherry-pick from reflog for lost commits; reflog/brnach restore for deleted branches; `git revert` (never rewrite) for published bad changes.
3. Bad merge/rebase on shared history: revert, don't rewrite; coordinate before any history rewrite, then `--force-with-lease`.
4. Leaked secret: rotate immediately (deletion is not rotation), purge with filter-repo/BFG, force-push with team coordination.
5. Verify: recovered files diffed against expectation, tests run, team notified of any rewritten history.

## Failure modes

- Continuing to commit on top of the damage (freezes the evidence); `reset --hard` without a backup branch; force-pushing a recovery nobody reviewed; rotating a secret everywhere except the one place it matters.

## Escalation

- Secret exposure beyond one repo → incident process with owner; history shared across forks → coordinate publicly before rewriting.
