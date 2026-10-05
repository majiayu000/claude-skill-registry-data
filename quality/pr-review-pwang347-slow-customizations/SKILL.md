---
name: pr-review
description: Review a pull request for code quality, security, and standards. Use proactively after code changes or when asked to review a PR.
context: fork
agent: Explore
---

# PR Review

Review the current PR or the specified PR number: $ARGUMENTS

## Checklist

1. Run `git diff main...HEAD` to see changes
2. Check each changed file against [review-checklist.md](./review-checklist.md)
3. Look for security issues using [security-checks.md](./security-checks.md)
4. Summarize findings by priority: Critical / Warning / Suggestion
