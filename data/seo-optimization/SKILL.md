---
name: SEO Optimization
description: Optimize content for search engines to increase organic traffic and rankings
version: 1.0.0
triggers:
  - "seo"
  - "seo optimization"
  - "search optimization"
  - "keyword research"
  - "rank higher"
  - "skill:seo-optimization"
---

# SEO Optimization

## Purpose

Optimize content to rank higher in search engines and drive organic traffic:
- Research and target the right keywords
- Structure content for search intent
- Build technical SEO foundations
- Earn quality backlinks

## When to Use This Skill

- Optimizing existing blog posts
- Planning new content around keywords
- Technical SEO audits
- Competitor keyword analysis
- Local SEO optimization
- E-commerce product pages

## Core Concepts

### The SEO Pyramid

```
                    ┌─────────────┐
                    │  BACKLINKS  │ ← Authority building
                    └──────┬──────┘
               ┌───────────┼───────────┐
          ┌────┴────┐ ┌────┴────┐ ┌────┴────┐
          │Content  │ │On-Page  │ │Technical│
          │Quality  │ │Elements │ │ SEO     │
          └─────────┘ └─────────┘ └─────────┘
                    ┌───────────┐
                    │ KEYWORDS  │ ← Foundation
                    └───────────┘
```

### Search Intent Types

```typescript
type SearchIntent =
  | 'informational'    // "What is..." - Answer questions
  | 'navigational'     // "Netflix login" - Brand queries
  | 'transactional'    // "Buy iPhone" - Purchase intent
  | 'commercial'       // "Best laptop 2024" - Research before buy

function matchIntent(keyword: string, content: Content): boolean {
  // Informational: How-to guides, explanations
  // Navigational: Brand pages, login
  // Transactional: Pricing, demo, buy
  // Commercial: Comparisons, reviews
}
```

## Patterns

### Pattern 1: On-Page SEO Checklist

```markdown
## Title Tag (50-60 characters)
<title>[Primary Keyword] - [Benefit] | [Brand]</title>

## Meta Description (150-160 characters)
<meta name="description" content="[Compelling description with keywords and CTA]">

## Heading Structure
<H1>[Title matching title tag]</H1>
<H2>[Major section - includes secondary keywords]</H2>
<H3>[Sub-section - includes related keywords]</H3>
<H2>[Another major section]</H2>
...

## Content Optimization
✓ Primary keyword in first paragraph
✓ Secondary keywords in 2-3 paragraphs each
✓ Keywords in bold/strong (2-3 occurrences)
✓ Related keywords naturally throughout
✓ LSI keywords for context

## Image Optimization
✓ Alt text with keywords
✓ Compressed file sizes
✓ Descriptive filenames
✓ Lazy loading for below-fold images

## Internal Linking
✓ 2-4 internal links to related content
✓ Anchor text varies naturally
✓ Links to pillar/cluster content

## Technical Elements
✓ Fast loading (<3 seconds)
✓ Mobile responsive
✓ SSL certificate (HTTPS)
✓ XML sitemap submitted
✓ Robots.txt configured
✓ Canonical tags for duplicates
```

### Pattern 2: Keyword Research Framework

```typescript
interface KeywordData {
  keyword: string;           // Target keyword
  volume: number;            // Monthly searches
  difficulty: number;        // 0-100 scale
  cpc: number;               // Cost per click
  intent: SearchIntent;      // Type of search
  serpFeatures: string[];    // Featured snippets, etc.
}

const researchKeywords = (topic: string): KeywordData[] => {
  return [
    // Primary keyword (high volume, high difficulty)
    { keyword: `${topic}`, volume: 10000, difficulty: 70, intent: 'informational' },
    // Long-tail keyword (low volume, low difficulty)
    { keyword: `how to ${topic} for beginners`, volume: 1000, difficulty: 30, intent: 'informational' },
    // Commercial intent
    { keyword: `best ${topic} tools`, volume: 5000, difficulty: 60, intent: 'commercial' },
    // Question keyword (featured snippet)
    { keyword: `what is ${topic}`, volume: 3000, difficulty: 40, intent: 'informational' },
  ];
}
```

### Pattern 3: Content Brief Template

```markdown
# Content Brief: [Target Keyword]

## Basic Info
- Primary Keyword: [keyword]
- Target Search Intent: [informational/navigational/transactional/commercial]
- Target Word Count: [1,500-2,500 words]
- Suggested Title: "[title with keyword]"
- Target Ranking: [Position 1-3]

## Keyword Strategy
**Primary Keyword:** [keyword]
**Secondary Keywords:**
- [keyword 1]
- [keyword 2]
- [keyword 3]

**Related Terms to Include:**
- [term 1]
- [term 2]
- [term 3]

**Questions to Answer:**
- [Question 1]
- [Question 2]
- [Question 3]

## Content Structure
**H2 Outline:**
1. [Section about X]
2. [Section about Y]
3. [Section about Z]

**Featured Snippet Target:**
Question: "[Question to answer]"
Answer: "[50-word answer - direct, concise]"

## Competitor Analysis
**Top 3 Ranking Pages:**
1. [URL 1] - Strengths, weaknesses
2. [URL 2] - Strengths, weaknesses
3. [URL 3] - Strengths, weaknesses

**Content Gaps to Exploit:**
- [Gap 1]
- [Gap 2]

## Links to Include
**Internal Links (2-4):**
- [Link 1 to pillar/cluster content]
- [Link 2 to related content]

**External Links (2-4):**
- [Link to authoritative source 1]
- [Link to authoritative source 2]

## Success Metrics
- Target word count: [number]
- Readability grade: [6-8]
- Keyword density: [1-2%]
- Images: [3-5 with optimized alt text]
```

## Step-by-Step Process

1. **Keyword Research**
   - Use Ahrefs/Semrush/Moz for data
   - Find keywords with right volume/difficulty balance
   - Analyze search intent
   - Identify content gaps

2. **Competitive Analysis**
   - Analyze top-ranking pages
   - Identify what makes them rank
   - Find gaps to outrank them
   - Note their word count and structure

3. **Content Planning**
   - Create detailed content briefs
   - Define target word count
   - Plan headings and structure
   - Specify internal/external links

4. **On-Page Optimization**
   - Include keywords in title/meta
   - Structure with H2s/H3s
   - Optimize images
   - Add internal links

5. **Technical SEO**
   - Fix crawl errors
   - Improve page speed
   - Ensure mobile-friendliness
   - Submit sitemap

6. **Link Building**
   - Create link-worthy content
   - Reach out for backlinks
   - Build internal links
   - Monitor backlink profile

## FrankX Application

```markdown
# SEO Strategy: [TOPIC] for [AUDIENCE]

## The FrankX SEO Philosophy

Most SEO is playing defense.

FrankX plays offense.

**Our approach:**

1. Own the narrative, not just the keywords
2. Create content so good they have to link
3. Build topical authority, not just page authority

## Target Keyword Clusters

**Pillar Page:** "[Ultimate Guide to TOPIC]"
- 10,000+ words
- Comprehensive coverage
- Links to all cluster content

**Cluster Content:**
- "How to [TOPIC] for Beginners" (1,500 words)
- "[TOPIC] Mistakes to Avoid" (1,200 words)
- "The Science Behind [TOPIC]" (1,800 words)
- "[TOPIC] Case Studies" (2,000 words)

## Link Building Strategy

**Resource Page Outreach:**
- Create ultimate resource pages
- Pitch to relevant resource pages
- Track responses and follow up

**HARO/Connectively:**
- Position as expert source
- Provide valuable insights
- Earn backlinks from journalists

**Broken Link Building:**
- Find broken links in niche
- Offer content as replacement
- Easy wins for backlinks
```

## Anti-Patterns

| Bad Practice | Why It's Bad | Better Approach |
|--------------|--------------|-----------------|
| Keyword stuffing | Penalized by Google | Natural keyword usage |
| Ignoring search intent | Low engagement metrics | Match content to intent |
| Thin content (<1,000 words) | Doesn't satisfy users | Comprehensive 1,500+ words |
| No internal linking | Weak site structure | Connect related content |
| Duplicate content | Confuses search engines | Use canonical tags |
| Ignoring mobile | Poor rankings, UX | Mobile-first design |
| Slow page speed | High bounce rate | Optimize images, minify |

## Quick Commands

```bash
# Research keywords for topic
skill:seo-optimization, research keywords for [TOPIC]

# Audit existing content
skill:seo-optimization, audit my blog post at [URL]

# Create content brief
skill:seo-optimization, create a content brief for [KEYWORD]

# Optimize existing page
skill:seo-optimization, optimize my page [URL] for [KEYWORD]

# Find link building opportunities
skill:seo-optimization, find link building opportunities for [TOPIC]
```

## Related Skills

- `blog-writing` - Create SEO-optimized content
- `content-strategy` - Plan keyword-targeted content
- `social-media` - Promote content for backlinks
- `video-script` - Create YouTube SEO content

## Resources

- `resources/templates.md` - Content brief templates
- `resources/checklists.md` - Pre-publication SEO checklist
- `resources/tools.md` - SEO tool recommendations
- `resources/competitor-analysis.md` - Competitor research framework
