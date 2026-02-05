---
name: reviewing-prs
description: Use when the user wants to read, analyze, or respond to GitHub pull request reviews and comments
---

# Reviewing PRs

Help users read and respond to GitHub pull request reviews and comments using the `gh` CLI.

## Core Capabilities

1. **Fetch PR review data** - Get reviews, review comments, and issue comments
2. **Parse and present** - Display in a clear, organized format
3. **Respond to feedback** - Help draft responses or make requested changes

## Workflow

### 1. Identify the PR

Ask for or detect:
- PR number (e.g., `123`)
- Repository (use current repo if in git directory)
- Can accept URL: `https://github.com/owner/repo/pull/123`

### 2. Fetch Data

Use @commands.md for detailed command reference. Quick summary:

**Get high-level overview:**
```bash
gh pr view <number> --json reviews,comments,latestReviews,reviewRequests,title,body,author,state
```

**Get detailed review comments (inline code comments):**
```bash
gh api repos/{owner}/{repo}/pulls/{pull_number}/comments
```

**Get issue comments (general PR discussion):**
```bash
gh api repos/{owner}/{repo}/issues/{issue_number}/comments
```

### 3. Present Data

Organize by:
1. **Review Summary** - Overall state (approved/changes requested/commented)
2. **Review Comments** - Group by file, show code context with diff_hunk
3. **Issue Comments** - Chronological discussion thread

See @examples.md for output formatting examples.

### 4. Help Respond

**For review comments:**
- Suggest code changes addressing feedback
- Draft reply comments: `gh pr comment <number> --body "..."`

**For overall review:**
- Help implement requested changes
- Draft response review: `gh pr review <number> --comment --body "..."`

## Key Data Structures

See @commands.md for complete field reference.

**Review**: Has `state` (APPROVED/CHANGES_REQUESTED/COMMENTED), `body`, `user`
**Review Comment**: Has `path`, `line`, `diff_hunk`, `body` - tied to specific code
**Issue Comment**: Has `body`, `user`, `created_at` - general discussion

## Important Notes

- Review comments are inline (tied to code lines)
- Issue comments are general (PR thread discussion)
- A review can have both a state and review comments
- Use `gh pr view --comments` for quick read, but API endpoints give more detail
