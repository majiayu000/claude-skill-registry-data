---
description: Review changes for architecture violations, clean code, and security
argument-hint: "[staged | branch | path]"
allowed-tools: "Read, Glob, Grep, Bash(git diff:*), Bash(git log:*), Task"
---

# Code Review

## Context

!`git status --short`
!`git diff --stat`
!`git diff --cached --stat`

## Scope

- `staged` → `git diff --cached`
- `branch` → `git diff main...HEAD`
- a path → read the file directly
- empty → whichever of staged / unstaged / branch diff has content

## Instructions

Delegate to the **`clean-code-reviewer`** agent with the scope above. It holds the review criteria and reads `.claude/rules/*` itself — do not restate the criteria here.

For a diff touching **module boundaries** (a new module, a moved class, a cross-module import, a changed Facade signature), also delegate to **`hexagonal-architect`** and merge both reports.

## Before reporting

Verify each finding against the actual file — a diff hunk lacks the surrounding context that decides whether something is really wrong. Drop anything you cannot confirm.

## Output

Merge into one list, most severe first:

```
**[SEVERITY]** file:line — Category
What's wrong. What to do instead.
```

**CRITICAL** (security, data loss, broken behavior) · **MAJOR** (architecture violation, real smell) · **MINOR** · **SUGGESTION**

End with: verdict (**approve** / **request changes**), counts by severity, and the top items to fix first.
