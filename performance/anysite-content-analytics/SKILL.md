---
name: anysite-content-analytics
description: Track and analyze content performance across Instagram, YouTube, LinkedIn, Twitter/X, and Reddit using anysite MCP server. Measure engagement metrics, analyze post effectiveness, benchmark content strategy, identify top-performing content, and optimize posting strategies. Use when users need to measure content ROI, optimize social strategy, identify viral content patterns, or analyze content engagement across platforms.
---

# anysite Content Analytics

Measure and optimize content performance across social platforms using anysite MCP. Track engagement, identify top performers, and refine your content strategy.

## Overview

- **Track post performance** across Instagram, YouTube, LinkedIn, Twitter/X
- **Analyze engagement metrics** (likes, comments, shares, views)
- **Identify top content** and viral patterns
- **Benchmark against competitors** for strategy insights
- **Optimize posting strategy** based on data

**Coverage**: 80% - Strong for Instagram, YouTube, LinkedIn, Twitter, Reddit

## Supported Platforms

- ✅ **Instagram**: Posts, Reels, likes, comments, engagement rates
- ✅ **YouTube**: Videos, views, likes, comments, watch time indicators
- ✅ **LinkedIn**: Posts, articles, reactions, comments, shares
- ✅ **Twitter/X**: Tweets, retweets, likes, replies
- ✅ **Reddit**: Posts, upvotes, comments, awards

## v2 Tool Interface

All data fetching uses the anysite MCP v2 universal meta-tools:

- **`execute(source, category, endpoint, params)`** - Fetch data from any source. Returns first page + `cache_key`.
- **`get_page(cache_key, offset, limit)`** - Load more items from a previous execute() when `next_offset` is returned.
- **`query_cache(cache_key, conditions?, sort_by?, aggregate?, group_by?)`** - Filter, sort, and aggregate cached data without new API calls.
- **`export_data(cache_key, format)`** - Export full dataset as CSV, JSON, or JSONL. Returns a download URL.

### Error Handling

v2 responses may include `llm_hint` fields with guidance on how to resolve errors. Common patterns:
- **412**: Entity not found - verify the identifier (username, URN, URL).
- **422**: Invalid parameter format - check URN prefix format or param types.
- Always check `llm_hint` in error responses for specific resolution steps.

## Quick Start

**Step 1: Collect Content Data**

Platform-specific:
- Instagram: `execute("instagram", "user", "user_posts", {"user": "username", "count": 50})`
- LinkedIn: `execute("linkedin", "user", "user_posts", {"urn": "fsd_profile:ACoAAA...", "count": 50})`
- Twitter: `execute("twitter", "user", "user_posts", {"user": "username", "count": 100})`
- YouTube: `execute("youtube", "channel", "channel_videos", {"channel": "channel_id", "count": 30})`

**Step 2: Analyze Engagement**

Use `query_cache()` on the returned `cache_key` to analyze without re-fetching:
```
query_cache(cache_key, sort_by="likes desc", aggregate="avg:likes,comments")
```

Calculate metrics:
- Engagement rate: (likes + comments + shares) / followers
- Best performing content: Top 10% by engagement
- Content types: Video vs. image vs. text
- Posting frequency: Posts per week

**Step 3: Identify Patterns**

Look for:
- Best posting times (day of week, time)
- Top-performing topics/themes
- Optimal content length
- High-engagement formats

**Step 4: Optimize Strategy**

Based on findings:
- Double down on top content types
- Post more during peak engagement times
- Replicate successful topics
- Adjust content mix

**Step 5: Export Results**

```
export_data(cache_key, "csv")
```

Returns a download URL for the full dataset.

## Common Workflows

### Workflow 1: Instagram Content Audit

**Steps**:

1. **Get All Posts**
```
execute("instagram", "user", "user_posts", {"user": "username", "count": 100})
→ returns cache_key + first page of results
```

If more posts exist (response includes `next_offset`):
```
get_page(cache_key, offset=next_offset, limit=50)
```

2. **Calculate Metrics**
```
For each post:
- Engagement rate = (likes + comments) / follower_count
- Engagement per hour = engagement / hours_since_posted
- Content type (Reel, carousel, single image, video)
```

Use `query_cache` to sort and filter:
```
query_cache(cache_key, sort_by="likes desc", aggregate="avg:likes,comments")
```

3. **Identify Top Performers**
```
query_cache(cache_key, sort_by="likes desc")

Top 10%: Analyze for common patterns
- Topics/themes
- Visual style
- Caption style and length
- Hashtag strategy
```

4. **Analyze Content Mix**
```
query_cache(cache_key, group_by="type", aggregate="count:id,avg:likes,avg:comments")

Results show:
- Reels: X% of posts, Y% of engagement
- Carousels: X% of posts, Y% of engagement
- Single images: X% of posts, Y% of engagement
```

5. **Benchmark Against Competitors**
```
For each competitor:
  execute("instagram", "user", "user_posts", {"user": "competitor", "count": 50})
Compare:
- Posting frequency
- Engagement rates
- Content types
- Top themes
```

6. **Export Results**
```
export_data(cache_key, "csv")
```

**Expected Output**:
- Content performance report
- Top 10 performing posts
- Content type effectiveness
- Posting frequency analysis
- Competitive benchmark

### Workflow 2: LinkedIn Content Strategy Analysis

**Steps**:

1. **Collect Post History**
```
execute("linkedin", "user", "user_posts", {"urn": "fsd_profile:ACoAAA...", "count": 100})
→ returns cache_key + first page
```

For company page posts:
```
execute("linkedin", "company", "company_posts", {"urn": {"type": "company", "value": "1441"}, "count": 100})
```

Use `get_page(cache_key, offset, limit)` if more posts exist.

2. **Categorize Content**
```
Group by type:
- Text-only posts
- Image posts
- Video posts
- Article shares
- LinkedIn articles
- Polls
```

3. **Analyze Engagement by Type**
```
query_cache(cache_key, aggregate="avg:comment_count,avg:share_count", group_by="type")

For each content type:
- Average reactions
- Average comments
- Average shares
- Engagement rate
```

4. **Topic Analysis**
```
Extract themes from top posts:
- Industry insights
- Personal stories
- How-to/educational
- Company news
- Thought leadership
```

5. **Posting Timing Analysis**
```
Group posts by:
- Day of week
- Time of day
Calculate average engagement for each group
```

**Expected Output**:
- Best content types for engagement
- Top topics by engagement
- Optimal posting times
- Content frequency recommendations

### Workflow 3: YouTube Channel Performance Analysis

**Steps**:

1. **Get Channel Videos**
```
execute("youtube", "channel", "channel_videos", {"channel": "channel_id", "count": 50})
→ returns cache_key + first page
```

Use `get_page(cache_key, offset, limit)` for additional videos.

2. **Analyze Each Video**
```
For each video:
  execute("youtube", "video", "video", {"video": "video_id"})

Metrics:
- Views
- Likes/dislikes
- Comments
- View velocity (views per day since upload)
```

3. **Identify Patterns**
```
query_cache(cache_key, sort_by="views desc")

Analyze top 20% by views:
- Video length
- Titles (keywords, style)
- Thumbnail patterns
- Topics/themes
- Upload timing
```

4. **Engagement Analysis**
```
Check comments:
  execute("youtube", "video", "video_comments", {"video": "video_id", "count": 100})

Analyze:
- Comment quality
- Questions asked
- Sentiment
- Engagement timing
```

5. **Content Mix Optimization**
```
Compare:
- Long-form (>10 min) vs short (<5 min)
- Tutorial vs entertainment vs review
- Series vs one-offs
```

**Expected Output**:
- Video performance rankings
- Optimal video length
- Best topics and formats
- Title and thumbnail insights
- Upload strategy recommendations

## MCP Tools Reference (v2)

### Instagram
- `execute("instagram", "user", "user_posts", {"user": username, "count": N})` - Get posts with engagement
- `execute("instagram", "post", "post", {"post": post_id})` - Get detailed post metrics
- `execute("instagram", "post", "post_likes", {"post": post_id, "count": N})` - Analyze likers
- `execute("instagram", "post", "post_comments", {"post": post_id, "count": N})` - Get comments

### LinkedIn
- `execute("linkedin", "user", "user_posts", {"urn": "fsd_profile:ACoAAA...", "count": N})` - Get user post history
- `execute("linkedin", "company", "company_posts", {"urn": {"type": "company", "value": "ID"}, "count": N})` - Company page posts

### Twitter/X
- `execute("twitter", "user", "user_posts", {"user": username, "count": N})` - Get tweets
- `execute("twitter", "search", "search_posts", {"query": query, "count": N})` - Find trending tweets

### YouTube
- `execute("youtube", "channel", "channel_videos", {"channel": channel, "count": N})` - All videos
- `execute("youtube", "video", "video", {"video": video_id})` - Video details and metrics
- `execute("youtube", "video", "video_comments", {"video": video_id, "count": N})` - Comments

### Reddit
- `execute("reddit", "user", "user_posts", {"username": username, "count": N})` - User's posts
- `execute("reddit", "search", "search_posts", {"query": query, "count": N})` - Find popular posts

### Pagination & Analysis
- `get_page(cache_key, offset, limit)` - Fetch next page of results from any execute() call
- `query_cache(cache_key, conditions?, sort_by?, aggregate?, group_by?)` - Filter/sort/aggregate cached results
- `export_data(cache_key, "csv"|"json"|"jsonl")` - Export dataset as downloadable file

## Key Metrics

**Engagement Rate**:
- Formula: (Likes + Comments + Shares) / Followers x 100
- Instagram benchmark: 3-6%
- LinkedIn benchmark: 2-5% of connections
- Twitter benchmark: 0.5-1%

**Content Performance Score**:
```
Score = (Engagement Rate x 40) +
        (Comments/Likes Ratio x 30) +
        (Share Rate x 30)
```

**Viral Potential Indicators**:
- Engagement rate >2x average
- High share rate (>5% of engagement)
- Rapid engagement velocity (50% within 24h)
- Quality comments (questions, discussions)

## Output Formats

**Chat Summary**:
- Top 5 performing posts
- Key insights and patterns
- Recommendations for optimization

**CSV Export** (via `export_data(cache_key, "csv")`):
- Post URL, date, type
- Likes, comments, shares
- Engagement rate
- Performance rank

**JSON Export** (via `export_data(cache_key, "json")`):
- Full post data with metadata
- Time-series engagement data
- Historical trends

## Reference Documentation

- **[METRICS_GUIDE.md](references/METRICS_GUIDE.md)** - Detailed metrics definitions, calculation formulas, and benchmarks

---

**Ready to analyze content?** Ask Claude to help you track performance, identify top content, or optimize your posting strategy!
