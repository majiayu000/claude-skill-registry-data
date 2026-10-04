---
name: last30
version: "1.1.0"
description: "Deep research across Reddit, X/Twitter, Hacker News, YouTube, Polymarket, and the web from the last 30 days. Synthesizes findings into a grounded, cited briefing. Use when: researching trends, doing competitive analysis, answering 'what's the latest on X', or comparing tools/products."
homepage: https://github.com/ralphoei/last30
author: ralphoei
license: MIT
original-author: mvanhorn
original-repo: https://github.com/mvanhorn/last30days-skill
metadata:
  clawdbot:
    emoji: "📰"
    requires:
      env:
        - BRAVE_API_KEY
      bins:
        - python3
        - node
    files:
      - "scripts/*"
    tags:
      - research
      - deep-research
      - reddit
      - x
      - twitter
      - youtube
      - hackernews
      - hn
      - polymarket
      - web-search
      - trends
      - recency
      - news
      - citations
      - multi-source
---

# last30 — Research Any Topic from the Last 30 Days

> **Attribution:** Simplified port of [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) (v2.9.5) by [@mvanhorn](https://github.com/mvanhorn). Original uses ScrapeCreators API for Reddit/TikTok/Instagram; this port uses free public APIs (Reddit JSON, HN Algolia, Brave Search) for a lightweight, zero-API-key setup.

Research any topic across Reddit, X/Twitter, Hacker News, YouTube, Polymarket, and the web. Surface what people are actually discussing, recommending, debating, and betting on right now.

## Trigger Phrases

- `/last30 [topic]`
- `research [topic]`
- `what's trending in [topic]`
- `[topic] vs [topic]`
- `/last30days [topic]`

## Prerequisites

- `BRAVE_API_KEY` env var must be set (web search)
- `AUTH_TOKEN` + `CT0` env vars (optional, for X search via bird)
- `summarize` skill available for YouTube transcripts

## Parse User Intent

Before running any tools, parse the input:

1. **TOPIC**: What they want to learn about
2. **QUERY_TYPE**:
   - `RECOMMENDATIONS` — "best X", "top X", "what X should I use"
   - `NEWS` — "what's happening with X", "X news"
   - `COMPARISON` — "X vs Y", "X versus Y"
   - `GENERAL` — anything else

**Display your parsing:**

```
📰 Researching: {TOPIC}
Type: {QUERY_TYPE}
Sources: Reddit, X, Hacker News, YouTube, Polymarket, Web

Starting research (2-5 min)...
```

## Quick Mode

Use `--quick` for faster, fewer results:
- 10 results per source instead of 25

## Deep Mode

Use `--deep` for comprehensive research:
- 40 results per source
- Full synthesis

## Usage Examples

```
/last30 AI video tools
/last30 best CRM software
/last30 figma vs canva
/last30 openai news --deep
/last30 rust vs go --quick
```

## How It Works

1. **Reddit** — queries `reddit.com/r/[subreddit]/search.json` by relevance
2. **X/Twitter** — uses `bird` (xurl) for recent posts
3. **Hacker News** — queries `hn.algolia.com` API
4. **YouTube** — runs `summarize` skill for video transcripts
5. **Polymarket** — queries `polymarket.com` API for active prediction markets related to the topic
6. **Web** — Brave Search API

Results are scored by engagement signals, cross-platform convergence is detected, and a synthesis is generated with inline citations.

## Output Format

```
📰 Research: {TOPIC}
Date: {date} | Sources: Reddit, X, HN, YouTube, Web

## Key Findings
- [3-5 bullet points with citations]

## What People Are Saying
[Synthesis of top findings across all sources]

## YouTube Insights
[Video titles, channels, key moments]

## Reddit Discussions
[Top threads, top comments, upvote counts]

## X/Twitter Perspective
[Key posts, handles, engagement]

## Polymarket Insights
[Active prediction markets, consensus odds, question clarity]

## Web Findings
[News, blogs, tutorials discovered]

## Stats
- Reddit: {n} results
- X: {n} results
- HN: {n} results
- YouTube: {n} results
- Polymarket: {n} results
- Web: {n} results

Saved to: ~/Documents/Last30Days/{topic-slug}.md
```

## Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `BRAVE_API_KEY` | Yes | Brave Search for web results |
| `AUTH_TOKEN` | No | X/Twitter cookie auth for bird |
| `CT0` | No | X/Twitter cookie auth for bird |

## Auto-Save

Every run saves a `.md` file to `~/Documents/Last30Days/` with the full briefing. Filename: `{topic-slug}-{date}.md`
