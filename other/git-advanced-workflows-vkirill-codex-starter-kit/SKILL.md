---
name: git-advanced-workflows
description: Master advanced Git workflows including rebasing, cherry-picking, bisect, worktrees, and reflog to maintain clean history and recover from any situation. Use when managing complex Git
  histories, collaborating on feature branches, or troubleshooting repository issues.
tags:
  - git
---

# Git Advanced Workflows

## Use this skill when

- Cleaning up commit history before merging
- Applying specific commits across branches
- Finding commits that introduced bugs
- Working on multiple features simultaneously
- Recovering from Git mistakes or lost commits
- Managing complex branch workflows
- Preparing clean PRs for review
- Synchronizing diverged branches

## Do not use this skill when

- The task requires only basic Git operations (commit, push, pull, clone)
- You need Git hosting platform features (GitHub PRs, Actions) — use `github-actions-templates`

## Instructions

1. Clarify goals, constraints, and required inputs.
2. Apply relevant best practices and validate outcomes.
3. Provide actionable steps and verification.

## Capabilities

### Interactive Rebase

Interactive rebase (`git rebase -i`) is the primary tool for editing commit history. It opens an editor listing commits with actions per line:

- `pick` — keep commit as-is
- `reword` — change only the commit message
- `edit` — stop to amend commit content
- `squash` — combine with previous commit, merge messages
- `fixup` — like squash but discard the fixup commit message
- `drop` — remove commit entirely

Rebase scope can target: last N commits (`HEAD~N`), all commits on the branch (`git merge-base HEAD main`), or up to a specific commit hash. After rebase, force-push with `--force-with-lease` to prevent overwriting teammates' work.

Autosquash workflow: use `git commit --fixup <hash>` for incremental fixes, then `git rebase -i --autosquash main` to automatically order and mark fixup commits.

Splitting a commit: mark it `edit` in the rebase plan, then `git reset HEAD^` to unstage, commit logical chunks separately, and `git rebase --continue`.

### Cherry-Picking

Cherry-pick applies specific commits from one branch to another without merging the entire branch history. Useful for applying hotfixes to multiple release branches simultaneously.

A range of commits can be cherry-picked (exclusive start, inclusive end). The `-n` flag stages changes without committing, allowing manual review. The `-e` flag opens the editor to modify the commit message. Conflicts are resolved like merge conflicts; continue with `git cherry-pick --continue` or abort with `git cherry-pick --abort`.

Partial cherry-pick (specific files only): check out specific files from a commit with `git checkout <hash> -- path/to/file`, then commit manually.

### Git Bisect

Bisect performs a binary search through commit history to find the exact commit that introduced a bug. The workflow is: start bisect, mark current HEAD as bad, mark a known-good commit, test the commit Git checks out, mark it good or bad, and repeat until Git identifies the culprit.

Automated bisect uses a test script that exits 0 for good commits and non-zero for bad ones. Git runs the script automatically at each bisection point. Always run `git bisect reset` when done to return to the original branch.

### Worktrees

Worktrees allow simultaneous work on multiple branches in separate directories without stashing or switching. Each worktree shares the same object store but has its own working tree and `HEAD`.

Use cases: urgent hotfix while feature work is in progress, comparing two branches side-by-side, running tests on a different branch without disrupting current work. Stale worktrees (directory deleted without `git worktree remove`) accumulate and should be pruned with `git worktree prune`.

### Reflog

The reflog is a local safety net that records every ref movement — including commits from deleted branches and state before hard resets. Reflog entries are retained for 90 days by default.

Recovery workflow: view `git reflog` to find the hash of the lost commit or branch tip, then create a new branch pointing to that hash. Works for: accidentally deleted branches, commits lost after `git reset --hard`, detached HEAD states.

### Rebase vs Merge Decision

**Rebase** is appropriate for: cleaning up local commits before pushing, keeping a feature branch up-to-date with main (linear history), preparing a clean PR. Only rebase commits that have not been pushed and shared.

**Merge** is appropriate for: integrating completed features into main, preserving the exact collaboration history of a shared branch, public branches used by others.

Conflict resolution during rebase: after fixing conflicts, `git add` the files and `git rebase --continue`. If rebase is too complex, `git rebase --abort` returns to the pre-rebase state.

## Behavioral Traits

- Always uses `--force-with-lease` instead of `--force` for force pushes
- Creates a backup branch before any complex rebase (`git branch backup-branch`)
- Rebases only local commits — never rewrites shared history
- Tests after rebase to confirm history rewrite did not break functionality
- Uses descriptive, atomic commit messages — one logical change per commit
- Cleans up worktrees when done to free disk space

## Knowledge Base

- Interactive rebase actions: pick, reword, edit, squash, fixup, drop, exec
- `--force-with-lease` verifies the remote ref matches expectation before pushing
- Reflog retention: 90 days for reachable objects, 30 days for unreachable
- Cherry-pick creates a new commit with a different SHA even if the diff is identical
- Worktrees cannot check out the same branch that another worktree already has checked out
- Autosquash requires `git rebase -i --autosquash` and commits named `fixup! <original message>`
- Bisect exit codes: 0 = good, 1–127 (except 125) = bad, 125 = skip this commit

## Common Pitfalls

- Rebasing public branches causes history conflicts for collaborators
- Force pushing without `--lease` can overwrite a teammate's push
- Losing work during rebase by not resolving conflicts carefully
- Forgetting worktree cleanup — orphaned worktrees consume disk space
- Not backing up before a complex operation
- Running bisect with a dirty working directory — commit or stash first

## Reference Files
