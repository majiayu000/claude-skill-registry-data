---
name: seo-gsc-drops
description: >
  Detect ranking drops and lost traffic using Google Search Console data.
  Compares the last 28 days against the prior 28-day period to surface pages
  and keywords with the biggest declines. Use when user says "GSC drops",
  "ranking drops", "lost traffic", "pages losing rankings", or "keyword drops".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# GSC Drops — Ranking Drop Detection

@skills/seo/references/mcp-degradation.md
@skills/seo/references/gsc-api-reference.md

Identifies pages and keywords that lost clicks between the last 28 days and the
prior 28-day period. Sorts by biggest losses first. Highlights CRITICAL drops
(>50% loss).

## MCP Check

Before calling any GSC tool, verify the MCP is connected:

1. Use ToolSearch with query `+google-search-console`
2. If tools returned — note the actual tool name prefix, proceed to Inputs
3. If no tools returned — display the GSC MCP error template from
   `references/mcp-degradation.md` and stop:

```
## Google Search Console MCP Not Available

The `/seo gsc drops` command requires the GSC MCP, which is not currently connected.

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

Use Bash to calculate the two comparison periods (GSC has ~3 day delay):

```bash
currentEnd=$(date -v-3d +%Y-%m-%d)
currentStart=$(date -v-31d +%Y-%m-%d)
previousEnd=$(date -v-31d +%Y-%m-%d)
previousStart=$(date -v-59d +%Y-%m-%d)
echo "Current: $currentStart to $currentEnd | Previous: $previousStart to $previousEnd"
```

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
Call `compare_performance` with the same date params but:
- `dimension`: `"query"`
- `limit`: 500

**Post-processing:**
- Filter Step 1 results to rows where `clicksChange < 0` (pages that lost clicks)
- Filter Step 2 results to rows where `clicksChange < 0` (queries that lost clicks)
- Sort both lists by `clicksChange` ascending (biggest losses first)
- For each row, calculate change percentage if not provided:
  `changePercent = (clicksChange / previousClicks) * 100`
- Mark rows with `changePercent < -50` as CRITICAL

## Output Format

```
## GSC Drops: [site property]
**Current Period:** [currentStart] to [currentEnd]
**Previous Period:** [previousStart] to [previousEnd]

### Top Dropping Pages
| Page URL | Current Clicks | Previous Clicks | Change | Change% | Severity |
|----------|---------------|-----------------|--------|---------|----------|
| [url] | [n] | [n] | [n] | [X.X%] | CRITICAL / — |
...

### Top Dropping Queries
| Query | Current Clicks | Previous Clicks | Change | Change% | Severity |
|-------|---------------|-----------------|--------|---------|----------|
| [query] | [n] | [n] | [n] | [X.X%] | CRITICAL / — |
...

**Note:** CRITICAL = more than 50% drop in clicks between periods.
```

Show top 25 dropping pages and top 25 dropping queries.
Truncate long URLs to 60 characters with `...` for readability.
If no drops detected, report: "No pages or queries lost clicks between the two periods."
