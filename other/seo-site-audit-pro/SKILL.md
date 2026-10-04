---
name: seo-site-audit-pro
description: >
  Flagship comprehensive SEO audit combining Ahrefs and GSC data in sequential
  waves with checkpoint saves. Use when user says "site audit pro", "full audit",
  "comprehensive audit", "audit with live data", "deep audit", "pro audit",
  "complete SEO audit", "run a full site audit", or "audit everything for this domain".
  Requires domain param. Optional: site param for GSC overlay.
allowed-tools:
  - Read
  - Bash
  - ToolSearch
  - Write
---

# Site Audit Pro — Sequential Wave Multi-MCP Audit

Flagship audit combining Ahrefs and GSC data across 3 sequential waves with
checkpoint saves to disk. Designed to be resilient to rate-limit errors — each
tool call is independent, skipped tools are logged, and the audit always completes.

LOCKED DECISION (GitHub Issue #6594): Sequential wave execution only. Do NOT
parallelize tool calls. Do NOT spawn subagents. All tool calls are inline.

## References

@skills/seo/references/mcp-degradation.md
@skills/seo/references/ahrefs-api-reference.md
@skills/seo/references/gsc-api-reference.md

## Inputs

- `domain`: Bare domain to audit (required). Example: `example.com`. Strip `https://`, `http://`, and trailing slashes before use.
- `site` (optional): GSC property URL to include GSC data in the audit. Example: `https://example.com` or `sc-domain:example.com`. If not provided, audit runs Ahrefs-only.

## Important: API Usage Warning

**Before starting execution, display this notice to the user:**

> **API Usage Notice:** This command calls approximately 10–12 Ahrefs API tools
> sequentially. Each call consumes API units from your Ahrefs account. You can
> stop after any wave if budget is a concern. Estimated time: 3 waves × 1–2
> minutes each = 3–6 minutes total. Wave breakdown:
> - **Wave 1:** Domain Authority and Backlink Health (4 tool calls)
> - **Wave 2:** Keyword and Competitive Position (3–4 tool calls)
> - **Wave 3:** Content and Technical Insights (3–4 tool calls)

## MCP Check

Before proceeding, verify MCP availability:

**Ahrefs (required):**
1. Use ToolSearch with query `+ahrefs`
2. If tools returned → Ahrefs MCP available, proceed
3. If no tools returned → display the Ahrefs error template (see Error section below) and stop

**GSC (optional — only relevant if `site` param was provided):**
1. Use ToolSearch with query `+google-search-console`
2. If tools returned → note "GSC MCP available — will include GSC overlay in Waves 2 and 3"
3. If no tools returned AND `site` param was provided → note "GSC MCP unavailable — audit will use Ahrefs data only, GSC overlay skipped" and continue
4. If `site` param was NOT provided → skip GSC check entirely

## Architecture

This command uses SEQUENTIAL wave execution with checkpoint saves between waves.

**Critical design rules:**
- Each tool call runs ONE AT A TIME — never in parallel
- Results from each tool are stored before proceeding to the next
- After each wave completes, all results are written to a checkpoint file on disk
- If a tool returns a rate-limit error or any error: log as `SKIPPED: {tool-name} — {reason}` and continue to the next tool immediately
- A failed tool call NEVER stops the wave or the audit
- The final report lists all skipped data sources so the user knows what's missing

This pattern prevents cascade failures from shared AbortController state (GitHub Issue #6594).

## Execution

### Step 0 — Initialize Checkpoint File

Use Bash to resolve the absolute path for the checkpoint file:
```bash
echo "$(pwd)/seo-audit-pro-checkpoint-{domain}.md"
```

Use the Write tool to create the initial checkpoint file at that path:
```
# Site Audit Pro: {domain}
**Started:** {current date and time}
**Status:** In progress
**Waves:** 0 of 3 complete

---
```

Tell the user: "Checkpoint file created. Starting Wave 1..."

---

### Wave 1 — Domain Authority and Backlink Health

Run each tool call sequentially. For each: if success → store result. If error
of any kind → log `SKIPPED: {tool-name} — {error reason}` and immediately move
to the next tool. NEVER stop the wave because one tool failed.

**Tool call 1a — Site Metrics:**
Call `mcp__claude_ai_ahrefs__site-explorer-metrics` with:
- `target`: {domain}

Returns: `organic_traffic`, `traffic_cost` (CENTS — divide by 100 for USD),
`organic_keywords`, `backlinks`, `referring_domains`

Store result as Wave1_Metrics. If error: log `SKIPPED: site-explorer-metrics — {reason}`

**Tool call 1b — Domain Rating:**
Call `mcp__claude_ai_ahrefs__site-explorer-domain-rating` with:
- `target`: {domain}

Returns: `domain_rating` (0–100), `ahrefs_rank`

Store result as Wave1_DR. If error: log `SKIPPED: site-explorer-domain-rating — {reason}`

**Tool call 1c — All Backlinks (top 20):**
Call `mcp__claude_ai_ahrefs__site-explorer-all-backlinks` with:
- `target`: {domain}
- Limit/top results to 20

Returns: list of backlinks with source domain, anchor text, DR, link type

Store result as Wave1_Backlinks. If error: log `SKIPPED: site-explorer-all-backlinks — {reason}`

**Tool call 1d — Broken Backlinks:**
Call `mcp__claude_ai_ahrefs__site-explorer-broken-backlinks` with:
- `target`: {domain}

Returns: backlinks pointing to 404/broken pages on the domain

Store result as Wave1_BrokenLinks. If error: log `SKIPPED: site-explorer-broken-backlinks — {reason}`

**Wave 1 Checkpoint Save:**
Use the Write tool to APPEND Wave 1 results to the checkpoint file:
```
## Wave 1 Results — Domain Authority and Backlink Health
**Completed:** {timestamp}

### Metrics
{Wave1_Metrics data or "SKIPPED: {reason}"}

### Domain Rating
{Wave1_DR data or "SKIPPED: {reason}"}

### Top Backlinks (up to 20)
{Wave1_Backlinks data or "SKIPPED: {reason}"}

### Broken Backlinks
{Wave1_BrokenLinks data or "SKIPPED: {reason}"}

---
```

Tell the user: "Wave 1 complete (Domain Authority & Backlinks). Checkpoint saved. Starting Wave 2..."

---

### Wave 2 — Keyword and Competitive Position

**Tool call 2a — Organic Keywords (top 20):**
Call `mcp__claude_ai_ahrefs__site-explorer-organic-keywords` with:
- `target`: {domain}
- Limit to top 20 results

Returns: list of keywords with position, volume, traffic, difficulty

Store result as Wave2_Keywords. If error: log `SKIPPED: site-explorer-organic-keywords — {reason}`

**Tool call 2b — Organic Competitors:**
Call `mcp__claude_ai_ahrefs__site-explorer-organic-competitors` with:
- `target`: {domain}

Returns: list of competing domains with overlap score, common keywords, their traffic

Store result as Wave2_Competitors. If error: log `SKIPPED: site-explorer-organic-competitors — {reason}`

**Tool call 2c — Content Gap via Keywords Explorer:**
Using the top competitor identified from Wave2_Competitors (or skip if Wave2_Competitors was skipped):

First, use ToolSearch with query `keywords-explorer-matching-terms` to discover
the exact parameter schema for this tool. Do NOT assume parameter names.

Then call `mcp__claude_ai_ahrefs__keywords-explorer-matching-terms` using the
competitor domain as the seed to find content gap keywords.

Store result as Wave2_ContentGap. If error: log `SKIPPED: keywords-explorer-matching-terms — {reason}`

**Tool call 2d — GSC Query Analytics (only if `site` param provided AND GSC MCP available):**
If GSC is available and `site` param was given:
Call the GSC `query_search_analytics` tool (use ToolSearch "+google-search-console"
to find the exact tool name first) with:
- Site/property: {site}
- Row limit: 20
- Dimensions: query
- Sort by: clicks descending

Returns: top queries by clicks with impressions, CTR, average position

Note: CTR is returned as a decimal (e.g., 0.0523). Multiply by 100 for display (5.23%).

Store result as Wave2_GSC. If error or GSC unavailable: log `SKIPPED: GSC query_search_analytics — {reason}`

**Wave 2 Checkpoint Save:**
Use the Write tool to APPEND Wave 2 results to the checkpoint file:
```
## Wave 2 Results — Keyword and Competitive Position
**Completed:** {timestamp}

### Organic Keywords (top 20)
{Wave2_Keywords data or "SKIPPED: {reason}"}

### Organic Competitors
{Wave2_Competitors data or "SKIPPED: {reason}"}

### Content Gap (keywords competitor ranks for, you don't)
{Wave2_ContentGap data or "SKIPPED: {reason}"}

### GSC Query Analytics (top queries by clicks)
{Wave2_GSC data or "SKIPPED: not requested or GSC unavailable"}

---
```

Tell the user: "Wave 2 complete (Keywords & Competition). Checkpoint saved. Starting Wave 3..."

---

### Wave 3 — Content and Technical Insights

**Tool call 3a — GSC Opportunities (only if GSC available):**
If GSC MCP is available and `site` param was provided:
Use ToolSearch to find the GSC search analytics tool. Call it with:
- Site/property: {site}
- Filter: high impressions (e.g., > 1000), low CTR (e.g., < 0.05)
- Row limit: 20

This identifies pages/queries with visibility but poor click-through rate.

Store result as Wave3_GSC_Opportunities. If error or GSC unavailable: log `SKIPPED: GSC opportunities — {reason}`

**Tool call 3b — GSC Traffic Drops (only if GSC available):**
If GSC MCP is available and `site` param was provided:
Call GSC search analytics comparing last 28 days vs previous 28 days:
- Site/property: {site}
- Date range: last 28 days vs prior 28 days
- Sort by: click decline

Store result as Wave3_GSC_Drops. If error or GSC unavailable: log `SKIPPED: GSC drops — {reason}`

**Tool call 3c — Top Pages (top 10):**
Call `mcp__claude_ai_ahrefs__site-explorer-top-pages` with:
- `target`: {domain}
- Limit to top 10

Returns: top organic pages by estimated traffic

Store result as Wave3_TopPages. If error: log `SKIPPED: site-explorer-top-pages — {reason}`

**Tool call 3d — Anchor Text:**
Call `mcp__claude_ai_ahrefs__site-explorer-anchors` with:
- `target`: {domain}

Returns: anchor text distribution with count and percentage

Store result as Wave3_Anchors. If error: log `SKIPPED: site-explorer-anchors — {reason}`

**Wave 3 Checkpoint Save:**
Use the Write tool to APPEND Wave 3 results to the checkpoint file:
```
## Wave 3 Results — Content and Technical Insights
**Completed:** {timestamp}
**Status:** All waves complete

### GSC Opportunities (high impressions, low CTR)
{Wave3_GSC_Opportunities data or "SKIPPED: not requested or GSC unavailable"}

### GSC Traffic Drops (last 28 days)
{Wave3_GSC_Drops data or "SKIPPED: not requested or GSC unavailable"}

### Top Pages (by organic traffic)
{Wave3_TopPages data or "SKIPPED: {reason}"}

### Anchor Text Distribution
{Wave3_Anchors data or "SKIPPED: {reason}"}

---
```

Tell the user: "Wave 3 complete (Content & Technical). All waves done. Generating final report..."

---

### Step Final — Cross-MCP Synthesis and Final Report

Read back all stored wave data. Generate the comprehensive audit report below.
Print the full report to the terminal.

**CRITICAL monetary conversion:** All Ahrefs fields ending in `_cost`, `_value`,
or `cpc` are in CENTS. Divide by 100 before display. Format as USD with commas.
Example: `traffic_cost = 125000` → display as `$1,250`

**CTR conversion:** GSC CTR values are decimals. Multiply by 100 for display.
Example: `ctr = 0.0523` → display as `5.23%`

---

```
# Site Audit Pro: {domain}
**Date:** {current date}
**Waves completed:** 3 of 3
**Data sources:** Ahrefs{, Google Search Console (via {site})}
**Checkpoint file:** {absolute path to checkpoint file}

---

## Executive Summary

{AI-generated 3–5 sentence analysis of the domain's overall SEO health based
on all collected data. Synthesize DR, traffic, keyword position, content gaps,
and GSC performance into a coherent narrative. Be specific — use actual numbers
from the data.}

---

## Domain Authority Profile

| Metric | Value |
|--------|-------|
| Domain Rating | {domain_rating}/100 |
| Ahrefs Rank | #{ahrefs_rank} |
| Total Backlinks | {backlinks} |
| Referring Domains | {referring_domains} |
| Organic Keywords | {organic_keywords} |
| Est. Monthly Traffic | {organic_traffic} visits |
| Traffic Value | ${traffic_cost / 100}/mo |

{If any metrics were SKIPPED, note which ones and why.}

---

## Backlink Health

### Top Backlinks (up to 20)
{Table with source URL, anchor text, DR, link type from Wave1_Backlinks}
{Or: "Data unavailable — site-explorer-all-backlinks was skipped ({reason})"}

### Broken Backlinks (Reclamation Opportunities)
{List of backlinks pointing to broken pages, with source domain and target URL}
{Or: "Data unavailable — site-explorer-broken-backlinks was skipped ({reason})"}
{If broken links exist: "**Action:** Redirect or restore these {N} broken pages to reclaim link equity."}

---

## Keyword Portfolio

### Top Organic Keywords (by traffic)
{Table: keyword | position | volume | est. traffic from Wave2_Keywords}
{Or: "Data unavailable — site-explorer-organic-keywords was skipped ({reason})"}

### Organic Competitors
{Table: competitor domain | overlap score | common keywords | their organic traffic}
{Or: "Data unavailable — site-explorer-organic-competitors was skipped ({reason})"}

---

## Content Gaps

Keywords top competitors rank for that {domain} does not currently rank for:

{Table or list from Wave2_ContentGap}
{Or: "Data unavailable — keywords-explorer-matching-terms was skipped ({reason})"}

{If data available: Highlight top 5 highest-value gap keywords with estimated volume.}

---

## GSC Performance

{ONLY include this section if Wave2_GSC or Wave3_GSC_Opportunities or Wave3_GSC_Drops has data.
If no GSC data was collected, replace this entire section with:
"*GSC data not included — either no `site` parameter was provided or GSC MCP was unavailable.*"}

### Top Queries (by clicks)
{Table: query | clicks | impressions | CTR (×100%) | avg position from Wave2_GSC}

### Click-Through Opportunities
{Queries/pages with high impressions but low CTR from Wave3_GSC_Opportunities}
{Include suggested action: "Improve title/meta description for better CTR"}

### Traffic Drops (last 28 days)
{Pages or queries showing declining clicks from Wave3_GSC_Drops}

---

## Top Pages Analysis

{Table: page URL | est. organic traffic | top keyword from Wave3_TopPages}
{Or: "Data unavailable — site-explorer-top-pages was skipped ({reason})"}

{If data available: Note which pages drive disproportionate traffic and any concentration risk.}

---

## Anchor Text Profile

{Summary of anchor text distribution: branded vs. exact-match vs. generic vs. naked URLs}
{Raw data from Wave3_Anchors}
{Thresholds: branded >40% = healthy; exact-match >10% = over-optimized risk; generic >30% = low-quality signal}
{Or: "Data unavailable — site-explorer-anchors was skipped ({reason})"}

---

## Cross-MCP Insights

{ONLY include this section when BOTH Ahrefs AND GSC data are present in the report.
If only one data source was available, omit this section entirely.}

{Generate 3–5 specific insights that REQUIRE both data sources to identify. Examples:}

- "You rank #{GSC_position} for '{GSC_keyword}' per GSC but Ahrefs shows {N} competitors
  with DR {X}+ points higher — this is a priority opportunity where improving content
  quality could yield significant ranking gains"
- "GSC shows traffic declining for {page} but Ahrefs shows {N} new backlinks this month
  — possible algorithm volatility, not link loss. Monitor for 2 more weeks before acting."
- "Top organic keyword per GSC has {clicks} clicks but Ahrefs estimates {traffic} monthly
  traffic for this keyword — gap suggests click-through rate optimization opportunity"
- "Content gap keyword '{keyword}' (competitor ranks #{position}) correlates with GSC
  impressions for related term '{related}' — you have some visibility; targeted content
  could convert impressions to rankings"

{Each insight should be actionable and specific to the actual data collected.}

---

## Skipped Data Sources

{If ALL tools completed successfully: "None — all data sources returned successfully."}

{If any tools were skipped:}

| Tool | Reason Skipped |
|------|---------------|
| {tool-name} | {error reason — rate limit / error / not requested} |

*Skipped tools mean those report sections are incomplete. Re-run the audit when
API limits reset, or use individual `/seo ahrefs {command}` commands for specific data.*

---

## Prioritized Recommendations

Based on all available data, here are the top action items:

**Critical (address immediately):**
1. {Recommendation based on actual findings}

**High Priority (this week):**
2. {Recommendation}
3. {Recommendation}

**Medium Priority (this month):**
4. {Recommendation}
5. {Recommendation}

**Monitoring:**
- {Ongoing items to watch}

---

*Full data checkpoint saved to: {absolute path to checkpoint file}*
*Re-run this audit monthly to track progress.*
```

---

## Output Format

The full report is printed to the terminal. The checkpoint file remains on disk
at the path shown in the report header. Unlike `seo-report`, this command does
NOT save the final report to a file — the checkpoint file is the on-disk artifact.

---

## Error — Ahrefs MCP Not Available

If the Ahrefs MCP check fails, display this message and stop:

```
## Ahrefs MCP Not Available

The `/seo site-audit-pro` command requires the Ahrefs MCP, which is not
currently connected.

**What you can do:**
- Use `/seo audit <url>` for a full static SEO analysis without live Ahrefs data
- Use `/seo ahrefs overview <domain>` once Ahrefs is connected for a quick domain check

**To connect Ahrefs MCP:**
- Ensure the Ahrefs MCP is registered at user scope in ~/.claude/mcp.json
- Verify with: cat ~/.claude/mcp.json | grep -i ahrefs
- Ahrefs MCP must be registered at user scope (not project scope) to work in subagents
```

## Error — GSC Unavailable (Non-Fatal)

If GSC MCP is unavailable but `site` param was provided:

```
**Note:** GSC MCP is not available. The audit will proceed using Ahrefs data only.
GSC-dependent sections (GSC Performance, Traffic Drops, CTR Opportunities) will
show "Data unavailable — GSC not connected." The Cross-MCP Insights section will
be omitted. All Ahrefs waves will run normally.
```

Continue execution — this is NOT a stop condition.
