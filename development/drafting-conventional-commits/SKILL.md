---
name: drafting-conventional-commits
description: "Draft a Conventional Commits message from either a short summary of changes or by inspecting the local git diff. Use when the user wants a commit message formatted as type(scope): subject, with optional body and footers for breaking changes or issue references."
---

# Conventional Commit Drafter

## Overview

Turn a short change summary into a Conventional Commits message. If the user asks you to infer changes, inspect the local git diff. Ask only for missing essentials like type, scope, or breaking change details.

## Workflow

1. If the user provides a summary, read it. If they ask you to check changes, inspect `git status -sb` and `git diff --stat`, then open specific diffs as needed.
2. Infer a commit type.
3. Identify an optional scope (subsystem, module, or area). Omit if unclear.
4. Draft a concise subject in imperative mood, lower-case, no trailing period.
5. Include a brief body that explains the reason for the change (why, not how). If the reason is not clear from the summary or diff, ask the user for it.
6. Add footers for breaking changes or issue references.

## Conventional Commits Rules

- **Format:** `type(scope): subject`
- **Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- **Subject:** imperative, lower-case, no period, <= 72 chars when possible
- **Breaking change:** add `!` after type/scope and include `BREAKING CHANGE: <details>` footer
- **Issue refs:** include `Refs: #123` or `Closes: #123` footer when provided

## Type Selection Heuristics

- New user-facing behavior: `feat`
- Bug fix: `fix`
- Docs only: `docs`
- Formatting (no behavior change): `style`
- Refactor without behavior change: `refactor`
- Performance improvement: `perf`
- Tests only: `test`
- Build system/deps: `build`
- CI config/pipeline: `ci`
- Maintenance chores: `chore`
- Revert of a prior commit: `revert`

## Output

Return only the commit message, with no extra commentary. If you need the reason for the change, ask a short follow-up question instead of returning a commit message.

## Examples

Input summary: "add pagination to the invoices list"
Output:
```
feat(invoices): add pagination to list
```

Input summary: "fix crash when opening empty cart; breaking API change: remove legacy cart token"
Output:
```
fix(cart)!: prevent crash on empty cart

BREAKING CHANGE: remove legacy cart token
```

Input summary: "update readme with setup steps"
Output:
```
docs(readme): add setup steps
```
