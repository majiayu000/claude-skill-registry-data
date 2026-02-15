---
name: on-page-seo-auditor
description: 'Use when the user asks to "audit page SEO", "on-page SEO check", "SEO score", "page optimization", "what SEO issues does this page have", "what is wrong with this page SEO", "score my page", or "why is this page not ranking". Performs comprehensive on-page SEO audits to identify optimization opportunities including title tags, meta descriptions, headers, content quality, internal linking, and image optimization. For server, speed, and crawl issues, see technical-seo-checker. For full EEAT content quality scoring, see content-quality-auditor.'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "medium"
  tags:
    - seo
    - on-page audit
    - page optimization
    - seo audit
    - content optimization
    - header tags
    - image optimization
    - seo score
  triggers:
    - "audit page SEO"
    - "on-page SEO check"
    - "SEO score"
    - "page optimization"
    - "what SEO issues"
    - "check my page"
    - "on-page audit"
    - "what's wrong with this page's SEO"
    - "score my page"
    - "why isn't this page ranking"
---

# On-Page SEO Auditor


> **[SEO & GEO Skills Library](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)** · 20 skills for SEO + GEO · Install all: `npx skills add aaron-he-zhu/seo-geo-claude-skills`

<details>
<summary>Browse all 20 skills</summary>

**Research** · [keyword-research](../../research/keyword-research/) · [competitor-analysis](../../research/competitor-analysis/) · [serp-analysis](../../research/serp-analysis/) · [content-gap-analysis](../../research/content-gap-analysis/)

**Build** · [seo-content-writer](../../build/seo-content-writer/) · [geo-content-optimizer](../../build/geo-content-optimizer/) · [meta-tags-optimizer](../../build/meta-tags-optimizer/) · [schema-markup-generator](../../build/schema-markup-generator/)

**Optimize** · **on-page-seo-auditor** · [technical-seo-checker](../technical-seo-checker/) · [internal-linking-optimizer](../internal-linking-optimizer/) · [content-refresher](../content-refresher/)

**Monitor** · [rank-tracker](../../monitor/rank-tracker/) · [backlink-analyzer](../../monitor/backlink-analyzer/) · [performance-reporter](../../monitor/performance-reporter/) · [alert-manager](../../monitor/alert-manager/)

**Cross-cutting** · [content-quality-auditor](../../cross-cutting/content-quality-auditor/) · [domain-authority-auditor](../../cross-cutting/domain-authority-auditor/) · [entity-optimizer](../../cross-cutting/entity-optimizer/) · [memory-management](../../cross-cutting/memory-management/)

</details>

This skill performs detailed on-page SEO audits to identify issues and optimization opportunities. It analyzes all on-page elements that affect search rankings and provides actionable recommendations.

## When to Use This Skill

- Auditing pages before or after publishing
- Identifying why a page isn't ranking well
- Optimizing existing content for better performance
- Creating pre-publish SEO checklists
- Comparing your on-page SEO to competitors
- Systematic site-wide SEO improvements
- Training team members on SEO best practices

## What This Skill Does

1. **Title Tag Analysis**: Evaluates title optimization and CTR potential
2. **Meta Description Review**: Checks description quality and length
3. **Header Structure Audit**: Analyzes H1-H6 hierarchy
4. **Content Quality Assessment**: Reviews content depth and optimization
5. **Keyword Usage Analysis**: Checks keyword placement and density
6. **Internal Link Review**: Evaluates internal linking structure
7. **Image Optimization Check**: Audits alt text and file optimization
8. **Technical On-Page Review**: Checks URL, canonical, and mobile factors

## How to Use

### Audit a Single Page

```
Audit the on-page SEO of [URL]
```

```
Check SEO issues on this page targeting [keyword]: [URL/content]
```

### Compare Against Competitors

```
Compare on-page SEO of [your URL] vs [competitor URL] for [keyword]
```

### Audit Content Before Publishing

```
Pre-publish SEO audit for this content targeting [keyword]: [content]
```

## Data Sources

> See [CONNECTORS.md](../../CONNECTORS.md) for tool category placeholders.

**With ~~SEO tool + ~~web crawler connected:**
Claude can automatically pull page HTML via ~~web crawler, fetch keyword search volume and difficulty from ~~SEO tool, retrieve click-through rate data from ~~search console, and download competitor pages for comparison. This enables fully automated audits with live data.

**With manual data only:**
Ask the user to provide:
1. Page URL or complete HTML content
2. Target primary and secondary keywords
3. Competitor page URLs for comparison (optional)

Proceed with the full audit using provided data. Note in the output which findings are from automated crawl vs. manual review.

## Instructions

When a user requests an on-page SEO audit:

1. **Gather Page Information**

   ```markdown
   ### Audit Setup
   
   **Page URL**: [URL]
   **Target Keyword**: [primary keyword]
   **Secondary Keywords**: [additional keywords]
   **Page Type**: [blog/product/landing/service]
   **Business Goal**: [traffic/conversions/authority]
   ```

2. **Audit Title Tag**

   ```markdown
   ## Title Tag Analysis
   
   **Current Title**: [title]
   **Character Count**: [X] characters
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | Length (50-60 chars) | ✅/⚠️/❌ | [notes] |
   | Keyword included | ✅/⚠️/❌ | Position: [front/middle/end] |
   | Keyword at front | ✅/⚠️/❌ | [notes] |
   | Unique across site | ✅/⚠️/❌ | [notes] |
   | Compelling/clickable | ✅/⚠️/❌ | [notes] |
   | Matches intent | ✅/⚠️/❌ | [notes] |
   
   **Title Score**: [X]/10
   
   **Issues Found**:
   - [Issue 1]
   - [Issue 2]
   
   **Recommended Title**:
   "[Optimized title suggestion]"
   
   **Why**: [Explanation of improvements]
   ```

3. **Audit Meta Description**

   ```markdown
   ## Meta Description Analysis
   
   **Current Description**: [description]
   **Character Count**: [X] characters
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | Length (150-160 chars) | ✅/⚠️/❌ | [notes] |
   | Keyword included | ✅/⚠️/❌ | [notes] |
   | Call-to-action present | ✅/⚠️/❌ | [notes] |
   | Unique across site | ✅/⚠️/❌ | [notes] |
   | Accurately describes page | ✅/⚠️/❌ | [notes] |
   | Compelling copy | ✅/⚠️/❌ | [notes] |
   
   **Description Score**: [X]/10
   
   **Issues Found**:
   - [Issue 1]
   
   **Recommended Description**:
   "[Optimized description suggestion]" ([X] chars)
   ```

4. **Audit Header Structure**

   ```markdown
   ## Header Structure Analysis
   
   ### Current Header Hierarchy
   
   ```
   H1: [H1 text]
     H2: [H2 text]
       H3: [H3 text]
       H3: [H3 text]
     H2: [H2 text]
       H3: [H3 text]
     H2: [H2 text]
   ```
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | Single H1 | ✅/⚠️/❌ | Found: [X] H1s |
   | H1 includes keyword | ✅/⚠️/❌ | [notes] |
   | Logical hierarchy | ✅/⚠️/❌ | [notes] |
   | H2s include keywords | ✅/⚠️/❌ | [X]/[Y] contain keywords |
   | No skipped levels | ✅/⚠️/❌ | [notes] |
   | Descriptive headers | ✅/⚠️/❌ | [notes] |
   
   **Header Score**: [X]/10
   
   **Issues Found**:
   - [Issue 1]
   - [Issue 2]
   
   **Recommended Changes**:
   - H1: [suggestion]
   - H2s: [suggestions]
   ```

5. **Audit Content Quality**

   ```markdown
   ## Content Quality Analysis
   
   **Word Count**: [X] words
   **Reading Level**: [Grade level]
   **Estimated Read Time**: [X] minutes
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | Sufficient length | ✅/⚠️/❌ | [comparison to ranking content] |
   | Comprehensive coverage | ✅/⚠️/❌ | [notes] |
   | Unique value/insights | ✅/⚠️/❌ | [notes] |
   | Up-to-date information | ✅/⚠️/❌ | [notes] |
   | Proper formatting | ✅/⚠️/❌ | [notes] |
   | Readability | ✅/⚠️/❌ | [notes] |
   | E-E-A-T signals | ✅/⚠️/❌ | [notes] |
   
   **Content Elements Present**:
   - [ ] Introduction with keyword
   - [ ] Clear sections/structure
   - [ ] Bullet points/lists
   - [ ] Tables where appropriate
   - [ ] Images/visuals
   - [ ] Examples/case studies
   - [ ] Statistics with sources
   - [ ] Expert quotes
   - [ ] FAQ section
   - [ ] Conclusion with CTA
   
   **Content Score**: [X]/10
   
   **Gaps Identified**:
   - [Missing topic/section 1]
   - [Missing topic/section 2]
   
   **Recommendations**:
   1. [Specific improvement]
   2. [Specific improvement]
   ```

6. **Audit Keyword Usage**

   ```markdown
   ## Keyword Optimization Analysis
   
   **Primary Keyword**: "[keyword]"
   **Keyword Density**: [X]%
   
   ### Keyword Placement
   
   | Location | Present | Notes |
   |----------|---------|-------|
   | Title tag | ✅/❌ | Position: [X] |
   | Meta description | ✅/❌ | [notes] |
   | H1 | ✅/❌ | [notes] |
   | First 100 words | ✅/❌ | Word position: [X] |
   | H2 headings | ✅/❌ | In [X]/[Y] H2s |
   | Body content | ✅/❌ | [X] occurrences |
   | URL slug | ✅/❌ | [notes] |
   | Image alt text | ✅/❌ | In [X]/[Y] images |
   | Conclusion | ✅/❌ | [notes] |
   
   ### Secondary Keywords
   
   | Keyword | Occurrences | Status |
   |---------|-------------|--------|
   | [keyword 1] | [X] | ✅/⚠️/❌ |
   | [keyword 2] | [X] | ✅/⚠️/❌ |
   
   ### LSI/Related Terms
   
   **Present**: [list of related terms found]
   **Missing**: [important related terms not found]
   
   **Keyword Score**: [X]/10
   
   **Issues**:
   - [Issue 1]
   
   **Recommendations**:
   - [Suggestion 1]
   ```

7. **Audit Internal Links**

   ```markdown
   ## Internal Linking Analysis
   
   **Total Internal Links**: [X]
   **Unique Internal Links**: [X]
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | Number of internal links | ✅/⚠️/❌ | [X] (recommend 3-5+) |
   | Relevant anchor text | ✅/⚠️/❌ | [notes] |
   | Links to related content | ✅/⚠️/❌ | [notes] |
   | Links to important pages | ✅/⚠️/❌ | [notes] |
   | No broken links | ✅/⚠️/❌ | [X] broken found |
   | Natural placement | ✅/⚠️/❌ | [notes] |
   
   **Current Internal Links**:
   1. "[Anchor text]" → [URL]
   2. "[Anchor text]" → [URL]
   3. "[Anchor text]" → [URL]
   
   **Internal Linking Score**: [X]/10
   
   **Recommended Additional Links**:
   1. Add link to "[Related page]" with anchor "[suggested anchor]"
   2. Add link to "[Related page]" with anchor "[suggested anchor]"
   
   **Anchor Text Improvements**:
   - Change "[current anchor]" to "[improved anchor]"
   ```

8. **Audit Images**

   ```markdown
   ## Image Optimization Analysis
   
   **Total Images**: [X]
   
   ### Image Audit Table
   
   | Image | Alt Text | File Name | Size | Status |
   |-------|----------|-----------|------|--------|
   | [img1] | [alt or "missing"] | [filename] | [KB] | ✅/⚠️/❌ |
   | [img2] | [alt or "missing"] | [filename] | [KB] | ✅/⚠️/❌ |
   
   | Criterion | Status | Notes |
   |-----------|--------|-------|
   | All images have alt text | ✅/⚠️/❌ | [X]/[Y] have alt |
   | Alt text includes keywords | ✅/⚠️/❌ | [notes] |
   | Descriptive file names | ✅/⚠️/❌ | [notes] |
   | Appropriate file sizes | ✅/⚠️/❌ | [notes] |
   | Modern formats (WebP) | ✅/⚠️/❌ | [notes] |
   | Lazy loading enabled | ✅/⚠️/❌ | [notes] |
   
   **Image Score**: [X]/10
   
   **Recommendations**:
   1. Add alt text to image [X]: "[suggested alt text]"
   2. Compress image [Y]: Currently [X]KB, should be under [Y]KB
   3. Rename [filename] to [better-filename]
   ```

9. **Audit Technical On-Page Elements**

   ```markdown
   ## Technical On-Page Analysis
   
   | Element | Current Value | Status | Recommendation |
   |---------|---------------|--------|----------------|
   | URL | [URL] | ✅/⚠️/❌ | [notes] |
   | URL length | [X] chars | ✅/⚠️/❌ | [notes] |
   | URL keywords | [present/absent] | ✅/⚠️/❌ | [notes] |
   | Canonical tag | [URL or "missing"] | ✅/⚠️/❌ | [notes] |
   | Mobile-friendly | [yes/no] | ✅/⚠️/❌ | [notes] |
   | Page speed | [X]s | ✅/⚠️/❌ | [notes] |
   | HTTPS | [yes/no] | ✅/⚠️/❌ | [notes] |
   | Schema markup | [types or "none"] | ✅/⚠️/❌ | [notes] |
   
   **Technical Score**: [X]/10
   ```

10. **CORE-EEAT Content Quality Quick Scan**

    Run a quick scan of on-page-relevant CORE-EEAT items. Reference: [CORE-EEAT Benchmark](../../references/core-eeat-benchmark.md)

    ```markdown
    ## CORE-EEAT Quick Scan

    Content-relevant items from the 80-item benchmark:

    | ID | Check Item | Status | Notes |
    |----|-----------|--------|-------|
    | C01 | Intent Alignment | ✅/⚠️/❌ | Title promise = content delivery |
    | C02 | Direct Answer | ✅/⚠️/❌ | Core answer in first 150 words |
    | C09 | FAQ Coverage | ✅/⚠️/❌ | Structured FAQ present |
    | C10 | Semantic Closure | ✅/⚠️/❌ | Conclusion answers opening |
    | O01 | Heading Hierarchy | ✅/⚠️/❌ | H1→H2→H3, no skipping |
    | O02 | Summary Box | ✅/⚠️/❌ | TL;DR or Key Takeaways |
    | O03 | Data Tables | ✅/⚠️/❌ | Comparisons in tables |
    | O05 | Schema Markup | ✅/⚠️/❌ | Appropriate JSON-LD |
    | O06 | Section Chunking | ✅/⚠️/❌ | Single topic per section |
    | R01 | Data Precision | ✅/⚠️/❌ | ≥5 precise numbers |
    | R02 | Citation Density | ✅/⚠️/❌ | ≥1 per 500 words |
    | R06 | Timestamp | ✅/⚠️/❌ | Updated <1 year |
    | R08 | Internal Link Graph | ✅/⚠️/❌ | Descriptive anchors |
    | R10 | Content Consistency | ✅/⚠️/❌ | No contradictions |
    | Exp01 | First-Person Narrative | ✅/⚠️/❌ | "I tested" or "We found" |
    | Ept01 | Author Identity | ✅/⚠️/❌ | Byline + bio present |
    | T04 | Disclosure Statements | ✅/⚠️/❌ | Affiliate links disclosed |

    **CORE-EEAT Quick Score**: [X]/17 items passing

    > For a complete 80-item audit with weighted scoring, use [content-quality-auditor](../../cross-cutting/content-quality-auditor/).
    ```

11. **Generate Audit Summary**

    ```markdown
    # On-Page SEO Audit Report
    
    **Page**: [URL]
    **Target Keyword**: [keyword]
    **Audit Date**: [date]
    
    ## Overall Score: [X]/100
    
    ```
    Score Breakdown:
    ████████░░ Title Tag: 8/10
    ██████░░░░ Meta Description: 6/10
    █████████░ Headers: 9/10
    ███████░░░ Content: 7/10
    ██████░░░░ Keywords: 6/10
    █████░░░░░ Internal Links: 5/10
    ████░░░░░░ Images: 4/10
    ████████░░ Technical: 8/10
    ```
    
    ## Priority Issues
    
    ### 🔴 Critical (Fix Immediately)
    1. [Critical issue 1]
    2. [Critical issue 2]
    
    ### 🟡 Important (Fix Soon)
    1. [Important issue 1]
    2. [Important issue 2]
    
    ### 🟢 Minor (Nice to Have)
    1. [Minor issue 1]
    2. [Minor issue 2]
    
    ## Quick Wins
    
    These changes will have immediate impact:
    
    1. **[Change 1]**: [Why and how]
    2. **[Change 2]**: [Why and how]
    3. **[Change 3]**: [Why and how]
    
    ## Detailed Recommendations
    
    ### Title Tag
    - **Current**: [current title]
    - **Recommended**: [new title]
    - **Impact**: [expected improvement]
    
    ### Meta Description
    - **Current**: [current description]
    - **Recommended**: [new description]
    - **Impact**: [expected improvement]
    
    ### Content Improvements
    1. [Specific content change with location]
    2. [Specific content change with location]
    
    ### Internal Linking
    1. Add link: "[anchor]" → [destination]
    2. Add link: "[anchor]" → [destination]
    
    ### Image Optimization
    1. [Image 1]: [change needed]
    2. [Image 2]: [change needed]
    
    ## Competitor Comparison
    
    | Element | Your Page | Top Competitor | Gap |
    |---------|-----------|----------------|-----|
    | Word count | [X] | [Y] | [+/-Z] |
    | Internal links | [X] | [Y] | [+/-Z] |
    | Images | [X] | [Y] | [+/-Z] |
    | H2 headings | [X] | [Y] | [+/-Z] |
    
    ## Action Checklist
    
    - [ ] Update title tag
    - [ ] Rewrite meta description
    - [ ] Add keyword to H1
    - [ ] Add [X] more internal links
    - [ ] Add alt text to [X] images
    - [ ] Add [X] more content sections
    - [ ] Implement FAQ schema
    - [ ] [Additional action items]
    
    ## Expected Results

    After implementing these changes:
    - Estimated ranking improvement: [X] positions
    - Estimated CTR improvement: [X]%
    - Estimated traffic increase: [X]%
    ```

## Validation Checkpoints

### Input Validation
- [ ] Target keyword(s) clearly specified by user
- [ ] Page content accessible (either via URL or provided HTML)
- [ ] If competitor comparison requested, competitor URL provided

### Output Validation
- [ ] Every recommendation cites specific data points (not generic advice)
- [ ] Scores based on measurable criteria, not subjective opinion
- [ ] All suggested changes include specific locations (title tag, H2 #3, paragraph 5, etc.)
- [ ] Source of each data point clearly stated (~~SEO tool data, user-provided, ~~web crawler, or manual review)

## Example

**User**: "Audit the on-page SEO of https://example.com/best-noise-cancelling-headphones targeting 'best noise cancelling headphones'"

**Output**:

```markdown
# On-Page SEO Audit Report

**Page**: https://example.com/best-noise-cancelling-headphones
**Target Keyword**: best noise cancelling headphones
**Secondary Keywords**: wireless noise cancelling headphones, ANC headphones, noise cancelling headphones review
**Page Type**: commercial (reviews/roundup)
**Audit Date**: 2025-01-15

## Summary

| Audit Area | Score | Key Finding |
|------------|-------|-------------|
| Title Tag | 8/10 | Good keyword placement; slightly long at 63 chars |
| Meta Description | 6/10 | Missing CTA; keyword present but generic copy |
| Header Structure | 9/10 | Clean hierarchy; H2s cover all major products |
| Content Quality | 7/10 | 2,400 words is solid; lacks original test data |
| Keyword Optimization | 8/10 | Strong placement; density at 1.2% is healthy |
| Internal Links | 5/10 | Only 2 internal links; missing links to brand pages |
| Images | 6/10 | 3/8 images missing alt text; no WebP format |
| Technical Elements | 7/10 | Missing Product schema; good URL and mobile |

## Overall Score: 71/100

Calculation: (8x0.15 + 6x0.05 + 9x0.10 + 7x0.25 + 8x0.15 + 5x0.10 + 6x0.10 + 7x0.10) x 10 = 71

Score Breakdown:
████████░░ Title Tag:        8/10  (15%)
██████░░░░ Meta Description: 6/10  ( 5%)
█████████░ Headers:          9/10  (10%)
███████░░░ Content:          7/10  (25%)
████████░░ Keywords:         8/10  (15%)
█████░░░░░ Internal Links:   5/10  (10%)
██████░░░░ Images:           6/10  (10%)
███████░░░ Technical:        7/10  (10%)

## Priority Issues

### Critical
1. **Internal linking severely underdeveloped** — Only 2 internal links found. Add links to individual headphone review pages (/sony-wh1000xm5-review, /bose-qc-ultra-review) and the headphones category page. Target 5-8 contextual internal links.
2. **3 product images missing alt text** — Images for Sony WH-1000XM5, Bose QC Ultra, and Apple AirPods Max have empty alt attributes. Each missing alt tag is a lost ranking signal in Google Images.

### Important
1. **Meta description lacks call-to-action** — Current description states facts but does not compel clicks. Add "Compare prices and features" or "See our top picks" to drive CTR.

## Quick Wins

1. **Add alt text to 3 images** (5 min) — Use descriptive text like "Sony WH-1000XM5 noise cancelling headphones on desk" instead of empty attributes.
2. **Rewrite meta description with CTA** (5 min) — Change to: "Compare the 10 best noise cancelling headphones for 2025. Expert-tested picks from Sony, Bose, and Apple with pros, cons, and pricing. See our top picks."
3. **Add 4+ internal links** (10 min) — Link product names to their individual review pages and add a "See all headphones" link to the category hub.
```

## Audit Checklists by Page Type

### Blog Post Checklist

```markdown
- [ ] Title includes keyword and is compelling
- [ ] Meta description has keyword and CTA
- [ ] Single H1 with keyword
- [ ] H2s cover main topics
- [ ] Keyword in first 100 words
- [ ] 1,500+ words for competitive topics
- [ ] 3+ internal links with varied anchors
- [ ] Images with descriptive alt text
- [ ] FAQ section with schema
- [ ] Author bio with credentials
```

### Product Page Checklist

```markdown
- [ ] Product name in title
- [ ] Price and availability in description
- [ ] H1 is product name
- [ ] Product features in H2s
- [ ] Multiple product images with alt text
- [ ] Customer reviews visible
- [ ] Product schema implemented
- [ ] Related products linked
- [ ] Clear CTA button
```

### Landing Page Checklist

```markdown
- [ ] Keyword-optimized title
- [ ] Benefit-focused meta description
- [ ] Clear H1 value proposition
- [ ] Supporting H2 sections
- [ ] Trust signals (testimonials, logos)
- [ ] Single clear CTA
- [ ] Fast page load speed
- [ ] Mobile-optimized layout
```

## Tips for Success

1. **Prioritize issues by impact** - Fix critical issues first
2. **Compare to competitors** - See what's working for top rankings
3. **Balance optimization and readability** - Don't over-optimize
4. **Audit regularly** - Content degrades over time
5. **Test changes** - Track ranking changes after updates

## Scoring Rubric

### Section Weight Distribution

| Audit Section | Weight | Max Score | Rationale |
|--------------|--------|-----------|-----------|
| Title Tag | 15% | 15 | Strongest single ranking signal |
| Meta Description | 5% | 5 | CTR impact, not direct ranking factor |
| Header Structure | 10% | 10 | Content organization, semantic signals |
| Content Quality | 25% | 25 | Strongest holistic ranking factor |
| Keyword Optimization | 15% | 15 | Relevance signals |
| Internal/External Links | 10% | 10 | Authority flow, context signals |
| Image Optimization | 10% | 10 | Accessibility + image search opportunity |
| Page-Level Technical | 10% | 10 | Core Web Vitals, mobile, security |

### Scoring Scale per Factor

| Score | Meaning | Action Required |
|-------|---------|-----------------|
| 10/10 | Excellent — follows all best practices | None |
| 7-9/10 | Good — minor improvements possible | Optional optimization |
| 4-6/10 | Needs work — notable issues | Fix within this week |
| 1-3/10 | Poor — significant problems | Fix immediately (Critical) |
| 0/10 | Missing or broken | Fix immediately (Blocking) |

### Scoring Conversion Formula

Each section is scored out of 10, then converted to the 100-point overall score using section weights:

```
Overall Score = Sum of (section_score x section_weight) x 10
```

Where section weights are: Title 0.15, Meta 0.05, Headers 0.10, Content 0.25, Keywords 0.15, Links 0.10, Images 0.10, Technical 0.10.

**Worked example:**

| Section | Score /10 | Weight | Weighted |
|---------|-----------|--------|----------|
| Title Tag | 8 | 0.15 | 1.20 |
| Meta Description | 6 | 0.05 | 0.30 |
| Header Structure | 9 | 0.10 | 0.90 |
| Content Quality | 7 | 0.25 | 1.75 |
| Keyword Optimization | 8 | 0.15 | 1.20 |
| Internal/External Links | 5 | 0.10 | 0.50 |
| Image Optimization | 6 | 0.10 | 0.60 |
| Page-Level Technical | 7 | 0.10 | 0.70 |
| **Total** | | **1.00** | **7.15** |

**Overall Score** = 7.15 x 10 = **71 / 100**

## Common Issue Resolution Playbook

### Title Tag Issues

| Issue | Impact | Quick Fix Template |
|-------|--------|-------------------|
| Missing title | Critical | Add: "[Primary Keyword]: [Benefit] | [Brand]" |
| Too long (>60 chars) | Medium | Shorten: move brand to end, remove filler words |
| Too short (<30 chars) | Medium | Expand: add modifier, benefit, or year |
| Missing keyword | High | Rewrite to include primary keyword in first half |
| Duplicate title | High | Make each page title unique; add page-specific modifier |

### Meta Description Issues

| Issue | Impact | Quick Fix Template |
|-------|--------|-------------------|
| Missing description | Medium | Write: "[What this page covers]. [Key benefit]. [CTA]." (150-160 chars) |
| Too long (>160 chars) | Low | Trim from end; ensure core message fits in 150 chars |
| Missing keyword | Low | Naturally incorporate primary keyword |
| No CTA | Low | Add: "Learn more", "Discover", "Find out", "Get started" |
| Duplicated across pages | Medium | Write unique description for each page |

### Header Issues

| Issue | Impact | Quick Fix |
|-------|--------|-----------|
| Missing H1 | Critical | Add one H1 per page containing primary keyword |
| Multiple H1s | High | Keep one H1, convert others to H2 |
| Skipped heading levels | Medium | Use sequential hierarchy: H1→H2→H3 |
| Headers not descriptive | Medium | Rewrite to include keyword variations |
| No H2s (single long block) | Medium | Break content into sections with descriptive H2s every 200-300 words |

### Content Issues

| Issue | Impact | Quick Fix |
|-------|--------|-----------|
| Thin content (<300 words) | Critical | Expand with subtopics, FAQ, examples |
| Keyword stuffing (>3%) | High | Reduce usage, use synonyms and related terms |
| No structured data | Medium | Add relevant schema (FAQ, HowTo, Article) |
| Missing internal links | Medium | Add 3-5 contextual internal links |
| No images | Low | Add 2-3 relevant images with alt text |

## Industry Benchmark Data

### Content Length Benchmarks by Query Type

| Query Type | Top 10 Average Word Count | Recommended Minimum |
|-----------|--------------------------|-------------------|
| Informational (guides) | 2,200 words | 1,500 words |
| Commercial (reviews) | 1,800 words | 1,200 words |
| Transactional (product) | 800 words | 500 words |
| Local (service pages) | 600 words | 400 words |
| Definition queries | 1,200 words | 800 words |

### Page Speed Benchmarks

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤2.5s | 2.5-4.0s | >4.0s |
| FID/INP | ≤100ms/200ms | 100-300ms | >300ms |
| CLS | ≤0.1 | 0.1-0.25 | >0.25 |
| TTFB | ≤800ms | 800-1800ms | >1800ms |

## Reference Materials

- [Scoring Rubric](./references/scoring-rubric.md) — Detailed scoring criteria, weight distribution, and grade boundaries for on-page audits

## Related Skills

- [seo-content-writer](../../build/seo-content-writer/) — Create optimized content
- [technical-seo-checker](../technical-seo-checker/) — Technical SEO audit
- [meta-tags-optimizer](../../build/meta-tags-optimizer/) — Optimize meta tags
- [serp-analysis](../../research/serp-analysis/) — SERP context for audit findings
- [content-refresher](../content-refresher/) — Update existing content
- [content-quality-auditor](../../cross-cutting/content-quality-auditor/) — Full 80-item CORE-EEAT audit
- [internal-linking-optimizer](../internal-linking-optimizer/) — Optimize internal link structure
- [schema-markup-generator](../../build/schema-markup-generator/) — Validate and generate schema markup

