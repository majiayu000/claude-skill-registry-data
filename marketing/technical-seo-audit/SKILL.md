---
name: technical-seo-audit
description: >
  Deep technical SEO audit covering Core Web Vitals, crawlability, indexation,
  structured data, canonical/hreflang, redirect chains, and site architecture.
  Complements seo-auditor which focuses on on-page/off-page factors.
tags: [seo, technical, audit, performance, crawlability]
---

# Technical SEO Audit

Performs a deep technical SEO audit of a website, focusing on infrastructure-level issues that affect search engine crawling, indexing, and ranking. Complements `seo-auditor` (which covers on-page content and off-page signals) by going deeper into the technical foundation.

## Prerequisites

- Target website URL
- `agency.config.json` populated (for reporting context)
- WebSearch and WebFetch tools available
- Optional: Google Search Console access for indexation data

## Phase 0: Intake

Read `agency.config.json`:
- `agency.name` -- for report branding
- `services[]` -- to flag relevant service recommendations

Accept parameters:
- `url` -- (required) target website root URL
- `depth` -- (optional) `quick` (homepage + 5 pages), `standard` (up to 25 pages), `deep` (up to 100 pages). Default: `standard`
- `focus_areas` -- (optional) array to limit scope: `core-web-vitals`, `crawlability`, `indexation`, `structured-data`, `redirects`, `security`, `mobile`, `international`. Default: all
- `competitor_urls` -- (optional) array of competitor URLs for comparison
- `gsc_data` -- (optional) Google Search Console export data

## Phase 1: Core Web Vitals Analysis

Use WebFetch to check PageSpeed Insights API or Chrome UX Report signals:

### Metrics to Assess
| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5-4.0s | > 4.0s |
| INP (Interaction to Next Paint) | < 200ms | 200-500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1-0.25 | > 0.25 |
| FCP (First Contentful Paint) | < 1.8s | 1.8-3.0s | > 3.0s |
| TTFB (Time to First Byte) | < 800ms | 800-1800ms | > 1800ms |

### Page Types to Test
- Homepage
- Category/collection page
- Product/detail page
- Blog/content page
- Search results page (if applicable)

### Analysis
For each failing metric:
```
ISSUE: [metric] is [value] on [page type]
IMPACT: [how this affects rankings and UX]
CAUSE: [likely technical cause based on page analysis]
FIX: [specific technical recommendation]
PRIORITY: [HIGH/MEDIUM/LOW]
EFFORT: [quick-win / medium / major-refactor]
```

## Phase 2: Crawlability Audit

### Robots.txt Analysis
- Fetch and parse `robots.txt`
- Check for overly restrictive rules blocking important content
- Check for missing rules allowing crawl of admin/private pages
- Verify sitemap reference is present
- Check for user-agent specific rules

### XML Sitemap Analysis
- Fetch sitemap(s) from robots.txt or common locations (`/sitemap.xml`, `/sitemap_index.xml`)
- Count total URLs
- Check for:
  - URLs returning non-200 status codes
  - Orphaned URLs (in sitemap but not linked from site)
  - Missing URLs (important pages not in sitemap)
  - Last modified dates (are they accurate or all the same?)
  - Sitemap file size (under 50MB, under 50,000 URLs per file)
  - Proper XML formatting

### Crawl Depth Analysis
- Map internal link structure from homepage
- Flag pages requiring 4+ clicks to reach from homepage
- Identify orphan pages (no internal links pointing to them)
- Check for crawl traps (infinite pagination, faceted navigation creating duplicate URLs)

### Internal Linking
- Check for broken internal links (404s)
- Check for redirect chains in internal links
- Identify pages with very few internal links (low PageRank flow)
- Check for excessive internal links on single pages (>100)

## Phase 3: Indexation Audit

### Index Status Checks
- `site:domain.com` search to estimate indexed pages
- Compare indexed count vs sitemap count vs actual page count
- Flag significant discrepancies (indexed >> actual = duplicates; indexed << actual = indexation issues)

### Common Indexation Issues
Check for:
- `noindex` meta tags on pages that should be indexed
- `noindex` in HTTP headers (X-Robots-Tag)
- Pages blocked by robots.txt that have inbound links
- Thin content pages (under 300 words) that may be filtered
- Duplicate title tags across multiple pages
- Duplicate meta descriptions
- Missing or duplicate H1 tags

### Canonical Tag Audit
- Every page has a canonical tag
- Self-referencing canonicals on unique pages
- Canonical points to correct URL (not HTTP when HTTPS, not non-www when www)
- No canonical chains (A canonicals to B, B canonicals to C)
- Canonical matches the version in the sitemap

## Phase 4: Structured Data Validation

### Check for Existing Schema
Inspect pages for JSON-LD, Microdata, or RDFa markup:

| Page Type | Expected Schema | Priority |
|----------|----------------|----------|
| Homepage | Organization, WebSite, SearchAction | HIGH |
| Product | Product, Offer, AggregateRating, Review | HIGH |
| Collection | CollectionPage, ItemList | MEDIUM |
| Blog post | Article, BlogPosting, BreadcrumbList | MEDIUM |
| FAQ page | FAQPage | HIGH |
| About page | Organization, Person | LOW |
| Contact | LocalBusiness, ContactPoint | MEDIUM |

### Validation
For each schema found:
- Valid JSON-LD syntax
- Required properties present (per schema.org spec)
- No deprecated properties
- Proper nesting
- Consistent with page content (no schema spam)

### Missing Schema Opportunities
Flag pages where adding schema would provide rich result eligibility:
- Product pages without Product schema
- FAQ content without FAQPage schema
- Review content without Review schema
- Events without Event schema
- Breadcrumbs without BreadcrumbList schema

## Phase 5: Redirect Audit

### Redirect Chain Analysis
- Identify redirect chains (A -> B -> C) -- all should be A -> C
- Identify redirect loops
- Check for mixed HTTP/HTTPS redirects
- Check for mixed www/non-www redirects
- Verify 301 (permanent) vs 302 (temporary) usage is correct

### Common Redirect Issues
- Old URLs redirecting through multiple hops
- Trailing slash inconsistency (some URLs with, some without)
- Case sensitivity issues (uppercase URLs not redirecting to lowercase)
- Parameter-based redirects missing
- Deleted page 404s that should 301 to relevant alternatives

## Phase 6: Security & HTTPS

- Full HTTPS: no mixed content warnings
- HSTS header present and correctly configured
- SSL certificate valid and not expiring within 30 days
- No insecure resources loaded (images, scripts, stylesheets over HTTP)
- Security headers check: CSP, X-Frame-Options, X-Content-Type-Options
- Cookie security: Secure flag, HttpOnly, SameSite

## Phase 7: Mobile Friendliness

- Viewport meta tag present and correct
- No horizontal scroll on mobile viewports
- Touch targets adequately sized (min 48x48px)
- Font sizes readable without zooming (min 16px body text)
- No intrusive interstitials blocking content
- Mobile page speed (separate from desktop CWV)

## Phase 8: International SEO (if applicable)

- Hreflang tags present and correct
- Return tags (each hreflang pair must be bidirectional)
- x-default tag present
- Language/region targeting consistent across pages
- No conflicting canonical and hreflang signals

## Phase 9: Output

Return structured JSON:

```json
{
  "url": "https://example.com",
  "audit_date": "2026-03-13",
  "audit_depth": "standard",
  "pages_analyzed": 25,
  "overall_health_score": 72,
  "score_breakdown": {
    "core_web_vitals": 65,
    "crawlability": 80,
    "indexation": 75,
    "structured_data": 60,
    "redirects": 85,
    "security": 90,
    "mobile": 70
  },
  "critical_issues": [
    {
      "category": "core-web-vitals",
      "issue": "LCP 4.2s on product pages",
      "impact": "Ranking penalty, 53% bounce rate increase above 3s",
      "fix": "Optimize hero image: compress, add srcset, preload LCP image",
      "priority": "HIGH",
      "effort": "quick-win",
      "pages_affected": 45
    }
  ],
  "warnings": [
    {
      "category": "structured-data",
      "issue": "Product pages missing AggregateRating schema",
      "impact": "Missing star ratings in search results",
      "fix": "Add AggregateRating to Product JSON-LD",
      "priority": "MEDIUM",
      "effort": "medium"
    }
  ],
  "opportunities": [
    {
      "category": "indexation",
      "opportunity": "45 blog posts with thin content could be consolidated",
      "impact": "Reduce index bloat, concentrate PageRank",
      "effort": "major-refactor"
    }
  ],
  "competitor_comparison": {
    "our_score": 72,
    "competitor_scores": [
      {"url": "competitor1.com", "score": 68},
      {"url": "competitor2.com", "score": 81}
    ]
  },
  "recommendations_summary": [
    {"priority": 1, "action": "Fix LCP on product pages", "impact": "HIGH", "effort": "quick-win"},
    {"priority": 2, "action": "Add Product schema to all product pages", "impact": "HIGH", "effort": "medium"},
    {"priority": 3, "action": "Resolve 12 redirect chains", "impact": "MEDIUM", "effort": "quick-win"}
  ],
  "generated_at": "2026-03-13T10:00:00Z"
}
```

## Phase 10: Report & Handoff

Present findings as a prioritized action plan:
1. **Critical** (fix immediately): Issues causing ranking loss or indexation failures
2. **High priority** (fix this week): Significant performance or schema issues
3. **Medium priority** (fix this month): Optimization opportunities
4. **Low priority** (backlog): Nice-to-haves and future improvements

If `write_to_crm` context exists, log the audit as a prospect touchpoint.

## Example Usage

Trigger phrases:
- "Run a technical SEO audit on [url]"
- "Check Core Web Vitals for [url]"
- "Audit the structured data on [url]"
- "Check [url] for crawlability issues"
- "Run a redirect chain analysis on [url]"
- "Full technical SEO check on this prospect's site"
- "Compare our client's technical SEO against competitors"
