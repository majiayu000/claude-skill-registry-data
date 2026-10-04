---
name: seo-page
description: >
  Deep single-page SEO analysis covering on-page elements, content quality,
  technical meta tags, schema, images, and performance. Enhanced with live
  Ahrefs (page authority, referring domains) and GSC (search performance,
  top keywords) data when MCPs are available. Use when user says "analyze
  this page", "check page SEO", or provides a single URL for review.
allowed-tools:
  - Read
  - Bash
  - Glob
  - WebFetch
  - ToolSearch
---

# Single Page Analysis

## What to Analyze

### On-Page SEO
- Title tag: 50-60 characters, includes primary keyword, unique
- Meta description: 150-160 characters, compelling, includes keyword
- H1: exactly one, matches page intent, includes keyword
- H2-H6: logical hierarchy (no skipped levels), descriptive
- URL: short, descriptive, hyphenated, no parameters
- Internal links: sufficient, relevant anchor text, no orphan pages
- External links: to authoritative sources, reasonable count

### Content Quality
- Word count vs page type minimums (see quality-gates.md)
- Readability: Flesch Reading Ease score, grade level
- Keyword density: natural (1-3%), semantic variations present
- E-E-A-T signals: author bio, credentials, first-hand experience markers
- Content freshness: publication date, last updated date

### Technical Elements
- Canonical tag: present, self-referencing or correct
- Meta robots: index/follow unless intentionally blocked
- Open Graph: og:title, og:description, og:image, og:url
- Twitter Card: twitter:card, twitter:title, twitter:description
- Hreflang: if multi-language, correct implementation

### Schema Markup
- Detect all types (JSON-LD preferred)
- Validate required properties
- Identify missing opportunities
- NEVER recommend HowTo (deprecated) or FAQ (restricted to gov/health)

### Images
- Alt text: present, descriptive, includes keywords where natural
- File size: flag >200KB (warning), >500KB (critical)
- Format: recommend WebP/AVIF over JPEG/PNG
- Dimensions: width/height set for CLS prevention
- Lazy loading: loading="lazy" on below-fold images

### Core Web Vitals (reference only — not measurable from HTML alone)
- Flag potential LCP issues (huge hero images, render-blocking resources)
- Flag potential INP issues (heavy JS, no async/defer)
- Flag potential CLS issues (missing image dimensions, injected content)

## Output

### Page Score Card
```
Overall Score: XX/100

On-Page SEO:     XX/100  ████████░░
Content Quality: XX/100  ██████████
Technical:       XX/100  ███████░░░
Schema:          XX/100  █████░░░░░
Images:          XX/100  ████████░░
```

### Issues Found
Organized by priority: Critical → High → Medium → Low

### Recommendations
Specific, actionable improvements with expected impact

### Schema Suggestions
Ready-to-use JSON-LD code for detected opportunities

---

## Live Data Insights (MCP Overlay)

> This section appears only when MCP data sources are available. The static analysis above is complete and unchanged regardless of MCP availability.

### MCP Availability Check

Follow the self-contained check pattern from `seo/references/mcp-degradation.md`:
1. Use ToolSearch with query "+ahrefs" — if tools returned, Ahrefs is available
2. Use ToolSearch with query "+google-search-console" — if tools returned, GSC is available
3. Proceed with whichever MCPs are available; skip sections for unavailable MCPs

### Page Authority Data (Ahrefs)

If Ahrefs available: fetch page-level metrics via `site-explorer-metrics` for the specific URL (full URL with https://). Add a `### Page Authority Data` section:

```
### Page Authority Data (Ahrefs)

| Metric | Value |
|--------|-------|
| Referring Domains | XXX |
| Total Backlinks | X,XXX |
| Organic Keywords (this page) | XXX |
| Est. Monthly Traffic (this page) | XXX visits |
```

**Note:** All monetary values (`traffic_cost`, `cpc`) from Ahrefs are in cents — divide by 100 before displaying as USD.

### Search Performance — GSC (Last 28 Days)

If GSC available: fetch `get_search_analytics` filtered to this specific URL for the last 28 days. Add a `### Search Performance (GSC)` section:

```
### Search Performance (Google Search Console — Last 28 Days)

| Metric | Value |
|--------|-------|
| Total Clicks | X,XXX |
| Total Impressions | XX,XXX |
| Click-Through Rate | X.X% |
| Average Position | X.X |

**Top 10 Keywords Driving Traffic to This Page:**

| Keyword | Clicks | Impressions | CTR | Avg Position |
|---------|--------|-------------|-----|--------------|
| keyword 1 | XXX | X,XXX | X.X% | X.X |
| ... | ... | ... | ... | ... |

> CTR displayed as percentage (API returns decimal — multiply by 100 for display).
```

---

## Data Sources

Always append this footer to the page analysis output:

| Source | Status | Data Provided |
|--------|--------|---------------|
| Static Analysis | Always available | On-page elements, content quality, technical tags, schema, images, CWV signals |
| Ahrefs MCP | Available / Not connected | Referring domains, backlinks, organic keywords, page-level traffic |
| GSC MCP | Available / Not connected | Clicks, impressions, CTR, avg position, top keywords for this page |
