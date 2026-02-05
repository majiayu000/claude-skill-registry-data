---
name: github-changes
description: Get yesterday's code changes from a GitHub repository
---

# GitHub Changes Skill

Fetches recent commits and code changes from a GitHub repository.

## When to Use

Use this skill when you need to get:
- Yesterday's commits
- Files changed
- Lines added/removed
- Commit authors

## How to Use

```bash
# Get yesterday's changes (default)
$CLAUDE_CONFIG_DIR/skills/github-changes/scripts/get-changes.sh "owner/repo"

# Get changes for a specific date
$CLAUDE_CONFIG_DIR/skills/github-changes/scripts/get-changes.sh "owner/repo" "2024-12-15"
```

### Arguments
- `owner/repo` (required): The repository to query (e.g., "vm0-ai/vm0")
- `date` (optional): Specific date in YYYY-MM-DD format. Defaults to yesterday.

### Prerequisites
- `GITHUB_TOKEN` environment variable must be set (for private repos and higher rate limits)

## Output

Results are saved to `/tmp/data/github_changes_[timestamp].json`:

```json
{
  "repository": "vm0-ai/vm0",
  "date": "2024-12-15",
  "total_commits": 5,
  "commits": [
    {
      "sha": "abc123",
      "message": "feat: add new feature",
      "author": "username",
      "date": "2024-12-15T10:30:00Z",
      "additions": 50,
      "deletions": 10,
      "files_changed": 3
    }
  ],
  "summary": {
    "total_additions": 150,
    "total_deletions": 30,
    "total_files_changed": 12,
    "authors": ["user1", "user2"]
  }
}
```

Console output summary:
```
Repository: vm0-ai/vm0
Date: 2024-12-15
Total Commits: 5

Commits:
- feat: add new feature by @user1
- fix: resolve bug by @user2

Summary:
Files Changed: 12
Lines Added: +150
Lines Removed: -30
```

## Error Handling

- **401 Unauthorized**: Check that GITHUB_TOKEN is set correctly
- **404 Not Found**: The repository may not exist or is private
- **No commits found**: There may have been no commits on that date
