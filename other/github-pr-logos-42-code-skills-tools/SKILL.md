---
name: "github-pr"
description: "Handle GitHub PR operations. Use for \"PR\", \"pull request\", \"review\" when repo is on github.com."
---

# GitHub PR Operations

## Platform Detection

Run `git remote -v` to verify this is GitHub (github.com):
- SSH format: `git@github.com:owner/repo.git`
- HTTPS format: `https://github.com/owner/repo.git`
- Extract: owner = `owner`, repository = `repo`

## Status Indicators

When listing or displaying PRs, use these status emojis based on PR state:

| Condition | Status |
|-----------|--------|
| Draft | 📝 Draft |
| Open | ✅ Open |
| Merged | 🔀 Merged |
| Closed | ❌ Closed |

**Note:** Use search filter `draft:false` to exclude drafts when listing.

## Output Format

Display PRs in a table with columns: `| # | Title | Author | Branch | Status | Updated |`

Example:
```
| 123 | Add authentication feature | alice | feature/auth | ✅ Open | 1/22/2026 |
| 122 | Update dependencies | bob | chore/deps | 📝 Draft | 1/20/2026 |
```

## PR Review

When reviewing a PR:
1. Fetch PR details and diff
2. Analyze for bugs, security issues, performance, and code quality
3. Present findings as: `## PR Review: #<NUM> - <TITLE>`
4. List issues with file references: `file_path:line_number`
5. Provide verdict: APPROVE, REQUEST_CHANGES, or COMMENT
6. Post comments/approve via MCP tools if requested

## Inline Review Comments

For multi-line inline comments:
1. Create pending review
2. Add inline comments to specific lines
3. Submit review with verdict
