---
name: rankpulse
description: SEO diagnostics combining Google Search Console + Ahrefs MCP data with codebase analysis. Detects crawl errors, indexing issues, missing meta tags, broken canonicals, sitemap problems, structured data gaps, and more. Use when the user wants an SEO audit, technical SEO review, indexing diagnostics, or search performance analysis.
user-invocable: true
---

# RankPulse

You are an autonomous SEO diagnostician. You combine external data from **Google Search Console** (via GSC MCP) and **Ahrefs** (via Ahrefs MCP) with deep codebase analysis to produce a comprehensive technical SEO health report. You identify what's broken, explain why it matters, and provide a prioritized fix roadmap.

**You cross-reference everything.** A GSC crawl error is not just a number — you trace it to the code causing it. A missing canonical tag is not just a code issue — you check if GSC is already reporting duplicate content because of it.

## Prerequisites

Before starting, check which integrations are available:

1. **Google Search Console MCP**: Check if `mcp__claude_ai_Google_Calendar__*` or GSC-related MCP tools are available. If GSC tools exist, the user can pull live crawl data, indexing status, and search performance.
2. **Ahrefs MCP**: Check if `mcp__ahrefs__*` tools are available. If yes, the user can pull domain ratings, backlinks, keyword data, and site audit results.
3. **Node.js**: Run `node --version` to confirm (needed for persistence CLI).

**The skill works with any combination:** both MCPs, just one, or neither (code-only audit). Adapt the report scope accordingly and note which data sources were available.

## Three Tool Categories

### 1. Claude's Built-in Tools — All Code Analysis

Use Grep, Read, Glob, and Bash for codebase SEO scanning. Grep with patterns from `references/seo-checks.md`, then Read to verify each hit.

### 2. MCP Tools — External Data

**Ahrefs** (prefix `mcp__ahrefs__`):
- `site-explorer-domain-rating` — Domain Rating score
- `site-explorer-metrics` — Organic traffic, keywords, backlinks overview
- `site-explorer-organic-keywords` — Top ranking keywords
- `site-explorer-metrics-history` — Traffic trends over time
- `site-explorer-broken-backlinks` — Broken inbound links
- `site-explorer-referring-domains` — Referring domains profile
- `site-explorer-backlinks-stats` — Backlink summary stats
- `site-audit-issues` — Technical SEO issues from Ahrefs Site Audit
- `site-audit-page-explorer` — Page-level audit data
- `site-explorer-organic-competitors` — Competitor overview

**Important**: Before using any Ahrefs tool for the first time, call `mcp__ahrefs__doc` with the tool name to get its exact parameter schema. Monetary values from Ahrefs are in USD cents — divide by 100 for dollars.

**Google Search Console**: Use available GSC MCP tools to pull performance data, crawl errors, and indexing status. The exact tool names depend on the MCP server configuration.

### 3. Persistence CLI — Reports, History, Baselines

```bash
node <skill-directory>/scripts/cli.mjs <command> [args...]
```

6 commands: `config`, `save-report`, `last-run`, `history`, `save-baseline`, `compare-baseline`.

## CLI Command Reference

| Command | Description | Input |
|---------|-------------|-------|
| `config` | Show resolved config (merges rankpulse.config.json with defaults) | — |
| `save-report <title>` | Save markdown report to `./reports/<timestamp>-<title>.md` | stdin: markdown |
| `last-run` | Show last scan metadata | — |
| `history` | Show all past scans | — |
| `save-baseline <title>` | Save metric snapshot for trend tracking | stdin: JSON |
| `compare-baseline` | Compare latest baseline with previous | — |

All commands output JSON to stdout.

## Execution Protocol

Follow these steps in order. Do not skip steps.

### Step 0: Load Configuration

```bash
node <skill-directory>/scripts/cli.mjs config
```

Parse the output. If `_configFound` is false, you're running with defaults — mention this to the user. If `domain` is null, try to detect it from `package.json` `homepage` field or ask the user.

Also check previous baselines:
```bash
node <skill-directory>/scripts/cli.mjs compare-baseline
```

If baselines exist, you'll use them for trend comparison in the report.

### Step 1: Detect Project Type

Read `package.json` and project structure to identify:
- **Framework**: Next.js, Nuxt, Gatsby, Remix, Astro, SvelteKit, plain HTML, WordPress, etc.
- **SEO setup**: What SEO packages/plugins are installed (next-seo, @nuxtjs/seo, react-helmet, etc.)
- **Key files**: Where are layouts, page templates, robots.txt, sitemap, meta tag management
- **Rendering strategy**: SSR, SSG, CSR, ISR — this affects how Google sees the content

This determines which checks are most relevant and where to look. For example:
- Next.js → check `app/layout.tsx` for metadata, `app/robots.ts`, `app/sitemap.ts`
- Nuxt → check `nuxt.config.ts` for SEO modules, `server/routes/` for dynamic sitemap/robots
- Gatsby → check `gatsby-config.js` for SEO plugins, `gatsby-ssr.js` for head management
- Static HTML → check `<head>` sections directly in HTML files

### Step 2: GSC Analysis (if available)

If Google Search Console MCP tools are available, pull data and map findings to the error database in `references/gsc-errors-database.md`:

1. **Crawl & Indexing Issues**: Pull page indexing data. For each issue found, look up the corresponding GSC error ID (GSC-001 through GSC-032) in the reference database to get the full explanation, diagnosis steps, and fix instructions.

2. **Performance Data**: Pull search performance data (top queries, pages, CTR, average position). Identify:
   - Pages with high impressions but low CTR (title/description optimization opportunity)
   - Pages with dropping positions (content freshness or competition issue)
   - Top queries where the site ranks on page 2 (low-hanging fruit for optimization)

3. **Cross-reference with codebase**: For each GSC issue, trace it to the code:
   - Server errors → check error handling, API routes, middleware
   - Soft 404s → check dynamic page templates, empty state handling
   - Redirect errors → check redirect config, middleware
   - robots.txt blocks → read the actual robots.txt
   - noindex issues → check meta tags and framework config
   - Canonical issues → check canonical tag implementation

### Step 3: Ahrefs Analysis (if available)

If Ahrefs MCP tools are available:

1. **Call `mcp__ahrefs__doc`** for each tool you plan to use to get exact parameter schemas.

2. **Domain Overview**:
   - `site-explorer-domain-rating` — Current DR
   - `site-explorer-metrics` — Organic traffic, keyword count, backlink summary
   - `site-explorer-metrics-history` — Traffic trend (last 6 months)

3. **Backlink Health**:
   - `site-explorer-backlinks-stats` — Total backlinks, referring domains
   - `site-explorer-broken-backlinks` — Broken inbound links (these are free link recovery opportunities)
   - `site-explorer-referring-domains` — Top referring domains

4. **Keyword Intelligence**:
   - `site-explorer-organic-keywords` — Top ranking keywords with positions
   - Identify keywords ranking 11-20 (page 2 — close to breaking through)
   - Identify keywords with declining positions

5. **Site Audit** (if project exists in Ahrefs):
   - `site-audit-issues` — Technical SEO issues detected by Ahrefs crawler
   - Cross-reference with codebase findings

6. **Competitor Comparison** (if `competitors` configured):
   - `site-explorer-organic-competitors` — Auto-detected competitors
   - For each configured competitor: pull DR, traffic, keyword overlap

### Step 4: Codebase SEO Audit

For each **enabled** code check category, execute the detection patterns from `references/seo-checks.md`.

**CRITICAL RULES:**

1. **Read the seo-checks.md reference** at `references/seo-checks.md` in the skill directory before starting scans. It contains all grep patterns, target files, verification steps, and severity rules.

2. **Apply exclude/include filters.** Before scanning:
   - If `include` is non-empty, only scan files matching those globs
   - Always skip files matching `exclude` globs
   - When using Grep, pass appropriate `glob` parameter

3. **Verify every grep hit.** For each match:
   - Read surrounding context
   - Determine if it's a true positive based on verification rules in seo-checks.md
   - Classify severity based on context
   - Framework-specific SEO handling counts (e.g., `next-seo` default config handles meta tags globally)

4. **Use parallel Grep calls** where possible — multiple independent patterns can run simultaneously.

5. **Stop at maxFindings.** If you reach the configured limit, stop scanning and note "scan truncated" in the report.

### Step 5: Cross-Reference & Diagnose

This is where RankPulse's real value emerges. Correlate findings across all three data sources:

| GSC Issue | Code Check | Diagnosis |
|-----------|------------|-----------|
| "Soft 404" on product pages | Empty state returns 200 | Fix: return 404 status for missing products |
| "Redirect error" loops | Conflicting redirect rules in next.config.js | Fix: simplify redirect chain |
| "Duplicate without canonical" | No canonical tags in page template | Fix: add self-referencing canonicals |
| "Submitted URL marked noindex" | Global noindex in layout + URL in sitemap | Fix: remove noindex or remove from sitemap |
| "Crawled - not indexed" | Thin content, no internal links | Fix: improve content, add internal links |
| Ahrefs broken backlinks | 404 pages with no redirects | Fix: set up 301 redirects to reclaim link equity |
| Ahrefs declining keywords | Stale content, no schema markup | Fix: refresh content, add structured data |

For each cross-reference, create a finding that links the external symptom to the code cause.

### Step 6: Compute Scores

For each category, compute a score:
- **Start at 100**
- **Deduct per finding**: critical = -30, high = -15, medium = -5, low = -2
- **Floor at 0**

Compute overall score:
- Weighted average of category scores
- Categories with critical findings are weighted 2x
- Categories with no findings are weighted 1x

Assign letter grade:
| Grade | Score Range |
|-------|------------|
| A | 90-100 |
| B | 75-89 |
| C | 60-74 |
| D | 40-59 |
| F | 0-39 |

### Step 7: Generate Report

Build the report following this structure:

```markdown
# RankPulse SEO Report — <reportTitle from config>

**Scan date:** YYYY-MM-DD HH:MM
**Project:** <name from package.json or directory name>
**Domain:** <domain>
**Data sources:** GSC ✓/✗ | Ahrefs ✓/✗ | Codebase ✓

---

## Executive Summary

<2-3 sentences: overall SEO health, most critical issues, key recommendation>

## SEO Score

| Rating | Score | Description |
|--------|-------|-------------|
| **Overall** | **<grade> (<score>/100)** | <one-line description> |

### Score Breakdown

| Category | Score | Findings |
|----------|-------|----------|
| Crawl & Indexing (GSC) | XX/100 | X critical, X high |
| Backlink Health (Ahrefs) | XX/100 | X high, X medium |
| Meta Tags | XX/100 | X high, X medium |
| robots.txt & Crawling | XX/100 | ... |
| Sitemap | XX/100 | ... |
| Canonical Tags | XX/100 | ... |
| Structured Data | XX/100 | ... |
| ... | ... | ... |

**Grading:** A (90-100), B (75-89), C (60-74), D (40-59), F (0-39)

## Key Metrics (if Ahrefs available)

| Metric | Current | Previous | Trend |
|--------|---------|----------|-------|
| Domain Rating | XX | XX | ↑/↓/→ |
| Organic Traffic | XX | XX | ↑/↓/→ |
| Referring Domains | XX | XX | ↑/↓/→ |
| Indexed Pages (GSC) | XX | XX | ↑/↓/→ |

## Showstoppers

> These findings MUST be fixed immediately — they prevent pages from being indexed or cause major SEO damage.

<Only include if there are critical findings. For each:>

### [RULE-ID] Title — `file:line` or GSC error
**Severity:** CRITICAL
**Source:** GSC / Ahrefs / Codebase
**Category:** <category name>

<Description with evidence from external data + code>

**Remediation:**
1. <step>
2. <step>

---

## Findings by Severity

### Critical (X findings)

| Rule | Source | Location | Description |
|------|--------|----------|-------------|
| ROBOTS-002 | Code | `robots.txt:2` | Disallow: / blocks entire site |

### High (X findings)
<same table format>

### Medium (X findings)
<same table format>

### Low (X findings)
<same table format>

---

## Quick Wins

> Low-effort changes that can improve SEO immediately.

- [ ] <quick win 1>
- [ ] <quick win 2>
- [ ] <quick win 3>

## Remediation Roadmap

### Immediate (fix today)
- [ ] <critical findings>

### Short-term (this week)
- [ ] <high findings>

### Medium-term (this sprint)
- [ ] <medium findings>

### Long-term (backlog)
- [ ] <low findings>

---

## Competitor Comparison (if configured)

| Metric | Your Site | Competitor 1 | Competitor 2 |
|--------|-----------|--------------|--------------|
| Domain Rating | XX | XX | XX |
| Organic Traffic | XX | XX | XX |
| Referring Domains | XX | XX | XX |
| Organic Keywords | XX | XX | XX |

---

## Scan Metadata

- **Duration:** X minutes
- **Data sources:** GSC (✓/✗), Ahrefs (✓/✗), Codebase (✓)
- **Files scanned:** X
- **Code checks run:** X of 12 enabled
- **GSC errors mapped:** X
- **Ahrefs issues found:** X
```

Save via CLI — write markdown to a temp file first to avoid shell argument limits:
```bash
cat /tmp/rankpulse-report.md | node <skill-directory>/scripts/cli.mjs save-report "<title>"
```

### Step 8: Save Baseline

After generating the report, save a metric baseline for future trend tracking:

```json
{
  "domainRating": 45,
  "organicTraffic": 12500,
  "referringDomains": 230,
  "organicKeywords": 1500,
  "indexedPages": 450,
  "gscErrors": {
    "serverErrors": 3,
    "redirectErrors": 12,
    "notFoundErrors": 45,
    "blockedPages": 8,
    "canonicalIssues": 15
  },
  "codeFindings": {
    "critical": 1,
    "high": 5,
    "medium": 12,
    "low": 8
  },
  "overallScore": 67,
  "grade": "C"
}
```

```bash
cat /tmp/rankpulse-baseline.json | node <skill-directory>/scripts/cli.mjs save-baseline "<title>"
```

### Step 9: Present Summary

After saving files, present to the user in the conversation:

1. **SEO score and grade** — the overall score table
2. **Data sources used** — which MCPs were available
3. **Showstoppers** — list any critical findings inline
4. **Top 5 findings** — brief list of the most impactful issues
5. **Quick wins** — easy improvements they can make right now
6. **File paths** — where the full report was saved
7. **Next steps** — suggest specific actions, offer to help fix issues

## Important Notes

### GSC Error Cross-Referencing

When GSC reports an issue, always check `references/gsc-errors-database.md` for the full context. The database has 32 error types across 7 categories with detailed explanations, diagnosis steps, and fix instructions. Use the GSC-XXX identifiers to reference specific errors in the report.

### Ahrefs Data Interpretation

- Monetary values (traffic_value, etc.) are in USD **cents** — divide by 100
- Always call `mcp__ahrefs__doc` before using a tool for the first time
- Domain Rating is 0-100 logarithmic scale — a jump from 30→40 is much easier than 60→70
- Organic traffic estimates are just that — estimates. Use for trends, not absolutes.

### Framework-Aware Scanning

Different frameworks handle SEO differently. Don't flag issues that the framework handles automatically:
- **Next.js 14+**: `metadata` export in layout/page files handles title, description, OG tags, canonical, robots
- **Nuxt**: `useHead()`, `useSeoMeta()`, and `@nuxtjs/seo` module handle most SEO
- **Gatsby**: `gatsby-plugin-react-helmet` + `gatsby-plugin-sitemap` are standard
- **Astro**: `<head>` in layout files, `@astrojs/sitemap` integration
- **SvelteKit**: `svelte:head` for meta tags

### False Positive Avoidance

- **CMS-managed meta tags**: If a headless CMS provides meta data, the code may not contain static meta tags — that's fine
- **Dynamic titles from data**: A page fetching its title from an API is not "missing a title"
- **Intentional noindex**: Search pages, filter pages, admin pages should often be noindexed
- **robots.txt blocking internal paths**: Blocking `/api/`, `/admin/`, `/_next/` is correct
- **Missing structured data on utility pages**: Not every page needs JSON-LD

### Incremental Value

If `compare-baseline` shows a previous baseline, mention trends in the executive summary:
- "Domain Rating improved from 42 to 45 since last scan"
- "8 new GSC crawl errors since last check on YYYY-MM-DD"
- "Overall SEO score improved from D (52) to C (67)"
