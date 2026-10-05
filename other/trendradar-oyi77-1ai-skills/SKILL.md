---
name: trendradar
description: Use when aI-powered trending topic monitoring from 35+ platforms. Aggregate
  trends, analyze sentiment, and get real-time notifications. Based on TrendRadar
  MCP server (4.5K+ stars). Use when working with trendradar.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
- analysis
- investigation
- monitoring
- research
- trendradar
version: 1.0.0
category: research
---

persona:
  name: "Domain Expert"
  title: "Master of Trendradar"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# TrendRadar Skill

## Overview

AI-powered trending topic monitoring and analysis from 35+ platforms. Cut through information overload with intelligent aggregation, filtering, and AI-powered conversational analysis. Perfect for research, content ideation, and opportunity discovery.

**Source**: [sansan0/trendradar](https://github.com/sansan0/trendradar) (4.5K+ stars)  
**Platforms**: 35+ including Douyin, Zhihu, Bilibili, Weibo, Twitter, Reddit, HackerNews  
**Use Cases**: Research, content, investing, PR, market analysis

---


## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use
**Trigger phrases:**
- "trendradar"
- "AI-powered trending topic monitoring from 35+ platforms"


- Monitor industry trends in real-time
- Research content topics and viral hooks
- Track brand sentiment and PR
- Identify emerging opportunities early
- Multi-source trend aggregation
- Sentiment analysis for decisions

---

## MCP Server Setup

Configuration and connection setup for the MCP server.


### Installation
```json
{
  "mcpServers": {
    "trendradar": {
      "command": "npx",
      "args": ["-y", "@trendradar/mcp-server"],
      "env": {
        "TRENDRADAR_API_KEY": "${TRENDRADAR_API_KEY}"
      }
    }
  }
}
```

### Alternative: Direct Run
```bash
npx -y @trendradar/mcp-server
```

---

## Available Tools (13 MCP Tools)

Complete list of available MCP tools and their parameters.


### 1. Search Trends
```typescript
// Search trending topics across platforms
searchTrends({
  keyword: "AI",           // Search term
  platforms: ["twitter", "reddit", "hackernews"],
  timeRange: "24h",        // 1h, 6h, 24h, 7d, 30d
  limit: 20
})
```

### 2. Get Platform Trends
```typescript
// Get trends from specific platform
getPlatformTrends({
  platform: "twitter",      // twitter, reddit, hackernews, etc.
  category: "technology",
  limit: 50
})
```

### 3. Analyze Trend
```typescript
// Deep analysis of a trend
analyzeTrend({
  topic: "AI agents",
  includeSentiment: true,
  includeRelated: true
})
```

### 4. Get Trend History
```typescript
// Historical trend data
getTrendHistory({
  topic: "GPT-5",
  timeRange: "30d",
  interval: "1d"
})
```

### 5. Compare Topics
```typescript
// Compare trending topics
compareTopics({
  topics: ["AI", "crypto", "web3"],
  timeRange: "7d"
})
```

### 6. Get Sentiment Analysis
```typescript
// Sentiment for topic
getSentiment({
  topic: "Tesla",
  platforms: ["twitter", "reddit"]
})
```

### 7. Monitor Keywords
```typescript
// Set up keyword monitoring
monitorKeywords({
  keywords: ["AI startup", "new product"],
  platforms: ["twitter", "reddit"],
  notify: true
})
```

### 8. Get Trending Products
```typescript
// Find trending products
getTrendingProducts({
  category: "software",
  timeRange: "7d"
})
```

### 9. Get Viral Content
```typescript
// Find viral content
getViralContent({
  topic: "AI video",
  platforms: ["twitter", "tiktok"],
  limit: 10
})
```

### 10. Cross-Platform Analysis
```typescript
// Analyze across platforms
crossPlatformAnalysis({
  topic: "AI tools",
  includePlatforms: ["twitter", "reddit", "hackernews", "ProductHunt"]
})
```

---

## Supported Platforms

Platforms and services this skill integrates with.


### Social Media
| Platform | Type | Key Metrics |
|----------|------|-------------|
| Twitter/X | Trends | Engagement, Retweets |
| Reddit | Subreddits | Upvotes, Comments |
| HackerNews | Tech | Karma, Comments |
| Bilibili | Video | Views, Likes |
| Douyin | Short Video | Views, Shares |
| Weibo | Social | Reads, Likes |
| Zhihu | Q&A | Answers, Likes |

### News & Media
| Platform | Type |
|----------|------|
| Google News | News aggregation |
| NewsAPI | Global news |
| Bing News | Microsoft news |

### Tech & Product
| Platform | Type |
|----------|------|
| ProductHunt | Product launches |
| GitHub | Trending repos |
| Dev.to | Developer content |

---

## Use Cases

Real-world scenarios where this skill provides value.


### 1. Content Research
```
Use: larry-playbook + trendradar

1. Search trending topics in niche
2. Identify viral hooks
3. Analyze sentiment
4. Create content
5. Publish and track
```

### 2. Investment Research
```
Use: trading + trendradar

1. Monitor industry trends
2. Track company sentiment
3. Identify emerging tech
4. Analyze competitor mentions
```

### 3. Competitor Monitoring
```
Use: market-research + trendradar

1. Track competitor mentions
2. Sentiment analysis
3. PR impact analysis
4. Market positioning
```

### 4. PR & Brand Monitoring
```
Use: analytics + trendradar

1. Brand mention tracking
2. Sentiment monitoring
3. Crisis detection
4. Impact measurement
```

---

## Integration with 1ai-skills

How to connect this tool with the 1ai-skills ecosystem.


### Research Pipeline
```
trendradar → ai-research-agent → content-creation → publishing
   ↓              ↓                   ↓              ↓
Find trends   Analyze            Create          Distribute
```

### Skill Synergies

| Skill | Use Case |
|-------|----------|
| ai-research-agent | Deep trend analysis |
| larry-playbook | Viral content creation |
| market-research | Competitor analysis |
| content-creator | Multi-platform content |

### With Continuous Learning
```
1. Monitor trends daily
2. Track successful content
3. Learn what works
4. Improve recommendations
```

---

## Notification Channels

Configure alerts to:
- **WeCom** - Enterprise chat
- **Feishu** - Lark/Feishu
- **DingTalk** - Alibaba DingTalk
- **Telegram** - Bot notifications
- **Email** - Daily summaries
- **ntfy** - Push notifications

---

## Best Practices

Key aspects of trendradar relevant to this section.


### Do's
✅ Use specific keywords for targeted results  
✅ Set up daily monitoring for priorities  
✅ Cross-reference multiple platforms  
✅ Use sentiment for quality判断  
✅ Track historical data for patterns  

### Don'ts
❌ Don't monitor too many keywords  
❌ Don't ignore negative sentiment  
❌ Don't rely on single platform  
❌ Don't skip competitor monitoring  

---

## Metrics

| Metric | Target |
|--------|--------|
| Topics monitored | 20-50 |
| Platforms covered | 10+ |
| Update frequency | Real-time |
| Sentiment accuracy | >80% |

---

## Version History

- **v1.0** (2026-02-27) - Initial creation
  - Based on TrendRadar MCP server
  - 35+ platform integration

---


## When NOT to Use

- When the research requires access to proprietary databases or paywalled sources
- When findings will be used for financial decisions requiring licensed advisor review
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Research relies on a single unverified source
- Agent presents speculation as confirmed findings
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Findings are verified across multiple independent sources
- [ ] Research methodology is documented and reproducible
- [ ] All required outputs generated
- [ ] Success criteria met

## Agent Reach Integration

For deeper platform scraping beyond trend monitoring, use `skill://agent-reach`:

```bash
# After identifying trending topics via TrendRadar, deep-dive on Twitter
agent-reach twitter search "trending topic" --limit 100

# Reddit discussion analysis
agent-reach reddit search "trending topic" --limit 50

# YouTube video transcript analysis
agent-reach youtube search "trending topic" --limit 20 --transcript

# XiaoHongShu trend research (Chinese market)
agent-reach xhs search "热门话题" --limit 50
```

Use TrendRadar for monitoring and alerting, Agent Reach for deep content extraction. Combine with `skill://social-intelligence` for full sentiment analysis.

## Related Skills

- [ai-research-agent](../ai-research-agent/SKILL.md) - Deep research
- [larry-playbook](../../content/larry-playbook/SKILL.md) - Viral content
- [market-research](../../marketing/market-research/SKILL.md) - Competitor analysis
- [social-intelligence](../social-intelligence/SKILL.md) - Cross-platform sentiment
- [continuous-learning](../continuous-learning/SKILL.md) - Learn from trends

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
