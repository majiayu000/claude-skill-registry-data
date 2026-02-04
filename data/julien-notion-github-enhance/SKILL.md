---
name: julien-notion-github-enhance
description: Enrich a Github [DB] entry with GitHub API metadata (description, stars, language, cover image). Use when user wants to populate a GitHub repo entry with live metadata, enhance github entry, or add github info.
---

# Notion GitHub Enhance

Enrich Github [DB] entries with live metadata from GitHub API.

## Prerequisites

- `NOTION_TOKEN` environment variable set
- `GITHUB_TOKEN` environment variable (optional, for higher rate limits)
- `requests` package: `pip install requests`

## Usage

Run the enrichment script with a page ID or URL:

```bash
python ~/.claude/skills/notion-github-enhance-note/scripts/enrich.py <page_id_or_url>
```

**Arguments:**
- `page_id_or_url`: Notion page ID (UUID) or full URL of Github [DB] entry

**Example:**
```bash
python ~/.claude/skills/notion-github-enhance-note/scripts/enrich.py 12345678-1234-1234-1234-123456789abc
```

## Output

- On success: Confirmation with updated fields
- On failure: Error message with reason

## Data Retrieved

| Field | Source | Notes |
|-------|--------|-------|
| Description | GitHub API | Repo description |
| Language | GitHub API | Primary language |
| Stars | GitHub API | Star count |
| Cover | OpenGraph | Social preview image |

## Rate Limits

- **Without GITHUB_TOKEN**: 60 requests/hour
- **With GITHUB_TOKEN**: 5000 requests/hour

Set `GITHUB_TOKEN` environment variable for higher limits:
```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
```

## Error Handling

| Error | Meaning |
|-------|---------|
| `NOT_REPO_URL` | URL is org page or not a valid repo |
| `REPO_NOT_FOUND` | Repository deleted or private |
| `RATE_LIMITED` | GitHub API rate limit reached |
| `PAGE_NOT_FOUND` | Invalid page ID or no access |

## Database ID

- **Github [DB]**: `2cacdc04-12e3-81cc-a84e-fdbba086ab29`
