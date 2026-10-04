---
name: branches-cleanup
description: Automatically clean up local git branches that have been merged into the base branch
disable-model-invocation: true
allowed-tools: Bash(git *)
---

# Cleanup Merged Branches

Automatically clean up local git branches that have been merged into the base branch.

## Instructions

When this skill is invoked manually, clean up merged branches:

1. Run `git branch --merged <base-branch>` to find branches merged into the base branch
2. Exclude protected branches: `develop`, `main`, `master`
3. For each merged branch found, delete the local branch with `git branch -d <branch>`
4. Report what was cleaned up

## Protected Branches (NEVER delete)
- `develop`
- `main`
- `master`

## Automation

This skill automatically runs after `git pull` via the PostToolUse hook in `.claude/settings.json`.
