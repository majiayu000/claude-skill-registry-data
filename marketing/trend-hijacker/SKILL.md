---
description: Auto-identifies trending topics and suggests content angles.
---

# Trend Hijacker Skill

## Strategic Value

The Trend Hijacker skill automatically monitors social platforms, news sources, and search trends to identify topics gaining momentum. By detecting trending conversations early, it provides marketers with timely opportunities to create relevant, culturally resonant content that captures audience attention while interest is high. This real-time awareness transforms reactive marketing into proactive trend-riding, maximizing organic reach.

## Capabilities

- **Multi-Platform Trend Scanning:** Monitors Twitter/X, Reddit, TikTok, Google Trends, and news aggregators.
- **Trend Velocity Analysis:** Calculates rate of growth to distinguish fads from genuine trends.
- **Content Angle Generation:** Suggests brand-appropriate angles for trend participation.
- **Sentiment Screening:** Filters trends by sentiment—avoiding negative or controversial topics.
- **Relevance Scoring:** Ranks trends by relevance to defined target audiences and brand values.
- **Timing Alerts:** Notifies when a trend reaches optimal participation windows.

## Limitations

- Trend prediction involves some uncertainty—virality is never guaranteed.
- Requires brand guidelines integration to avoid off-brand content suggestions.
- Real-time monitoring depends on API availability and rate limits.

## Examples

### Example 1: Product Launch Timed to Trend

**User Prompt:** "Find trending topics that align with our new eco-friendly phone case launch. Target Gen Z audience."

**Trend Hijacker Response:**
```json
{
  "trend": "#SustainableLiving",
  "velocity": "+340% in 48 hours",
  "platforms": ["TikTok", "Instagram"],
  "content_angles": [
    "Showcase phone case made from ocean plastic—join the movement",
    "Documentarian style: From ocean trash to phone protection",
    "Challenge: How many phone cases fit in one plastic bottle?"
  ],
  "sentiment": "positive",
  "recommended_posting_window": "Next 18-36 hours"
}
```

### Example 2: Competitor Trend Response

**User Prompt:** "My competitor just posted about AI features—what's trending around AI in mobile right now?"

**Trend Hijacker Response:**
```json
{
  "trend": "AI Photography Features",
  "velocity": "+180% in 24 hours",
  "platforms": ["YouTube", "Twitter"],
  "content_angles": [
    "Comparison: Our AI portrait vs. real photographer shots",
    "Behind-the-scenes: How our AI learns from 10M photos",
    "User showcase: Best AI-edited photos from our community"
  ],
  "sentiment": "neutral to positive",
  "opportunity": "Position as accessible alternative"
}
```

## Configuration (config.yaml)

```yaml
trend_sources:
  - twitter
  - reddit
  - tiktok
  - google_trends
  - news_api

monitoring:
  scan_interval_minutes: 30
  min_velocity_threshold: 100  # % growth threshold

filters:
  excluded_keywords: ["controversial", "political", "nsfw"]
  required_sentiment: "positive"

target_audiences:
  gen_z:
    age_range: "18-26"
    interests: ["tech", "sustainability", "creativity"]
  young_professionals:
    age_range: "25-35"
    interests: ["productivity", "design", "finance"]
```
