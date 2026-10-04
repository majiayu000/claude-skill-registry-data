---
name: seo-gsc-cannibalization
description: >
  Detect keyword cannibalization by identifying queries where multiple pages are
  competing for the same ranking. Uses Google Search Console data to find queries
  appearing across 2 or more pages. Use when user says "keyword cannibalization",
  "same keyword multiple pages", "cannibalizing keywords", or "duplicate rankings".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# GSC Cannibalization — Keyword Cannibalization Detection

@skills/seo/references/mcp-degradation.md
@skills/seo/references/gsc-api-reference.md

Finds queries where multiple pages compete for the same ranking, causing them to
cannibalize each other's traffic. Identifies the "winning" page and "losing" pages
for each cannibalized keyword.

## MCP Check

Before calling any GSC tool, verify the MCP is connected:

1. Use ToolSearch with query `+google-search-console`
2. If tools returned — note the actual tool name prefix, proceed to Inputs
3. If no tools returned — display the GSC MCP error template from
   `references/mcp-degradation.md` and stop:

```
## Google Search Console MCP Not Available

The `/seo gsc cannibalization` command requires the GSC MCP, which is not currently connected.

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
  - If user provides a bare domain (no prefix), call `list_sites` to identify
    the correct property format registered in GSC.

## Date Calculation

Use Bash to calculate dates (GSC has ~3 day delay):

```bash
endDate=$(date -v-3d +%Y-%m-%d)
startDate=$(date -v-31d +%Y-%m-%d)
echo "endDate: $endDate | startDate: $startDate"
```

## Execution

**Step 1 — Pull query+page data:**
Call `query_search_analytics` with:
- `siteUrl`: the site property
- `startDate`: calculated startDate
- `endDate`: calculated endDate
- `dimensions`: `["query", "page"]`
- `rowLimit`: 1000

**Post-processing — detect cannibalization:**
Group the results by `query`. For each query:
- Count distinct `page` values
- If a query has 2 or more distinct pages → it is cannibalized
- Keep only cannibalized queries for the report

For each cannibalized query, identify:
- "Winning" page: the page with the most `clicks` for that query
- "Losing" pages: all other pages competing for the same query

Sort cannibalized queries by total impressions descending (highest-traffic
cannibalization issues first).

CTR display rule: API returns CTR as decimal — multiply by 100 for display.

## Output Format

```
## GSC Cannibalization Report: [site property]
**Period:** [startDate] to [endDate] (28 days)
**Cannibalized queries found:** [count]

### Cannibalized Keywords

#### Query: "[query]" ([total impressions] impressions)
| Role | Page URL | Clicks | Impressions | CTR | Position |
|------|----------|--------|-------------|-----|----------|
| WINNING | [url] | [n] | [n] | [X.XX%] | [X.X] |
| losing | [url] | [n] | [n] | [X.XX%] | [X.X] |

**Recommendation:** [recommendation based on situation]

[Repeat for each cannibalized query...]

### Summary
| Metric | Value |
|--------|-------|
| Total cannibalized queries | [count] |
| Total pages involved | [count] |
| Estimated lost clicks | [sum of losing page clicks] |
```

**Recommendation logic:**
- If winning page has much higher position (lower number): consolidate losing pages
  into winning page via redirect or canonical
- If positions are close (within 3): add canonical signals pointing from losing to
  winning page; consider merging content
- If the pages cover distinct subtopics: differentiate content more clearly or use
  internal links to signal hierarchy

If no cannibalization found, report: "No keyword cannibalization detected. Each
query appears on only one page in the top 1000 results."
