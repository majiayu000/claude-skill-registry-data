---
name: seo-auditor
description: Full technical, on-page, and off-page SEO audit with prioritized fix list
tags: [seo, audit, technical-seo, on-page, off-page, backlinks]
---

# SEO Auditor

Performs a comprehensive SEO audit across three dimensions: technical SEO (crawlability, site speed, mobile-friendliness, indexation), on-page SEO (titles, meta descriptions, headings, content quality, keyword usage), and off-page SEO (backlink profile, domain authority, brand mentions). Uses WebSearch and browser automation to gather live data. Returns a prioritized fix list with impact scores and estimated effort for each recommendation.

## Prerequisites

- WebSearch tool available for SERP analysis and external data gathering
- Browser automation tool available for crawling target site pages
- Target website URL
- Optional: `agency.config.json` for service-specific audit focus and client context

## Capabilities Used

1. `content-seo-optimizer` -- for detailed on-page analysis of individual pages
2. `schema-generator` -- for structured data gap identification

## Phase 0: Intake

1. Read `agency.config.json` from the project root (if available).
2. Extract `services[]` to understand which SEO areas the agency can deliver on.
3. Extract `icp.segments[]` to contextualize recommendations for the client's market.
4. Accept parameters:
   - `url` -- (required) the website to audit
   - `depth` -- `quick` (homepage + one inner page) | `standard` (homepage + 5 key pages) | `deep` (full site crawl, up to 50 pages). Default: `standard`
   - `focus` -- (optional) specific area: `technical`, `on-page`, `off-page`, or `all`. Default: `all`
   - `competitor_urls` -- (optional) array of competitor URLs for comparative analysis

## Phase 1: Technical SEO Audit

### Crawlability and Indexation
- Check `robots.txt` at `{{url}}/robots.txt` -- parse directives, identify blocked paths
- Check `sitemap.xml` at `{{url}}/sitemap.xml` -- verify existence, validate format, count URLs
- WebSearch: `site:{{domain}}` -- compare indexed page count against sitemap URLs
- Check for canonical tags on sampled pages -- identify self-referencing and cross-domain canonicals
- Check for `noindex`, `nofollow` meta tags on pages that should be indexed
- Look for orphan pages (in sitemap but not linked from navigation)

### Site Speed
- WebSearch: `"{{domain}}" pagespeed OR "page speed" OR "core web vitals"`
- Check visible indicators: image optimization (WebP/AVIF usage, lazy loading), font loading strategy, render-blocking resources
- Note any visible layout shifts (CLS indicators)
- Check for excessive JavaScript bundle size indicators (slow interactivity)
- Mobile speed: test primary pages on mobile viewport

### Mobile-Friendliness
- Visit site on mobile viewport via browser automation
- Check responsive layout, touch target sizes, font readability
- Verify mobile menu functionality
- Check for horizontal scroll issues
- Verify viewport meta tag is set correctly

### URL Structure and Architecture
- Evaluate URL patterns: clean, descriptive, consistent hierarchy
- Check for URL parameters creating duplicate content
- Verify HTTPS across all pages (mixed content warnings)
- Check redirect chains (301/302 hops)
- Evaluate internal linking depth (clicks from homepage to deepest content)

### International SEO (if applicable)
- Check for hreflang tags
- Verify language/region targeting
- Check for proper locale-specific URLs

## Phase 2: On-Page SEO Audit

For each sampled page, evaluate:

### Title Tags
- Present and unique per page
- Length: 50-60 characters optimal
- Primary keyword placement (front-loaded)
- Brand name inclusion pattern
- Compelling for click-through (not just keyword-stuffed)

### Meta Descriptions
- Present and unique per page
- Length: 150-160 characters optimal
- Include primary keyword naturally
- Contain a call-to-action or value proposition
- Compelling enough to improve CTR from SERPs

### Heading Structure
- Single H1 per page containing primary keyword
- Logical H2/H3 hierarchy (no skipped levels)
- Keywords distributed naturally across headings
- Headings reflect content structure (not just styled text)

### Content Quality
- Word count per page (thin content < 300 words on key pages is a red flag)
- Keyword density: primary keyword appears naturally (1-3% density)
- Related keywords and LSI terms present
- Content freshness: last updated dates, outdated references
- Duplicate content: check for substantially similar pages
- Internal linking: each page links to 3-5 relevant internal pages

### Image Optimization
- Alt text present and descriptive on all images
- File names descriptive (not IMG_001.jpg)
- Image file sizes reasonable (< 200KB for most images)
- Next-gen formats (WebP, AVIF) in use
- Responsive images with srcset attributes

### Structured Data
- Check for existing JSON-LD markup
- Identify missing schema types (Organization, Product, FAQ, BreadcrumbList)
- Validate existing schema for errors
- Flag rich snippet opportunities not being captured

## Phase 3: Off-Page SEO Audit

### Backlink Profile
- WebSearch: `"{{domain}}" -site:{{domain}}` -- estimate external mention volume
- WebSearch: `link:{{domain}}` -- check for backlink indicators
- WebSearch: `"{{domain}}" backlinks OR "domain authority" OR "domain rating"` -- find third-party reports
- Identify linking domains by category: editorial, directory, social, forum, spam
- Check for toxic backlink indicators (spammy anchor text, irrelevant foreign domains)

### Domain Authority Signals
- WebSearch: `"{{domain}}" "domain authority" OR "DA" OR "domain rating" OR "DR"`
- Compare against competitor DA/DR if competitor URLs provided
- Check domain age and registration history signals

### Brand Presence
- WebSearch: `"{{brand_name}}" -site:{{domain}}` -- find brand mentions
- Check for unlinked brand mentions (link building opportunities)
- Social media presence and engagement signals
- Google Business Profile presence (for local businesses)
- Review site presence (G2, Trustpilot, Clutch for B2B)

### Competitor Comparison (if competitor URLs provided)
- Compare indexed page counts
- Compare visible backlink profiles
- Compare content volume and freshness
- Identify keywords competitors rank for that the target does not

## Phase 4: SERP Analysis

### Current Visibility
- WebSearch: `site:{{domain}}` -- check indexed pages and featured results
- Search for brand name -- verify knowledge panel, sitelinks
- Search for primary service/product keywords -- check if domain appears in top 20
- Check for featured snippet ownership on key queries

### SERP Feature Opportunities
- Identify queries where "People Also Ask" boxes appear -- content gap opportunities
- Check for video carousel presence -- video content opportunity
- Check for image pack presence -- image optimization opportunity
- Local pack presence -- local SEO opportunity
- Shopping results -- product feed opportunity

## Phase 5: Score and Prioritize

Assign scores from 1-10 for each area:

- **Technical SEO**: crawlability, speed, mobile, URL structure
- **On-Page SEO**: titles, meta, headings, content, images, schema
- **Off-Page SEO**: backlinks, DA, brand presence
- **Overall SEO Health**: weighted average (Technical 35%, On-Page 40%, Off-Page 25%)

Scoring guide:
- 9-10: Excellent, minor optimizations only
- 7-8: Good, clear improvement areas that will compound
- 5-6: Average, significant gaps losing organic traffic
- 3-4: Below average, fundamental issues blocking growth
- 1-2: Critical, site is nearly invisible to search engines

Prioritize all findings by:
1. **Impact**: How much organic traffic will this fix recover/gain? (High/Medium/Low)
2. **Effort**: How long to implement? (Quick win / Medium project / Major initiative)
3. **Urgency**: Is this actively harming rankings? (Critical / Important / Nice-to-have)

## Phase 6: Output

Return structured JSON:

```json
{
  "url": "https://example.com",
  "audited_at": "2024-01-15T14:30:00Z",
  "depth": "standard",
  "pages_audited": [
    "https://example.com",
    "https://example.com/products/example",
    "https://example.com/blog/example-post"
  ],
  "overall_score": "5.8/10",
  "score_breakdown": {
    "technical_seo": "6/10",
    "on_page_seo": "5/10",
    "off_page_seo": "6/10"
  },
  "critical_issues": [
    {
      "area": "Technical",
      "issue": "No sitemap.xml found",
      "impact": "High",
      "effort": "Quick win (1 hour)",
      "urgency": "Critical",
      "fix": "Generate and submit XML sitemap via Google Search Console. Most CMS platforms auto-generate this.",
      "impact_score": 9
    }
  ],
  "high_priority": [
    {
      "area": "On-Page",
      "issue": "Missing meta descriptions on 70% of pages",
      "impact": "High",
      "effort": "Medium (4-8 hours)",
      "urgency": "Important",
      "fix": "Write unique meta descriptions for all key pages, starting with highest-traffic pages.",
      "impact_score": 8
    }
  ],
  "medium_priority": [
    {
      "area": "Off-Page",
      "issue": "12 unlinked brand mentions found",
      "impact": "Medium",
      "effort": "Medium (outreach campaign)",
      "urgency": "Nice-to-have",
      "fix": "Contact site owners to convert mentions into backlinks.",
      "impact_score": 5
    }
  ],
  "low_priority": [],
  "strengths": [
    "Clean URL structure with descriptive slugs",
    "HTTPS properly configured across all pages",
    "Good internal linking between related content"
  ],
  "quick_wins": [
    "Add sitemap.xml and submit to Search Console",
    "Fix 15 missing alt tags on homepage images",
    "Add FAQ schema to the 3 support pages"
  ],
  "competitor_comparison": {
    "indexed_pages": { "target": 120, "competitor_avg": 450 },
    "estimated_da": { "target": "25", "competitor_avg": "42" },
    "content_gap_keywords": ["keyword1", "keyword2", "keyword3"]
  },
  "next_steps": [
    "Fix critical technical issues (Week 1)",
    "Optimize on-page elements for top 10 pages (Week 2-3)",
    "Launch link building campaign for unlinked mentions (Week 4+)"
  ]
}
```

## Phase 7: Review Gate

Present findings to the user before taking action. The user may:
- Adjust scores or remove false positives
- Request deeper analysis on specific areas
- Select which fixes to prioritize for implementation
- Request a comparison with specific competitors

## Example Usage

Trigger phrases:
- "Run an SEO audit on [url]"
- "Check [url] for SEO issues"
- "Full SEO analysis of [domain]"
- "Technical SEO check on [url]"
- "How is [url] doing on SEO?"

```
User: Run an SEO audit on https://brandx.com
Assistant: [crawls homepage and key pages, checks technical/on-page/off-page, returns scored findings with prioritized fix list]
```

```
User: Quick SEO check on example.com, focus on technical issues
Assistant: [homepage + one inner page, technical SEO only, returns critical and high-priority technical fixes]
```

```
User: Deep SEO audit of brandx.com vs competitor1.com and competitor2.com
Assistant: [full crawl up to 50 pages, all dimensions, comparative analysis against both competitors]
```
