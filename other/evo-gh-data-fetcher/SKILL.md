---
name: evo-gh-data-fetcher
description: Fetches pull request and issue data from a GitHub repository using the GitHub REST API via curl/subprocess. Handles JSON output parsing, pagination, date range filtering, and error handling. Use when you need to retrieve structured PR or issue data from GitHub for analysis.
---

# evo-gh-data-fetcher

Fetches PR and issue data from GitHub repositories using the GitHub REST API (via curl subprocess calls). Works without gh CLI authentication by using unauthenticated API access for public repos.

## Key Concepts

- Uses GitHub Search API (`/search/issues`) with query qualifiers like `type:pr`, `type:issue`, `created:YYYY-MM-DD..YYYY-MM-DD`
- Search API returns max 1000 results per query; pagination handled automatically
- PR details (merge status, merged_at) require individual PR endpoint calls (`/repos/{owner}/{repo}/pulls/{number}`)
- Timestamps are ISO 8601 format with Z suffix (e.g., `2024-12-15T10:30:00Z`)
- Rate limiting: unauthenticated = 60 req/hour; with token = 5000 req/hour
- PR states from API: `open`, `closed` with `merged` boolean and `merged_at` timestamp
- Issue labels are returned as array of objects: `[{"name": "bug", ...}]`

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-gh-data-fetcher/scripts')
from utils import fetch_prs_fast, fetch_issues_with_labels, parse_gh_timestamp

# Fetch PRs
prs = fetch_prs_fast("cli/cli", "2024-12-01", "2024-12-31")

# Fetch Issues
issues = fetch_issues_with_labels("cli/cli", "2024-12-01", "2024-12-31")

# Parse timestamps
from datetime import datetime
dt = parse_gh_timestamp("2024-12-15T10:30:00Z")
```

## Functions

- `parse_gh_timestamp(ts_string)` - Parse ISO 8601 GitHub timestamp to datetime
- `run_github_api(url)` - Execute curl to GitHub REST API, return parsed JSON
- `fetch_search_results(query, per_page, max_pages)` - Paginated search API fetcher
- `fetch_prs_fast(repo, date_start, date_end)` - Fetch PRs with merge details
- `fetch_issues_with_labels(repo, date_start, date_end)` - Fetch issues with labels

## PR Data Structure (from /repos/{owner}/{repo}/pulls/{number})

- `number`: int
- `state`: "open" or "closed"
- `merged`: boolean
- `created_at`: ISO 8601 timestamp
- `merged_at`: ISO 8601 timestamp or null
- `closed_at`: ISO 8601 timestamp or null
- `user.login`: string (author)
- `labels`: [{"name": "...", ...}]

## Issue Data Structure (from search API)

- `number`: int
- `state`: "open" or "closed"
- `created_at`: ISO 8601 timestamp
- `closed_at`: ISO 8601 timestamp or null
- `user.login`: string (author)
- `labels`: [{"name": "...", ...}]
