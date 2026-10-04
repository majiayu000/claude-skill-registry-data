---
name: News
slug: news
version: 1.0.1
description: Personalized news briefings that learn your interests, formats, and timing preferences.
homepage: https://clawic.com/skills/news
changelog: Added structure with Core Rules and memory system
metadata:
  clawdbot:
    emoji: 📰
    os:
    - linux
    - darwin
    - win32
    displayName: News
---

## When to Use

User wants personalized news briefings. Agent builds a news profile, delivers formatted briefings, learns interests over time, and handles multi-source coverage.

## Architecture

Memory lives in `~/Clawic/data/news/`. See `memory-template.md` for setup.

```
~/Clawic/data/news/
├── memory.md       # Profile: interests, format, timing
├── history.md      # Past briefings and engagement
└── sources.md      # Trusted sources and biases
```

## Quick Reference

| Topic | File |
|-------|------|
| Memory setup | `memory-template.md` |

## Core Rules

### 1. Build Profile Before Delivering
On first interaction, ask about:
- Specific interests (not generic categories)
- Proportions if multiple interests ("70% AI, 30% markets")
- Format preference (bullets, narrative, headlines-only)
- Timing (morning, evening, weekly, on-demand)

### 2. Check Memory First
Before every briefing, read `~/Clawic/data/news/memory.md` for user preferences. Tailor content to their stated interests and format.

### 3. Facts First, Analysis Second
Lead with what happened before why it matters. Always include when news broke. Cite sources by name.

### 4. Multi-Source on Contested Topics
Present at least 2 sources when covering controversy. Note when sources disagree. State editorial leanings when relevant.

### 5. Never Fabricate
If uncertain whether something happened, say so. Never assume or invent news events.

### 6. Update Memory from Engagement
Track which stories user engages with vs skips. Periodically suggest profile adjustments based on patterns.

## Common Traps

- Presenting stale news as fresh → destroys trust
- Single-source on controversy → reckless reporting
- Generic categories ("tech") → ask for specifics ("AI startups")
- Overwhelming with items → morning briefings max 5-7 items

## Security & Privacy

**Data that stays local:**
- User preferences in `~/Clawic/data/news/`
- Engagement history in `~/Clawic/data/news/history.md`

**This skill does NOT:**
- Send data to external services
- Access files outside `~/Clawic/data/news/`
- Store news content permanently

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/<slug> (install if the user confirms):
- `summarizer` — condense long articles
- `scrape` — extract web content
- `reading` — reading lists and tracking

## Feedback

- If useful, star it: https://clawic.com/skills/news
- Latest version: https://clawic.com/skills/news
