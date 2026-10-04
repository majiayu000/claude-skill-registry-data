---
name: keyword-miner
description: Find keyword gaps, SERP opportunities, and low-competition high-intent keywords
tags: [seo, keywords, serp, content-strategy, keyword-research]
---

# Keyword Miner

Finds keyword gaps and SERP opportunities by analyzing competitor rankings, "People Also Ask" boxes, related searches, and autocomplete suggestions. Identifies low-competition high-intent keywords that represent realistic ranking opportunities. Groups findings into keyword clusters with volume estimates, difficulty assessments, and content recommendations. Designed to feed into content strategy, programmatic SEO planning, and paid search campaigns.

## Prerequisites

- WebSearch tool available for SERP analysis and competitor keyword discovery
- Target website URL or business description
- Optional: `agency.config.json` for service context and ICP understanding
- Optional: list of competitor URLs for gap analysis
- Optional: seed keywords to start from

## Capabilities Used

1. `content-seo-optimizer` -- for evaluating existing content against discovered keywords

## Phase 0: Intake

1. Read `agency.config.json` from the project root (if available).
2. Extract `services[].keywords` for seed keyword ideas relevant to the agency's offerings.
3. Extract `icp.segments[].industries` to understand target market context.
4. Accept parameters:
   - `url` -- (required) target website or business to find keywords for
   - `seed_keywords` -- (optional) array of starting keywords. If not provided, derive from the site's content and meta tags.
   - `competitor_urls` -- (optional) array of competitor URLs for gap analysis
   - `intent` -- (optional) filter: `informational`, `commercial`, `transactional`, `navigational`, or `all`. Default: `all`
   - `market` -- (optional) geographic market: `US`, `UK`, `IN`, `AU`, `global`. Default: derive from config
   - `depth` -- `quick` (top 20 keywords) | `standard` (50-100 keywords) | `deep` (200+ keywords). Default: `standard`

## Phase 1: Seed Keyword Expansion

### Extract Keywords from Target Site
- Visit target URL, extract:
  - Title tags and meta descriptions from key pages
  - H1 and H2 headings
  - Navigation labels and category names
  - Product/service names
  - Blog post titles (if blog exists)
- Compile initial keyword list from on-site content

### Autocomplete Mining
For each seed keyword, search and capture:
- WebSearch: `{{seed_keyword}}` -- note autocomplete suggestions
- WebSearch: `{{seed_keyword}} a`, `{{seed_keyword}} b`, ... `{{seed_keyword}} z` -- alphabet soup method
- WebSearch: `{{seed_keyword}} for`, `{{seed_keyword}} vs`, `{{seed_keyword}} how to`
- WebSearch: `best {{seed_keyword}}`, `{{seed_keyword}} near me`, `{{seed_keyword}} online`

### Related Searches
- For each SERP, capture "Related searches" at the bottom of results
- For each SERP, capture "People Also Search For" suggestions
- Capture any "Searches related to" boxes

## Phase 2: People Also Ask Mining

For each seed keyword:
- WebSearch the keyword and extract all "People Also Ask" questions
- Click/expand PAA boxes to reveal nested questions (up to 3 levels deep)
- Categorize questions by:
  - **Informational**: "What is...", "How does...", "Why do..."
  - **Commercial**: "Best...", "Top...", "Reviews of..."
  - **Transactional**: "Buy...", "Price of...", "Where to get..."
  - **Comparison**: "X vs Y", "Difference between...", "Alternative to..."

Compile all PAA questions into a master list, deduplicated and categorized.

## Phase 3: Competitor Keyword Gap Analysis

### If Competitor URLs Provided
For each competitor:
- WebSearch: `site:{{competitor_domain}}` -- catalog their indexed pages
- Extract keywords from competitor page titles, headings, and meta descriptions
- WebSearch: `site:{{competitor_domain}} blog` -- catalog their content topics
- Identify keywords competitors rank for by searching their page titles

### Gap Identification
- **Keywords competitors cover that target does not**: content gaps
- **Keywords target covers but competitors do not**: defensible positions
- **Keywords ALL competitors cover**: table-stakes topics that must be addressed
- **Keywords NO ONE covers well**: blue ocean opportunities

### Comparative SERP Checks
For the most promising gap keywords:
- Search each keyword, check if competitor appears in top 10
- Note the type of content ranking (blog post, product page, tool, video)
- Note domain authority of ranking sites (are they beatable?)

## Phase 4: Keyword Qualification

For each discovered keyword, assess:

### Search Volume Estimation
- WebSearch: `"{{keyword}}" search volume` or `"{{keyword}}" monthly searches`
- Cross-reference with Google Trends relative interest
- Categorize: High (10K+), Medium (1K-10K), Low (100-1K), Very Low (<100)
- Note trending direction: rising, stable, declining, seasonal

### Difficulty Assessment
- Search the keyword, analyze page 1 results:
  - Domain authority of ranking sites (all high-DA = hard, mixed = medium, low-DA = easy)
  - Content quality of ranking pages (thin content = opportunity)
  - Content type ranking (if all are mega-guides, a quick answer page won't compete)
  - SERP features present (featured snippets, video carousels, knowledge panels)
- Score difficulty: Easy (can rank in 1-3 months), Medium (3-6 months), Hard (6-12 months), Very Hard (12+ months)

### Intent Classification
- **Informational**: user wants to learn ("how to", "what is", "guide")
- **Commercial Investigation**: user is comparing options ("best", "vs", "review", "top 10")
- **Transactional**: user wants to buy/act ("buy", "price", "discount", "sign up", "hire")
- **Navigational**: user wants a specific site ("brand name", "login", "support")

### Business Value
- How directly does this keyword relate to the target's products/services?
- Does ranking for this keyword attract buyers or browsers?
- Can the target credibly create authoritative content on this topic?
- Score: High value (direct revenue), Medium value (pipeline builder), Low value (brand awareness only)

## Phase 5: Keyword Clustering

Group qualified keywords into topical clusters:

### Cluster Formation
- Group keywords that share the same search intent and can be served by a single page
- Identify the "pillar" keyword for each cluster (highest volume, broadest intent)
- Identify "supporting" keywords that can be subtopics or sections within the pillar content
- Map clusters to content types: blog post, product page, landing page, FAQ page, tool page

### Content Mapping
For each cluster:
- Recommended page type (new page, optimize existing page, blog post)
- Target URL path
- Primary keyword (in title, H1, URL)
- Secondary keywords (in H2s, body content)
- Supporting keywords (in related sections, FAQ)
- Internal linking targets (which existing pages should link to/from this content)

## Phase 6: Opportunity Scoring

Rank all keyword clusters by opportunity score:

```
Opportunity Score = (Volume x Intent Value x Business Relevance) / Difficulty
```

Where:
- Volume: 1-10 scale
- Intent Value: Transactional=10, Commercial=8, Informational=4, Navigational=2
- Business Relevance: 1-10 scale
- Difficulty: 1-10 scale (1=easy, 10=very hard)

Sort clusters by opportunity score descending. Top clusters are the highest-ROI content investments.

## Phase 7: Output

Return structured JSON:

```json
{
  "target_url": "https://example.com",
  "mined_at": "2024-01-15T14:30:00Z",
  "depth": "standard",
  "market": "US",
  "seed_keywords_used": ["shopify agency", "ecommerce development"],
  "total_keywords_found": 147,
  "keyword_clusters": [
    {
      "cluster_name": "Shopify Store Setup",
      "pillar_keyword": "shopify store setup service",
      "opportunity_score": 8.5,
      "estimated_volume": "Medium (1K-10K)",
      "difficulty": "Medium",
      "intent": "Transactional",
      "business_value": "High",
      "keywords": [
        { "keyword": "shopify store setup service", "volume_tier": "Medium", "difficulty": "Medium", "intent": "Transactional" },
        { "keyword": "hire shopify developer", "volume_tier": "Medium", "difficulty": "Medium", "intent": "Transactional" },
        { "keyword": "shopify store setup cost", "volume_tier": "Medium", "difficulty": "Easy", "intent": "Commercial" },
        { "keyword": "how to set up shopify store", "volume_tier": "High", "difficulty": "Hard", "intent": "Informational" }
      ],
      "paa_questions": [
        "How much does it cost to set up a Shopify store?",
        "Can I hire someone to build my Shopify store?",
        "How long does it take to set up a Shopify store?"
      ],
      "recommended_content": {
        "type": "Landing page + supporting blog post",
        "target_url": "/services/shopify-store-setup",
        "title_suggestion": "Shopify Store Setup Service | Expert Setup in 2 Weeks",
        "content_outline": ["Service overview", "What's included", "Pricing tiers", "Timeline", "Portfolio examples", "FAQ"]
      }
    }
  ],
  "competitor_gaps": [
    {
      "keyword": "shopify migration service",
      "competitors_ranking": ["competitor1.com", "competitor2.com"],
      "target_ranking": "Not found in top 50",
      "opportunity": "High -- competitors rank with thin content, strong content piece could outrank"
    }
  ],
  "quick_wins": [
    {
      "keyword": "shopify cro audit",
      "current_position": "Page 2",
      "action": "Optimize existing /services/cro page with better keyword targeting",
      "estimated_impact": "Move to page 1, capture ~200 visits/month"
    }
  ],
  "trending_keywords": [
    { "keyword": "shopify ai features", "trend": "Rising 150% YoY", "opportunity": "First-mover content advantage" }
  ],
  "summary": {
    "total_clusters": 12,
    "high_opportunity_clusters": 4,
    "estimated_total_monthly_volume": "15K-25K",
    "biggest_gap": "No content targeting comparison/vs keywords",
    "recommended_priority": ["Cluster 1: Shopify Setup", "Cluster 3: CRO Services", "Cluster 5: Migration Guide"]
  }
}
```

## Phase 8: Review Gate

Present findings to the user. The user may:
- Filter clusters by intent type or difficulty
- Request deeper analysis on specific clusters
- Adjust business value scores based on internal priorities
- Export keyword list for use in other tools

## Example Usage

Trigger phrases:
- "Find keyword opportunities for [url]"
- "What keywords should [business] target?"
- "Keyword gap analysis: [url] vs [competitor]"
- "Mine keywords for [topic/niche]"
- "Find low-competition keywords for [industry]"

```
User: Find keyword opportunities for plasho.com
Assistant: [extracts seed keywords from site, mines autocomplete and PAA, analyzes competitors, returns clustered opportunities ranked by score]
```

```
User: Keyword gap analysis: plasho.com vs competitor1.com and competitor2.com
Assistant: [identifies keywords competitors rank for that plasho.com does not, returns prioritized gap list with content recommendations]
```

```
User: Find low-competition transactional keywords for Shopify development services in India
Assistant: [focuses on transactional intent, India market, filters for easy/medium difficulty, returns actionable keyword clusters]
```
