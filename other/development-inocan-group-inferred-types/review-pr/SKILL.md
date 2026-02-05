---
name: review-pr
description: Review pull requests using GitHub CLI. Invoke with /review-pr <pr-number-or-url>
allowed-tools: Read, Grep, Glob, Bash(gh pr:*), Bash(gh api:*), Bash(git diff:*), Bash(git show:*), Bash(git log:*)
---

# PR Review

Review the specified pull request thoroughly.

## Arguments

- `$ARGUMENTS` - PR number (e.g., `123`) or full URL (e.g., `https://github.com/org/repo/pull/123`)

## Process

1. **Fetch PR metadata** - Get title, description, author, base/head branches
2. **Get the diff** - Review all changed files
3. **Read full context** - For complex changes, read the complete files to understand surrounding code
4. **Check against project standards** - Reference CLAUDE.md and existing patterns

## Review Criteria

- **Correctness** - Does the code do what it claims?
- **Security** - Any vulnerabilities (injection, XSS, auth issues)?
- **Tests** - Are changes adequately tested?
- **Style** - Follows project conventions?
- **Complexity** - Is it overengineered or too clever?

## Output Format

Provide a structured review:

```
## Summary
One-line assessment (approve/request changes/needs discussion)

## Changes Overview
Brief description of what the PR does

## Feedback
### Issues (must fix)
- ...

### Suggestions (nice to have)
- ...

### Questions
- ...

## Files Reviewed
- path/to/file.py - brief note
```
