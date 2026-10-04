---
name: seo-gsc-brand-vs-nonbrand
description: >
  Analyze branded vs non-branded traffic split using Google Search Console data.
  Shows what percentage of organic clicks come from brand name searches vs generic
  queries. Requires user to confirm brand terms before analysis. Use when user says
  "brand vs nonbrand", "branded traffic", "brand queries",
  "non-brand traffic", or "branded vs generic".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# GSC Brand vs Non-Brand — Brand Traffic Split Analysis

@skills/seo/references/mcp-degradation.md
@skills/seo/references/gsc-api-reference.md

Analyzes what share of organic traffic comes from branded queries vs generic queries.
IMPORTANT: This command REQUIRES user-provided brand terms before making any API call.
The `analyze_brand_queries` tool needs a `brandTerms` array — never guess brand terms.

## MCP Check

Before calling any GSC tool, verify the MCP is connected:

1. Use ToolSearch with query `+google-search-console`
2. If tools returned — note the actual tool name prefix, proceed to Inputs
3. If no tools returned — display the GSC MCP error template from
   `references/mcp-degradation.md` and stop:

```
## Google Search Console MCP Not Available

The `/seo gsc brand-vs-nonbrand` command requires the GSC MCP, which is not currently connected.

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

## Brand Terms Confirmation (REQUIRED — do before any API call)

Before calling `analyze_brand_queries`, the user MUST confirm their brand terms.

1. Extract a suggested brand term from the site URL:
   - From `sc-domain:example.com` → suggest `["example"]`
   - From `https://www.mybrand.co.uk` → suggest `["mybrand"]`
   - Remove TLD, www, subdomains, and hyphens for the suggestion

2. Present the confirmation prompt to the user:

```
I'll analyze brand vs non-brand traffic for [site].

**Please confirm your brand terms:** `["[suggested-term]"]`

You can:
- Confirm these terms as-is
- Add additional terms (e.g. product names, common misspellings): `["brand", "brand product", "brandname"]`
- Remove terms that aren't actually branded

Brand terms are used to separate branded queries (e.g. "acme widgets") from
non-brand queries (e.g. "best widgets for home"). Include all variations users
search for your brand.
```

3. Wait for the user to confirm or modify the brand terms.
4. Only proceed to the API call after receiving explicit confirmation.

## Date Calculation

Use Bash to calculate dates (GSC has ~3 day delay):

```bash
endDate=$(date -v-3d +%Y-%m-%d)
startDate=$(date -v-31d +%Y-%m-%d)
echo "endDate: $endDate | startDate: $startDate"
```

## Execution

After brand terms are confirmed:

**Call `analyze_brand_queries` with:**
- `siteUrl`: the site property
- `startDate`: calculated startDate
- `endDate`: calculated endDate
- `brandTerms`: the confirmed array of brand terms

**Post-processing:**
- Calculate brand percentage of total clicks: `(brandClicks / totalClicks) * 100`
- Calculate non-brand percentage: `(nonBrandClicks / totalClicks) * 100`
- Add strategic insight based on brand percentage:
  - >70% branded: Note dependency risk — organic visibility heavily reliant on brand
  - 40-70% branded: Balanced mix — healthy brand recognition with non-brand growth
  - 10-40% branded: Non-brand dominant — good organic reach beyond brand searches
  - <10% branded: Note brand awareness opportunity — consider brand-building content

CTR display rule: API returns CTR as decimal — multiply by 100 for display.

## Output Format

```
## GSC Brand vs Non-Brand: [site property]
**Period:** [startDate] to [endDate] (28 days)
**Brand terms analyzed:** [list of confirmed brand terms]

### Brand Traffic Split
| Category | Clicks | Impressions | CTR | Avg Position | % of Total Clicks |
|----------|--------|-------------|-----|--------------|-------------------|
| Branded | [n] | [n] | [X.XX%] | [X.X] | [X.X%] |
| Non-Brand | [n] | [n] | [X.XX%] | [X.X] | [X.X%] |
| **Total** | **[n]** | **[n]** | **[X.XX%]** | **[X.X]** | **100%** |

### Top Branded Queries
| Query | Clicks | Impressions | CTR | Position |
|-------|--------|-------------|-----|----------|
| [query] | [n] | [n] | [X.XX%] | [X.X] |
...

### Top Non-Brand Queries
| Query | Clicks | Impressions | CTR | Position |
|-------|--------|-------------|-----|----------|
| [query] | [n] | [n] | [X.XX%] | [X.X] |
...

### Strategic Insight
[Insight based on brand percentage thresholds above]
```

Show top 10 branded queries and top 10 non-brand queries, sorted by clicks descending.
