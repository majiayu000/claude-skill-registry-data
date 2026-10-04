---
name: seo-serp
description: >
  Analyze SERP for a keyword using Ahrefs live data: ranking pages, DR scores,
  traffic estimates, and content angle analysis. Use when user says "SERP
  analysis", "who ranks for", "SERP breakdown", "competitors ranking for
  keyword", "serp overview", "what's ranking for", "show me the SERP for",
  or "SERP competition for".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# SERP Analysis

Fetches live SERP data for a keyword from Ahrefs, showing ranking pages with
DR scores, traffic estimates, and content angle analysis. WebMCP enriches page
titles when available; Ahrefs-only mode is the primary operating mode.

## References

@skills/seo/references/mcp-degradation.md
@skills/seo/references/ahrefs-api-reference.md

## Inputs

- `keyword`: The search query to analyze (required). Example: `"best project management software"`

## MCP Check

Before proceeding, verify MCPs are available:

**Primary check (required):**
1. Use ToolSearch with query `+ahrefs`
2. If tools returned → Ahrefs MCP is available, proceed to Execution
3. If no tools returned → display the Ahrefs MCP error template from
   `references/mcp-degradation.md` and stop

**Secondary check (non-blocking):**
1. Use ToolSearch with query `+webmcp`
2. If tools returned → note "WebMCP available — will enrich top 3 URLs with page titles"
3. If no tools returned → note "WebMCP not connected — running Ahrefs-only mode" and proceed

## Execution

**Step 1 — Discover serp-overview parameter schema**

Use ToolSearch with query `serp-overview` to inspect the tool definition and
discover its parameter names. The keyword parameter may be named `keyword`,
`query`, or `term` — do not assume. Use the exact parameter name found in the
schema for the call in Step 2.

**Step 2 — Call serp-overview**

Call `mcp__claude_ai_ahrefs__serp-overview` using the parameter name discovered
in Step 1 with the user's keyword as the value.

Returns: list of ranking pages with fields that may include `url`, `domain_rating`,
`traffic`, `traffic_cost`, `position`, `title`.

**Step 3 — WebMCP enrichment (only if WebMCP available from MCP Check)**

For the top 3 URLs from the SERP results, use WebMCP to fetch each page and
extract:
- Page `<title>` tag content
- First `<h1>` tag content

Use these to determine the content angle each top-ranking page is targeting.
If WebMCP is unavailable, skip this step entirely — do not attempt the calls.

**Step 4 — CRITICAL: Monetary conversion**

Any fields ending in `_cost`, `_value`, or `cpc` are returned in CENTS.
Divide by 100 before display. Format as USD with comma thousands separators.

Example: `traffic_cost = 125000` → display as `$1,250`

**Step 5 — SERP difficulty assessment**

Calculate average DR of the top 10 ranking pages. Use this scale:
- Average DR < 20 → "Low difficulty — achievable for new or low-authority sites"
- Average DR 20–40 → "Moderate difficulty — requires solid backlink profile"
- Average DR 41–60 → "High difficulty — needs established authority"
- Average DR > 60 → "Very high difficulty — major brands dominating SERP"

## Output Format

```
## SERP Analysis: "{keyword}"

**SERP Difficulty:** {assessment} (avg DR of top 10: {avg_dr})
**Data source:** Ahrefs serp-overview{, enriched via WebMCP | — Ahrefs-only mode}

### Ranking Pages

| Rank | URL | DR | Est. Traffic | Content Angle |
|------|-----|----|-------------|---------------|
| 1 | example.com/page-one... | 72 | 8,200 | {angle from WebMCP title/H1, or "N/A — Ahrefs-only"} |
| 2 | competitor.com/article... | 65 | 5,100 | {angle} |
| 3 | site.com/guide... | 58 | 3,400 | {angle} |
| 4 | domain.com/resource... | 71 | 2,900 | N/A |
| 5 | blog.com/post... | 44 | 1,800 | N/A |

*URLs truncated to 60 characters. {If WebMCP used: "Page titles enriched via WebMCP." If not: "Ahrefs-only mode — page titles from SERP data where available."}*

### Key Insights

- **Top competitor:** {highest-DR domain} (DR {score}) — {what makes them dominant}
- **Content pattern:** {what type of content dominates — guides, tool pages, listicles, etc.}
- **Traffic concentration:** Top 3 results capture ~{X}% of estimated SERP traffic
- **Opportunity signal:** {any lower-DR pages ranking — weakness in the SERP}

### Competitive Summary

{2–3 sentence synthesis: what the SERP looks like, who dominates, what content
type wins, and whether there's a realistic path to ranking for this keyword.}
```

## Error — Ahrefs MCP Not Available

If the Ahrefs MCP check fails, display this message and stop:

```
## Ahrefs MCP Not Available

The `/seo serp` command requires the Ahrefs MCP, which is not currently connected.

**What you can do:**
- Use `/seo audit <url>` for a full static SEO analysis without live SERP data
- Use `/seo technical <url>` for technical SEO issues without keyword data

**To connect Ahrefs MCP:**
- Ensure the Ahrefs MCP is registered at user scope in ~/.claude/mcp.json
- Verify with: cat ~/.claude/mcp.json | grep -i ahrefs
- Ahrefs MCP must be registered at user scope (not project scope) to work in subagents
```

## Error — WebMCP Degraded Mode

If WebMCP is unavailable, display this note (non-blocking — continue execution):

```
## WebMCP Not Available — Running Ahrefs-Only Mode

The `/seo serp` command works best with both Ahrefs and WebMCP, but WebMCP
is not currently connected. Proceeding with Ahrefs data only.

**What's reduced:**
- Content angle analysis for top 3 URLs (page titles and H1s will not be fetched)
- SERP table will show "N/A" for Content Angle column

**To connect WebMCP:**
- Verify WebMCP registration status in ~/.claude/mcp.json
```
