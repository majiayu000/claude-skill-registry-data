---
name: anysite-trend-analysis
description: Discover and track emerging trends across Twitter/X, Reddit, YouTube, LinkedIn, and Instagram using anysite MCP server. Identify viral content, monitor topic momentum, detect trending hashtags, analyze search patterns, and track industry shifts. Supports multi-platform trend detection, sentiment analysis, and momentum tracking. Use when users need to identify emerging trends, track viral content, monitor market shifts, discover trending topics, or analyze social media conversations for strategic insights.
---

# anysite Trend Analysis

Discover emerging trends and track viral content across social platforms using anysite MCP. Identify what's gaining momentum before it peaks.

## Overview

- **Detect emerging trends** across multiple platforms
- **Track viral content** and identify breakout topics
- **Monitor hashtag performance** and trending keywords
- **Analyze topic momentum** and growth patterns
- **Identify market shifts** through social listening

**Coverage**: 75% - Good for Twitter, Reddit, YouTube, LinkedIn, Instagram

## Supported Platforms

- **Twitter/X**: Trending topics, viral tweets, hashtag tracking
- **Reddit**: Trending posts, subreddit activity, upvote velocity
- **YouTube**: Trending videos, search trends, rising channels
- **LinkedIn**: Professional trends, industry discussions
- **Instagram**: Trending hashtags, viral content

## v2 Tool Interface

All data fetching uses the universal `execute()` meta-tool. Always call `discover(source, category)` first if you need to verify endpoint names or available parameters.

**Core tools**:
- `execute(source, category, endpoint, params)` - Fetch data. Returns first page + `cache_key`.
- `get_page(cache_key, offset, limit)` - Load more results from a previous execute.
- `query_cache(cache_key, conditions, sort_by, aggregate, group_by)` - Filter, sort, or aggregate cached data without new API calls.
- `export_data(cache_key, format)` - Export full dataset as CSV, JSON, or JSONL.

**Error handling**: If execute() returns an error with `llm_hint`, follow the hint to fix the request (e.g., correcting a parameter name or adjusting the query).

## Quick Start

**Step 1: Search for Trending Content**

By platform:
- Twitter: `execute("twitter", "search", "search_tweets", {"query": "<topic>", "count": 100})` sorted by engagement
- Reddit: `execute("reddit", "search", "search", {"query": "<topic>"})` sorted by upvotes
- YouTube: `execute("youtube", "search", "search_videos", {"query": "<topic>", "count": 50})` by recent
- LinkedIn: `execute("linkedin", "post", "search_posts", {"keywords": "<topic>"})` by engagement
- Instagram: `execute("instagram", "search", "search_users", {"query": "<topic>"})` for hashtag/topic discovery

**Step 2: Analyze Momentum**

Use `query_cache()` to filter and sort cached results:
```
query_cache(cache_key, sort_by="engagement_desc", conditions=[{"field": "date", "op": ">", "value": "2024-01-01"}])
```

Check indicators:
- Engagement velocity (growth rate)
- Cross-platform presence
- Comment volume and sentiment
- Share/retweet patterns

**Step 3: Track Over Time**

Monitor changes:
- Daily engagement growth
- New platform adoption
- Mainstream vs. niche spread
- Peak timing prediction

**Step 4: Report Insights**

Use `export_data(cache_key, "csv")` to generate downloadable reports.

Deliver:
- Trending topics list
- Momentum indicators
- Strategic recommendations
- Early warnings or opportunities

## Common Workflows

### Workflow 1: Multi-Platform Trend Detection

**Scenario**: Identify what's trending in tech/AI space

**Steps**:

1. **Search Across Platforms**
```
# Twitter
execute("twitter", "search", "search_tweets", {"query": "AI OR artificial intelligence", "count": 100})
→ Filter for: Posted within 24-48h, high engagement
→ Save cache_key as twitter_cache

# Reddit
execute("reddit", "search", "search", {"query": "artificial intelligence"})
→ Filter: r/technology, r/MachineLearning, r/singularity
→ Save cache_key as reddit_cache

# YouTube
execute("youtube", "search", "search_videos", {"query": "AI news", "count": 50})
→ Filter: Published this week, views >10k
→ Save cache_key as youtube_cache

# LinkedIn
execute("linkedin", "post", "search_posts", {"keywords": "artificial intelligence"})
→ Filter: High engagement, recent
→ Save cache_key as linkedin_cache
```

2. **Use query_cache to Filter Results**
```
# Filter Twitter for high-engagement posts
query_cache(twitter_cache, sort_by="engagement_desc", conditions=[{"field": "likes", "op": ">", "value": 100}])

# Filter Reddit for specific subreddits
query_cache(reddit_cache, conditions=[{"field": "subreddit", "op": "contains", "value": "technology"}])

# Aggregate YouTube view counts
query_cache(youtube_cache, aggregate={"field": "views", "op": "avg"})
```

3. **Load More Results if Needed**
```
# If execute() returned next_offset, paginate
get_page(twitter_cache, offset=10, limit=50)
get_page(reddit_cache, offset=10, limit=50)
```

4. **Extract Common Themes**
```
Analyze content for recurring:
- Keywords and phrases
- Company/product mentions
- Events or announcements
- Questions or concerns
```

5. **Calculate Trend Score**
```
For each theme:
- Platform count (how many platforms)
- Total engagement
- Growth velocity
- Sentiment distribution
```

6. **Identify Breakout Trends**
```
Trends with:
- Presence on 3+ platforms
- Engagement growing >50% daily
- Positive or controversial sentiment
- Coverage by influencers/media
```

**Expected Output**:
- Top 5-10 trending themes
- Platform-by-platform breakdown
- Momentum indicators
- Strategic implications

### Workflow 2: Hashtag Performance Tracking

**Scenario**: Monitor hashtag growth and adoption

**Steps**:

1. **Search by Hashtag**
```
# Instagram - discover users/content around the hashtag
execute("instagram", "search", "search_users", {"query": "sustainability"})
→ Save cache_key as ig_cache

# Twitter
execute("twitter", "search", "search_tweets", {"query": "#sustainability", "count": 100})
→ Track tweet volume over time
→ Save cache_key as tw_cache

# LinkedIn
execute("linkedin", "post", "search_posts", {"keywords": "sustainability"})
→ Check professional adoption
→ Save cache_key as li_cache
```

2. **Calculate Velocity with query_cache**
```
# Sort by recency and engagement
query_cache(tw_cache, sort_by="date_desc")
query_cache(ig_cache, sort_by="followers_desc")

Hashtag velocity:
- Posts in last 24h vs. previous 24h
- Engagement rate change
- New accounts using hashtag
- Geographic spread
```

3. **Analyze Content Evolution**
```
Compare early vs. recent posts:
- Topic shifts
- Audience changes
- Influencer involvement
- Commercial adoption
```

4. **Export Results**
```
export_data(tw_cache, "csv")
export_data(ig_cache, "json")
→ Share downloadable reports
```

5. **Predict Peak**
```
Based on growth curve:
- Early stage (accelerating)
- Peak stage (plateauing)
- Decline stage (slowing)
```

**Expected Output**:
- Hashtag performance report
- Growth trajectory
- Peak timing estimate
- Strategic recommendations

### Workflow 3: Reddit Trend Mining

**Scenario**: Find emerging discussions in specific communities

**Steps**:

1. **Search Target Subreddits**
```
execute("reddit", "posts", "get", {"subreddit": "technology"})
→ Get top posts from last week
→ Save cache_key as reddit_tech_cache
```

2. **Analyze Post Momentum**
```
# Sort cached posts by engagement
query_cache(reddit_tech_cache, sort_by="upvotes_desc")

# Aggregate engagement metrics
query_cache(reddit_tech_cache, aggregate={"field": "upvotes", "op": "avg"})

For each high-momentum post:
  execute("reddit", "search", "search", {"query": "<post topic>"})
  → Deeper analysis

Calculate:
- Upvotes per hour
- Comment velocity
- Award count
- Controversial score
```

3. **Extract Discussion Themes**
```
From high-momentum posts:
- What problems are discussed?
- What solutions are proposed?
- What companies/products mentioned?
- What sentiment (positive, negative, concerned)?
```

4. **Track Cross-Pollination**
```
Check if trending Reddit topics appear on:
- Twitter: execute("twitter", "search", "search_tweets", {"query": "<topic>"})
- LinkedIn: execute("linkedin", "post", "search_posts", {"keywords": "<topic>"})
- YouTube: execute("youtube", "search", "search_videos", {"query": "<topic>"})
```

**Expected Output**:
- Top Reddit trends
- Community sentiment
- Mainstream potential
- Early mover opportunities

## MCP Tools Reference (v2)

### Twitter/X
- `execute("twitter", "search", "search_tweets", {"query": ..., "count": N})` - Find tweets, filter by engagement
- `execute("twitter", "user", "get", {"username": ...})` - Check influencer adoption

### Reddit
- `execute("reddit", "search", "search", {"query": ...,})` - Find discussions
- `execute("reddit", "posts", "get", {"subreddit": ...})` - Get subreddit posts and momentum
- `execute("reddit", "user", "get", {"username": ...})` - Get user details

### YouTube
- `execute("youtube", "search", "search_videos", {"query": ..., "count": N})` - Find trending videos
- `execute("youtube", "video", "video", {"video": ...})` - Track view velocity
- `execute("youtube", "video", "video_comments", {"video": ..., "count": N})` - Gauge interest

### LinkedIn
- `execute("linkedin", "post", "search_posts", {"keywords": ...})` - Professional trends
- `execute("linkedin", "company", "get", {"company": ...})` - Company details

### Instagram
- `execute("instagram", "search", "search_users", {"query": ...})` - Discover users/hashtags
- `execute("instagram", "post", "post", {"post": ...})` - Engagement metrics

### Pagination & Analysis
- `get_page(cache_key, offset, limit)` - Load additional results from any execute() call
- `query_cache(cache_key, conditions, sort_by, aggregate, group_by)` - Filter, sort, aggregate cached data
- `export_data(cache_key, "csv"|"json"|"jsonl")` - Export datasets for reporting

## Trend Identification Framework

**Trend Stages**:

1. **Emergence** (0-20% awareness)
   - Niche communities discussing
   - Low but accelerating engagement
   - Early adopters experimenting
   - Action: Monitor closely, prepare strategy

2. **Growth** (20-50% awareness)
   - Crossing into mainstream platforms
   - Rapid engagement growth
   - Influencer adoption
   - Action: Create content, engage actively

3. **Peak** (50-80% awareness)
   - Maximum visibility
   - Slowing growth rate
   - Saturation approaching
   - Action: Maximize presence before decline

4. **Decline** (80-100% awareness)
   - Engagement decreasing
   - Moving to "background noise"
   - New trends emerging
   - Action: Shift focus to next trend

**Momentum Indicators**:
- **Volume**: Mentions per day
- **Velocity**: Growth rate (% change)
- **Reach**: Unique accounts discussing
- **Spread**: Number of platforms
- **Sentiment**: Positive/negative ratio
- **Influence**: Key accounts involved

## Output Formats

**Chat Summary**:
- Top 5 trends with momentum scores
- Platform breakdown
- Strategic recommendations

**CSV Export** (via `export_data(cache_key, "csv")`):
- Trend name, platforms, volume
- Growth rate, sentiment
- Key influencers mentioning

**JSON Export** (via `export_data(cache_key, "json")`):
- Complete trend data
- Time-series metrics
- Cross-platform correlations

## Reference Documentation

- **[SOCIAL_MONITORING.md](references/SOCIAL_MONITORING.md)** - Social listening techniques, monitoring strategies, and trend prediction methods

---

**Ready to discover trends?** Ask Claude to help you identify emerging topics, track viral content, or monitor market shifts across social platforms!
