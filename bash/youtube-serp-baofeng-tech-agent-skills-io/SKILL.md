---
name: youtube-serp
description: 'Search YouTube SERP results through AISA for video research, channel discovery, trend checking, and competitor tracking. Use when: you need ranked YouTube results for a query, optionally filtered by country or language.'
license: MIT
allowed-tools: Read Bash Grep
when_to_use: you need ranked YouTube results for a query, optionally filtered by country or language
---

> Release note: This package is published for Claude Code. References to OpenClaw below describe the original source workflow, a companion runtime, or compatibility guidance unless the skill is explicitly about OpenClaw itself.

# YouTube SERP 📺

Search ranked YouTube results through AISA for content research, channel discovery, trend analysis, and competitor tracking.

## Compatibility

Works with any [agentskills.io](https://agentskills.io)-compatible harness, including:

- **Claude Code** and **Claude**
- **OpenAI Codex**
- **Cursor**
- **Gemini CLI**
- **OpenCode**, **Goose**, **OpenClaw**, **Hermes**
- and other tools that implement the [Agent Skills specification](https://agentskills.io/specification)

Requires Python 3, a POSIX shell, and `AISA_API_KEY` from [aisa.one](https://aisa.one).

## Use when

- You want the top YouTube results for a keyword or topic
- You need region-specific or language-specific YouTube search results
- You are researching competitor videos or channels
- You want quick SERP-style inputs for content planning or SEO analysis

## Example requests

### Content research

```text
Find top-ranking videos about "AI agents tutorial" to see what is performing well.
```

### Competitor tracking

```text
Search for videos from competitor channels about "machine learning".
```

### Trend discovery

```text
What are the top YouTube videos about "GPT-5" right now?
```

### Topic analysis

```text
Find popular videos on "autonomous driving" to understand audience interest.
```

### Channel discovery

```text
Search for channels creating content about "crypto trading".
```

## Quick start

```bash
export AISA_API_KEY="your-key"
```

## Core capabilities

### Basic YouTube search

```bash
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI+agents+tutorial" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Search with country filter

```bash
# Search in specific country (US)
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=machine+learning&gl=us" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Search in Japan
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI&gl=jp&hl=ja" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Search with language filter

```bash
# Search with interface language
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=python+tutorial&hl=en" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Chinese interface
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=编程教程&hl=zh-CN&gl=cn" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Pagination with filter token

```bash
# Use sp parameter for pagination or advanced filters
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI&sp=<filter_token>" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

## Python client

```bash
# Basic search
python3 scripts/youtube_client.py search --query "AI agents tutorial"

# Search with country
python3 scripts/youtube_client.py search --query "machine learning" --country us

# Search with language
python3 scripts/youtube_client.py search --query "python tutorial" --lang en

# Full options
python3 scripts/youtube_client.py search --query "GPT-5 news" --country us --lang en

# Competitor research
python3 scripts/youtube_client.py search --query "OpenAI tutorial"

# Trend discovery
python3 scripts/youtube_client.py search --query "AI trends 2025"
```

## Use cases

### 1. Content gap analysis

Find what content is ranking well to identify gaps in your strategy:

```python
# Search for top videos in your niche
results = client.search("AI automation tutorial")
# Analyze titles, views, and channels to find opportunities
```

### 2. Competitor monitoring

Track what competitors are publishing:

```python
# Search for competitor brand + topic
results = client.search("OpenAI GPT tutorial")
# Monitor ranking changes over time
```

### 3. Keyword research

Discover what topics are trending:

```python
# Search broad topics to see what's popular
results = client.search("artificial intelligence 2025")
# Extract common keywords from top-ranking titles
```

### 4. Audience research

Understand what your target audience watches:

```python
# Search in specific regions
results = client.search("coding tutorial", country="jp", lang="ja")
# Analyze regional content preferences
```

### 5. SEO analysis

Analyze how videos rank for specific keywords:

```python
# Track ranking positions for target keywords
keywords = ["AI tutorial", "machine learning basics", "Python AI"]
for kw in keywords:
    results = client.search(kw)
    # Record top 10 videos and their channels
```

## API endpoint reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/youtube/search` | GET | Search YouTube SERP |

## Request parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| engine | string | Yes | Must be `youtube` |
| q | string | Yes | Search query |
| gl | string | No | Country code (for example `us`, `jp`, `uk`, `cn`) |
| hl | string | No | Interface language (for example `en`, `ja`, `zh-CN`) |
| sp | string | No | YouTube filter token for pagination or filters |

## Response format

```json
{
  "search_metadata": {
    "id": "search_id",
    "status": "Success",
    "created_at": "2025-01-15T12:00:00Z",
    "request_time_taken": 1.23,
    "total_time_taken": 1.45
  },
  "search_results": [
    {
      "video_id": "abc123xyz",
      "title": "Complete AI Agents Tutorial 2025",
      "link": "https://www.youtube.com/watch?v=abc123xyz",
      "channel_name": "AI Academy",
      "channel_link": "https://www.youtube.com/@aiacademy",
      "description": "Learn how to build AI agents from scratch...",
      "views": "125K views",
      "published_date": "2 weeks ago",
      "duration": "45:30",
      "thumbnail": "https://i.ytimg.com/vi/abc123xyz/hqdefault.jpg"
    }
  ]
}
```

## Country codes (`gl`)

| Code | Country |
|------|---------|
| us | United States |
| uk | United Kingdom |
| jp | Japan |
| cn | China |
| de | Germany |
| fr | France |
| kr | South Korea |
| in | India |
| br | Brazil |
| au | Australia |

## Language codes (`hl`)

| Code | Language |
|------|----------|
| en | English |
| ja | Japanese |
| zh-CN | Chinese (Simplified) |
| zh-TW | Chinese (Traditional) |
| ko | Korean |
| de | German |
| fr | French |
| es | Spanish |
| pt | Portuguese |
| ru | Russian |

## Pricing

| API | Cost |
|-----|------|
| YouTube search | ~$0.002 |

## Get started

1. Sign up at [aisa.one](https://aisa.one)
2. Get your API key
3. Add credits (pay-as-you-go)
4. Set the environment variable: `export AISA_API_KEY="your-key"`

## Full API reference

See [API Reference](https://aisa.one/docs/api-reference/) for complete endpoint documentation.
