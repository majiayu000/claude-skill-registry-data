---
name: code-review
description: Use this skill for code review and PR review tasks. Covers review methodology, what to flag, what to skip, and output structure.
---

# Code Review

Review a GitHub pull request for substantive issues. Focus on what matters, skip what doesn't.

## Steps

1. Run `gh pr view {pr_number} --json title,body,files` to understand the PR's purpose and scope.
2. Run `gh pr diff {pr_number}` to read the full diff.
3. Before commenting, read surrounding code to understand full context — a pattern that looks wrong in isolation may be an established convention.

## Focus Areas (priority order)

1. **Correctness** — Logic bugs, edge cases, error handling
2. **Security** — Input validation, injection risks, secrets exposure
3. **Reliability** — Race conditions, failure modes, resource leaks
4. **Performance** — Inefficient algorithms, N+1 queries, unnecessary work
5. **Breaking changes** — API/behavior changes affecting callers
6. **Test coverage** — Are new code paths tested?

Skip style/formatting unless it materially impacts readability. Do not nitpick naming, style preferences, or issues linters catch.

## Severity Levels

- **Blocking**: Must fix before merge (bugs, security, significant reliability/performance issues, breaking changes)
- **Non-blocking**: Suggestions for improvement (optional)

## Output Format

### Findings

For each issue found:

#### [Issue Title]

- **Severity**: blocking | non-blocking
- **Location**: `file_path:line_number`
- **Description**: What the issue is and why it matters
- **Suggested Fix**: Concrete code change or approach

If no issues found, state that the changes look correct and explain why.

### Summary

Overall assessment: is the PR ready to merge, or does it need changes? List the most important issues if any.
