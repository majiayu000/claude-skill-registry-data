---
name: stale-branch-audit
description: >
  Audit local + remote branches for staleness. Lists branches >30 days old,
  merged branches with no worktree, orphaned worktrees, and branches whose
  remote is gone. Prioritized cleanup output.

  Trigger this skill when:
  - User says "cleanup branches", "stale branch audit", "prune old branches", or
    invokes `/stale-branch-audit`.
  - Session lands in a repo with >20 local branches.
  - Before switching machines / migration.
---

## Behavior

Emit a **prioritized cleanup list** — grouped by how safe it is to delete.

### Group 1 — Safe to delete (auto-suggest, `git branch -D` OK)

- Merged to `main` / `dev` AND last commit >30 days ago AND no worktree pinning it.

Query:
```
git branch --merged dev | grep -v -E "(dev|main|master|\*)" | while read b; do
  age_days=$(( ($(date +%s) - $(git log -1 --format=%ct "$b")) / 86400 ))
  if [ "$age_days" -gt 30 ]; then echo "$b ($age_days days)"; fi
done
```

### Group 2 — Review before deleting

- Merged to `main` / `dev` AND last commit ≤30 days (recent merges you may still need locally).
- Unmerged local branches that match a closed/merged PR remotely (`gh pr list --state merged --head <branch>`).

### Group 3 — Do not delete without confirming

- Branches with unmerged commits AND no matching remote PR.
- Branches pinned by a worktree (`git worktree list` matches).
- Branches whose upstream remote is deleted (need `git fetch --prune` first).

## Output

```
=== <repo> ===

Group 1 (safe, N branches):
  fix/some-bug (42 days) — merged, no worktree
  chore/tooling-bump (58 days) — merged, no worktree

Group 2 (review, M branches):
  feat/half-done (12 days) — recently merged

Group 3 (keep, K branches):
  feat/wip-experiment (5 days) — 3 unmerged commits, no PR
  feat/user-mgmt (worktree at ~/wt/user-mgmt) — pinned

Cleanup suggestion:
  git branch -D fix/some-bug chore/tooling-bump
```

## Batch across repos

If user says "audit all repos", iterate the standard Nimbus locations:
```
~/Development/cidca/cidca-platform
~/Development/cidca/cidca-services
~/Development/horus/horus-v2
~/Development/zotea
```

Print one section per repo.

## Do not

- **Don't auto-delete anything.** This skill outputs the plan; the user runs the
  commands.
- Never touch `main`, `dev`, `master`, current branch, or the default branch of
  the remote.
- Don't include remote-only branches (`origin/*`) unless user explicitly asks
  — those are usually tracked by teammates.
- Don't invoke `worktree-cleanup` from here; hand off if a worktree is pinning
  a branch the user wants to remove.

## Freshness caveat

Run `git fetch --all --prune` before auditing to make sure "remote is gone"
signals are accurate. Skill offers to do this as step 0.
