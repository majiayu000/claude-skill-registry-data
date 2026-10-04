---
name: blog-researcher
description: Monitor competitor blogs and industry publications to surface content opportunities
tags: [research, content, competitors, trends, seo]
---

# Blog Researcher

Monitors competitor blogs, industry publications, and content hubs to extract insights, identify trending topics, and surface content gaps the agency can exploit. Uses WebSearch to scan the landscape systematically. Outputs a content opportunities matrix ranking topics by relevance, competition, and alignment with agency expertise.

## Prerequisites

- `agency.config.json` at repo root with `services`, `icp`, `case_studies`, and `agency` sections
- WebSearch tool available
- Optional: list of specific competitor domains to monitor
- Optional: list of industry publications to track

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `agency.name` -- for context on the agency's brand
   - `services[].name` and `services[].keywords` -- defines expertise areas and content lanes
   - `icp.segments[]` -- the audience whose problems the content should address
   - `icp.primary_keywords` -- topics the agency should own
   - `icp.secondary_keywords` -- adjacent topics worth covering
   - `case_studies[]` -- proof points that can anchor content pieces
3. Accept parameters:
   - `competitors` -- (optional) array of competitor domains or brand names to monitor
   - `publications` -- (optional) array of industry publication domains to scan
   - `topic_focus` -- (optional) narrow the scan to a specific topic area (e.g., "Shopify CRO", "D2C performance marketing")
   - `lookback_days` -- how far back to scan. Default: 30
   - `max_results` -- maximum number of opportunities to return. Default: 20

## Phase 1: Competitor Discovery

If competitors are not provided, discover them:

**Search queries for competitor identification:**
- `"{{service_keyword}}" agency blog` for each service keyword
- `"{{primary_keyword}}" tips site:*.com/blog`
- `best {{service_name}} agencies {{current_year}}`
- `"shopify agency" blog content marketing`

**For each discovered competitor:**
- Domain and blog URL
- Content frequency (posts per month estimate)
- Primary topics covered
- Content quality tier: basic (recycled advice), moderate (original angles), advanced (data/research-backed)
- Social engagement indicators (shares, comments visible on articles)

Build a competitor content map:
```
COMPETITOR BLOG MAP:
---
1. [competitor.com/blog] -- Posts: ~[X]/month -- Topics: [list] -- Quality: [tier]
2. [competitor.com/blog] -- Posts: ~[X]/month -- Topics: [list] -- Quality: [tier]
3. [competitor.com/blog] -- Posts: ~[X]/month -- Topics: [list] -- Quality: [tier]
```

Aim for 5-10 competitor blogs.

## Phase 2: Content Landscape Scan

For each competitor blog and industry publication, scan recent content:

**WebSearch queries:**
- `site:{{competitor_domain}} blog {{current_year}}`
- `site:{{competitor_domain}} {{primary_keyword}}`
- `site:{{publication_domain}} {{service_keyword}} {{current_year}}`

**For each article found (aim for 30-50 across all sources):**
- Title and URL
- Publication date
- Topic category (map to agency service areas)
- Content type: how-to, listicle, case study, opinion, data report, comparison, guide
- Estimated word count
- Key angle or unique hook
- Engagement signals (comments, shares if visible)
- Keywords targeted (from title, URL slug, H1)

## Phase 3: Trend Analysis

Aggregate findings to identify patterns:

**Topic frequency analysis:**
- Count how many articles cover each topic across all sources
- Rank topics by frequency: what is everyone writing about?
- Identify velocity: which topics are accelerating (more articles in recent weeks)?

**Format analysis:**
- Which content types perform best (based on engagement signals)?
- What lengths dominate (short-form, mid-form, long-form)?
- Are competitors using multimedia (videos, infographics, interactive tools)?

**Keyword gap analysis:**
- Cross-reference competitor topics against `services[].keywords`
- Identify agency keywords that NO competitor is covering well
- Identify agency keywords where competitors have weak or outdated content

**Trending topic detection via broader search:**
- `{{industry}} trends {{current_year}}`
- `{{primary_keyword}} news this week`
- `{{icp_industry}} challenges {{current_year}}`
- Reddit and community searches: `{{primary_keyword}} site:reddit.com`
- Identify emerging topics not yet covered by competitor blogs

## Phase 4: Content Gap Identification

Map the gaps between what exists and what the agency can uniquely cover:

**Gap types:**

1. **Topic gaps**: subjects nobody is covering that the agency has expertise in
2. **Depth gaps**: topics covered superficially everywhere, agency can go deeper with case study data
3. **Recency gaps**: important topics where all existing content is 12+ months old
4. **Format gaps**: topics only covered as blog posts but ripe for guides, tools, or interactive content
5. **Perspective gaps**: topics covered generically but not from the agency's unique angle (e.g., India D2C market, sports brand CRO)
6. **Data gaps**: topics where everyone offers opinions but nobody has real numbers (agency has case study data)

**For each gap, assess:**
- Relevance to ICP (1-10)
- Agency expertise level (1-10)
- Competition level (low/medium/high)
- Content effort required (small/medium/large)
- Potential to drive inbound leads (1-10)

## Phase 5: Opportunity Scoring

Score each content opportunity using a weighted formula:

| Factor | Weight | Scale |
|---|---|---|
| ICP relevance | 30% | 1-10 |
| Agency expertise | 25% | 1-10 |
| Competition level | 20% | Low=10, Med=5, High=2 |
| Inbound lead potential | 15% | 1-10 |
| Effort efficiency | 10% | Small=10, Med=6, Large=3 |

**Score = (ICP * 0.30) + (Expertise * 0.25) + (Competition * 0.20) + (Lead Potential * 0.15) + (Effort * 0.10)**

Rank all opportunities by score. Flag the top 5 as "priority topics."

## Phase 6: Output

Return structured JSON:

```json
{
  "scan_metadata": {
    "competitors_scanned": 8,
    "publications_scanned": 4,
    "articles_analyzed": 47,
    "lookback_days": 30,
    "scan_date": "2026-03-12"
  },
  "competitor_map": [
    {
      "domain": "competitor.com",
      "blog_url": "competitor.com/blog",
      "posts_per_month": 6,
      "primary_topics": ["Shopify development", "CRO", "D2C marketing"],
      "quality_tier": "moderate",
      "notable_articles": [
        {"title": "Article title", "url": "https://...", "date": "2026-02-15", "topic": "CRO"}
      ]
    }
  ],
  "trending_topics": [
    {"topic": "AI-powered product recommendations", "velocity": "accelerating", "article_count": 12},
    {"topic": "Shopify Markets expansion", "velocity": "stable", "article_count": 8}
  ],
  "content_gaps": [
    {
      "gap_type": "depth",
      "topic": "CRO for sports D2C brands",
      "description": "Multiple articles cover generic CRO, none specific to sports category with real data",
      "agency_advantage": "Kibi Sports case study with measurable conversion uplift"
    }
  ],
  "opportunities": [
    {
      "rank": 1,
      "topic": "CRO audit checklist for D2C brands on Shopify",
      "gap_type": "depth",
      "suggested_format": "guide",
      "suggested_word_count": 3000,
      "icp_relevance": 9,
      "expertise_score": 10,
      "competition": "medium",
      "lead_potential": 9,
      "effort": "medium",
      "total_score": 8.65,
      "unique_angle": "Backed by real audit data from Kibi Sports, not generic advice",
      "target_keywords": ["shopify CRO audit", "CRO checklist D2C", "ecommerce conversion audit"],
      "suggested_cta": "Book a free CRO audit for your store"
    }
  ],
  "quick_wins": [
    {
      "topic": "Topic with low competition and small effort",
      "reason": "No recent content exists, agency has expertise, can publish in 1-2 days"
    }
  ],
  "recommended_content_calendar": {
    "week_1": {"topic": "Priority topic 1", "format": "blog", "target_keywords": ["..."]},
    "week_2": {"topic": "Priority topic 2", "format": "guide", "target_keywords": ["..."]},
    "week_3": {"topic": "Priority topic 3", "format": "case-study", "target_keywords": ["..."]},
    "week_4": {"topic": "Priority topic 4", "format": "comparison", "target_keywords": ["..."]}
  }
}
```

## Example Usage

Trigger phrases:
- "Research what competitors are blogging about"
- "Find content gaps in our niche"
- "What topics should we write about?"
- "Scan competitor blogs for opportunities"
- "What's trending in Shopify/D2C content?"
- "Build a content calendar based on competitor research"

```
User: Research what our competitors are blogging about and find gaps we can exploit
Assistant: [reads config, discovers competitor blogs, scans 50+ articles, identifies gaps, scores opportunities, returns ranked matrix with content calendar]
```

```
User: What should our next 4 blog posts be about?
Assistant: [scans landscape, identifies top 4 opportunities by score, returns with suggested formats, keywords, and unique angles]
```
