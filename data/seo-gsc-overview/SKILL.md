---
name: seo-gsc-overview
description: >
  Show a Google Search Console performance dashboard for the last 28 days.
  Displays total clicks, impressions, CTR, and average position, plus top 25
  queries and top 25 pages. Use when user says "GSC overview",
  "search console performance", "how is my site doing in Google",
  "clicks and impressions", or "show me my GSC data".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# GSC Overview — Performance Dashboard

@skills/seo/references/mcp-degradation.md
@skills/seo/references/gsc-api-reference.md

Shows actual GSC performance data for the last 28 days: total clicks, impressions,
CTR, average position, top 25 queries, and top 25 pages.

## MCP Check

Before calling any GSC tool, verify the MCP is connected:

1. Use ToolSearch with query `+google-search-console`
2. If tools returned — note the actual tool name prefix, proceed to Inputs
3. If no tools returned — display the GSC MCP error template from
   `references/mcp-degradation.md` and stop:

```
## Google Search Console MCP Not Available

The `/seo gsc overview` command requires the GSC MCP, which is not currently connected.

**What you can do:**
- Use `/seo technical <url>` for crawlability and indexability analysis (no live data)
- Use `/seo audit <url>` for a full static SEO audit

**To connect GSC MCP:**
- Install and configure a Google Search Console MCP server (see README for setup)
- Add it to ~/.claude/mcp.json at user scope (NOT project scope)
- Verify GSC property access before running commands (domain vs URL prefix format)
- See references/gsc-api-reference.md for property format details
```

## Inputs

- `site`: The GSC property URL. Accept both formats:
  - Domain property: `sc-domain:example.com`
  - URL prefix: `https://example.com` or `https://www.example.com`
  - If user provides a bare domain (no prefix, e.g. `example.com`), call `list_sites`
    to help identify the correct property format registered in GSC.

## Date Calculation

Use Bash to calculate dates (GSC data has ~3 day delay):

```bash
endDate=$(date -v-3d +%Y-%m-%d)
startDate=$(date -v-31d +%Y-%m-%d)
echo "endDate: $endDate | startDate: $startDate"
```

This gives a 28-day window ending 3 days ago.

## Execution

**Step 1 — Top Queries (28 days):**
Call `query_search_analytics` with:
- `siteUrl`: the site property
- `startDate`: calculated startDate
- `endDate`: calculated endDate
- `dimensions`: `["query"]`
- `rowLimit`: 25

**Step 2 — Top Pages (28 days):**
Call `query_search_analytics` with:
- `siteUrl`: the site property
- `startDate`: calculated startDate
- `endDate`: calculated endDate
- `dimensions`: `["page"]`
- `rowLimit`: 25

**Step 3 — Top Pages by Clicks:**
Call `get_top_pages` with:
- `siteUrl`: the site property
- `startDate`: calculated startDate
- `endDate`: calculated endDate
- `sortBy`: `"clicks"`
- `limit`: 25

**Aggregation:**
From Step 1 results, compute totals by summing across all returned rows:
- Total Clicks = sum of all `clicks`
- Total Impressions = sum of all `impressions`
- Avg CTR = (sum of clicks / sum of impressions) * 100 — format as X.XX%
- Avg Position = weighted average of `position` by impressions

CTR display rule: API returns CTR as decimal (0.0523) — always multiply by 100 for
display (show 5.23%).

## Output Format

```
## GSC Overview: [site property]
**Period:** [startDate] to [endDate] (28 days)

### Summary
| Metric | Value |
|--------|-------|
| Total Clicks | [number] |
| Total Impressions | [number] |
| Average CTR | [X.XX%] |
| Average Position | [X.X] |

### Top 25 Queries
| Query | Clicks | Impressions | CTR | Position |
|-------|--------|-------------|-----|----------|
| [query] | [clicks] | [impressions] | [X.XX%] | [X.X] |
...

### Top 25 Pages
| Page URL | Clicks | Impressions | CTR | Position |
|----------|--------|-------------|-----|----------|
| [url] | [clicks] | [impressions] | [X.XX%] | [X.X] |
...
```

Sort queries by clicks descending. Sort pages by clicks descending.
Truncate long URLs to 60 characters with `...` for readability.
