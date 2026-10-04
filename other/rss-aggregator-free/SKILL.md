---
name: rss-aggregator-free
description: RSS Aggregator (Free). Aggregate RSS feeds into digestible summaries.
version: 3.0.0
author: AgentBoost Open Source
enterprise: false
category: Communications
---

### System Instructions
You are equipped with the `rss-aggregator-free` deterministic tool. This tool consolidates multiple RSS/Atom feeds into structured daily digests. It performs simple keyword tagging and summarizes recent entries to identify industry trends and breaking news.

### Execution Protocol
Invoke the RSS engine by passing strictly formatted JSON:

```json
{
  "feed_urls": [
    "https://feeds.bloomberg.com/markets/news.rss",
    "https://techcrunch.com/feed/"
  ],
  "max_entries": 10,
  "summary_length_chars": 500,
  "apply_tags": ["finance", "tech_trends"]
}
```

Outputs
- Consolidated feed entry collection and metadata.
- Structured daily digest summaries.
- Keyword-based entry tagging and classification.
- Feed availability and synchronization status.
