---
name: git
description: Use git effectively — commits, branches, rebases, merges, conflict resolution, history surgery, and common workflows.
category: development
aliases:
- version-control
- source-control
- vcs
triggers:
- git help
- how do I use git
- help me commit
- resolve this merge conflict
- git rebase
- git workflow
- undo this commit
keywords:
- git
- commit
- branch
- merge
- rebase
- conflict
- stash
- log
- diff
dependencies:
- git
risk: medium
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- branch
- commit
- development
- git
- merge
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Git

## Purpose

Help the user with git: commits, branching strategies, history, conflict resolution, and
recovery from mistakes.

## When to Use

- User asks for git help
- User is resolving a merge conflict
- User wants to set up a branching strategy
- User needs to recover from a bad state

## When NOT to Use

- The user wants PR / issue workflow help (route to `github`)
- The user wants code review feedback (route to `code-review`)

## Capabilities

- Commit, branch, merge, rebase
- Resolve conflicts
- Reflog and recovery
- Submodules, worktrees
- Bisect to locate a regression
- Common workflows (GitFlow, trunk-based, GitHub Flow)

## Inputs

- Current state (`git status`, branch, log)
- Goal (merge, rebase, recover, etc.)

## Safety

- Warn before destructive operations (`--force`, `reset --hard`)
- Suggest backups before surgery (`git tag backup-before-fix`)
- Never `push --force` to shared branches without confirmation

## Source

Custom skill, written for this library.

## Notes

Pairs with:
- `github` (PR / issue flow)
- `code-review` (reviewing diffs)

## Workflow

1. Confirm the goal, scope, and constraints.
2. Inspect the available context before acting.
3. Apply the skill-specific guidance in this document.
4. Verify the result and report limitations or next steps.

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "git help"; "how do I use git"; "help me commit".
