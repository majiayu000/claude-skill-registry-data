---
name: review
description: "Review code changes for quality, security, and correctness"
---

# /review — Code Review

## When to use
When the user runs /review or asks to review changes/PR.

## Steps

1. Identify what to review:
   - If a PR number is given: `gh pr diff <number>`
   - Otherwise: `git diff` for unstaged, `git diff --staged` for staged
2. Read each changed file fully for context
3. Check for:
   - **Security**: injection, XSS, hardcoded secrets, OWASP top 10
   - **Correctness**: edge cases, off-by-one, null handling, race conditions
   - **Quality**: naming, complexity, duplication, dead code
   - **Performance**: N+1 queries, unnecessary allocations, missing indexes
   - **Tests**: adequate coverage, meaningful assertions
4. Report findings grouped by severity:
   - CRITICAL: security issues, data loss risks
   - WARNING: bugs, correctness issues
   - SUGGESTION: style, refactoring opportunities

## Rules
- Be specific: reference file:line
- Suggest fixes, don't just point out problems
- Acknowledge what's done well
- Don't nitpick formatting if a linter is configured
