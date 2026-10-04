---
name: seo-gsc-content-decay
description: >
  Detect content decay by identifying pages that are losing both clicks and
  impressions over a 90-day comparison window in Google Search Console. Surfaces
  pages with true long-term decline (not seasonal variation) and assigns decay
  severity ratings. Use when user says "content decay", "declining pages",
  "losing rankings", "pages losing traffic over time", or "90 day decline".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# GSC Content Decay — 90-Day Decline Detection

@skills/seo/references/mcp-degradation.md
@skills/seo/references/gsc-api-reference.md

Identifies pages experiencing true content decay: both clicks AND impressions
declining over a 90-day comparison period. Filters out seasonal variation by
requiring both metrics to decline simultaneously.

## MCP Check

Before calling any GSC tool, verify the MCP is connected:

1. Use ToolSearch with query `+google-search-console`
2. If tools returned — note the actual tool name prefix, proceed to Inputs
3. If no tools returned — display the GSC MCP error template from
   `references/mcp-degradation.md` and stop:

```
## Google Search Console MCP Not Available

The `/seo gsc content-decay` command requires the GSC MCP, which is not currently connected.

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

Use Bash to calculate 90-day comparison windows (GSC has ~3 day delay):

```bash
currentEnd=$(date -v-3d +%Y-%m-%d)
currentStart=$(date -v-93d +%Y-%m-%d)
previousEnd=$(date -v-93d +%Y-%m-%d)
previousStart=$(date -v-183d +%Y-%m-%d)
echo "Current: $currentStart to $currentEnd | Previous: $previousStart to $previousEnd"
```

## Execution

**Call `compare_performance` with 90-day window:**
- `siteUrl`: the site property
- `currentStartDate`: currentStart
- `currentEndDate`: currentEnd
- `previousStartDate`: previousStart
- `previousEndDate`: previousEnd
- `dimension`: `"page"`
- `limit`: 1000

**Post-processing — identify true decay:**
Filter results to rows where BOTH conditions are true:
1. `clicksChange < 0` (clicks declined)
2. Impressions declined (if `impressionsChange` field available, check `impressionsChange < 0`;
   if not available, use the presence of lower current impressions vs previous)

This double-filter removes pages that lost clicks but maintained/grew impressions
(which often indicates seasonal or competitor CTR changes, not content decay).

Sort by `clicksChangePercent` ascending (most severe decay first).

**Calculate decay severity:**
For each decaying page, compute click change percentage if not provided:
`changePercent = abs(clicksChange / previousClicks) * 100`

Severity classification:
- `changePercent > 50`: CRITICAL
- `changePercent >= 30 and <= 50`: HIGH
- `changePercent >= 10 and < 30`: MEDIUM

**Recommendation per page based on position change:**
- Position declined significantly (positionChange > 5): "Review competitor content — rankings lost"
- Position stable but impressions fell: "Check for technical issues — may have indexing problems"
- Position slightly declined (positionChange 1-5): "Update and refresh content to regain relevance"
- Position improved but clicks fell: "Review search intent — content may no longer match query intent"

CTR display rule: API returns CTR as decimal — multiply by 100 for display.

## Output Format

```
## GSC Content Decay: [site property]
**Current Period:** [currentStart] to [currentEnd] (90 days)
**Previous Period:** [previousStart] to [previousEnd] (90 days)
**Decay pages found:** [count]

### Content Decay Report
| Decay Severity | URL | Current Clicks | Previous Clicks | Change% | Curr Position | Prev Position | Pos Change | Action |
|----------------|-----|---------------|-----------------|---------|---------------|---------------|------------|--------|
| CRITICAL | [url] | [n] | [n] | -X.X% | [X.X] | [X.X] | ↑/↓ X.X | [action] |
| HIGH | [url] | [n] | [n] | -X.X% | [X.X] | [X.X] | ↑/↓ X.X | [action] |
| MEDIUM | [url] | [n] | [n] | -X.X% | [X.X] | [X.X] | ↑/↓ X.X | [action] |
...

### Summary by Severity
| Severity | Pages | Avg Click Loss |
|----------|-------|----------------|
| CRITICAL (>50% drop) | [n] | [X.X%] |
| HIGH (30-50% drop) | [n] | [X.X%] |
| MEDIUM (10-30% drop) | [n] | [X.X%] |
```

Truncate long URLs to 60 characters with `...` for readability.
If no decay pages found, report: "No content decay detected. No pages show simultaneous
decline in both clicks and impressions over the 90-day comparison period."
