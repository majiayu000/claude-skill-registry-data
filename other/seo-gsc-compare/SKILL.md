---
name: seo-gsc-compare
description: >
  Compare Google Search Console performance between two time periods to identify
  trends and changes. Supports month-over-month (MoM), year-over-year (YoY), or
  custom date ranges. Use when user says "GSC compare", "period comparison",
  "month over month", "year over year", "compare performance", "MoM", or "YoY".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# GSC Compare — Period-over-Period Comparison

@skills/seo/references/mcp-degradation.md
@skills/seo/references/gsc-api-reference.md

Compares GSC performance between two date periods — by default month-over-month
(last 28 days vs prior 28 days). Surfaces top movers by page and query with
directional indicators.

## MCP Check

Before calling any GSC tool, verify the MCP is connected:

1. Use ToolSearch with query `+google-search-console`
2. If tools returned — note the actual tool name prefix, proceed to Inputs
3. If no tools returned — display the GSC MCP error template from
   `references/mcp-degradation.md` and stop:

```
## Google Search Console MCP Not Available

The `/seo gsc compare` command requires the GSC MCP, which is not currently connected.

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
- `type` (optional): Comparison type — `mom` (default), `yoy`, or `custom`
- `current_start`, `current_end`, `previous_start`, `previous_end` (optional):
  Only used when `type=custom`. Accept YYYY-MM-DD format.

## Date Calculation

Use Bash to calculate comparison periods based on the requested type.
GSC has ~3 day delay — all end dates use today-3.

**Month-over-month (MoM, default):**
```bash
currentEnd=$(date -v-3d +%Y-%m-%d)
currentStart=$(date -v-31d +%Y-%m-%d)
previousEnd=$(date -v-31d +%Y-%m-%d)
previousStart=$(date -v-59d +%Y-%m-%d)
comparisonLabel="Month-over-Month (last 28 days vs prior 28 days)"
```

**Year-over-year (YoY):**
```bash
currentEnd=$(date -v-3d +%Y-%m-%d)
currentStart=$(date -v-31d +%Y-%m-%d)
previousEnd=$(date -v-3d -v-1y +%Y-%m-%d)
previousStart=$(date -v-31d -v-1y +%Y-%m-%d)
comparisonLabel="Year-over-Year (last 28 days vs same period last year)"
```

**Custom:** Use the user-provided dates directly.

## Execution

**Step 1 — Page-level comparison:**
Call `compare_performance` with:
- `siteUrl`: the site property
- `currentStartDate`: currentStart
- `currentEndDate`: currentEnd
- `previousStartDate`: previousStart
- `previousEndDate`: previousEnd
- `dimension`: `"page"`
- `limit`: 500

**Step 2 — Query-level comparison:**
Call `compare_performance` with same dates but:
- `dimension`: `"query"`
- `limit`: 500

**Post-processing:**
For each result set:
- Calculate summary totals (sum all current clicks vs previous clicks)
- Separate into "top gainers" (clicksChange > 0, sort descending) and
  "top losers" (clicksChange < 0, sort ascending)
- Compute overall percentage change: `(currentTotal - previousTotal) / previousTotal * 100`

Direction indicators (unicode arrows for markdown):
- Positive change: ↑ (upward arrow)
- Negative change: ↓ (downward arrow)
- No change: → (rightward arrow)

CTR display rule: API returns CTR as decimal — multiply by 100 for display.

## Output Format

```
## GSC Compare: [site property]
**[comparisonLabel]**
**Current:** [currentStart] to [currentEnd]
**Previous:** [previousStart] to [previousEnd]

### Summary Deltas
| Metric | Current | Previous | Change | Change% |
|--------|---------|----------|--------|---------|
| Total Clicks | [n] | [n] | ↑/↓ [n] | ↑/↓ X.X% |
| Total Impressions | [n] | [n] | ↑/↓ [n] | ↑/↓ X.X% |
| Avg CTR | [X.XX%] | [X.XX%] | ↑/↓ X.XX% | — |
| Avg Position | [X.X] | [X.X] | ↑/↓ X.X | — |

### Top Gaining Pages (by clicks)
| Page URL | Current Clicks | Previous Clicks | Change | Change% |
|----------|---------------|-----------------|--------|---------|
| [url] | [n] | [n] | ↑ [n] | ↑ X.X% |
...

### Top Losing Pages (by clicks)
| Page URL | Current Clicks | Previous Clicks | Change | Change% |
|----------|---------------|-----------------|--------|---------|
| [url] | [n] | [n] | ↓ [n] | ↓ X.X% |
...

### Top Gaining Queries
| Query | Current Clicks | Previous Clicks | Change | Change% |
|-------|---------------|-----------------|--------|---------|
| [query] | [n] | [n] | ↑ [n] | ↑ X.X% |
...

### Top Losing Queries
| Query | Current Clicks | Previous Clicks | Change | Change% |
|-------|---------------|-----------------|--------|---------|
| [query] | [n] | [n] | ↓ [n] | ↓ X.X% |
...
```

Show top 10 gainers and top 10 losers for both pages and queries.
Truncate long URLs to 60 characters with `...` for readability.
