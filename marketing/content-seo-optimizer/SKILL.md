---
name: content-seo-optimizer
description: On-page SEO optimization for existing content with before/after scoring
tags: [seo, on-page, content-optimization, keywords, meta-tags]
---

# Content SEO Optimizer

Performs detailed on-page SEO analysis of existing content -- either a live URL or raw text -- against a target keyword. Evaluates title tag, meta description, heading structure, keyword density, internal links, image alt tags, schema markup, and content length. Scores current optimization level, provides specific actionable fixes, and outputs a before/after optimization checklist.

## Prerequisites

- WebSearch tool available for SERP analysis and competitive content benchmarking
- Browser automation tool available for crawling and extracting page elements
- Target URL or content text to analyze
- Target keyword or keyword phrase
- Optional: `agency.config.json` for client context

## Phase 0: Read Config

1. Read `agency.config.json` from the project root (if available).
2. Extract `services[]` for understanding the content's business context.
3. Extract `icp.segments[]` to tailor optimization for the right audience.
4. Check `tools.websearch` and `tools.browser` availability.
5. Accept parameters:
   - `url` -- (optional) live page URL to analyze
   - `content` -- (optional) raw text/HTML content to analyze (use if URL not provided)
   - `target_keyword` -- (required) primary keyword to optimize for
   - `secondary_keywords` -- (optional) array of secondary keywords to check for
   - `content_type` -- (optional) `blog_post` | `landing_page` | `product_page` | `service_page` | `homepage`. Default: auto-detect
   - `market` -- (optional) `US` | `UK` | `IN` | `AU` | `global`. Default: derive from config

## Phase 1: Content Extraction

### If URL Provided
- Visit the URL via browser automation
- Extract the full page HTML
- Parse out:
  - `<title>` tag content
  - `<meta name="description">` content
  - All heading tags (H1 through H6) in order
  - Body text content (stripped of HTML)
  - All `<img>` tags with src and alt attributes
  - All internal links (href values pointing to same domain)
  - All external links
  - Any JSON-LD or microdata structured data
  - Word count of body content
  - URL slug

### If Raw Content Provided
- Parse the text/HTML directly
- Extract same elements as above where available
- Note any missing elements (no title tag, no meta description, etc.)

## Phase 2: Title Tag Analysis

### Current State Assessment
- Is a title tag present?
- Title text content and character length
- Does the title contain the target keyword?
- Keyword position within the title (front-loaded is better)
- Is the brand name included?
- Is the title compelling for click-through?

### Optimization Recommendations
- Optimal length: 50-60 characters
- Target keyword should appear in the first 60 characters
- Front-load the primary keyword when possible
- Include a value proposition or emotional hook
- Include brand name at the end (separated by ` | ` or ` - `)
- Generate 3 optimized title tag options

### SERP Competitor Check
- WebSearch the target keyword
- Extract title tags from the top 5 ranking pages
- Identify patterns: what are top rankers doing differently?
- Note any truncation risks

## Phase 3: Meta Description Analysis

### Current State Assessment
- Is a meta description present?
- Description text and character length
- Does it contain the target keyword?
- Does it include a call-to-action?
- Is it compelling enough to drive clicks over competitors?

### Optimization Recommendations
- Optimal length: 150-160 characters
- Include the target keyword naturally (Google bolds matching terms)
- Include a clear CTA or value proposition
- Differentiate from competitor descriptions
- Generate 2 optimized meta description options

## Phase 4: Heading Structure Analysis

### Current State Assessment
- Count of H1 tags (should be exactly 1)
- H1 content and keyword presence
- Full heading hierarchy: H1 > H2 > H3 > H4 > H5 > H6
- Are heading levels skipped? (H1 > H3 without H2 is bad)
- Do headings contain keywords naturally?
- Do headings reflect the content structure logically?

### Optimization Recommendations
- Single H1 containing the primary keyword
- H2s for major sections, each targeting a related keyword or subtopic
- H3s for subsections within H2 blocks
- No skipped levels
- Generate suggested heading structure with keywords woven in

## Phase 5: Keyword Density and Placement

### Current State Assessment
- Primary keyword count and density (occurrences / total words x 100)
- Secondary keyword counts and densities
- Keyword placement map:
  - In title tag?
  - In meta description?
  - In H1?
  - In first 100 words of body?
  - In at least one H2?
  - In image alt tags?
  - In URL slug?
  - In last 100 words / conclusion?

### Optimization Recommendations
- Target density: 1-3% for primary keyword (avoid over-optimization)
- Primary keyword must appear in: title, H1, first paragraph, at least one H2, conclusion
- Secondary keywords should appear 2-5 times each in body content
- Use semantic variations and LSI terms naturally
- Identify keyword stuffing risks and recommend reductions where needed

## Phase 6: Internal Link Analysis

### Current State Assessment
- Count of internal links on the page
- Internal link anchor text analysis
- Are links pointing to relevant related pages?
- Are there orphan page risks (no internal links pointing to this page)?
- Link depth from homepage

### Optimization Recommendations
- Target: 3-5 internal links per 1000 words
- Use descriptive anchor text containing keywords (not "click here")
- Link to topically related pages (sibling content, pillar pages)
- Add links from high-traffic pages pointing to this page
- Suggest specific internal links to add, with anchor text

## Phase 7: Image Optimization Analysis

### Current State Assessment
- Total image count on the page
- Images missing alt text (count and list)
- Alt text quality: descriptive and keyword-relevant vs generic
- File name analysis: descriptive vs IMG_0001.jpg
- Image format: WebP/AVIF vs JPEG/PNG
- Lazy loading present?

### Optimization Recommendations
- Every image needs descriptive alt text
- Include target keyword in at least one image alt tag (naturally)
- Rename files to descriptive slugs matching content
- Convert to WebP/AVIF where possible
- Add lazy loading for below-fold images
- Generate suggested alt text for each image missing it

## Phase 8: Schema Markup Analysis

### Current State Assessment
- Is any structured data present? (JSON-LD, Microdata, RDFa)
- What schema types are implemented?
- Are there validation errors in existing schema?
- What schema types are missing but relevant?

### Optimization Recommendations
- Recommend applicable schema types based on content_type:
  - Blog post: Article, BreadcrumbList, FAQ (if FAQ section exists)
  - Product page: Product, Review, BreadcrumbList, FAQ
  - Service page: Service, Organization, BreadcrumbList, FAQ
  - Landing page: Organization, BreadcrumbList, FAQ
  - Homepage: Organization, WebSite, SearchAction
- Flag opportunity for `schema-generator` capability to create the markup

## Phase 9: Content Quality Assessment

### Current State Assessment
- Word count (thin content threshold: < 300 words for key pages)
- Readability: sentence length, paragraph length, reading level
- Content freshness: any dates or references that are outdated?
- Unique value: does this content offer something competitors don't?
- Content completeness: are there obvious subtopics missing?

### Competitive Content Benchmarking
- WebSearch the target keyword
- Analyze top 3 ranking pages:
  - Word count comparison
  - Subtopics covered that this content misses
  - Content formats used (lists, tables, images, videos)
  - FAQ sections present
- Identify content gaps vs top rankers

### Optimization Recommendations
- Minimum word count recommendations by content type
- Subtopics to add based on competitor analysis
- Content format improvements (add a table, add an FAQ section, add a summary)
- Freshness updates needed

## Phase 10: Scoring and Output

### Before/After Scoring

Score each element from 0-10:

| Element | Weight | Current Score | Optimized Score (projected) |
|---------|--------|---------------|----------------------------|
| Title Tag | 15% | ? | ? |
| Meta Description | 10% | ? | ? |
| Heading Structure | 15% | ? | ? |
| Keyword Density | 15% | ? | ? |
| Internal Links | 10% | ? | ? |
| Image Optimization | 10% | ? | ? |
| Schema Markup | 10% | ? | ? |
| Content Quality | 15% | ? | ? |
| **Overall** | **100%** | **?** | **?** |

### Output JSON

```json
{
  "url": "https://example.com/blog/target-post",
  "target_keyword": "shopify store optimization",
  "analyzed_at": "2024-01-15T14:30:00Z",
  "content_type": "blog_post",
  "current_score": "4.8/10",
  "projected_score": "8.5/10",
  "score_breakdown": {
    "title_tag": { "current": 3, "projected": 9, "weight": "15%" },
    "meta_description": { "current": 2, "projected": 8, "weight": "10%" },
    "heading_structure": { "current": 5, "projected": 9, "weight": "15%" },
    "keyword_density": { "current": 6, "projected": 8, "weight": "15%" },
    "internal_links": { "current": 4, "projected": 8, "weight": "10%" },
    "image_optimization": { "current": 3, "projected": 8, "weight": "10%" },
    "schema_markup": { "current": 0, "projected": 9, "weight": "10%" },
    "content_quality": { "current": 7, "projected": 9, "weight": "15%" }
  },
  "optimizations": [
    {
      "element": "Title Tag",
      "priority": "High",
      "current": "Our Blog Post Title",
      "recommended": "Shopify Store Optimization: 12 Proven Tactics for 2024 | Brand",
      "alternatives": ["Alt title 1", "Alt title 2"],
      "impact": "High -- title directly affects CTR and rankings"
    }
  ],
  "keyword_placement_checklist": {
    "title_tag": { "present": false, "action": "Add target keyword to title" },
    "meta_description": { "present": false, "action": "Add target keyword to meta description" },
    "h1": { "present": true, "action": "No change needed" },
    "first_100_words": { "present": false, "action": "Add keyword to opening paragraph" },
    "h2_headings": { "present": true, "action": "No change needed" },
    "image_alt": { "present": false, "action": "Add keyword to hero image alt text" },
    "url_slug": { "present": true, "action": "No change needed" },
    "conclusion": { "present": false, "action": "Add keyword to closing paragraph" }
  },
  "content_gaps": [
    "Competitors cover 'Shopify speed optimization' -- add a section on this",
    "Top rankers include a comparison table -- add one",
    "FAQ section present on 3/5 top rankers -- add FAQ with PAA questions"
  ],
  "internal_link_suggestions": [
    { "anchor_text": "Shopify CRO audit", "target_url": "/services/cro-audit", "context": "Add in section about conversion optimization" }
  ],
  "schema_recommendation": "Add Article + FAQ + BreadcrumbList schema. Use schema-generator skill to create."
}
```

## Example Usage

Trigger phrases:
- "Optimize [url] for [keyword]"
- "SEO check on [url] for [keyword]"
- "How well is [url] optimized for [keyword]?"
- "On-page SEO analysis for [url]"
- "Content SEO score for [url] targeting [keyword]"

```
User: Optimize plasho.com/services/shopify for "shopify development agency"
Assistant: [crawls the page, analyzes all on-page elements against the keyword, returns scored checklist with specific fixes]
```

```
User: How well is my blog post optimized for "ecommerce CRO tips"?
Assistant: [analyzes title, meta, headings, keyword density, links, images, schema, content quality, returns before/after scorecard]
```
