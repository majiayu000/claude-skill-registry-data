---
name: linkedin-researcher
description: Research top-performing LinkedIn content in your niche and generate a content playbook
tags: [linkedin, content-research, social-media, thought-leadership, content-strategy]
---

# LinkedIn Researcher

Researches top-performing LinkedIn content in your niche by analyzing viral posts, hooks, formats, topics, and engagement patterns. Identifies what resonates with your ICP audience on LinkedIn and produces a structured content playbook with templates, topic clusters, and posting cadence recommendations.

## Prerequisites

- `agency.config.json` at repo root with `services`, `icp`, and `outreach` sections
- WebSearch tool available
- Optional: `thought-leadership` skill for content creation from playbook outputs

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `agency.name`, `agency.founder` -- for positioning context
   - `services[].name`, `services[].keywords` -- content topic seeds
   - `icp.segments[].industries`, `icp.segments[].titles` -- audience definition
   - `icp.primary_keywords`, `icp.secondary_keywords` -- topic relevance signals
   - `outreach.tone` -- voice alignment for templates
3. Accept parameters:
   - `niche_keywords` -- additional topic keywords beyond config (default: use config keywords)
   - `influencers` -- specific LinkedIn profiles/names to study (default: discover automatically)
   - `content_types` -- filter: `text | carousel | video | poll | article | newsletter` (default: all)
   - `time_window` -- how far back to analyze (default: "past 30 days")
   - `max_posts` -- max posts to analyze (default: 50)

## Phase 1: Influencer Discovery

Identify top voices in the niche using WebSearch:

### Discovery queries:
- `site:linkedin.com/in "{service_keyword}" "followers" "{industry}"`
- `site:linkedin.com/posts "{service_keyword}" "likes" OR "comments"`
- `"top linkedin influencer" "{industry}" OR "{service_keyword}"`
- `"linkedin creator" "{industry}" "{icp_title}"`
- `"best linkedin posts" "{service_keyword}" {time_window}`

### For each discovered influencer, capture:
```json
{
  "name": "Full name",
  "profile_url": "LinkedIn URL",
  "headline": "Their LinkedIn headline",
  "follower_estimate": "Approximate follower count if visible",
  "niche": "Their primary topic area",
  "relevance_to_icp": "HIGH | MEDIUM | LOW"
}
```

### Filtering rules:
- Prioritize creators whose audience overlaps with ICP titles (founders, CMOs, heads of ecommerce).
- Skip profiles with fewer than 1,000 estimated followers (micro-influencers handled by `influencer-finder`).
- Target 10-20 influencers for post analysis.

## Phase 2: Post Collection

For each identified influencer and for niche keywords generally, search for high-performing posts:

### Post search queries:
- `site:linkedin.com/posts "{influencer_name}" "{service_keyword}"`
- `site:linkedin.com/posts "{service_keyword}" "agree" OR "this" OR "100%"` (engagement markers)
- `site:linkedin.com/pulse "{service_keyword}" "{industry}"`
- `"{influencer_name}" linkedin post "{topic_keyword}"`

### For each post found, extract:
```json
{
  "post_url": "URL if available",
  "author": "Name",
  "hook": "First 2 lines of the post (the scroll-stopper)",
  "full_text": "Complete post text (first 500 chars if truncated)",
  "format": "text_only | listicle | story | contrarian | how_to | carousel | poll | video | article",
  "topic": "Primary topic of the post",
  "engagement_signals": "Likes/comments/reposts if visible in search snippet",
  "posted_date": "Date if available",
  "cta_type": "question | link | dm_me | comment_below | none",
  "length": "short (<500 chars) | medium (500-1500) | long (1500+)"
}
```

## Phase 3: Pattern Analysis

Analyze collected posts to identify winning patterns:

### Hook Analysis
Categorize all hooks into types:
- **Contrarian**: "Stop doing X" / "X is dead" / "Unpopular opinion:"
- **Story opener**: "Last week I..." / "3 years ago..." / "True story:"
- **Data lead**: "We analyzed X..." / "97% of..." / "After X conversions..."
- **List promise**: "X things I learned..." / "X mistakes that..." / "The X framework for..."
- **Question**: "Why do most..." / "What if..." / "Ever wondered..."
- **Bold claim**: "This one change..." / "The secret to..." / "Nobody talks about..."

Count frequency and estimate engagement per hook type.

### Format Analysis
For each content format (text, carousel, poll, article, video):
- Count of posts found
- Average engagement signals
- Best-performing examples
- Common structural patterns

### Topic Cluster Analysis
Group posts into topic clusters:
- Map each post to 1-2 topic clusters from service keywords
- Identify which clusters have highest engagement
- Find underserved topics (low competition, relevant to ICP)

### Posting Pattern Analysis
If dates are available:
- Day of week distribution for high-performing posts
- Posting frequency of top creators
- Consistency patterns

## Phase 4: Template Generation

Based on patterns identified, generate reusable templates:

### For each of the top 5 hook types, create:
```json
{
  "hook_type": "contrarian",
  "template": "Stop [common practice]. Here's what [top performers] do instead:",
  "example_filled": "Stop A/B testing your homepage hero. Here's what brands doing 8-figure revenue do instead:",
  "when_to_use": "When challenging conventional wisdom in your space",
  "engagement_prediction": "HIGH -- contrarian hooks get 2-3x more comments"
}
```

### For each winning format, create a structural template:
- Text post template with hook, body, CTA
- Carousel outline template with slide-by-slide guidance
- Poll template with option framing guidance
- Article template with section structure

### Content calendar seeds:
Generate 20 specific post ideas mapped to:
- Service keyword they promote
- ICP segment they target
- Hook type to use
- Format to use
- Estimated effort (low/medium/high)

## Phase 5: Output

Return structured playbook:

```json
{
  "research_summary": {
    "posts_analyzed": 50,
    "influencers_studied": 15,
    "time_period": "past 30 days",
    "platforms": ["LinkedIn"]
  },
  "top_influencers": [
    {
      "name": "...",
      "profile_url": "...",
      "headline": "...",
      "follower_estimate": "...",
      "niche": "...",
      "top_post_hook": "...",
      "content_style": "..."
    }
  ],
  "hook_analysis": {
    "contrarian": { "frequency": 12, "avg_engagement": "high", "examples": [] },
    "story_opener": { "frequency": 8, "avg_engagement": "medium", "examples": [] }
  },
  "format_analysis": {
    "text_only": { "count": 25, "avg_engagement": "medium", "best_example": "..." },
    "carousel": { "count": 10, "avg_engagement": "high", "best_example": "..." }
  },
  "topic_clusters": [
    { "topic": "Shopify CRO", "post_count": 8, "engagement": "high", "saturation": "medium" }
  ],
  "templates": [],
  "content_calendar": [],
  "recommendations": {
    "posting_frequency": "3-4x per week",
    "best_days": ["Tuesday", "Wednesday", "Thursday"],
    "top_formats": ["text_only", "carousel"],
    "top_hooks": ["contrarian", "data_lead"],
    "topics_to_own": ["...", "..."],
    "voice_notes": "Align with agency tone: direct, helpful, zero fluff"
  }
}
```

Present a formatted summary alongside the JSON:

```
LINKEDIN CONTENT PLAYBOOK
Analyzed: {N} posts from {M} influencers

TOP HOOKS THAT WORK:
1. {hook_type} -- used {N} times, {engagement} engagement
   Template: "{template}"

WINNING FORMATS:
1. {format} -- {count} posts, {engagement} avg

TOPIC OPPORTUNITIES:
1. {topic} -- {saturation} saturation, {engagement} potential

CONTENT CALENDAR (Next 20 posts):
1. [{format}] {topic} -- Hook: {hook_type} -- Effort: {level}
...

POSTING CADENCE: {frequency} on {best_days}
```

## Example Usage

Trigger phrases:
- "Research LinkedIn content in our niche"
- "What's working on LinkedIn for Shopify agencies?"
- "Build a LinkedIn content playbook"
- "Analyze top LinkedIn posts about ecommerce"
- "Find viral LinkedIn content about D2C"
- "What hooks work best on LinkedIn?"

```
User: Research what's working on LinkedIn for Shopify and ecommerce content
Assistant: [reads config, discovers top influencers, collects high-performing posts, analyzes hooks/formats/topics, generates templates and content calendar, presents playbook]
```

```
User: Build a LinkedIn playbook focused on CRO content, study these 5 creators: [names]
Assistant: [same flow but focused on CRO keywords, studies specified creators plus discovers additional ones]
```
