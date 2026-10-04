---
name: seo-gsc-new-keywords
description: >
  Discover newly ranking keywords using Google Search Console data. Finds queries
  that had zero clicks or impressions in the prior 28 days but started appearing
  in the current period, revealing emerging content opportunities. Use when user
  says "new keywords", "new rankings", "keywords started ranking",
  "recently ranking", or "new queries".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# GSC New Keywords — New Ranking Discovery

@skills/seo/references/mcp-degradation.md
@skills/seo/references/gsc-api-reference.md

Identifies queries that are newly appearing in Google Search results — either
completely new (no prior impressions) or newly clicking through (no prior clicks).
Sorts by current clicks to surface the most impactful new rankings first.

## MCP Check

Before calling any GSC tool, verify the MCP is connected:

1. Use ToolSearch with query `+google-search-console`
2. If tools returned — note the actual tool name prefix, proceed to Inputs
3. If no tools returned — display the GSC MCP error template from
   `references/mcp-degradation.md` and stop:

```
## Google Search Console MCP Not Available

The `/seo gsc new-keywords` command requires the GSC MCP, which is not currently connected.

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

**Call `compare_performance` with 28-day window:**
- `siteUrl`: the site property
- `currentStartDate`: currentStart
- `currentEndDate`: currentEnd
- `previousStartDate`: previousStart
- `previousEndDate`: previousEnd
- `dimension`: `"query"`
- `limit`: 1000

**Post-processing — identify new keywords:**
Filter results to rows where EITHER condition is true:
1. Previous period had 0 clicks AND current period has > 0 clicks
   (truly new click-generating keywords)
2. Previous period had 0 impressions AND current period has > 0 impressions
   (just started appearing in search results, may not click yet)

Label each result by type:
- "New Clicks" — was showing but not clicking before, now getting clicks
- "New Ranking" — was not appearing at all, now showing in search results

Sort by current clicks descending (most impactful new keywords first).

**Emerging topic detection:**
After filtering, look for common words or phrases across the new keywords.
If 3 or more new keywords share a common root word or topic cluster, note it as
an emerging content opportunity.

CTR display rule: API returns CTR as decimal — multiply by 100 for display.

## Output Format

```
## GSC New Keywords: [site property]
**Current Period:** [currentStart] to [currentEnd]
**Previous Period:** [previousStart] to [previousEnd]
**New keywords found:** [count]

### Newly Ranking Keywords
| Type | Query | Current Clicks | Current Impressions | CTR | Position |
|------|-------|---------------|---------------------|-----|----------|
| New Clicks | [query] | [n] | [n] | [X.XX%] | [X.X] |
| New Ranking | [query] | [n] | [n] | [X.XX%] | [X.X] |
...

### Emerging Topics
[If 3+ new keywords share a topic cluster:]
- **"[topic]" cluster:** [n] new keywords (e.g. "[kw1]", "[kw2]", "[kw3]")
  Opportunity: Consider creating or expanding content targeting this topic area.

[If no clear topic clusters:]
No clear topic clusters detected among new keywords.

### Summary
| Metric | Value |
|--------|-------|
| New click-generating keywords | [n] |
| New ranking keywords (impressions only) | [n] |
| Total new keywords | [n] |
| Top new keyword by clicks | "[query]" ([n] clicks) |
```

If no new keywords found, report: "No new keywords detected. All queries in the
current period also appeared in the previous period."
