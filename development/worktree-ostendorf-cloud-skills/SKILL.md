---
name: worktree
description: "Creates a git worktree under .claude/worktrees/<branch> for a parallel session, and removes it once its branch is merged. Use when starting a session that must not disturb an already checked out branch, or cleaning up after one."
---

# Worktree

One checkout, one session, without disturbing a branch another session already has open.

## When to use

- Starting a session that needs its own checkout alongside an existing one.
- A branch merged and its worktree is no longer needed.
- The worktree list has grown and needs pruning.
- An investigation or a reproduction needs a checkout to build or run in, with no branch and no
  pull request of its own.

## Steps

1. Check `.gitignore` for a `.claude/worktrees/` entry. Add it when missing.
2. Branch off the base from config `pr.base`, else the repository default branch:
   `git worktree add --no-track .claude/worktrees/<branch> -b <branch> <base>`. Without
   `--no-track` the upstream write to `.git/config` can fail in a sandbox, after the branch exists
   and before the worktree does. Clear that state with `git worktree prune`, then
   `git branch -D <branch>`, then add again.
3. Install dependencies inside the new worktree when a lock file exists there.
4. Run every command for that session from inside `.claude/worktrees/<branch>`, never from the
   original checkout.
5. Once the branch's pull request merges: `git worktree remove .claude/worktrees/<branch>`, then
   `git branch -d <branch>`, then `git worktree prune`. A worktree lives as long as its pull
   request. A `could not lock config file .git/config` message on the remove is harmless once
   `git worktree list` no longer shows the path. Prune afterwards.
6. List existing worktrees with `git worktree list` and prune one left behind by a merged or
   abandoned branch. A session that ends checks for its own stale worktrees first.

## Investigation worktrees

- A reproduction or an investigation with no branch and no pull request gets a detached
  worktree instead: `git worktree add --detach <path> <base>`, outside every repository under
  the session's scratch directory, never under `.claude/worktrees/`.
- It carries no branch and is never pushed. Nothing written there is committed from the parent
  checkout.
- Remove it with `git worktree remove <path>` in the same task that created it.

## Guardrails

- One branch, one worktree, one session. Never point two sessions at the same worktree.
- Before dispatching an agent into an existing worktree, check the agent list or the task list
  for another running agent on it.
- No status update proves an agent has stopped, a completion notice for one turn included. The
  same agent can be resumed and keep working in the same worktree. It holds the worktree until
  its termination is confirmed.
- Never remove a worktree whose branch still has unmerged work without checking first.
- A commit, amend, rebase or cherry-pick in a worktree follows the same identity rule: no
  `GIT_CONFIG_GLOBAL=/dev/null` without `GIT_COMMITTER_EMAIL` in the same command. See
  `git-conventions`.
- `.claude/worktrees/` stays in `.gitignore`. Never commit a worktree's contents from the parent
  checkout.
- A detached investigation worktree lives outside the repository and outside `.claude/worktrees/`,
  carries no branch, and is removed before the task ends.

## Config

- `pr.base`: base branch for the new worktree. Default: the repository default branch.

## References

- `git-conventions` for the branch naming and history rules a worktree's branch still follows.
