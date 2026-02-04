---
name: github
description: |
  Integrate with GitHub for issue tracking, pull requests, and repository operations.
  Use when asked about: github, gh, issues, pull requests, pr, create issue, my github issues,
  what issues are assigned to me, github repos, close issue, merge pr.
  Requires: GitHub CLI (gh) installed and authenticated via gh auth login.
---

# GitHub Integration

Integrate with GitHub for issues, pull requests, and repositories using the GitHub CLI.

## Quick Start

```bash
# Check prerequisites
python3 skills/github/scripts/check-prerequisites.py

# Query your open issues across all repos
python3 skills/github/scripts/query-issues.py --preset my-open

# Query issues you created
python3 skills/github/scripts/query-issues.py --preset created-by-me

# Query issues in a specific repo
python3 skills/github/scripts/query-issues.py --repo owner/repo --state open
```

## Prerequisites Check

Before any GitHub operation, verify prerequisites:

```bash
python3 skills/github/scripts/check-prerequisites.py
```

Or manually:

```bash
# 1. Check GitHub CLI installation
gh --version

# 2. Check authentication
gh auth status

# If not logged in: gh auth login
```

## Query Presets

Use presets for common queries:

```bash
python3 skills/github/scripts/query-issues.py --preset PRESET_NAME [--format table]
```

| Preset | Description |
|--------|-------------|
| `my-open` | Open issues assigned to me |
| `my-all` | All issues assigned to me |
| `created-by-me` | Issues I created |
| `mentioned` | Issues where I'm mentioned |
| `recent` | Recently updated issues (last 7 days) |
| `high-priority` | Issues labeled 'priority:high' or 'urgent' |
| `bugs` | Issues labeled 'bug' |
| `features` | Issues labeled 'enhancement' or 'feature' |

List all presets:
```bash
python3 skills/github/scripts/query-issues.py --list-presets
```

## Common Operations

### Issues

**Query issues (recommended - use presets):**
```bash
python3 skills/github/scripts/query-issues.py --preset my-open --format table
```

**Query issues in specific repo:**
```bash
python3 skills/github/scripts/query-issues.py --repo owner/repo --state open
```

**Get issue details:**
```bash
gh issue view 123 --repo owner/repo
```

**Create issue:**
```bash
gh issue create --repo owner/repo --title "Issue title" --body "Description" --label "bug"
```

**Close issue:**
```bash
gh issue close 123 --repo owner/repo
```

**Add comment:**
```bash
gh issue comment 123 --repo owner/repo --body "Comment text"
```

**Assign issue:**
```bash
gh issue edit 123 --repo owner/repo --add-assignee @me
```

### Pull Requests

**List PRs:**
```bash
gh pr list --repo owner/repo --state open
```

**View PR:**
```bash
gh pr view 123 --repo owner/repo
```

**Create PR:**
```bash
gh pr create --repo owner/repo --title "PR title" --body "Description"
```

**Merge PR:**
```bash
gh pr merge 123 --repo owner/repo --squash
```

**Review PR:**
```bash
gh pr review 123 --repo owner/repo --approve
gh pr review 123 --repo owner/repo --request-changes --body "Please fix..."
```

### Repositories

**List your repos:**
```bash
gh repo list --limit 50
```

**Clone repo:**
```bash
gh repo clone owner/repo
```

**View repo:**
```bash
gh repo view owner/repo
```

## Issue Reference Format

GitHub uses `#123` for issue references within a repo, or `owner/repo#123` for cross-repo references.

In commit messages:
```
Fix login bug #123
Closes #456
Fixes owner/repo#789
```

Keywords that auto-close issues: `close`, `closes`, `closed`, `fix`, `fixes`, `fixed`, `resolve`, `resolves`, `resolved`

## Labels

Common label conventions:

| Label | Purpose |
|-------|---------|
| `bug` | Something isn't working |
| `enhancement` | New feature or improvement |
| `documentation` | Documentation changes |
| `good first issue` | Good for newcomers |
| `help wanted` | Extra attention needed |
| `priority:high` | High priority |
| `priority:low` | Low priority |
| `wontfix` | Won't be worked on |

**Add label:**
```bash
gh issue edit 123 --repo owner/repo --add-label "bug,priority:high"
```

**Remove label:**
```bash
gh issue edit 123 --repo owner/repo --remove-label "wontfix"
```

## Milestones

Milestones group issues for releases or sprints:

**List milestones:**
```bash
gh api repos/owner/repo/milestones --jq '.[].title'
```

**Create milestone:**
```bash
gh api repos/owner/repo/milestones -f title="v1.0" -f due_on="2025-01-15T00:00:00Z"
```

**Assign issue to milestone:**
```bash
gh issue edit 123 --repo owner/repo --milestone "v1.0"
```

## Projects (Kanban Boards)

GitHub Projects provide kanban-style boards:

**List projects:**
```bash
gh project list --owner owner
```

**View project:**
```bash
gh project view PROJECT_NUMBER --owner owner
```

## WSR Integration

To include GitHub issues in weekly status reports, gather issues and format as WSR entries:

```bash
# Get issues closed this week
gh issue list --repo owner/repo --state closed --json number,title,closedAt,labels \
  --jq '[.[] | select(.closedAt > "2025-12-08")]'
```

Then import into WSR:
```json
{
  "entries": [{
    "title": "Fixed authentication bug",
    "status": "Completed",
    "work_items": [{
      "id": 123,
      "title": "Login fails with special characters",
      "type": "bug",
      "state": "closed",
      "url": "https://github.com/owner/repo/issues/123"
    }]
  }]
}
```

## URL Formats

| Resource | URL Pattern |
|----------|-------------|
| Issue | `https://github.com/owner/repo/issues/123` |
| PR | `https://github.com/owner/repo/pull/123` |
| Commit | `https://github.com/owner/repo/commit/sha` |
| File | `https://github.com/owner/repo/blob/branch/path` |
| Line | `https://github.com/owner/repo/blob/branch/path#L10` |

## Troubleshooting

### Authentication Issues

```bash
# Check status
gh auth status

# Re-authenticate
gh auth login

# Use different account
gh auth login --hostname github.com
```

### Rate Limiting

GitHub API has rate limits (5000 requests/hour for authenticated users).

```bash
# Check rate limit status
gh api rate_limit --jq '.rate'
```

### Permission Issues

```bash
# Check token scopes
gh auth status

# Request additional scopes
gh auth refresh -s repo,read:org
```

## Scripts Reference

| Script | Purpose | Key Features |
|--------|---------|--------------|
| `check-prerequisites.py` | Verify setup | CLI, auth validation |
| `query-issues.py` | Query issues | Presets, multi-repo, table output |
| `github_client.py` | API client | Rate limiting, error handling |

## References

- [GitHub CLI Manual](https://cli.github.com/manual/)
- [GitHub Issues](https://docs.github.com/en/issues)
- [GitHub REST API](https://docs.github.com/en/rest)
- [GitHub GraphQL API](https://docs.github.com/en/graphql)
