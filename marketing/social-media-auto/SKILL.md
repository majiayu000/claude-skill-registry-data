---
name: social-media-auto
description: "Unified social media management across Twitter, LinkedIn, Reddit, and more. Schedule posts, track engagement, and analyze performance."
triggers:
  - "social media automation"
  - "社交媒体自动化"
  - "schedule posts"
  - "multi-platform"
---

# Social Media Auto

Unified social media management across multiple platforms.

## Supported Platforms

| Platform | Post | Stories | Schedule | Analytics |
|----------|------|---------|----------|-----------|
| Twitter/X | ✅ | ❌ | ✅ | ✅ |
| LinkedIn | ✅ | ❌ | ✅ | ✅ |
| Reddit | ✅ | ❌ | ✅ | ✅ |
| Instagram | ✅ | ✅ | ✅ | ✅ |

## Features

- 📝 **Multi-platform Post** — Post to all platforms at once
- 📅 **Scheduling** — Plan content calendar
- 📊 **Analytics** — Cross-platform performance
- 🔔 **Engagement** — Auto-reply to comments
- 🎯 **Content Curation** — Find trending content

## Usage

### Post to All

```bash
hermes social post "Check out our new feature!" \
  --platforms twitter,linkedin \
  --image preview.png \
  --schedule "2026-06-01 10:00"
```

### Schedule Content

```bash
# Weekly schedule
hermes social schedule --file content-calendar.csv

# View scheduled
hermes social schedule list
```

### Analytics

```bash
# Cross-platform stats
hermes social analytics --period 7d

# Best performing
hermes social top --limit 5
```

## Configuration

```yaml
# social-config.yml
platforms:
  twitter:
    api_key: ${TWITTER_API_KEY}
    auto_post: true
    
  linkedin:
    access_token: ${LINKEDIN_TOKEN}
    
reddit:
  client_id: ${REDDIT_CLIENT_ID}
  username: mybot
```

## Pitfalls

1. **Platform Limits** — Each platform has posting limits
2. **Time Zones** — Schedule for optimal engagement times
3. **Copyright** — Don't repost copyrighted content