---
name: merge
description: 'Absorb one or more feature branches into the base branch. Recommends merge vs rebase per branch. On conflict, aborts that branch + surfaces the file list + stops. Resolution out of scope; routes to the harness-named conflict-resolution agent or the user.'
tags: [merge, git, branch]
---

# merge — Branch Absorption

Absorb feature branches into the base branch. Per-branch rebase-vs-merge recommendation, mechanical execution. **Conflict resolution is NOT this skill's job** — abort, surface, stop.

## Branch Absorption Lane (load-bearing)

Branch integration is a topology operation on the commit graph. Route through the merge tool — `git merge`, this skill, or worker-direct-merge. File extension is not a routing signal; a docs-only branch is still branch integration.

### Pre-flight when integration is in scope

Triggers: branch named for absorption, current branch behind base, worker returned with branch unmerged.

1. `git branch --no-merged <base>` — list unmerged tips.
2. For any file slated for edit: `git log <base>..<branch> -- <path>`. Non-empty → merge lane.
3. To inspect merge state, materialize it: `git merge --no-commit --no-ff <branch>`, then `git merge --abort`. Read `git diff <base>..<branch>` for review only, never as input to a hand-applied edit across base.

## Conflict Doctrine (load-bearing)

When `git merge` or `git rebase` produces conflicts:

1. **Abort immediately** — `git merge --abort` (for merge) or `git rebase --abort` (for rebase). Restore the working tree.
2. **Surface, don't resolve.** Output the branch name, the conflict file list (`git diff --name-only --diff-filter=U` captured BEFORE abort), and which strategy hit the conflict.
3. **Stop the run.** Do not attempt resolution — resolution never runs inside this skill. The step-2 surface is the conflict scope. Route it: if the consuming repo's harness names a conflict-resolution agent (its CLAUDE.md or agent roster — e.g. a builder/implementer agent), offer dispatching that agent with the conflict scope as the recommended next step; otherwise the user resolves manually or re-dispatches with a different strategy.

This rule applies to every branch in the queue. If branch A conflicts, abort A, surface, then continue with branches B, C — they're independent attempts. Don't skip them silently.

## Protocol

### 1. Gather state (parallel)

- `git branch --show-current` — identify current branch
- `git status` — ensure working tree is clean (if dirty, abort the run, tell user to commit or stash)
- `git branch -v` — list all local branches with last commit
- `git log --oneline --graph --all --decorate -20` — visual overview

### 2. Identify target branches

- If user specified branches: use those
- If on a feature branch with no args: absorb current branch into base
- If on base branch with no args: list all feature branches with divergence info; ask user to clarify which to absorb

### 3. For each candidate branch, gather intel (parallel per branch)

- `git log --oneline {base}..{branch}` — commits ahead
- `git log --oneline {branch}..{base}` — commits behind (base moved since branch)
- `git diff --stat {base}...{branch}` — files changed
- Commit count

### 4. Recommend strategy per branch

| Condition                                | Strategy                                                    |
| ---------------------------------------- | ----------------------------------------------------------- |
| 1 commit, clean apply                    | **Rebase + fast-forward**                                   |
| 2-3 commits, single logical change       | **Rebase + fast-forward**                                   |
| Multi-commit, preserving context matters | **Merge --no-ff**                                           |
| Branch has been pushed/shared            | **Merge --no-ff** — don't rewrite shared history            |

Conflict probability is NOT a reason to pick merge over rebase — both surface and abort identically per the conflict doctrine.

Present recommendations as a table. Wait for user confirmation before executing.

### 5. Execute sequentially

Order matters — earlier merges can shift the base for later ones.

For each branch in confirmed order:

**Rebase strategy:**

```
git rebase {base} {branch}
git checkout {base}
git merge {branch} --ff-only
```

**Merge strategy:**

```
git checkout {base}
git merge {branch} --no-ff
```

**On conflict (either strategy):** apply the Conflict Doctrine above. Capture conflict files, abort, surface, continue with the next branch.

### 6. Per-branch post-absorption

For successfully absorbed branches:

- `git log --oneline -3` to confirm
- Note: do NOT delete the branch. Branch deletion is the user's call after testing.

### 7. Final summary

Report to user:

- Branches absorbed cleanly (with strategy used per branch)
- Branches that hit conflicts (with file lists — the conflict scope for resolution)
- Branches skipped and why
- Final `git log --oneline --graph -10`

### 8. Push (where a push surface exists)

Probe first, ask second — the probe is a fact the gateway reads itself. `git remote` prints nothing → no push surface: §7's report is the next and only output. A remote but no upstream for the base (`git rev-parse --abbrev-ref @{u}` errors) → say so in one line and ask once: **"Set upstream and push {base} (`git push -u <remote> {base}`)? (y / skip)"** — `<remote>` is the sole remote, or the one the user names when several exist. Remote + upstream → present base → remote, commits ahead of remote, which branches were folded in; ask **"Push {base} now? (y / skip)"**. Push on explicit yes only; skip on silence or decline. Never force. Branches that hit conflicts are not pushed. Same push-probe shape as the commit skill's § 6.

## Rules

- Run inline — no subagent dispatch.
- Push asks only where a push surface exists, and only on explicit confirmation — §8's probe decides whether the question fires; present what will push, never force, never unannounced.
- Never resolve conflicts inline. Surface and stop. (See Conflict Doctrine above.)
- Never force-merge.
- Never delete branches.
- Dirty working tree: surface to user; staging or stashing is the user's call.
- If on a detached HEAD: stop, surface to user.
- Process branches one at a time within a queue — independence not assumed across the queue.
