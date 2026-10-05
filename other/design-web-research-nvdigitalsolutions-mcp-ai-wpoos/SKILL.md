---
type: Skill
name: design-web-research
description: Perform quick web searches, local business lookups, and URL content extraction. Covers web_search for general queries, brave_local_search for location-based discovery, and run_crawl4ai_job for deep page crawling. Use when fact-checking, trend spotting, doing competitor analysis, looking up local businesses, extracting page content, or performing content research that doesn't need multi-step deep research.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Web Research

Use this skill for quick web lookups, local searches, and page content extraction — faster and lighter than `deep_research`.

## Available Tools

| Tool | Purpose | Speed | Depth |
|---|---|---|---|
| `web_search` | General web search (Brave/Tavily/DuckDuckGo) | Fast (1–3s) | Light — top N results |
| `brave_web_search` | Alternative web search | Fast | Light |
| `brave_local_search` | Local businesses, places, "near me" queries | Fast | Light |
| `run_crawl4ai_job` | Crawl specific URLs for full content extraction | Slow (10–120s) | Heavy — full page content |

## When to use this skill

Trigger when ANY of the following is true:

- Quick fact-checking or looking up current information.
- The task asks to "search for", "look up", or "find information about" something.
- Researching trends, news, or recent developments.
- Finding local businesses, stores, or services.
- Extracting content from specific web pages for research or repurposing.
- Competitor website analysis — what are they doing?
- Price checking or availability lookup.
- The task needs current web data but doesn't require a multi-step research report.

**Do NOT use this skill for:**
- Deep, multi-source research reports → use `design-deep-research`
- Product SKU research with WooCommerce intent → use `design-product-research`

## `web_search` — General Web Queries

The primary tool for quick web lookups. Configured to use Brave Search by default, with Tavily and DuckDuckGo as alternatives.

### Parameters

```
query          — Search query (required)
max_results    — Number of results 1–10 (default: 5)
country        — ISO country code for geo-targeting (e.g., "LK" for Sri Lanka)
language       — ISO language code (e.g., "en")
freshness      — "pd" (past day), "pw" (past week), "pm" (past month), "py" (past year)
save_to_paper_store — Auto-save results (default: false)
paper_store_collection — Target collection (default: "web-search-results")
paper_store_tags — Tags for the saved record
```

### Query Tips

```
Good:  "luxury fragrance market Sri Lanka 2026"
Good:  "Carolina Herrera Good Girl price"
Good:  "best Instagram engagement rate benchmarks retail 2026"
Bad:   "tell me about perfumes" (too vague)
Bad:   "what is the best perfume for men in sri lanka that is affordable
        and long lasting and comes in a nice bottle" (too long — be specific)
```

### Geo-Targeting for Sri Lanka

When researching The Parfumerie's market:

```
web_search {
  query: "online perfume shopping Sri Lanka trends"
  country: "LK"
  language: "en"
}
```

### Trend Research

Use `freshness` to focus on recent developments:

```
web_search {
  query: "fragrance trends 2026"
  freshness: "pm"  // past month
  max_results: 10
}
```

## `brave_local_search` — Local Discovery

Search for businesses, places, and services with location context.

### Parameters

```
query   — Search query (e.g., "perfume shops Colombo")
count   — Results 1–20 (default: 5)
```

### When to use

- Finding competitor locations
- Researching local market presence
- Discovering potential stockists or partners
- Location-based content ("best perfume shops in Colombo")

### Example

```
brave_local_search {
  query: "luxury perfume shops Colombo Sri Lanka"
  count: 10
}
```

## `run_crawl4ai_job` — Deep Page Crawling

Extract full content from one or more URLs. Use when you need to read and analyze a competitor's website, extract product details from a page, or ingest a long article for repurposing.

### Parameters

```
urls                 — Array of URLs to crawl (required, or use single `url`)
url                  — Single URL (alternative to urls)
priority             — Job priority 0–100 (default: not set)
options              — Additional Crawl4AI options (crawler config, hooks)
wait_for_completion  — Poll until done (default: false, returns immediately)
poll_interval        — Seconds between polls (default: 3, max: 30)
timeout              — Max wait time in seconds (default: 120, max: 600)
```

### Modes

| Mode | When | How |
|---|---|---|
| **Fire-and-forget** | Crawling many pages, not urgent | `wait_for_completion: false` → returns job ID |
| **Wait for result** | Need content immediately, 1–2 URLs | `wait_for_completion: true` |

### Use Cases

```
1. Competitor product page analysis:
   run_crawl4ai_job {
     url: "https://competitor.lk/product-page"
     wait_for_completion: true
   }

2. Research article ingestion:
   run_crawl4ai_job {
     urls: ["https://example.com/fragrance-trends-2026",
            "https://example.com/luxury-market-sri-lanka"]
     wait_for_completion: true
     timeout: 300
   }

3. Bulk competitor scan (background):
   run_crawl4ai_job {
     urls: ["url1", "url2", "url3", ...]
     wait_for_completion: false
   }
```

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for web research workflows. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai harness` | Semantic search across research outputs and crawled content |
| `wp mcp-ai bulk` | Batch crawl and index URLs via Crawl4AI |
| `wp mcp-ai log` | View crawl job logs, errors, and timeout diagnostics |

## Choosing the Right Search Tool

```
Need a quick answer?                    → web_search
Need local business info?               → brave_local_search
Need to read a specific web page?       → run_crawl4ai_job
Need a comprehensive report?            → deep_research (design-deep-research)
Need product specs and WooCommerce copy? → research_product (design-product-research)
```

## Paper Store Integration (on request)

When explicitly asked to persist search results:

```
paper_store_write {
  collection: "web-search-results"
  id: "search-topic-slug"
  title: "Search: [Query]"
  connection_id: "conn_8srcad8zylhe"
  tags: ["web-search", "topic-tag"]
  body: {
    query: "..."
    results: [...]
    searched_at: "YYYY-MM-DD"
  }
}
```

## Critical Rules

- **Use the lightest tool for the job** — `web_search` for quick facts, `deep_research` for reports, never the other way around.
- **Geo-target when relevant** — use `country: "LK"` for Sri Lanka-specific searches.
- **Use freshness for trends** — `freshness: "pw"` or `"pm"` for current information.
- **Don't crawl unnecessarily** — `run_crawl4ai_job` is heavyweight. Use it only when you need the full content of a specific page.
- **Save results when asked** — Paper Store persistence only on explicit request.

## Common Mistakes

```
WRONG:
  ● Using deep_research for "What's the weather?" (use web_search)
  ● Crawling 50 URLs with wait_for_completion: true (will time out)
  ● Not geo-targeting local searches (missing Sri Lanka results)
  ● Searching without freshness for trends (getting 2024 results in 2026)

RIGHT:
  ✅ web_search for quick facts, current events, trend checks
  ✅ run_crawl4ai_job with fire-and-forget for bulk crawls
  ✅ country: "LK" for Sri Lankan market research
  ✅ freshness: "pm" for trend monitoring
```

## What This Skill Does NOT Cover

- Deep multi-source research reports with citations → `design-deep-research`
- Product SKU research with WooCommerce intent → `design-product-research`
- SEO keyword research and competitive SERP analysis → `design-seo-content`
- Converting research findings into WordPress drafts → `design-content-research`
- Persistent storage and structured tagging of research data → `paper_store_*` tools
- Brand or market trend analysis with strategic recommendations → `design-deep-research`

## Cross-references

- Run **`design-deep-research`** for comprehensive multi-source research — use `deep_research`.
- Run **`design-product-research`** for product SKU lookups — use `research_product`.
- Run **`design-content-research`** to convert crawled content into WordPress drafts.
- Run **`design-seo-content`** to apply search insights to product page optimization.
- Run **`design-analytics-reporting`** to research industry benchmarks for performance comparison.
- Use **`paper_store_*`** with `connection_id` to persist search results to specific sites.
