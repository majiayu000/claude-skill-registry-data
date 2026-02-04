---
name: scrape-url
description: >
  Web crawling with Tantivy full-text search indexing. Supports crawl, search, and auto-crawl.
  WHEN: User wants to "scrape a website", "crawl documentation", "search crawled content", "index a site".
  WHEN NOT: Single page fetch (use browser_navigate), web search (use web_search).
version: 0.1.0
---

# scrape_url - Web Crawling with Search

## Core Concept

`mcp__plugin_kg_kodegen__scrape_url` crawls websites, saves content as Markdown, and builds a Tantivy full-text search index. Uses an action-based interface with connection isolation and background execution support.

## Actions

| Action | Description | Required Parameters |
|--------|-------------|---------------------|
| `SEARCH` | Search with auto-crawl (RECOMMENDED) | `url`, `query` |
| `CRAWL` | Explicit crawl | `url` |
| `READ` | Check crawl progress | None |
| `LIST` | Show all active crawls | None |
| `KILL` | Cancel crawl | None |

## Key Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `action` | string | `"CRAWL"` | Action to perform |
| `url` | string | null | Target URL (required for CRAWL/SEARCH) |
| `crawl_id` | number | 0 | Crawl instance (0, 1, 2...) |
| `query` | string | null | Search query (SEARCH action) |
| `max_depth` | number | 3 | Maximum crawl depth |
| `limit` | number | null | Max pages to crawl |
| `await_completion_ms` | number | 600000 | Timeout (10 min default) |
| `crawl_rate_rps` | number | 2 | Requests per second |
| `search_limit` | number | 10 | Max search results |
| `search_offset` | number | 0 | Search pagination offset |
| `search_highlight` | boolean | true | Highlight matches |

## Usage Examples

### One-Step Search (Recommended)
Auto-crawls if index doesn't exist:
```json
{
  "action": "SEARCH",
  "url": "https://ratatui.rs",
  "crawl_id": 0,
  "query": "layout widgets"
}
```

### Explicit Crawl
```json
{
  "action": "CRAWL",
  "crawl_id": 0,
  "url": "https://docs.rs/tokio"
}
```

### Crawl with Limits
```json
{
  "action": "CRAWL",
  "url": "https://example.com/docs",
  "max_depth": 2,
  "limit": 50,
  "crawl_rate_rps": 1
}
```

### Check Progress
```json
{
  "action": "READ",
  "crawl_id": 0
}
```

### List Active Crawls
```json
{ "action": "LIST" }
```

### Cancel Crawl
```json
{
  "action": "KILL",
  "crawl_id": 0
}
```

## Search Query Syntax

Tantivy supports advanced queries:

| Query Type | Example | Description |
|------------|---------|-------------|
| Text | `layout components` | Search all fields |
| Phrase | `"exact phrase"` | Exact match |
| Boolean | `layout AND widgets` | Logical operators |
| Field | `title:layout` | Search specific field |
| Fuzzy | `layot~2` | Allow 2 character differences |

## Output Directory Structure

Content saved to `.kodegen/citescrape/{domain}/`:

```
.kodegen/citescrape/ratatui.rs/
├── manifest.json          # Crawl metadata
├── .search_index/         # Tantivy search index
├── index.md               # Homepage
├── tutorials/
│   └── hello-world.md
└── api/
    └── widgets.md
```

## Workflows

### Research Documentation
1. `SEARCH` with url and query (auto-crawls if needed)
2. Review results
3. Follow up with more specific queries

### Full Site Crawl
1. `CRAWL` with url, max_depth, limit
2. Monitor with `READ`
3. Search with `SEARCH` action

## Remember

- **SEARCH with url** auto-crawls if index missing - simplest approach
- Crawls are isolated by `crawl_id` - use different numbers for parallel crawls
- Rate limiting default is 2 req/sec - be respectful of servers
- Content saved as Markdown for easy reading
- Search index enables fast full-text queries
- Use `READ` to check on background crawls
- Timeout returns partial results - crawl continues in background
