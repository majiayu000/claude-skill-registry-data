---
name: git-workflow
description: Use when committing work, creating branches, preparing PRs, resolving merge conflicts, when grouping related changes into commits, when cleaning up history before merging, or when deciding what should be a separate commit vs squashed.
---

# Git Workflow

## Overview

Each commit is an atomic, independently-revertable unit of work. Commit messages explain WHY, not WHAT (the diff shows what). Branch names reference task IDs. PRs link to the originating task and contract.

## When to Use

- Committing completed work from `incremental-implementation`
- Creating a branch for a new task
- Preparing a PR for review
- Resolving merge conflicts

## When NOT to Use

- You're in the middle of implementing — finish the task first, then commit
- Exploratory work not yet at a stable state — use `git stash` or a WIP commit

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "I'll squash it all at the end" | Squashing discards the incremental story — keep atomic commits |
| "The commit message can be 'fix'" | Future you and your teammates need to know WHY |
| "I'll just force push to clean up" | Force push rewrites shared history — never on shared branches |
| "One big commit is fine for a small change" | Small changes are the easiest place to practice atomic commits |

## Red Flags

- Commit touches files from more than one task
- Commit message describes the diff ("update user.ts") not the reason ("guard against null session on logout")
- Unrelated test fixes bundled with a feature commit
- Merge conflict resolved by accepting one side wholesale without reading both

## Core Process

### Branch naming

```
feat/T001-user-registration
fix/T023-null-session-logout
chore/update-dependencies
```

### Commit format

```
[T001] Implement user registration

Guard against duplicate email on create — UserService.create() now returns
DuplicateEmailError instead of throwing, matching the contract invariant.

Closes: T001
```

- First line: `[TASK-ID] imperative verb + what changed` (≤72 chars)
- Body: WHY this change was needed, not what the diff shows
- Footer: task reference

### Before committing

- [ ] Only files from the current task are staged
- [ ] `git diff --staged` reviewed — no debug logs, no TODO left in
- [ ] Tests pass: `<run test command>`
- [ ] Build passes: `<run build command>`

### PR checklist

- [ ] PR title matches the task title
- [ ] PR description links to task ID and to the relevant `.forge/contracts/` file
- [ ] "What changed and why" section in PR body — not just the task title
- [ ] No unresolved review comments before merge
- [ ] Merge strategy: squash only if commits are truly WIP; prefer merge commit to preserve atomic history

## Verification

- [ ] Each commit is independently revertable
- [ ] Commit messages explain WHY, not WHAT
- [ ] No debug artifacts committed (console.log, TODO, commented-out code)
- [ ] Branch references task ID
- [ ] PR links to task and contract
