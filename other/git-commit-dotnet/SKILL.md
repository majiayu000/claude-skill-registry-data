---
name: git-commit-dotnet
description: Generate a concise conventional commit message from the current diff and commit host repository changes.
engines: [AGNOSTIC]
---

## When to use
Use only when the user explicitly asks to commit changes.

## Commit style
Prefer:
- feat(scope): summary
- fix(scope): summary
- refactor(scope): summary
- docs(scope): summary
- test(scope): summary
- chore(scope): summary

## Command
../commands/git-commit.sh "<message>"
