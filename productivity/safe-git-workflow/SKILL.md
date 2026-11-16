---
name: safe-git-workflow
description: Perform Git operations while preserving user work and avoiding accidental publication or history loss. Use for branch, staging, commit, rebase, merge, or push tasks.
---

# Safe Git Workflow

1. Inspect `git status`, branch, upstream, remotes, staged and unstaged diffs, and untracked files before acting.
2. Read project instructions and identify the intended base/target branch.
3. Stage explicit paths where practical; inspect the staged diff before committing.
4. Preserve unrelated changes. Never use destructive cleanup commands as a shortcut.
5. Before rebase, reset, force-push, branch deletion, or history rewrite, explain the effect and obtain explicit authorization if not already granted.
6. Before push or opening a PR, confirm the target repository, branch, visibility, and intended content.
7. After the operation, inspect status, commit contents, and remote state if a network action occurred.

Do not commit secrets, local configuration, generated clutter, or personal files. Never claim a push or merge succeeded without observing the host result. When a conflict occurs, resolve only the intended files and rerun relevant checks.
