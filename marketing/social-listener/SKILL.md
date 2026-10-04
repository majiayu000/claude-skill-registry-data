---
name: social-listener
description: Monitor social platforms and forums for brand mentions, category discussions, and competitor activity
tags: [social-monitoring, brand-mentions, competitor-intel, community, sentiment]
---

# Social Listener

Monitors Reddit, Hacker News, Product Hunt, Twitter/X, and industry forums for brand mentions, category discussions, and competitor mentions. Uses WebSearch with site-specific operators to surface real-time conversations relevant to your agency and ICP. Outputs categorized mentions with sentiment analysis and engagement potential scoring.

## Prerequisites

- `agency.config.json` at repo root with `agency`, `services`, `icp`, and `outreach` sections
- WebSearch tool available
- Optional: `crm-writer` skill for logging high-value mentions to CRM

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `agency.name`, `agency.domain` -- brand identity to monitor
   - `services[].name`, `services[].keywords` -- service categories to track
   - `icp.primary_keywords`, `icp.secondary_keywords` -- topic relevance signals
   - `icp.segments[].industries` -- industry verticals to monitor
   - `icp.negative_keywords` -- filter out self-promotion noise
   - `case_studies[].name` -- client names to track mentions of
3. Accept parameters:
   - `platforms` -- list of platforms to monitor (default: all)
   - `competitors` -- competitor names/domains to track (default: none, user must supply)
   - `time_window` -- lookback period (default: "past 3 days")
   - `mention_types` -- filter by type: `brand | category | competitor | pain_point` (default: all)
   - `max_results` -- max mentions to return (default: 30)

## Phase 1: Query Generation

Build three query categories, each with platform-specific syntax.

### Brand Mention Queries

Track direct mentions of the agency, founder, and clients:

- `"{agency_name}"` across all platforms
- `"{agency_domain}"` for link mentions
- `"{founder_name}" "{agency_name}"` for attributed mentions
- `"{case_study_name}" "{service_keyword}"` for client-related discussions

### Category Discussion Queries

Track conversations in your service categories:

**Reddit:**
- `site:reddit.com/r/shopify "{service_keyword}" after:{date}`
- `site:reddit.com/r/ecommerce "{industry}" "{intent_keyword}"`
- Target subreddits: r/shopify, r/ecommerce, r/smallbusiness, r/DTC, r/Entrepreneur, r/startups, r/digital_marketing

**Hacker News:**
- `site:news.ycombinator.com "{service_keyword}" OR "{industry_keyword}"`
- `site:news.ycombinator.com "Show HN" "{industry_keyword}"`

**Product Hunt:**
- `site:producthunt.com "{industry}" OR "{service_keyword}"`
- Focus on newly launched products in ICP industries

**Twitter/X:**
- `site:twitter.com OR site:x.com "{service_keyword}" "{intent_keyword}"`
- `site:twitter.com OR site:x.com "{agency_name}" OR "{agency_domain}"`

**Industry Forums:**
- `site:community.shopify.com "{service_keyword}"`
- `site:indiehackers.com "{industry}" "{service_keyword}"`
- `site:dev.to "{service_keyword}"` for technical discussions

### Competitor Mention Queries

For each competitor provided:
- `"{competitor_name}" review OR feedback OR experience`
- `"{competitor_name}" vs OR alternative OR switch`
- `"{competitor_name}" complaint OR issue OR problem`
- `"{competitor_name}" "{service_keyword}"`

### Query generation rules:

- Generate 2-3 queries per platform per category.
- Prioritize recency: always include time filters where supported.
- Total queries per scan: 20-35 across all platforms and categories.
- Rotate keywords across queries to maximize coverage.

## Phase 2: Search Execution

Execute searches using WebSearch with rate limiting:

- **Max 3 concurrent searches** at any time.
- **2-second pause between batches** of 3.
- Process results as they arrive; do not wait for all to complete.

For each result, extract:
- `url` -- source URL
- `title` -- page/post title
- `snippet` -- text excerpt from search result
- `platform` -- inferred from URL domain
- `posted_date` -- if visible in the result
- `author` -- if identifiable from snippet or title

## Phase 3: Mention Classification

Classify each mention into one of four categories:

1. **Brand Mention**: Direct reference to agency name, domain, founder, or clients
2. **Category Discussion**: Conversations about services you offer (without naming you)
3. **Competitor Mention**: References to competitors you're tracking
4. **Pain Point Signal**: Prospects expressing frustration or need in your service area

### Sentiment Analysis

Score each mention's sentiment:
- **POSITIVE**: Praise, recommendation, success story, excitement
- **NEUTRAL**: Informational, question, comparison without strong opinion
- **NEGATIVE**: Complaint, frustration, criticism, churn signal
- **MIXED**: Contains both positive and negative elements

### Engagement Potential Scoring

Rate each mention's engagement opportunity (1-10):
- **9-10**: Direct question seeking help in your service area, high-traffic thread, no existing expert response
- **7-8**: Active discussion in your niche, multiple participants, room for expert contribution
- **5-6**: Relevant topic but already well-answered, or lower traffic
- **3-4**: Tangentially related, limited engagement opportunity
- **1-2**: Informational only, no engagement path

## Phase 4: Entity Extraction

For each classified mention, produce structured output:

```json
{
  "mention_id": "auto-generated sequential ID",
  "category": "brand | category | competitor | pain_point",
  "platform": "Reddit | HackerNews | ProductHunt | Twitter | ShopifyCommunity | IndieHackers | DevTo",
  "url": "https://...",
  "title": "Post or thread title",
  "snippet": "Relevant excerpt (max 300 chars)",
  "author": "Username or name if identifiable",
  "posted_date": "ISO date or relative",
  "sentiment": "POSITIVE | NEUTRAL | NEGATIVE | MIXED",
  "engagement_score": 7,
  "engagement_reason": "Active thread, OP seeking Shopify CRO help, no expert reply yet",
  "competitor_mentioned": "CompetitorName or null",
  "keywords_matched": ["shopify CRO", "conversion rate"],
  "suggested_action": "ENGAGE | MONITOR | RESPOND | IGNORE",
  "suggested_response": "Brief outline of what to say if action is ENGAGE or RESPOND"
}
```

### Action rules:
- **ENGAGE**: High engagement score (7+), category or pain_point type, no expert has replied
- **RESPOND**: Brand mention that is negative or a question directed at you
- **MONITOR**: Competitor mention or ongoing discussion worth tracking
- **IGNORE**: Low relevance, already resolved, or stale thread

## Phase 5: Dedup & Filter

1. Remove exact URL duplicates.
2. Merge mentions from different platforms about the same underlying event (e.g., a Product Hunt launch discussed on Reddit and HN).
3. Apply negative keyword filter: discard self-promotion matches.
4. Apply recency filter: flag anything outside the `time_window` as STALE.

## Phase 6: Output

Present results grouped by category, sorted by engagement score within each group:

```
SOCIAL LISTENING REPORT
Period: {time_window}
Platforms scanned: {platform_list}

BRAND MENTIONS ({count}):
1. [{platform}] {sentiment} -- "{title}" -- Engagement: {score}/10
   URL: ...
   Action: {suggested_action}

CATEGORY DISCUSSIONS ({count}):
1. [{platform}] {sentiment} -- "{title}" -- Engagement: {score}/10
   URL: ...
   Action: {suggested_action}

COMPETITOR MENTIONS ({count}):
1. [{platform}] {sentiment} -- "{competitor}" -- "{title}"
   URL: ...

PAIN POINT SIGNALS ({count}):
1. [{platform}] -- "{title}" -- Engagement: {score}/10
   URL: ...
   Suggested response: ...

SUMMARY:
- Total mentions: {N}
- Actionable (ENGAGE/RESPOND): {count}
- Sentiment breakdown: {pos}/{neutral}/{neg}/{mixed}
- Top platform by volume: {platform}
- Top competitor mentioned: {competitor} ({count} mentions)
```

Return the full structured JSON array alongside the formatted summary.

## Phase 7: CRM Logging

If `crm-writer` is available and user approves:
- Log ENGAGE and RESPOND items to the CRM pipeline tab with columns: Date, Platform, Category, URL, Sentiment, Engagement Score, Action, Status
- Set initial status: "PENDING_RESPONSE"

## Example Usage

Trigger phrases:
- "Monitor social mentions"
- "What are people saying about us?"
- "Run social listener"
- "Track competitor mentions on Reddit"
- "Find discussions about Shopify CRO this week"
- "Scan Reddit and HN for category discussions"

```
User: Run social listener for the past week, track competitors WebSavvy and Starter Labs
Assistant: [reads config, builds brand/category/competitor queries across Reddit/HN/ProductHunt/Twitter/forums, executes with rate limiting, classifies and scores mentions, presents categorized report with engagement recommendations]
```

```
User: Monitor Reddit and Shopify Community for pain points about Shopify CRO
Assistant: [same flow limited to 2 platforms, filtered to pain_point category]
```
