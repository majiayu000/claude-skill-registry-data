---
name: seo-sitemap
description: >
  Analyze existing XML sitemaps or generate new ones with GSC indexing
  cross-reference. Validates format, URLs, and structure against actual
  indexing status. Use when user says "sitemap", "generate sitemap",
  "sitemap issues", "XML sitemap", or "sitemap indexing".
allowed-tools:
  - Read
  - Bash
  - Glob
  - WebFetch
  - ToolSearch
---

# Sitemap Analysis & Generation

## Mode 1: Analyze Existing Sitemap

### Validation Checks
- Valid XML format
- URL count <50,000 per file (protocol limit)
- All URLs return HTTP 200
- `<lastmod>` dates are accurate (not all identical)
- No deprecated tags: `<priority>` and `<changefreq>` are ignored by Google
- Sitemap referenced in robots.txt
- Compare crawled pages vs sitemap — flag missing pages

### Quality Signals
- Sitemap index file if >50k URLs
- Split by content type (pages, posts, images, videos)
- No non-canonical URLs in sitemap
- No noindexed URLs in sitemap
- No redirected URLs in sitemap
- HTTPS URLs only (no HTTP)

### Common Issues
| Issue | Severity | Fix |
|-------|----------|-----|
| >50k URLs in single file | Critical | Split with sitemap index |
| Non-200 URLs | High | Remove or fix broken URLs |
| Noindexed URLs included | High | Remove from sitemap |
| Redirected URLs included | Medium | Update to final URLs |
| All identical lastmod | Low | Use actual modification dates |
| Priority/changefreq used | Info | Can remove (ignored by Google) |

## Mode 2: Generate New Sitemap

### Process
1. Ask for business type (or auto-detect from existing site)
2. Load industry template from `assets/` directory
3. Interactive structure planning with user
4. Apply quality gates:
   - ⚠️ WARNING at 30+ location pages (require 60%+ unique content)
   - 🛑 HARD STOP at 50+ location pages (require justification)
5. Generate valid XML output
6. Split at 50k URLs with sitemap index
7. Generate STRUCTURE.md documentation

### Safe Programmatic Pages (OK at scale)
✅ Integration pages (with real setup docs)
✅ Template/tool pages (with downloadable content)
✅ Glossary pages (200+ word definitions)
✅ Product pages (unique specs, reviews)
✅ User profile pages (user-generated content)

### Penalty Risk (avoid at scale)
❌ Location pages with only city name swapped
❌ "Best [tool] for [industry]" without industry-specific value
❌ "[Competitor] alternative" without real comparison data
❌ AI-generated pages without human review and unique value

## Sitemap Format

### Standard Sitemap
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page</loc>
    <lastmod>2026-02-07</lastmod>
  </url>
</urlset>
```

### Sitemap Index (for >50k URLs)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-pages.xml</loc>
    <lastmod>2026-02-07</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-posts.xml</loc>
    <lastmod>2026-02-07</lastmod>
  </sitemap>
</sitemapindex>
```

## Output

### For Analysis
- `VALIDATION-REPORT.md` — analysis results
- Issues list with severity
- Recommendations

### For Generation
- `sitemap.xml` (or split files with index)
- `STRUCTURE.md` — site architecture documentation
- URL count and organization summary

## Live Data Insights (MCP Overlay)

@skills/seo/references/mcp-degradation.md

### GSC Indexing Cross-Reference

If GSC available: Use ToolSearch with query "+google-search-console" to check availability.

- If GSC MCP tools are returned: fetch `get_indexing_status` or `inspect_url` for a sample of sitemap URLs (max 20 URLs to avoid rate-limit issues).
- Add `### Sitemap vs Index Coverage (GSC)` section showing how many sitemap URLs are actually indexed, which are not indexed, and the specific non-indexing reasons reported by Google.
- This is the most valuable cross-reference for sitemap audits — it reveals whether Google is actually processing the sitemap correctly.
- If GSC MCP is not available: proceed with static sitemap validation only, noting that live indexing status is unavailable.

### Sitemap vs Index Coverage (when GSC available)

| Metric | Count | Notes |
|--------|-------|-------|
| Sitemap URLs sampled | [up to 20] | |
| Confirmed indexed | [count] | |
| Not indexed | [count] | |
| Coverage errors | [count] | See breakdown below |

**Non-indexing reasons breakdown** (from GSC `inspect_url`):
- Crawled — currently not indexed: [count]
- Discovered — currently not indexed: [count]
- Blocked by robots.txt: [count]
- Page with redirect: [count]
- Other reasons: [count]

## Data Sources

| Source | Status | Data Provided |
|--------|--------|---------------|
| Static XML Analysis | Always available | Format validation, URL checks, structure review |
| GSC MCP (`+google-search-console`) | If connected | Live indexing status per URL, non-indexing reasons |
