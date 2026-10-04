---
name: github-star-bot
description: "Automate GitHub starring, tracking repositories, and managing star-based alerts."
triggers:
  - "auto star github"
  - "GitHub stars"
  - "自动 star"
  - "star tracking"
---

# GitHub Star Bot

Automated GitHub starring and repository tracking.

## Features

- ⭐ **Auto Star** — Star repositories by topic/language
- 📊 **Star Analytics** — Track your starred repos
- 🔔 **New Repo Alert** — Get notified of new repos
- 🏷️ **Topic Tracking** — Follow specific topics

## Usage

### Star Repositories

```bash
# Star by topic
hermes github star --topic "ai,python" --min-stars 100

# Star by language
hermes github star --language "TypeScript" --min-stars 50

# Star specific user
hermes github star --user "clowlove" --all
```

### Track Stars

```bash
# List starred
hermes github star list --sort stars

# Star analytics
hermes github star stats
```

## Configuration

```yaml
# github-star-config.yml
github:
  token: ${GITHUB_TOKEN}
  
auto_star:
  topics: ["ai", "python", "typescript"]
  min_stars: 100
  max_per_day: 50
  
tracking:
  notify: telegram
  keywords: ["hermes", "agent", "ai"]
```

## Pitfalls

1. **Rate Limits** — 5000 requests/hour max
2. **Quality** — Don't star low-quality repos blindly
3. **Personal** — Use separate account for bot activity