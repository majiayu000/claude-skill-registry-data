---
name: wp-seo-auditor
description: Automated WordPress SEO audit with actionable fix list. Checks on-page SEO, technical SEO, EEAT signals, GEO readiness, schema markup, internal linking, and content quality. Produces a scored audit report with prioritized fixes. Use when user wants to audit a published WordPress article, check an article's SEO health, find on-page SEO issues, or review content quality against EEAT/GEO benchmarks.
---

# WordPress SEO Auditor

Audit published or draft WordPress articles against SEO best practices. Output a scored report with specific, prioritized fix actions.

## Audit Checklist: 8 Dimensions

### 1. On-Page SEO (Weight: 20%)

- [ ] Title tag includes primary keyword and is ≤ 60 characters
- [ ] Meta Description includes primary keyword and is ≤ 160 characters
- [ ] H1 matches or closely mirrors the title, includes primary keyword
- [ ] H2/H3 hierarchy is correct — no skipped levels, no orphaned H3s
- [ ] URL slug is clean: hyphen-case, includes primary keyword, ≤ 75 characters
- [ ] Primary keyword appears in first 100 words of body text
- [ ] Keyword density: 0.5-2.0% for primary, 0.3-1.0% for secondaries
- [ ] No keyword stuffing — check adjacency of repeated keyword instances

### 2. EEAT Signal Audit (Weight: 15%)

- [ ] Expertise: Does the article cite specific technical knowledge, engineering details, or professional credentials?
- [ ] Experience: Is there a real-world case study, project example, or hands-on insight?
- [ ] Authoritativeness: Are industry standards, certifications, or authoritative references cited?
- [ ] Trustworthiness: Are warranty info, contact details, certifications, and transparent pricing included?
- [ ] Author byline present and links to an author page with credentials?

### 3. GEO Readiness (Weight: 15%)

- [ ] TL;DR or executive summary present (50-80 words at top)
- [ ] Key Takeaways bullet list (3-5 items)
- [ ] At least one comparison table or step-by-step list
- [ ] FAQ section present with 4-6 Q&As using proper Question/Answer format
- [ ] Headings framed as questions users actually search (PAA optimization)

### 4. Technical SEO (Weight: 15%)

- [ ] Canonical URL is set and self-referencing
- [ ] Open Graph title, description, and image tags present
- [ ] Twitter Card tags present
- [ ] Article is in the XML sitemap
- [ ] robots meta is "index, follow" (not noindex)
- [ ] Page load speed: check for oversized images, missing lazy load
- [ ] Mobile viewport meta tag present

### 5. Schema Markup (Weight: 10%)

- [ ] Article schema present and valid
- [ ] FAQ schema present if article has FAQs
- [ ] HowTo schema present if article has step-by-step instructions
- [ ] No schema errors (validate against schema.org validator)
- [ ] Publisher/Organization info correctly filled

### 6. Internal & External Links (Weight: 10%)

- [ ] At least 3 internal links: product page, case page, contact page
- [ ] Anchor text is descriptive (not "click here" or "read more")
- [ ] At least 2-3 external links to authoritative sources
- [ ] External links open in new tab: `target="_blank" rel="noopener noreferrer"`
- [ ] No broken links (check HTTP status for every link)
- [ ] External link profile balanced (not all Wikipedia, not all commercial)

### 7. Content Quality (Weight: 10%)

- [ ] Word count ≥ 2500 for cornerstone content, ≥ 1500 for standard
- [ ] No AI cliché openings ("In today's fast-paced world", "In the ever-evolving landscape")
- [ ] No fluff phrases ("It is important to note that" — flagged for removal)
- [ ] Average sentence length ≤ 25 words
- [ ] Paragraph length ≤ 4 sentences
- [ ] Readability: Flesch Reading Ease ≥ 50
- [ ] Data claims backed by sources — flag any unsupported statistics

### 8. Image Audit (Weight: 5%)

- [ ] At least 1 image per 500 words
- [ ] Every image has descriptive Alt text (include keyword where natural)
- [ ] Image file names are descriptive (not IMG_001.jpg)
- [ ] Images are compressed and properly sized
- [ ] Key images have ImageObject schema

## Score Calculation

| Dimension | Max Score | Weight |
|---|---|---|
| On-Page SEO | 20 | 20% |
| EEAT Signals | 15 | 15% |
| GEO Readiness | 15 | 15% |
| Technical SEO | 15 | 15% |
| Schema Markup | 10 | 10% |
| Links | 10 | 10% |
| Content Quality | 10 | 10% |
| Image Audit | 5 | 5% |
| **Total** | **100** | **100%** |

## Output Format

1. **Overall Score** (X/100) with a grade: A (90+) / B (80-89) / C (70-79) / D (60-69) / F (<60)
2. **Dimension Breakdown** — score per dimension with flagged items
3. **Priority Fix List** — ranked by impact (Critical / High / Medium / Low):
   - Critical: Fixes that directly block indexing or ranking (broken canonical, noindex, missing title)
   - High: Strong ranking signals (missing H1 keyword, no EEAT, thin content)
   - Medium: Optimization opportunities (add FAQ, optimize images, improve readability)
   - Low: Nice-to-haves (Twitter cards, minor schema enhancements)
4. **Before/After Summary** — what will change after applying Critical + High fixes

## Execution

- Accept article URL or raw HTML/text as input
- If URL provided, fetch the page and extract: title, meta tags, headings, body text, schema blocks, all links, all images
- Run all 8 dimension checks against the extracted content
- Produce the scored report with the four output sections above