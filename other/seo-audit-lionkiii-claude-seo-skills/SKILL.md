---
name: seo-audit
description: >
  Full website SEO audit with parallel subagent delegation. Crawls up to 500
  pages, detects business type, delegates to up to 7 specialists, generates health
  score. Enhanced with live Ahrefs (DR, backlinks, traffic) and GSC (indexing,
  top pages) data when MCPs are available. Use when user says "audit", "full
  SEO check", "analyze my site", or "website health check".
allowed-tools:
  - Read
  - Bash
  - Glob
  - WebFetch
  - ToolSearch
---

# Full Website SEO Audit

<!-- Updated: 2026-06-10 -->

## Process

0. **Load reference** — read `seo/references/google-seo-guide.md` for category-aligned checks
1. **Fetch homepage** — use `scripts/fetch_page.py` to retrieve HTML
2. **Detect business type** — analyze homepage signals per seo orchestrator
3. **Crawl site** — follow internal links up to 500 pages, respect robots.txt
4. **Delegate to subagents** (if available, otherwise run inline sequentially):
   - `seo-technical` — robots.txt, sitemaps, canonicals, Core Web Vitals, security headers
   - `seo-content` — E-E-A-T, readability, thin content, AI citation readiness
   - `seo-schema` — detection, validation, generation recommendations
   - `seo-sitemap` — structure analysis, quality gates, missing pages
   - `seo-performance` — LCP, INP, CLS measurements
   - `seo-visual` — screenshots, mobile testing, above-fold analysis
   - `seo-ai-optimization` — AI search readiness (AI Overviews eligibility, llms.txt, AI crawler access) (if installed)
5. **Score** — aggregate into SEO Health Score (0-100)
6. **Report** — generate prioritized action plan

## Crawl Configuration

```
Max pages: 500
Respect robots.txt: Yes
Follow redirects: Yes (max 3 hops)
Timeout per page: 30 seconds
Concurrent requests: 5
Delay between requests: 1 second
```

## Output Files

- `FULL-AUDIT-REPORT.md` — Comprehensive findings
- `ACTION-PLAN.md` — Prioritized recommendations (Critical → High → Medium → Low)
- `screenshots/` — Desktop + mobile captures (if Playwright available)

## Scoring Weights

| Category | Weight |
|----------|--------|
| Technical SEO | 25% |
| Content Quality | 25% |
| On-Page SEO | 20% |
| Schema / Structured Data | 10% |
| Performance (CWV) | 10% |
| Images | 5% |
| AI Search Readiness | 5% |

## Report Structure

### Executive Summary
- Overall SEO Health Score (0-100)
- Business type detected
- Top 5 critical issues
- Top 5 quick wins

### Technical SEO
- Crawlability issues
- Indexability problems
- Security concerns
- Core Web Vitals status

### Content Quality
- E-E-A-T assessment
- Thin content pages
- Duplicate content issues
- Readability scores

### On-Page SEO
- Title tag issues
- Meta description problems
- Heading structure
- Internal linking gaps

### Schema & Structured Data
- Current implementation
- Validation errors
- Missing opportunities

### Performance
- LCP, INP, CLS scores
- Resource optimization needs
- Third-party script impact

### Images
- Missing alt text
- Oversized images
- Format recommendations

### AI Search Readiness
- Citability score
- Structural improvements
- Authority signals

## Priority Definitions

- **Critical**: Blocks indexing or causes penalties (fix immediately)
- **High**: Significantly impacts rankings (fix within 1 week)
- **Medium**: Optimization opportunity (fix within 1 month)
- **Low**: Nice to have (backlog)

---

## Live Data Insights (MCP Overlay)

> This section appears only when MCP data sources are available. The static analysis above is complete and unchanged regardless of MCP availability.

### MCP Availability Check

Follow the self-contained check pattern from `seo/references/mcp-degradation.md`:
1. Use ToolSearch with query "+ahrefs" — if tools returned, Ahrefs is available
2. Use ToolSearch with query "+google-search-console" — if tools returned, GSC is available
3. Proceed with whichever MCPs are available; skip sections for unavailable MCPs

### Domain Authority Context (Ahrefs)

If Ahrefs available: after completing the static scoring step, fetch domain-level metrics via `site-explorer-metrics` for the target domain (bare domain, no https://). Display a `### Domain Authority Context` section:

```
### Domain Authority Context

| Metric | Value |
|--------|-------|
| Domain Rating (DR) | XX/100 |
| Ahrefs Rank | #XX,XXX |
| Total Backlinks | XX,XXX |
| Referring Domains | X,XXX |
| Organic Keywords | XX,XXX |
| Est. Monthly Organic Traffic | XX,XXX visits |
```

Annotate the SEO Health Score line with: *(Data enriched with live Ahrefs metrics)*

**Note:** All monetary values (`traffic_cost`, `cpc`) from Ahrefs are in cents — divide by 100 before displaying as USD.

### Indexing Status (GSC)

If GSC available: fetch indexing coverage using `get_indexing_status` for up to 20 top pages. Add a `### Indexing Status` section:

```
### Indexing Status (Google Search Console)

- Indexed pages: XX
- Not indexed: XX
  - Top reasons: [reason 1], [reason 2]
  - Non-indexed pages: [url1], [url2], ...

> Note: GSC property format — use sc-domain: for domain properties or full https:// URL for URL-prefix properties.
```

### Top Performing Pages (GSC)

If GSC available: fetch `get_search_analytics` for the site's top pages (last 28 days, sorted by clicks). Add a `### Top Performing Pages` section:

```
### Top Performing Pages (Google Search Console — Last 28 Days)

| Page | Clicks | Impressions | CTR | Avg Position |
|------|--------|-------------|-----|--------------|
| /page-1 | X,XXX | XX,XXX | X.X% | X.X |
| /page-2 | ... | ... | ... | ... |

> CTR displayed as percentage (API returns decimal — multiply by 100 for display).
```

---

## Data Sources

Always append this footer to the audit output:

| Source | Status | Data Provided |
|--------|--------|---------------|
| Static Analysis | Always available | Crawl, scoring, on-page, technical, content, schema, performance |
| Ahrefs MCP | Available / Not connected | DR, backlinks, referring domains, organic keywords, traffic |
| GSC MCP | Available / Not connected | Indexing coverage, top-performing pages, clicks, impressions |
