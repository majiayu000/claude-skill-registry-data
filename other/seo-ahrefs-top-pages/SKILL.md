---
name: seo-ahrefs-top-pages
description: >
  Find a domain's best performing pages by organic traffic from Ahrefs. Shows
  estimated traffic, traffic share, keyword count, and top keyword per page. Use
  when user says "top pages", "best pages", "highest traffic pages", "top
  performing pages", or "pages by traffic".
allowed-tools:
  - Read
  - Bash
  - ToolSearch
---

# Ahrefs Top Pages

Fetches the highest-traffic pages for a domain from Ahrefs, sorted by estimated
monthly traffic, with concentration risk analysis.

## References

@skills/seo/references/mcp-degradation.md
@skills/seo/references/ahrefs-api-reference.md

## Inputs

- `domain`: The bare domain to analyze (e.g., `example.com`). Strip `https://`,
  `http://`, and trailing slashes before passing to Ahrefs tools.

## MCP Check

Before proceeding, verify Ahrefs MCP is available:

1. Use ToolSearch with query `+ahrefs`
2. If tools are returned → Ahrefs MCP is available, proceed to Execution
3. If no tools returned → display the Ahrefs MCP error template from
   `references/mcp-degradation.md` and stop

## Execution

**Step 1 — Call Top Pages**

Call `mcp__claude_ai_ahrefs__site-explorer-top-pages` with:
- `target`: the bare domain (e.g., `example.com`)

Returns per page: `url`, `traffic` (estimated monthly visits), `traffic_percent`
(share of total site traffic), `keywords` (number of ranking keywords), `top_keyword`

**Step 2 — Sort and Analyze**

- Sort by `traffic` descending (highest-traffic pages first)
- Calculate cumulative traffic share of top 5 pages:
  - Sum `traffic_percent` for the top 5 pages
  - If any single page accounts for >30% of traffic → flag as concentration risk
  - If top 5 pages account for >70% of total traffic → flag as concentration risk

**Step 3 — Insights**

Note the top 5 pages and their combined traffic percentage. Identify concentration
risk and recommend diversification if needed.

## Output Format

```
## Ahrefs Top Pages: example.com

### Top Pages by Organic Traffic

| URL | Est. Monthly Traffic | Traffic % | Keywords | Top Keyword |
|-----|---------------------|-----------|----------|-------------|
| /blog/seo-guide | 12,400 | 23.1% | 340 | "seo guide" |
| /tools/keyword-research | 8,900 | 16.6% | 210 | "keyword research tool" |
| / (homepage) | 6,200 | 11.6% | 180 | "brand name" |
| /blog/backlinks | 4,100 | 7.7% | 95 | "how to build backlinks" |
| /pricing | 2,800 | 5.2% | 42 | "seo tool pricing" |

### Concentration Analysis
- **Top page share:** /blog/seo-guide = 23.1% of total traffic
- **Top 5 pages combined:** 64.2% of total site traffic

**Status:** MODERATE CONCENTRATION — top 5 pages drive 64.2% of traffic.
Consider expanding content across more pages to reduce dependency on a small
number of high-traffic URLs.

### Risk Assessment
- No single page exceeds 30% threshold (highest: 23.1%) — acceptable
- Top 5 pages at 64.2% is approaching concentration territory (threshold: 70%)
- Recommended: build 5-10 new high-value pages targeting mid-volume keywords to
  distribute traffic more evenly

### Summary
Total estimated monthly traffic: 53,600 visits across [X] indexed pages.
The top-performing page (/blog/seo-guide) drives 23.1% of all organic traffic
with 340 ranking keywords.
```

### High Concentration Warning

If top page `traffic_percent` > 30%, add:

```
CONCENTRATION RISK: /page accounts for [X]% of all organic traffic.
If this page loses rankings (algorithm update, content becomes outdated), overall
traffic could drop significantly. Priority action: replicate this page's success
by building more content targeting the same topic cluster.
```

### Error — Ahrefs MCP Not Available

If MCP check fails, display the Ahrefs error template from
`references/mcp-degradation.md`:

```
## Ahrefs MCP Not Available

The `/seo ahrefs top-pages` command requires the Ahrefs MCP, which is not
currently connected.

**What you can do:**
- Use `/seo audit <url>` for a full static SEO analysis without live Ahrefs data
- Use `/seo technical <url>` for technical SEO issues without backlink/keyword data

**To connect Ahrefs MCP:**
- Ensure the Ahrefs MCP is registered at user scope in ~/.claude/mcp.json
- Verify with: cat ~/.claude/mcp.json | grep -i ahrefs
- Ahrefs MCP must be registered at user scope (not project scope) to work in subagents
```
