---
name: seo-keyword-research
description: Deep competitive keyword research and SEO strategy. Takes a primary keyword and researches supporting keywords, competitor analysis, search intent, and per-page keyword mapping. Outputs docs/seo-analysis.md. Triggers on "keyword research", "SEO research", "SEO strategy", "competitive analysis", "rank for keyword".
---

# SEO Keyword Research & Competitive Analysis

Comprehensive keyword research to rank for competitive markets.

## Prerequisites

- docs/sitemap.md should exist (run sitemap-structure skill first)
- User provides primary keyword they want to rank for

## Workflow

1. **Gather Input** - Primary keyword, location, business type, competitors (if known)
2. **Competitive Analysis** - Analyze top 5 ranking competitors via WebSearch
3. **Keyword Discovery** - Find primary, secondary, long-tail, local, question, and semantic keywords
4. **Intent Classification** - Categorize every keyword by search intent
5. **SERP Analysis** - Understand what Google rewards for target keywords
6. **Keyword Mapping** - Assign keywords to pages from docs/sitemap.md
7. **Content Gap Analysis** - Find opportunities competitors miss
8. **Write Output** - Create docs/seo-analysis.md

## Input Template

```
Primary Keyword: [The main keyword you want to rank for]
Location: [Target geographic area]
Business Type: [Industry/niche]
Known Competitors: [URLs of competitors, if known - optional]
```

---

## Keyword Research Process (WebSearch)

### Step 1: Competitor Discovery

**Search queries to run:**
1. `[primary keyword]` - See who ranks #1-5
2. `[primary keyword] [location]` - Local competitors
3. `[primary keyword] site:google.ch` or `site:google.de` - Regional results
4. `best [service] [location]` - Review/comparison sites

**For each top 5 competitor, note:**
- Domain URL
- Title tag content
- Meta description
- Their apparent primary keyword
- Content depth (comprehensive or thin?)

### Step 2: Competitor Analysis Framework

For each top 5 competitor, analyze:

| Analysis Point | What to Look For |
|----------------|------------------|
| Title Tags | Keywords used, format, length (50-60 chars) |
| Meta Descriptions | CTAs, keywords, unique selling points |
| H1 Headlines | Primary keyword placement |
| Content Structure | H2/H3 topics they cover |
| Page Count | How many pages, what topics |
| Content Depth | Word count, comprehensiveness |
| Unique Content | What they do that others don't |
| Weaknesses | Gaps we can exploit |

### Step 3: Keyword Discovery

**Search queries to run:**

```
[primary keyword] + related searches
[primary keyword] + "wie", "was", "warum" (informational intent)
[primary keyword] + "kaufen", "buchen", "bestellen" (transactional intent)
[primary keyword] + "vergleich", "test", "erfahrung" (commercial investigation)
[primary keyword] + [location variations]
[primary keyword] + [service variations]
```

**Keyword types to find:**

| Type | Description | Example | Priority |
|------|-------------|---------|----------|
| Primary | Main target, high competition | "Webdesign Zürich" | Must rank |
| Secondary | Supporting, medium competition | "Website erstellen lassen" | Should rank |
| Long-tail | Specific, lower competition | "Webdesign Agentur für KMU Zürich" | Quick wins |
| Local | Geographic variations | "Webdesign Winterthur" | Expansion |
| Semantic (LSI) | Related concepts | "Webentwicklung", "Homepage erstellen" | Natural use |
| Question | FAQ opportunities | "Was kostet eine Website?" | Content |

### Step 4: Search Intent Classification

**Classify EVERY keyword by intent:**

| Intent | Signal Words (DE) | Signal Words (EN) | User Goal | Content Type |
|--------|-------------------|-------------------|-----------|--------------|
| Transactional | kaufen, buchen, bestellen, preis | buy, book, order, price | Ready to buy | Service pages, pricing |
| Commercial Investigation | vergleich, beste, test, erfahrung | comparison, best, review | Comparing options | Comparison, reviews |
| Informational | wie, was, warum, anleitung | how, what, why, guide | Learning | Blog, FAQ, guides |
| Navigational | [brand name], [company] | [brand name], [company] | Find specific site | Homepage, about |

### Step 5: SERP Feature Analysis

For primary keywords, note what Google shows:

| SERP Feature | Impact on Strategy |
|--------------|-------------------|
| Featured Snippet | Target with structured content (lists, tables) |
| Local Pack (Map) | Need Google Business Profile optimized |
| Images | Optimize image ALT text, consider gallery |
| Videos | Consider video content creation |
| People Also Ask | FAQ content opportunities |
| Related Searches | Long-tail keyword ideas |

### Step 6: Keyword Difficulty Assessment

**Estimate difficulty based on:**

| Factor | Low Difficulty | High Difficulty |
|--------|----------------|-----------------|
| Competitor Authority | Small local sites | Major brands/portals |
| Content Quality | Thin/outdated content | Comprehensive guides |
| Backlink Profiles | Few backlinks | Many quality backlinks |
| SERP Features | Organic results only | Many SERP features |
| Search Volume | Under 500/month | Over 5000/month |

**Difficulty Rating:**
- **Easy**: Local competitors, thin content, low authority - Target immediately
- **Medium**: Mix of local and regional competitors - Target with quality content
- **Hard**: National brands, comprehensive content - Long-term target
- **Very Hard**: Major portals, Wikipedia, government sites - Consider alternatives

### Step 7: Per-Page Keyword Mapping

Read docs/sitemap.md and assign keywords to each page:

| Page | Primary Keyword | Secondary Keywords | Long-tail Keywords |
|------|-----------------|--------------------|--------------------|
| Homepage | [main keyword] | [2-3 supporting] | [2-3 specific] |
| Services | [service keyword] | [service variations] | [specific services] |
| About | [brand + location] | [trust keywords] | [differentiators] |
| Contact | [contact + location] | [booking keywords] | [specific CTAs] |

**Rules:**
- ONE primary keyword per page (avoid cannibalization)
- Related keywords support the primary
- Different intent = different page
- Homepage: brand + main service + location
- Service pages: specific service + location

### Step 8: Content Gap Analysis

Identify opportunities competitors miss:

1. **Topics they don't cover** - Missing service pages, FAQ topics
2. **Questions they don't answer** - Use "People Also Ask" for ideas
3. **Local pages they lack** - Neighborhood/region targeting
4. **Content depth gaps** - Thin content you can expand on
5. **Fresh content opportunities** - Outdated competitor content

---

## Output Format: docs/seo-analysis.md

```markdown
# SEO Analysis - [Business Name]

## Executive Summary

**Primary Keyword:** [keyword]
**Target Position:** Top 3 within [X months]
**Competitive Landscape:** [Easy/Medium/Hard]
**Key Opportunities:** [1-2 sentence summary]

---

## Competitor Analysis

### Market Overview

| Rank | Competitor | Domain | Key Strength | Key Weakness |
|------|------------|--------|--------------|--------------|
| 1 | [Name] | [URL] | [strength] | [weakness] |
| 2 | [Name] | [URL] | [strength] | [weakness] |
| 3 | [Name] | [URL] | [strength] | [weakness] |
| 4 | [Name] | [URL] | [strength] | [weakness] |
| 5 | [Name] | [URL] | [strength] | [weakness] |

### Competitor Content Analysis

**[Competitor 1 - Current #1]**
- Title: "[their title tag]"
- H1: "[their H1]"
- Content Focus: [topics they cover]
- Strengths: [what works]
- Weaknesses: [gaps to exploit]

[Repeat for top 3 competitors]

### Competitive Advantages We Can Exploit

1. [Gap 1 - e.g., "No competitor has comprehensive pricing transparency"]
2. [Gap 2 - e.g., "All competitors have slow, outdated sites"]
3. [Gap 3 - e.g., "No one targets [specific long-tail keyword]"]

---

## Keyword Strategy

### Primary Keywords (Target: Position 1-3)

| Keyword | Difficulty | Intent | Target Page |
|---------|------------|--------|-------------|
| [keyword] | [Easy/Med/Hard] | [Trans/Comm/Info] | [page route] |

### Secondary Keywords (Target: Position 1-10)

| Keyword | Difficulty | Intent | Target Page |
|---------|------------|--------|-------------|
| [keyword] | [difficulty] | [intent] | [page route] |

### Long-tail Keywords (Quick Wins)

| Keyword | Intent | Target Page | Content Angle |
|---------|--------|-------------|---------------|
| [keyword] | [intent] | [page route] | [how to use it] |

### Local Keywords

| Keyword | Target Page | Priority |
|---------|-------------|----------|
| [service] [city] | [page route] | [P1/P2] |
| [service] [region] | [page route] | [P1/P2] |

### Question Keywords (FAQ Opportunities)

| Question | Intent | Where to Answer |
|----------|--------|-----------------|
| Was kostet [service]? | Commercial | Pricing page / FAQ |
| Wie funktioniert [service]? | Informational | Services page / FAQ |
| [Service] vs [alternative]? | Commercial | Blog / Comparison |

### Semantic Keywords (LSI)

Use these naturally throughout content:
- [semantic keyword 1]
- [semantic keyword 2]
- [semantic keyword 3]
- [semantic keyword 4]

---

## Per-Page Optimization Guide

### Homepage `/`

**Primary Keyword:** [keyword]
**Search Intent:** [Transactional/Navigational]

| Element | Recommendation |
|---------|----------------|
| Title (50-60 chars) | [Primary Keyword] - [Brand] - [Benefit] |
| Meta Description (150-160 chars) | [Description with keyword, USP, and CTA] |
| H1 | [Primary keyword naturally integrated] |
| H2 Topics | [List of H2s to include] |
| Keyword Density | 1-2% for primary, natural for secondary |
| Internal Links | Link to: [pages to link] |

**Secondary Keywords to Include:**
- [keyword 1] - use in [section]
- [keyword 2] - use in [section]

### Services Page `/dienstleistungen`

**Primary Keyword:** [keyword]
**Search Intent:** [intent]

| Element | Recommendation |
|---------|----------------|
| Title (50-60 chars) | [recommendation] |
| Meta Description (150-160 chars) | [recommendation] |
| H1 | [recommendation] |
| H2 Topics | [list] |

**Secondary Keywords to Include:**
- [keyword] - use in [section]

### About Page `/ueber-uns`

[Same format]

### Contact Page `/kontakt`

[Same format]

---

## Content Gap Opportunities

### Pages Competitors Have That We Should Consider

| Page Topic | Competitor Example | Potential Value |
|------------|-------------------|-----------------|
| [topic] | [competitor URL] | [why valuable] |

### Topics No Competitor Covers Well

| Topic | Keyword Opportunity | Recommended Content |
|-------|---------------------|---------------------|
| [topic] | [keyword] | [content type] |

### Blog/Content Ideas (Future)

| Topic | Target Keyword | Search Intent |
|-------|----------------|---------------|
| [topic] | [keyword] | [intent] |

---

## SERP Features Strategy

| Feature | Target Keywords | How to Optimize |
|---------|-----------------|-----------------|
| Featured Snippet | [keywords] | [strategy] |
| Local Pack | [keywords] | Google Business Profile |
| People Also Ask | [questions] | FAQ section |

---

## Implementation Priority

### Phase 1: Foundation (Launch)
- [ ] Optimize homepage for [primary keyword]
- [ ] Optimize services page for [service keywords]
- [ ] Implement all meta titles/descriptions
- [ ] Add FAQ schema for question keywords

### Phase 2: Expansion (Month 1-3)
- [ ] Target long-tail keywords with content
- [ ] Build local pages for [locations] if needed
- [ ] Create content for gap opportunities

### Phase 3: Authority (Month 3-6)
- [ ] Blog content for informational keywords
- [ ] Build backlinks for [target keywords]
- [ ] Local SEO (Google Business Profile)

---

## Success Metrics

| Metric | Current | 3-Month Target | 6-Month Target |
|--------|---------|----------------|----------------|
| Primary Keyword Rank | - | Top 10 | Top 3 |
| Organic Traffic | 0 | [target] | [target] |
| Pages Indexed | 0 | [all pages] | [all pages] |
```

---

## Rules

1. **ALWAYS use WebSearch** for real competitor data - don't guess
2. **Classify EVERY keyword** by search intent
3. **Map EVERY keyword** to a specific page
4. **Identify at least 3** competitive gaps
5. **Provide actionable per-page** recommendations
6. **Prioritize quick wins** (long-tail) alongside primary keywords
7. **One primary keyword per page** - avoid cannibalization

## What This Skill Does NOT Do

- Create the sitemap (use sitemap-structure skill first)
- Write the actual content (use seo-content-optimization skill)
- Implement technical SEO (use technical-seo skill)
- Generate page content (provides strategy only)
