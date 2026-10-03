---
name: ls-git-workflows
description: "Advanced git operations beyond add/commit/push. Use when rebasing, bisecting bugs, using worktrees for parallel development, recovering with reflog, managing subtrees/submodules, resolving merge conflicts, cherry-picking across branches, or working with monorepos."
metadata:
  version: "1.3"
compatibility: "Requires git (Linux, macOS, Windows)."
---

# Git Workflows

Use this skill for advanced Git operations that can rewrite history, move work
between branches, recover lost commits, or manage large and multi-repository
codebases. Keep this file as the activation and safety workflow; open the
references only for the procedure you need.

## When to Use

- Cleaning up commit history before merging.
- Finding which commit introduced a bug.
- Working on multiple branches at the same time.
- Recovering lost commits, dropped stashes, or mistaken resets.
- Cherry-picking commits across branches or forks.
- Managing subtrees, submodules, or sparse checkouts.
- Resolving complex merge or rebase conflicts.
- Inspecting history with blame, pickaxe, or file-following log commands.

## Safety Workflow

1. Inspect the repository before changing it:

```bash
git status --short --branch
git remote -v
git branch --show-current
```

2. Identify whether the target branch is shared. Do not rebase, amend, reset, or
   force-push shared history unless the user explicitly asks for that operation.
3. Preserve unrelated work. If the worktree is dirty, only stage or modify files
   that belong to the task.
4. Before **every** `git reset --hard`, require a clean worktree. Preserve desired
   staged, unstaged, and relevant untracked work first with an approved WIP
   commit, patch, stash (use `-u` when needed), or separate worktree. A backup
   branch or tag preserves only commits; it does not preserve uncommitted work.

```bash
git status --short
git stash push -u -m "WIP before recovery"
git branch backup/before-recovery
```

5. Prefer non-interactive commands when automating. Use interactive rebase only
   when the user can review the intended commit list or the change is clearly
   local and scoped.
6. After each operation, re-check status and confirm the branch, staged files,
   and diff match the requested outcome.

## Rule ownership

This skill owns advanced Git operations and traceability behavior. `GIT_TRACEABILITY.md` is the public reference; use this skill for branch, history, worktree, release-tag, and checkpoint decisions.

- Preserve unrelated dirty-tree work.
- Record commit hashes or branch names when a decision depends on a past state.
- Use `ls-unfuck-my-git-state` for broken worktree/index/ref symptoms instead of improvising repair steps here.

## Workflow Router

Open the matching reference and follow only that recipe:

- [Rebase and bisect](references/rebase-and-bisect.md) - interactive rebase,
  autosquash, abort/continue flows, manual bisect, automated bisect, and skipped
  build failures.
- [Worktrees, recovery, and history](references/worktrees-recovery-and-history.md)
  - worktree setup, reflog recovery, cherry-pick, stash patterns, blame, and log
  archaeology.
- [Repository structure and conflicts](references/repo-structure-and-conflicts.md)
  - subtree, submodule, sparse checkout, merge conflict resolution, rebase
  conflicts, and rerere.
- [Tags, releases, and tips](references/tags-releases-and-tips.md) - tag
  commands, release tag handling, and compact advanced Git tips.

## Quick Triage

Use these read-only commands before selecting a recipe:

```bash
git log --oneline --decorate --graph -20
git diff --stat
git diff --cached --stat
git reflog --date=relative -20
```

For branch divergence:

```bash
git fetch --all --prune
git status --short --branch
git log --oneline --left-right --cherry-pick HEAD...@{upstream}
```

If an operation is already in progress, inspect Git's state before continuing:

```bash
git status
git rebase --show-current-patch
git diff --cc
```

## Completion Checks

- `git status --short --branch` shows the expected branch and worktree state.
- `git diff --stat` and `git diff --cached --stat` match the task scope.
- Any rewritten or moved commits were verified with `git log --oneline --graph`.
- Recovery work leaves a named branch or clear reflog handle for rollback when
  the operation could discard reachable work.
