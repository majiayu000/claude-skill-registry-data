---
name: Exa
description: >
  Neural web search via the Exa API backend. Use for searches that need date filtering,
  domain targeting, category scoping, or neural semantic search quality. Exa is the
  default search backend — Firecrawl handles page extraction and crawling.
  Triggers on: "exa search", "find recent papers on", "search arxiv for", 
  "find news from last month about", "search github for", "research papers about",
  any search that needs date ranges, domain filtering, or content-type scoping.
targets: [hermes-default, hermes-gpt]
---

# Exa Neural Search

Exa is the **search backend** for web_search in Hermes. Firecrawl handles page extraction via `web_extract` and `web_crawl`.

## When Exa Shines

Exa's neural search is better than keyword search when:
- You need semantic understanding of a query, not just keyword matching
- Searching for research papers, arXiv content, GitHub repos
- Need date-filtered results (last week, this year, date ranges)
- Want results only from specific domains
- Looking for specific content categories (news articles, company info, financial reports)

## Advanced Search Parameters

All parameters are available through the standard `web_search` tool. Unrecognized params are silently ignored by non-Exa backends.

### Date Filtering

```yaml
# Only results from 2024 onwards
start_published_date: "2024-01-01"

# Specific date range
start_published_date: "2024-06-01"
end_published_date: "2024-12-31"

# Recent news (combine with category)
start_published_date: "2025-04-01"
category: "news"
```

Date params accept ISO date strings (`YYYY-MM-DD`). Both start and end are optional.

### Domain Targeting

```yaml
# Only academic sources
include_domains: ["arxiv.org", "scholar.google.com", "academic.oup.com"]

# Block low-quality sources
exclude_domains: ["wikipedia.org", "medium.com"]

# GitHub-only search
include_domains: ["github.com"]
```

### Content Categories

The `category` param scopes results to a specific content type:

- `"research paper"` — academic papers, preprints
- `"news"` — news articles
- `"pdf"` — PDF documents
- `"github"` — GitHub repositories and discussions
- `"company"` — company websites and profiles
- `"tweet"` — tweets (X/Twitter)
- `"personal site"` — personal websites, blogs
- `"linkedin profile"` — LinkedIn pages
- `"financial report"` — financial documents, SEC filings

## Effective Query Patterns

**Research literature search:**
```
web_search(query="CRISPR delivery nanoparticles lipid", 
           category="research paper", 
           start_published_date="2024-01-01",
           limit=10)
```

**Competitive analysis:**
```
web_search(query="AI coding assistant CLI tools",
           category="company",
           limit=10)
```

**GitHub projects:**
```
web_search(query="websocket proxy relay",
           include_domains=["github.com"],
           limit=5)
```

**Recent news:**
```
web_search(query="LLM pricing changes",
           category="news",
           start_published_date="2025-04-01",
           limit=5)
```

## Backend Architecture

- `web.search_backend: exa` — all `web_search` calls go through Exa
- `web.extract_backend: firecrawl` — `web_extract` and `web_crawl` use Firecrawl

This split gives us neural search quality + Firecrawl's superior JS rendering and crawling.
