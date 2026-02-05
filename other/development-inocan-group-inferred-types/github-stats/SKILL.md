---
name: github-stats
description: Get GitHub repository statistics including stars, forks, and watchers
---

# GitHub Stats Skill

Fetches repository statistics from GitHub API.

## When to Use

Use this skill when you need to get:
- Star count for a repository
- Fork count
- Watcher count
- Open issues count

## How to Use

```bash
$CLAUDE_CONFIG_DIR/skills/github-stats/scripts/repo-stats.sh "owner/repo"
```

### Arguments
- `owner/repo`: The repository to query (e.g., "vm0-ai/vm0")

### Prerequisites
- `GITHUB_TOKEN` environment variable must be set (for higher rate limits)

## Output

Results are saved to `/tmp/data/github_stats_[timestamp].json`:

```json
{
  "full_name": "vm0-ai/vm0",
  "stargazers_count": 1234,
  "forks_count": 56,
  "watchers_count": 78,
  "open_issues_count": 10,
  "subscribers_count": 45,
  "description": "Repository description",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-12-15T00:00:00Z"
}
```

Console output summary:
```
Repository: vm0-ai/vm0
Stars: 1234
Forks: 56
Watchers: 78
Open Issues: 10
```

## Error Handling

- **401 Unauthorized**: Check that GITHUB_TOKEN is set correctly
- **404 Not Found**: The repository may not exist or is private
- **403 Forbidden**: Rate limit exceeded, wait or use authenticated requests
