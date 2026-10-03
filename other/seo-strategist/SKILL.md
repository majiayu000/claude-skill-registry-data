---
name: seo-strategist
description: "SEO specialist for keyword research, content gap analysis, on-page optimization, and technical SEO audits. Builds prioritized SEO roadmaps ranked by traffic potential and difficulty. Use when planning content strategy, auditing site SEO, researching keywords, analyzing competitor content, or improving search rankings. Triggers: SEO, keyword research, content strategy, search rankings, on-page optimization, technical SEO, content gap."
metadata:
  version: 1.0.0
  author: Humblytics
---

# SEO Strategist

## Purpose

Build an SEO strategy grounded in keyword data, competitor analysis, on-page optimization, and technical health. Produces prioritized roadmaps ranked by **traffic potential × winnability** — not vanity keyword lists. Bridges technical SEO, content strategy, and conversion intent.

## When to Use

- Building a content calendar backed by keyword research
- Auditing an existing site's SEO health before a relaunch
- Researching keywords for a new product or landing page
- Identifying content gaps vs competitors
- Diagnosing a traffic drop or ranking loss
- Planning a link-building or topical authority strategy

## Before You Start

1. **Goal clarity** — Traffic? Leads? Rankings for specific queries? Brand vs non-brand?
2. **Target audience** — B2B? B2C? Geographic focus? Language?
3. **Current baseline** — Google Search Console data (impressions, clicks, top queries)
4. **Competitive set** — 3-5 direct and indirect competitors to benchmark against
5. **Tool access** — Ahrefs / Semrush / GSC access; if none, note assumptions
6. **Site crawlability** — Technical SEO audit requires a crawl (Screaming Frog, Sitebulb, or Ahrefs Site Audit)

## Core Workflow

### Step 1: Keyword Research with Intent Clustering

Don't chase keywords in isolation. Cluster by **search intent**:

| Intent | Query Pattern | Content Type | Conversion Distance |
|--------|--------------|--------------|---------------------|
| Informational | "how to", "what is", "guide" | Blog post, guide | Far (top-of-funnel) |
| Navigational | "[brand] login", "[product] pricing" | Brand pages | Close (if on-brand) |
| Commercial | "best X", "X vs Y", "X review" | Comparison, listicle | Mid-funnel |
| Transactional | "buy X", "X free trial", "[tool] tool" | Product page, pricing | Close |

For each cluster, rank by:
- **Search volume** (monthly searches)
- **Keyword difficulty** (how hard to rank — KD score)
- **Traffic potential** (not just volume — includes SERP features, CTR)
- **Business relevance** (does the query match your buyer?)
- **Current position** (if already ranking, how close to top 3?)

**The winnability filter:** Prioritize keywords where you can realistically rank top 3 in 3-6 months given your domain authority.

### Step 2: Content Gap Analysis

For each competitor:

1. Pull their top 50-100 ranking pages
2. Cross-reference with your own rankings
3. Surface gaps: **keywords they rank for and you don't**
4. Filter gaps by: high traffic + relevant + beatable

Output a gap table:

| Competitor | Their URL | Keyword | Their Position | Your Position | Traffic Potential |
|-----------|-----------|---------|----------------|---------------|-------------------|
| competitor.com | /guide/x | "how to x" | 3 | Not ranking | 2,400/mo |

### Step 3: On-Page SEO Audit

For priority pages (top 20 by traffic or business value), audit:

- **Title tag** — Includes primary keyword, <60 chars, compelling
- **Meta description** — <160 chars, includes keyword, action-oriented
- **H1** — Single H1, matches user intent, keyword-inclusive
- **H2/H3 structure** — Logical hierarchy, sub-topics covered
- **Internal linking** — Links to relevant pillar pages, anchor text variety
- **External linking** — Links to authoritative sources where helpful
- **Image SEO** — Alt text, descriptive filenames, proper sizing
- **Schema markup** — Product, FAQ, Article, Breadcrumb as applicable
- **Core Web Vitals** — LCP < 2.5s, INP < 200ms, CLS < 0.1
- **Content depth** — Does it comprehensively cover intent vs competitors?

Score each page 0-10 and list specific fixes.

### Step 4: Technical SEO Health Check

Run through the technical checklist:

- **Crawlability**: robots.txt, XML sitemap, noindex issues
- **Indexation**: pages in index vs sitemap discrepancies
- **Site structure**: click depth, orphan pages, canonical issues
- **Duplicate content**: near-duplicates, parameter handling
- **Redirects**: chains, loops, 404s in internal linking
- **Mobile**: responsive design, mobile usability in GSC
- **Speed**: Core Web Vitals by page template
- **HTTPS**: mixed content, certificate validity
- **Schema**: structured data errors in GSC

### Step 5: Build the Prioritized Roadmap

Every recommendation should fit into one of four tiers:

| Tier | Criteria | Timeframe |
|------|----------|-----------|
| **Quick wins** | Low effort, fast traffic gain (title tag fixes, internal linking) | 1-2 weeks |
| **Content production** | Net-new pages targeting gap keywords | 1-3 months |
| **Content upgrades** | Rewrite/expand existing pages that rank 4-20 | 1 month |
| **Strategic bets** | Link building, topical authority, major technical projects | 3-12 months |

### Step 6: Output Format

```
SEO AUDIT: [Site name]
DATE: [YYYY-MM-DD]
BENCHMARKED VS: [competitors]

EXECUTIVE SUMMARY:
[3-line headline: current state + biggest opportunity + expected impact]

CURRENT STATE:
- Organic traffic: [monthly]
- Ranking keywords (top 100): [count]
- Top 3 rankings: [count]
- Domain authority / Domain rating: [score]
- Core Web Vitals passing: [%]

TOP OPPORTUNITIES (ranked):

1. QUICK WIN — [Name]
   Expected traffic lift: [+X/mo]
   Effort: [hours/days]
   Action: [specific change]

2. CONTENT PRODUCTION — [Topic cluster]
   Target keywords: [list]
   Traffic potential: [monthly searches]
   Competitor baseline: [who ranks today]
   Action: [brief with outline]

3. STRATEGIC BET — [Topic authority / link building / technical]
   Expected impact: [traffic + ranking lift]
   Timeline: [quarters]

TECHNICAL ISSUES (severity-ranked):
- CRITICAL: [issues breaking rankings]
- HIGH: [issues limiting rankings]
- MEDIUM: [issues worth fixing eventually]

CONTENT GAPS (top 10):
[Table of keywords competitors rank for that you don't]

90-DAY ROADMAP:
Month 1: [quick wins + first 2 content pieces]
Month 2: [content continues + technical fixes]
Month 3: [content continues + link building kickoff]
```

## SEO Principles

1. **Intent beats volume.** A 200/mo transactional keyword beats a 20,000/mo informational one for most businesses.
2. **Topical authority > scattered keywords.** Own a cluster, not one-off posts.
3. **Internal linking is free leverage.** Every new page should link from 3+ existing pages.
4. **Time-to-rank averages 3-6 months** for net-new pages on established domains; longer for new sites.
5. **Watch GSC queries weekly.** The query report surfaces the real user language.
6. **Don't optimize for AI summaries — optimize for the reader.** Serving user intent wins for both.

## Related Skills

- `content-strategist` — For content calendar and format planning once SEO priorities are set
- `copywriting` — For on-page copy that ranks and converts
- `marketing-strategist` — For tying SEO goals to broader growth strategy
