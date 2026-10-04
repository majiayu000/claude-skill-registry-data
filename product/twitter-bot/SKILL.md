---
name: twitter-bot
description: "Automate Twitter/X posting, engagement, and analytics. Supports scheduling, threading, and trending话题 analysis."
triggers:
  - "twitter auto post"
  - "推特自动化"
  - "schedule tweets"
  - "twitter thread"
---

# Twitter Bot

Automated Twitter/X management and engagement.

## Features

- 📝 **Auto Posting** — Schedule and publish tweets
- 🧵 **Thread Creation** — Create multi-tweet threads
- 📊 **Analytics** — Track engagement metrics
- 🔍 **Trending** — Monitor trending topics
- 💬 **Auto Reply** — Engage with mentions

## Usage

### Post Tweet

```bash
# Simple tweet
hermes twitter post "Hello world! 🐦"

# With media
hermes twitter post "Check this out!" --image screenshot.png

# Schedule tweet
hermes twitter post "Thread coming soon!" --schedule "2026-06-01 09:00"
```

### Create Thread

```bash
# Create thread
hermes twitter thread \
  "1/ Excited to announce..." \
  "2/ Here's what we built..." \
  "3/ Key features include..." \
  "4/ Try it now! [link]"

# Reply as thread
hermes twitter thread-reply "Let me explain..." --reply-to tweet-id
```

### Analytics

```bash
# View stats
hermes twitter stats --days 7

# Top tweets
hermes twitter top --limit 10

# Follower growth
hermes twitter followers --trend
```

## Configuration

```yaml
# twitter-config.yml
account:
  api_key: ${TWITTER_API_KEY}
  api_secret: ${TWITTER_API_SECRET}
  
posting:
  max_per_day: 10
  min_interval: 30m
  
engagement:
  auto_like: true
  auto_retweet: false
  keywords: ["#AI", "#Tech", "#Python"]
```

## Pitfalls

1. **Rate Limits** — Twitter has strict API limits
2. **Content Policy** — Avoid spam-like behavior
3. **Media Size** — Max 5MB image, 15MB video