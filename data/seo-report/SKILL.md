---
name: seo-report
description: >
  Generate and save a complete SEO report to disk. Use when user says "SEO report",
  "generate report", "monthly report", "weekly report", "audit report",
  "competitor report", "save report", "export SEO data", "create SEO summary",
  "export my SEO data", "save Ahrefs report", "download SEO report".
  Requires report type: monthly | weekly | audit | competitor.
allowed-tools:
  - Read
  - Bash
  - ToolSearch
  - Write
---

# SEO Report Generator — File-Persisted Reports

Generates complete, AI-analyzed SEO reports and saves them to disk as markdown files.
Supports four report types: monthly, weekly, audit, and competitor. This is the first
sub-skill in the project that uses the Write tool for file persistence.

## References

@skills/seo/references/mcp-degradation.md
@skills/seo/references/ahrefs-api-reference.md
@skills/seo/references/gsc-api-reference.md

## Inputs

- `type`: Report type — one of: `monthly`, `weekly`, `audit`, `competitor` (required)
- `domain`: The domain to report on, bare domain e.g. `example.com` (required).
  Strip `https://`, `http://`, and trailing slashes.
- `site` (optional): GSC property URL for including Google Search Console data.
  Format: `https://example.com/` or `sc-domain:example.com`
- `competitor` (optional, required for `competitor` type): Competitor domain to
  compare against, e.g. `competitor.com`
- `output_dir` (optional): Directory path to save the report file.
  Default: current working directory (pwd).

## MCP Check

Before proceeding, check MCP availability:

1. **Ahrefs (required for all report types):**
   Use ToolSearch with query `+ahrefs`
   - If tools returned → Ahrefs available, proceed
   - If no tools returned → display Ahrefs error template from mcp-degradation.md and stop

2. **GSC (optional — only if `site` parameter is provided):**
   Use ToolSearch with query `+google-search-console`
   - If tools returned → GSC available, include GSC data in report
   - If no tools returned → continue with Ahrefs-only, note missing GSC data in report

## Execution

### Step 0 — Generate Filename and Resolve Output Path

Use Bash to generate the absolute file path:
```bash
echo "$(pwd)/seo-report-$(date +%Y-%m-%d)-{domain}-{type}.md"
```

If `output_dir` is provided, replace `$(pwd)` with the provided directory path.
Store this absolute path — it is used in Step 4 (Write) and Step 5 (confirmation).

Filename convention: `seo-report-YYYY-MM-DD-domain-type.md`
Example: `seo-report-2026-03-02-example.com-monthly.md`

### Step 1 — Gather Data (varies by report type)

For each tool call: if a rate-limit error or tool-not-found error occurs, log
`Data unavailable: {tool} — {error}` and continue. The report notes all skipped
data sources clearly.

---

#### Monthly Report Data

**a) Ahrefs Overview:**
- Call `mcp__claude_ai_ahrefs__site-explorer-metrics` with `target: {domain}`
  Returns: organic_traffic, traffic_cost (CENTS — divide by 100), organic_keywords,
  backlinks, referring_domains
- Call `mcp__claude_ai_ahrefs__site-explorer-domain-rating` with `target: {domain}`
  Returns: domain_rating (0-100), ahrefs_rank

**b) Ahrefs Top Keywords:**
- Call `mcp__claude_ai_ahrefs__site-explorer-organic-keywords` with `target: {domain}`
  Request top 20 results. Returns: keyword, position, traffic, volume, difficulty.

**c) Ahrefs DR History:**
- Call `mcp__claude_ai_ahrefs__site-explorer-domain-rating-history` with `target: {domain}`
  Request last 12 months. Returns: date series with domain_rating values.

**d) GSC Month-over-Month (only if `site` provided and GSC available):**
- Query `query_search_analytics` (or equivalent GSC tool discovered via ToolSearch)
  for current month vs previous month.
  Compare: clicks, impressions, CTR, average position.
  CTR from GSC is a decimal — multiply by 100 for display (0.0523 → 5.23%).

---

#### Weekly Report Data

**a) GSC Traffic Drops (only if `site` provided and GSC available):**
- Query GSC search analytics for last 7 days vs prior 7 days.
  Identify pages/queries with significant traffic decline (>20% drop).
  CTR is decimal — multiply by 100 for display.

**b) GSC Opportunities (only if `site` provided and GSC available):**
- Query GSC for queries with high impressions (>100/week) and low CTR (<5%).
  These are quick-win opportunities.
  CTR is decimal — multiply by 100 for display.

**c) Ahrefs New Referring Domains:**
- Call `mcp__claude_ai_ahrefs__site-explorer-referring-domains` with `target: {domain}`
  Filter or sort by date to surface domains added in the last 7 days.
  Note: If the tool lacks a native date filter, sort by first_seen descending and
  take entries from the last 7 days based on the first_seen field.

---

#### Audit Report Data

**a) Ahrefs Overview:**
- Same as Monthly step (a) above — site-explorer-metrics + domain-rating.

**b) Ahrefs Backlinks:**
- Call `mcp__claude_ai_ahrefs__site-explorer-all-backlinks` with `target: {domain}`
  Request top 20. Returns: source URL, anchor text, DR of source, dofollow status.

**c) Ahrefs Broken Backlinks:**
- Call `mcp__claude_ai_ahrefs__site-explorer-broken-backlinks` with `target: {domain}`
  Returns: source URLs linking to 404/gone pages — reclamation opportunities.

**d) Ahrefs Anchor Analysis:**
- Call `mcp__claude_ai_ahrefs__site-explorer-anchors` with `target: {domain}`
  Returns: anchor text distribution — identify over-optimized exact-match patterns.

**e) Ahrefs Top Pages:**
- Call `mcp__claude_ai_ahrefs__site-explorer-top-pages` with `target: {domain}`
  Request top 10. Returns: URL, organic traffic, keywords count, top keyword.

---

#### Competitor Report Data

**a) Ahrefs Overview — Both Domains:**
- Call site-explorer-metrics + domain-rating for BOTH `{domain}` and `{competitor}`.
  Display side-by-side for comparison.

**b) Ahrefs Organic Competitors:**
- Call `mcp__claude_ai_ahrefs__site-explorer-organic-competitors` with `target: {domain}`
  Returns: list of organic competitors with overlap metrics.

**c) Ahrefs Content Gap:**
- Call `mcp__claude_ai_ahrefs__keywords-explorer-matching-terms` with filters to
  find keywords where competitor ranks but domain does not.
  Note: Use ToolSearch to discover this tool's exact parameter schema first if
  content-gap filtering is not straightforward.

**d) Ahrefs Anchor Analysis — Both Domains:**
- Call site-explorer-anchors for BOTH `{domain}` and `{competitor}`.
  Compare anchor text strategies.

---

### Step 2 — Generate AI Executive Summary

Before assembling the report, analyze ALL gathered data and write an executive
summary paragraph of 3-5 sentences that:
1. Identifies the single most important finding from the data
2. Interprets what the data patterns mean for the domain's SEO health
3. Suggests one concrete priority action

This is NOT a raw data dump. It is Claude's analytical interpretation.

Example for monthly: "Domain authority has grown from DR 45 to DR 52 over the past
6 months, driven primarily by 340 new referring domains. However, organic traffic
declined 12% month-over-month, suggesting a potential Google algorithm impact on
the /blog section which lost 8 high-ranking positions. Priority: Investigate the
traffic drop using `/seo gsc drops` for affected pages before making any content
changes."

### Step 3 — Assemble Report Document

Build the full markdown report with sections appropriate to the report type:

```
# SEO {Type} Report: {domain}
**Generated:** {date}
**Report Type:** {type}
**Data Sources:** {list of MCPs actually used, e.g. "Ahrefs, Google Search Console"}
**Covers:** {date range, e.g. "Last 30 days" or "Month-over-month comparison"}

---

## Executive Summary

{AI-generated narrative from Step 2}

---

## {Section per data source gathered — use appropriate headings per report type}

{Tables with actual data}

{For monetary values: ALL Ahrefs cost/value fields are in CENTS — divide by 100 and
display as $X,XXX before including in report}

---

## Data Gaps

{List any tools that were skipped due to errors or unavailable MCPs}
{If no gaps: "All requested data sources returned successfully."}

---
*Generated by /seo report — Claude SEO Skill*
*Data sources: {Ahrefs | Google Search Console | both}*
*Timestamp: {ISO 8601 timestamp}*
```

### Step 4 — Save Report to Disk

Use the Write tool:
- `file_path`: the absolute path generated in Step 0
- `content`: the complete markdown report from Step 3

### Step 5 — Confirm to User

After Write completes, output to terminal:

```
Report saved to: {absolute_file_path}

Summary: {N} sections covering {data sources used}
Report type: {type} | Domain: {domain}
```

CRITICAL: Always print the FULL ABSOLUTE PATH so the user can locate the file.
The report content is NOT printed to the terminal — it is in the saved file only.

## Output Format

Terminal output is the save confirmation only (Step 5). The full report is in the
saved markdown file. Do NOT print the report contents to the terminal.

Example terminal output:
```
Report saved to: /Users/username/projects/seo-report-2026-03-02-example.com-monthly.md

Summary: 5 sections covering Ahrefs (DR history, keywords, overview) and GSC (MoM comparison)
Report type: monthly | Domain: example.com
```

## Error — Ahrefs MCP Not Available

```
## Ahrefs MCP Not Available

The `/seo report` command requires the Ahrefs MCP, which is not currently connected.
All report types depend on Ahrefs data as their primary data source.

**What you can do:**
- Use `/seo audit <url>` for a full static SEO analysis without live Ahrefs data
- Use `/seo technical <url>` for technical SEO issues analysis

**To connect Ahrefs MCP:**
- Ensure the Ahrefs MCP is registered at user scope in ~/.claude/mcp.json
- Verify with: cat ~/.claude/mcp.json | grep -i ahrefs
- Ahrefs MCP must be registered at user scope (not project scope) to work in subagents
```

## Error — GSC Not Available (Non-Fatal)

When `site` parameter is provided but GSC MCP is not available, do NOT stop.
Continue with Ahrefs-only data and include this note in the report:

```
## Google Search Console Data
**Status:** GSC MCP not connected — GSC data excluded from this report.
To include GSC data, connect the GSC MCP and re-run with the `site` parameter.
```
