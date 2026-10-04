---
name: code-review
description: Review code for bugs, security issues, and quality. Use when asked to review code or before creating a PR.
---

Perform a thorough code review of the changes in the current branch.

## Step 1 — Get the changes
```bash
git diff develop...HEAD
git diff --stat develop...HEAD
```

If there is no `develop` branch, use `main` or `master` as the base.

## Step 2 — Review checklist

### Security (CRITICAL — block PR if any found)
- [ ] No hardcoded secrets, tokens, or credentials in code
- [ ] No SQL string interpolation (use parameterized queries / ORM)
- [ ] User input validated before processing
- [ ] Authentication/authorization enforced on protected routes
- [ ] No sensitive data exposed in API responses (passwords, tokens)
- [ ] No `console.log` / `print` of sensitive data

### Architecture & Patterns
- [ ] Code follows the project's existing conventions (check CLAUDE.md)
- [ ] Business logic separated from HTTP/presentation layer
- [ ] No circular dependencies introduced
- [ ] Functions do one thing (single responsibility)

### Code Quality
- [ ] Functions < 50 lines
- [ ] No duplicated logic (DRY)
- [ ] Meaningful variable and function names
- [ ] No commented-out code left behind
- [ ] Proper error handling (no silent failures, no bare `catch` / `except`)
- [ ] No unnecessary `any` types (TypeScript projects)

### Tests
- [ ] New features have tests
- [ ] Bug fixes have regression tests
- [ ] Happy path + main error cases covered

### Performance
- [ ] No obvious N+1 queries
- [ ] No blocking operations in async contexts
- [ ] Large lists paginated, not fetched all at once

## Step 3 — Report

Format your review as:

**BLOCKING** — Must fix before merge:
- [issue] in `file:line`

**IMPORTANT** — Should fix:
- [issue] in `file:line`

**SUGGESTIONS** — Nice to have:
- [suggestion]

**GOOD** — What was done well

$ARGUMENTS
