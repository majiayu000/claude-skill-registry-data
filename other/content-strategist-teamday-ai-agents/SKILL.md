---
name: content-strategist
description: Analyze keyword data and propose high-impact content topics. Identifies keyword opportunities, analyzes SERP competition, and creates prioritized content roadmaps.
allowed-tools: Read, Write, WebSearch
---

# Content Strategist Skill

Research keywords, analyze competition, and propose high-ROI content topics for your website.

## When to Use

- User asks "what should I write about?"
- User wants content topic ideas
- User asks for keyword research
- User wants to find SEO opportunities
- Planning content calendar or roadmap

## Prerequisites

**Ahrefs MCP must be authenticated.** If you get token errors, tell user to run `/mcp` and authorize Ahrefs.

## Workflow

### Phase 1: Understand Current Performance

Get baseline data from Search Console:

```
mcp__search-console__get_performance_summary(days=28)
mcp__search-console__get_top_queries(days=28, limit=25)
mcp__search-console__get_top_pages(days=28, limit=25)
```

Identify:
- Top performing content themes
- Keywords already ranking (positions 1-20)
- High impression/low CTR opportunities

### Phase 2: Define Keyword Clusters

Define clusters based on your product's focus areas. Example structure:

| Cluster | Relevance | Example Seeds |
|---------|-----------|---------------|
| **Core Product** | Highest | your main product keywords |
| **Use Cases** | High | problem-solution keywords |
| **Thought Leadership** | Medium | industry trend keywords |
| **Adjacent Topics** | Lower | related but broader topics |

Adapt clusters to the user's specific business and industry.

### Phase 3: Keyword Research

For each cluster, use Ahrefs keywords-explorer-overview:

```
mcp__ahrefs__keywords-explorer-overview(
  keywords="keyword1,keyword2,keyword3",
  country="us",
  select="keyword,volume,difficulty,cpc,traffic_potential,global_volume"
)
```

**Critical columns:**
- `volume` = US monthly searches
- `global_volume` = Worldwide monthly searches
- `difficulty` = Keyword Difficulty (0-100)
- `traffic_potential` = Max traffic if ranking #1

**Difficulty interpretation for lower DR sites:**
- KD 0-20: Easy - Target immediately
- KD 21-40: Achievable - Good targets
- KD 41-60: Challenging - Need quality content + links
- KD 61+: Hard - Long-term play only

### Phase 4: SERP Analysis

For promising keywords (high volume, low-medium KD), analyze the SERP:

```
mcp__ahrefs__serp-overview(
  keyword="target keyword",
  country="us",
  select="position,url,domain_rating,traffic,backlinks"
)
```

**Look for:**
- Low DR sites ranking (DR < 50 = opportunity)
- Few backlinks needed to compete
- Content gaps (thin content ranking)
- Outdated content

### Phase 5: Opportunity Scoring

Score each keyword opportunity:

| Factor | Weight | Scoring |
|--------|--------|---------|
| Search Volume | 25% | >1000=5, 500-1000=4, 200-500=3, 50-200=2, <50=1 |
| Keyword Difficulty | 30% | <20=5, 20-40=4, 40-60=3, 60-80=2, >80=1 |
| SERP Weakness | 25% | Low DR competitor=5, Medium=3, Giants only=1 |
| Brand Relevance | 20% | Core product=5, Adjacent=3, Tangential=1 |

**Priority tiers:**
- Score 4.0+: Immediate priority (this month)
- Score 3.0-3.9: Short-term (30-60 days)
- Score 2.0-2.9: Medium-term (60-90 days)
- Score <2.0: Monitor only

### Phase 6: Content Roadmap

Deliver a prioritized content roadmap with target keywords, search volume, difficulty, SERP analysis, content angle, and estimated effort for each piece.

## Output Format

```markdown
# Content Strategy Report - [Date]

## Executive Summary
[2-3 sentence overview of top opportunities]

## Current Performance Snapshot
[Key metrics from Search Console]

## Keyword Research Results

### Cluster 1: [Name]
| Keyword | US Vol | Global Vol | KD | Traffic Pot. | Priority |
|---------|--------|------------|-----|--------------|----------|

## SERP Analysis: Top Opportunities

### "[Keyword 1]" - KD [X]
**Volume:** [US] / [Global]
**Current SERP:**
| Pos | URL | DR | Backlinks |
|-----|-----|-----|-----------|

**Opportunity:** [Why you can rank]

## Content Roadmap

### Immediate (This Month)
1. **[Article Title]**
   - Target: [keyword]
   - Volume: [X] | KD: [Y]
   - Angle: [Why this will win]

## Quick Wins Summary
| Keyword | Why It's Winnable | Recommended Action |
|---------|-------------------|-------------------|
```

## Ahrefs API Column Reference

**keywords-explorer-overview:**
- keyword, volume, difficulty, cpc, traffic_potential, global_volume, clicks, cps, intents

**serp-overview:**
- position, url, domain_rating, traffic, backlinks

**site-explorer-organic-keywords:**
- keyword, best_position, volume, sum_traffic, best_position_url, keyword_difficulty

**site-explorer-organic-competitors:**
- competitor_domain, keywords_common, traffic, domain_rating

## Tips for Quality Analysis

1. **Don't just list keywords** - Analyze WHY each is an opportunity
2. **Check SERP for every priority keyword** - Validate difficulty with real data
3. **Consider content effort** - A 10K volume keyword requiring 20 hours may be worse than 1K volume needing 2 hours
4. **Look for first-mover advantage** - New/emerging keywords without established KD
5. **Cluster keywords for content** - One article can target multiple related keywords
6. **Consider existing content** - Can you optimize vs create new?
