---
name: influencer-finder
description: Discover KOLs and micro-influencers relevant to your ICP across LinkedIn, Instagram, YouTube, and Twitter
tags: [influencer, kol, micro-influencer, partnership, social-media, discovery]
---

# Influencer Finder

Discovers Key Opinion Leaders (KOLs) and micro-influencers whose audiences overlap with your ICP. Searches across LinkedIn, Instagram, YouTube, and Twitter/X to find creators with genuine engagement, topical relevance, and audience alignment. Evaluates authenticity signals, content quality, and partnership potential. Outputs a ranked influencer list with collaboration recommendations and outreach templates.

## Prerequisites

- `agency.config.json` at repo root with `services`, `icp`, and optionally `outreach` sections
- WebSearch tool available
- Optional: `linkedin-researcher` skill for deeper LinkedIn creator analysis
- Optional: `person-researcher` skill for enriching influencer profiles
- Optional: `visual-brand` skill for assessing visual alignment with your brand

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `agency.name`, `agency.domain` -- for partnership context
   - `services[].name`, `services[].keywords` -- topic alignment criteria
   - `icp.segments[].industries`, `icp.segments[].titles` -- audience overlap targets
   - `icp.segments[].markets` -- geographic relevance
   - `icp.primary_keywords`, `icp.secondary_keywords` -- content relevance signals
   - `outreach.tone` -- voice alignment for outreach templates (if present)
3. Accept parameters:
   - `niche` -- primary niche/topic to search (default: derive from config service keywords)
   - `platforms` -- platforms to search: `linkedin | instagram | youtube | twitter` (default: all)
   - `follower_range` -- min-max follower count (default: "1000-100000" for micro-influencers)
   - `geography` -- target regions (default: derive from ICP markets)
   - `content_types` -- preferred content types: `video | carousel | text | podcast | newsletter` (default: all)
   - `max_results` -- max influencers to return (default: 30)
   - `partnership_type` -- collaboration goals: `content | co-marketing | affiliate | guest_post | podcast_guest` (default: all)

## Phase 1: Define Influencer Criteria

Build a scoring rubric based on config and parameters:

### Relevance criteria:
- **Topic alignment**: Content covers topics in `services[].keywords` or related adjacent topics
- **Audience overlap**: Their followers match ICP titles, industries, and seniority levels
- **Geographic fit**: Creator or audience concentrated in ICP markets
- **Platform presence**: Active on platforms where ICP audience spends time

### Quality criteria:
- **Engagement rate**: Comments and shares relative to follower count (>2% good, >5% excellent)
- **Content consistency**: Regular posting cadence (at least weekly)
- **Content depth**: Substantive posts vs shallow motivational content
- **Authenticity signals**: Real comments from real people, not bots or engagement pods

### Disqualification criteria:
- Follower count outside specified range
- No posts in the past 30 days (inactive)
- Engagement that looks artificial (thousands of likes, zero meaningful comments)
- Content exclusively self-promotional with no educational value
- Direct competitor or their employee

## Phase 2: Platform-Specific Discovery

### LinkedIn Discovery

Search queries:
- `site:linkedin.com/in "{service_keyword}" "followers" "{industry}"`
- `"top linkedin creator" "{niche}" "{icp_market}"`
- `"linkedin influencer" "{service_keyword}" "posts about"`
- `site:linkedin.com/newsletters "{service_keyword}" "{industry}"`

Extract for each:
```json
{
  "name": "Full name",
  "profile_url": "LinkedIn URL",
  "headline": "LinkedIn headline",
  "follower_estimate": "Approximate count",
  "content_focus": "Primary topics they cover",
  "posting_frequency": "Daily | 3-4x/week | Weekly | Irregular",
  "newsletter": "Newsletter name if they have one"
}
```

### Instagram Discovery

Search queries:
- `site:instagram.com "{service_keyword}" "{industry}" creator`
- `"instagram influencer" "{niche}" "{icp_market}" followers`
- `"{service_keyword}" "instagram" "content creator" "{industry}"`
- `"top instagram accounts" "{niche}" "{year}"`

Extract for each:
```json
{
  "handle": "@username",
  "profile_url": "Instagram URL",
  "follower_estimate": "Approximate count",
  "content_style": "Reels | Carousels | Stories | Mixed",
  "visual_quality": "HIGH | MEDIUM | LOW",
  "niche_focus": "Primary topic area"
}
```

### YouTube Discovery

Search queries:
- `site:youtube.com "{service_keyword}" channel "{industry}"`
- `"youtube channel" "{niche}" "{icp_market}" subscribers`
- `site:youtube.com "{service_keyword}" "tutorial" OR "guide" OR "review"`
- `"best youtube channels" "{niche}" "{year}"`

Extract for each:
```json
{
  "channel_name": "Channel name",
  "channel_url": "YouTube URL",
  "subscriber_estimate": "Approximate count",
  "content_type": "Tutorials | Reviews | Vlogs | Interviews | Mixed",
  "avg_views": "Rough average per video",
  "upload_frequency": "Weekly | Bi-weekly | Monthly | Irregular"
}
```

### Twitter/X Discovery

Search queries:
- `site:twitter.com OR site:x.com "{service_keyword}" "{industry}" bio`
- `"twitter influencer" "{niche}" "{icp_market}"`
- `site:twitter.com "{service_keyword}" "thread" followers`
- `"top twitter accounts" "{niche}" "{industry}" "{year}"`

Extract for each:
```json
{
  "handle": "@username",
  "profile_url": "Twitter URL",
  "follower_estimate": "Approximate count",
  "content_style": "Threads | Short-form | Curated | Mixed",
  "engagement_pattern": "High replies | High retweets | Community-driven"
}
```

## Phase 3: Profile Enrichment

For the top candidates from each platform (top 50% by initial relevance):

### Cross-platform presence check:
- Search for `"{influencer_name}" site:linkedin.com` if found on other platform first
- Search for `"{influencer_name}" site:instagram.com` if found on LinkedIn first
- Map multi-platform presence: more platforms = higher reach potential

### Engagement quality assessment:
- Search for `"{influencer_name}" "{service_keyword}" comments OR replies` to gauge discussion quality
- Look for engagement pod signals: same people commenting on every post, generic comments
- Check if they respond to comments (community builder vs broadcaster)

### Content quality assessment:
- Search for `"{influencer_name}" "{niche}" article OR post OR video` to sample content depth
- Categorize content mix: educational (how-to, tutorials) vs opinion (hot takes) vs promotional (sponsored)
- Note unique angles or perspectives they bring

### Audience alignment estimation:
- If they have a newsletter, check topic alignment with ICP interests
- If they speak at events, check event types (industry conferences = good audience overlap)
- If they have a podcast, check guest types (ICP-matching guests = aligned audience)

## Phase 4: Scoring and Ranking

Score each influencer on a 100-point scale:

### Topic relevance (0-30 points):
- Content directly covers your service keywords: 25-30
- Content covers adjacent topics: 15-24
- Content is in the right industry but different angle: 5-14
- Tangential relevance: 0-4

### Audience overlap (0-25 points):
- Audience clearly matches ICP titles and industries: 20-25
- Audience partially overlaps: 10-19
- Audience is in the right industry but wrong seniority: 5-9
- Unclear audience composition: 0-4

### Engagement quality (0-20 points):
- High engagement rate + quality comments: 16-20
- Good engagement rate + mixed comment quality: 10-15
- Low engagement rate or suspicious patterns: 0-9

### Accessibility (0-15 points):
- Micro-influencer, likely to respond: 12-15
- Mid-tier, may respond with good pitch: 7-11
- Large following, hard to reach: 0-6

### Authenticity (0-10 points):
- Clear genuine engagement, no pod signals: 8-10
- Mostly authentic with some questionable patterns: 4-7
- Suspected engagement manipulation: 0-3

### Tier assignment:
- **TIER 1** (80-100): High-priority partnership targets
- **TIER 2** (60-79): Strong candidates, worth pursuing
- **TIER 3** (40-59): Secondary targets, pursue if bandwidth allows
- **BELOW THRESHOLD** (<40): Skip

## Phase 5: Partnership Recommendations

For each TIER 1 and TIER 2 influencer, generate:

### Collaboration format recommendation:
```json
{
  "recommended_formats": [
    {
      "format": "guest_post | co-created_content | product_review | podcast_interview | joint_webinar | affiliate | ambassador | event_collab",
      "fit_reason": "Why this format works for this influencer",
      "estimated_effort": "LOW | MEDIUM | HIGH",
      "estimated_reach": "Number range based on their audience size"
    }
  ],
  "outreach_angle": "Specific reason to reach out that references their content",
  "value_proposition": "What you bring to them (not just what they bring to you)",
  "talking_points": ["Point 1 referencing their recent content", "Point 2 about mutual benefit"],
  "avoid": "Topics or approaches that would not resonate"
}
```

### Outreach template:
Generate a personalized outreach message skeleton for each TIER 1 influencer:
- Reference a specific piece of their content
- Explain mutual benefit clearly
- Propose a specific low-commitment first step
- Keep it under 150 words

## Phase 6: Output

Return structured influencer report:

```json
{
  "discovery_summary": {
    "platforms_searched": ["LinkedIn", "Instagram", "YouTube", "Twitter"],
    "total_candidates_found": 85,
    "after_scoring": 30,
    "tier_breakdown": {
      "tier_1": 5,
      "tier_2": 12,
      "tier_3": 13
    },
    "top_niches": ["Shopify development", "D2C marketing", "Ecommerce CRO"]
  },
  "influencers": [
    {
      "name": "Creator Name",
      "platforms": {
        "linkedin": { "url": "...", "followers": "..." },
        "instagram": { "url": "...", "followers": "..." }
      },
      "primary_platform": "LinkedIn",
      "niche": "Ecommerce growth",
      "content_focus": ["Shopify tips", "D2C strategy"],
      "follower_total": "25,000 across platforms",
      "engagement_rate": "4.2%",
      "engagement_quality": "HIGH",
      "authenticity_score": 9,
      "total_score": 87,
      "tier": "TIER_1",
      "audience_profile": "D2C founders and ecommerce managers in India/US",
      "partnership_recommendations": [],
      "outreach_template": "...",
      "recent_content_sample": "Title or topic of recent post"
    }
  ],
  "platform_insights": {
    "linkedin": { "candidates": 20, "avg_score": 68, "top_niche": "..." },
    "instagram": { "candidates": 15, "avg_score": 55, "top_niche": "..." },
    "youtube": { "candidates": 10, "avg_score": 62, "top_niche": "..." },
    "twitter": { "candidates": 8, "avg_score": 52, "top_niche": "..." }
  },
  "recommendations": {
    "priority_outreach": ["Name 1", "Name 2", "Name 3"],
    "quick_wins": "Micro-influencers who are easy to reach and highly relevant",
    "long_term_targets": "Larger creators worth building relationships with over time",
    "partnership_budget_estimate": "Range based on tier and format"
  }
}
```

Present formatted summary:

```
INFLUENCER DISCOVERY REPORT
Searched: {platforms} for "{niche}"
Total found: {N} candidates, {scored} scored

TIER 1 -- PRIORITY TARGETS ({count}):
1. {name} -- {primary_platform} -- {followers} followers -- Score: {N}/100
   Niche: {niche}
   Engagement: {rate}% ({quality})
   Best collab format: {format}
   Outreach angle: {angle}

TIER 2 -- STRONG CANDIDATES ({count}):
1. {name} -- {primary_platform} -- {followers} -- Score: {N}/100
   Niche: {niche}
   Best collab format: {format}

PLATFORM BREAKDOWN:
- LinkedIn: {count} candidates, avg score {N}
- Instagram: {count} candidates, avg score {N}
- YouTube: {count} candidates, avg score {N}
- Twitter: {count} candidates, avg score {N}

RECOMMENDED NEXT STEPS:
1. Reach out to TIER 1 targets this week
2. {quick_win recommendation}
3. {long_term recommendation}
```

## Example Usage

Trigger phrases:
- "Find influencers in our niche"
- "Discover micro-influencers for partnership"
- "Who are the top creators in ecommerce?"
- "Find KOLs for Shopify and D2C"
- "Search for influencers we could collaborate with"
- "Find YouTube creators covering Shopify development"

```
User: Find micro-influencers in the Shopify and D2C space for co-marketing
Assistant: [reads config, searches LinkedIn/Instagram/YouTube/Twitter for Shopify and D2C creators with 1K-100K followers, scores by relevance/engagement/authenticity, generates partnership recommendations and outreach templates]
```

```
User: Find LinkedIn influencers in India covering ecommerce, 5K-50K followers
Assistant: [same flow limited to LinkedIn, filtered to India geography and 5K-50K range, deeper enrichment on LinkedIn-specific signals]
```
