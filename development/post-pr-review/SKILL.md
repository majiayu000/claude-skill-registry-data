---
name: post-pr-review
description: Self-review and fix PR issues after creating a PR. Use after PR creation, when user says "PRレビュー", "セルフレビュー", "PR修正", or "review my PR". Runs pr-review-toolkit and fixes critical/important issues and suggestions.
---

# Post-PR Review

## Workflow

After PR creation, execute this workflow:

### 1. Run PR Review

Execute `/pr-review-toolkit:review-pr` to analyze the PR.

### 2. Fix Issues by Priority

Fix in this order:

1. **Critical Issues** - Must fix immediately (security, bugs, breaking changes)
2. **Important Issues** - Should fix (code quality, performance)
3. **Suggestions** - Nice to have (style, minor improvements)

### 3. Commit and Push Fixes

After fixing each category, commit with a descriptive message that reflects the actual changes:

```bash
git add -A && git commit -m "fix: <describe what was fixed>"
git push
```

Use appropriate commit message based on fix type:
- `fix: resolve null safety issue in XxxAnalyzer`
- `fix: add missing error handling for API calls`
- `refactor: simplify validation logic per review feedback`

### 4. Re-run Review (Optional)

If significant changes were made, re-run `/pr-review-toolkit:review-pr` to verify.

## Issue Categories

| Category | Action | Examples |
|----------|--------|----------|
| Critical | Must fix | Security vulnerabilities, data loss risks, breaking changes |
| Important | Should fix | Missing error handling, performance issues, code smells |
| Suggestions | Consider | Naming improvements, documentation, minor refactors |

## Notes

- Always run code-quality checks after fixes: `composer format:fix && composer analyze && composer test`
- If CI fails after push, check GitHub Actions status with `gh pr checks`
