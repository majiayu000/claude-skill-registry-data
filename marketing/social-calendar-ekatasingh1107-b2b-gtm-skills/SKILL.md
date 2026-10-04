---
name: social-calendar
description: >
  Generates a weekly social media content calendar across platforms.
  Chains blog-researcher + linkedin-researcher + social-content-writer
  to produce 5-7 posts/week with posting schedule.
tags: [social-media, calendar, content-planning, scheduling]
---

# Social Calendar

Generates a complete weekly social media content calendar with ready-to-post content across LinkedIn, X/Twitter, Instagram, and Reddit. Chains research skills to find trending topics and content angles, then generates platform-native posts with optimal scheduling.

## Prerequisites

- `agency.config.json` populated (agency info, services, case studies, outreach tone)
- WebSearch tool available (for trend research)
- Optional: recent blog posts or content to repurpose

## Capabilities Used

1. `blog-researcher` -- find trending topics, competitor content, industry news
2. `linkedin-researcher` -- find trending LinkedIn discussions in the niche
3. `social-content-writer` -- generate platform-native posts for each slot

## Phase 0: Intake

Read `agency.config.json`:
- `agency.name`, `agency.founder` -- brand identity
- `services[]` -- content pillars aligned to services
- `case_studies[]` -- case study content to feature
- `outreach.tone` -- voice baseline

Accept parameters:
- `week_start` -- (required) date string (YYYY-MM-DD) for Monday of the target week
- `platforms` -- (optional) array of platforms to include. Default: `["linkedin", "twitter", "instagram"]`
- `posts_per_week` -- (optional) total target. Default: 7
- `content_pillars` -- (optional) themes to focus on. Default: derived from services
- `repurpose_content` -- (optional) array of existing content URLs/text to repurpose
- `exclude_topics` -- (optional) topics to avoid this week
- `include_case_study` -- boolean, include at least one case study post. Default: `true`

## Phase 1: Content Pillar Definition

Define 3-5 content pillars from `services[]` and agency expertise:

```
CONTENT PILLARS
---
1. [Pillar name]: [description, 1-2 sentences]
   Post types: [thought leadership, how-to, case study]
   Platforms: [which platforms this pillar works best on]

2. [Pillar name]: [description]
   ...
```

Default pillars for Plasho:
1. **Shopify CRO**: Product page optimization, conversion tips, A/B test insights
2. **D2C Growth**: Industry trends, brand building, scaling strategies
3. **Case Studies**: Client results, before/after, specific tactics that worked
4. **Behind the Scenes**: Agency culture, process insights, tools and workflows
5. **Industry Commentary**: Hot takes on ecommerce news, trends, platform updates

## Phase 2: Topic Research

### Execute `blog-researcher`
- Search for trending topics in the agency's niche (last 7 days)
- Find competitor social content that performed well
- Identify industry news worth commenting on

### Execute `linkedin-researcher`
- Find trending LinkedIn posts in D2C, ecommerce, Shopify spaces
- Identify popular discussion threads to contribute to
- Note hashtags and topics gaining traction

### Compile Research
```
TRENDING THIS WEEK
---
1. [Topic]: [source, why it's trending, relevance to pillars]
2. [Topic]: ...

COMPETITOR CONTENT THAT PERFORMED
---
1. [Competitor]: [post summary, engagement, platform]
2. ...

INDUSTRY NEWS
---
1. [News item]: [summary, our angle]
2. ...
```

## Phase 3: Calendar Slot Planning

Allocate posts across the week using optimal timing:

### Default Weekly Template (7 posts)
| Day | Platform | Post Type | Pillar | Time (IST) |
|-----|----------|-----------|--------|------------|
| Monday | LinkedIn | Thought Leadership | D2C Growth | 9:30 AM |
| Tuesday | Instagram | Carousel | Shopify CRO | 12:00 PM |
| Wednesday | Twitter | Thread | Industry Commentary | 8:30 AM |
| Wednesday | LinkedIn | Engagement Question | Behind the Scenes | 1:00 PM |
| Thursday | Instagram | Case Study | Case Studies | 11:00 AM |
| Friday | LinkedIn | Hot Take | Industry Commentary | 10:00 AM |
| Saturday | Instagram | Story | Behind the Scenes | 7:00 PM |

### Allocation Rules
- LinkedIn: 2-3 posts/week (Tue-Thu peak)
- Twitter: 1-2 posts/week (threads perform best)
- Instagram: 2-3 posts/week (carousels + stories)
- Reddit: 0-1 posts/week (only when genuinely helpful, not promotional)
- No back-to-back posts on the same platform within 24 hours
- At least one case study post per week (if `include_case_study` = true)
- Mix post types: no two consecutive thought leadership posts

## Phase 4: Content Generation

For each calendar slot, execute `social-content-writer`:
- Pass the topic, platform, post type, and relevant research
- Generate 2 variants per post
- Select the stronger variant (or present both for user choice)

### Per-Post Output
```
POST [N]: [Day] [Time] -- [Platform]
---
Topic: [topic]
Pillar: [content pillar]
Type: [post type]
Research source: [what informed this post]

VARIANT A:
[Full post text]

VARIANT B:
[Full post text]

Visual: [image/carousel/video suggestion]
Hashtags: [platform-appropriate hashtags]
Engagement hook: [how this post drives engagement]
```

## Phase 5: Repurpose Planning

If `repurpose_content` provided, identify cross-posting opportunities:
- Blog post -> LinkedIn article summary + Twitter thread + Instagram carousel
- Case study -> LinkedIn post + Instagram before/after + Twitter stats thread
- Video -> Reel clips + quote graphics + behind-the-scenes story

Map repurposed content into available calendar slots.

## Phase 6: Quality Check

Before returning the full calendar:
1. **Pillar balance**: No single pillar > 40% of posts
2. **Platform balance**: Each active platform has 1+ posts
3. **Type variety**: No more than 2 of the same post type in a week
4. **Tone consistency**: All posts align with `outreach.tone` adapted per platform
5. **No cannibalization**: No two posts covering the exact same angle
6. **Banned phrases**: None present in any post
7. **Weekend appropriateness**: Weekend posts are lighter, more casual

## Phase 7: Output

Return structured JSON:

```json
{
  "week_start": "2026-03-16",
  "week_end": "2026-03-22",
  "total_posts": 7,
  "platforms": {
    "linkedin": 3,
    "instagram": 3,
    "twitter": 1
  },
  "pillar_distribution": {
    "Shopify CRO": 2,
    "D2C Growth": 1,
    "Case Studies": 2,
    "Industry Commentary": 1,
    "Behind the Scenes": 1
  },
  "research_sources": [
    "Trending: Shopify's new checkout extensibility update",
    "Competitor: Brand X's carousel on CRO got 500+ reactions",
    "News: India D2C funding round announcements this week"
  ],
  "calendar": [
    {
      "day": "Monday",
      "date": "2026-03-16",
      "platform": "linkedin",
      "time": "09:30 IST",
      "post_type": "thought-leadership",
      "pillar": "D2C Growth",
      "topic": "Why most D2C brands plateau at 10 Cr ARR",
      "text": "Full post text...",
      "hashtags": ["#D2C", "#Ecommerce", "#ShopifyIndia"],
      "visual_suggestion": "Simple text quote card with key stat",
      "engagement_hook": "Asks founders to share their growth plateau experience",
      "variant_b": "Alternative post text..."
    }
  ],
  "repurposed_content": [
    {
      "source": "Blog: 5 CRO Tips for Shopify Stores",
      "repurposed_as": "Instagram carousel (Thursday)",
      "adaptation_notes": "Extracted 5 tips as 5 carousel slides"
    }
  ],
  "approval_needed": true,
  "generated_at": "2026-03-13T10:00:00Z"
}
```

## Phase 8: Approval & Scheduling

Present the full calendar for review:
```
WEEKLY CONTENT CALENDAR: [Week dates]
---
[Day-by-day listing with post previews]

APPROVE ALL / EDIT INDIVIDUAL POSTS / REGENERATE SPECIFIC SLOTS
```

After approval:
- Mark approved posts as ready
- Flag posts needing visual creation (hand off to `social-creative-brief`)
- Provide copy-paste ready text for each platform

## Example Usage

Trigger phrases:
- "Plan next week's social media content"
- "Generate a content calendar for this week"
- "Create 7 social posts for the week of March 16"
- "Plan social content around the Kibi Sports case study"
- "Build a content calendar focused on CRO topics"
- "Repurpose our latest blog post into social content for the week"
