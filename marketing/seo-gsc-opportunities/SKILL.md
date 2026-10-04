---
name: seo-gsc-opportunities
description: >
  Find quick SEO wins by identifying high-impression, low-CTR keywords using
  Google Search Console data. Surfaces keywords already ranking where better
  titles or content expansion could quickly boost traffic. Use when user says
  "GSC opportunities", "quick wins", "low CTR keywords",
  "high impressions low clicks", or "easy SEO wins".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# GSC Opportunities — High-Impression Low-CTR Finder

@skills/seo/references/mcp-degradation.md
@skills/seo/references/gsc-api-reference.md

Finds keywords with significant impressions but low click-through rates — indicating
ranking positions where optimization can quickly increase organic traffic without
new content creation.

## MCP Check

Before calling any GSC tool, verify the MCP is connected:

1. Use ToolSearch with query `+google-search-console`
2. If tools returned — note the actual tool name prefix, proceed to Inputs
3. If no tools returned — display the GSC MCP error template from
   `references/mcp-degradation.md` and stop:

```
## Google Search Console MCP Not Available

The `/seo gsc opportunities` command requires the GSC MCP, which is not currently connected.

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

**Step 1 — Find keyword opportunities:**
Call `find_keyword_opportunities` with:
- `siteUrl`: the site property
- `startDate`: calculated startDate
- `endDate`: calculated endDate
- `minImpressions`: 100 (keywords need at least 100 impressions to matter)
- `maxCtr`: 0.05 (5% CTR threshold — keywords below this are underperforming)
- `maxPosition`: 20 (only keywords ranking in top 20 positions)

**Post-processing:**
Sort results by impressions descending (highest opportunity volume first).

For each keyword, add a "Potential" action recommendation:
- Position 1-3 and CTR < 3%: "Review snippet — may have featured snippet competing"
- Position 4-10 and CTR < 3%: "Optimize title tag and meta description"
- Position 4-10 and CTR 3-5%: "A/B test title variations"
- Position 11-20: "Content expansion to move into top 10"

CTR display rule: API returns CTR as decimal (0.0523) — multiply by 100 for display
(show 5.23%).

## Output Format

```
## GSC Opportunities: [site property]
**Period:** [startDate] to [endDate] (28 days)
**Filters:** Impressions >= 100, CTR < 5%, Position <= 20

### Keyword Opportunities
| Keyword | Impressions | Clicks | CTR | Position | Recommended Action |
|---------|------------|--------|-----|----------|--------------------|
| [keyword] | [n] | [n] | [X.XX%] | [X.X] | [action] |
...

**Total opportunities found:** [count]

### Quick Wins Summary
- **Title/meta optimization candidates:** [count] keywords in positions 4-10
- **Content expansion candidates:** [count] keywords in positions 11-20
```

If no opportunities found with default thresholds, note: "No keywords found with
>=100 impressions and <5% CTR in top 20 positions for this period."
