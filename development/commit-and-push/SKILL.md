---
name: commit-and-push
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git push:*), Bash(gh pr create:*)
description: Create a git commit and push
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

1. Analyze the diff in depth - understand what changed and why
2. Create a single commit with a clear, descriptive message
3. Push to origin
4. If on a feature branch: create a PR using `gh pr create`
5. If on main: just push (no PR needed)
