---
name: anysite-brand-reputation
description: Monitor brand reputation and sentiment across Twitter/X, Reddit, Instagram, YouTube, and LinkedIn using anysite MCP server. Track brand mentions, analyze customer sentiment, monitor social conversations, identify reputation issues, and measure brand health. Supports social media listening, sentiment analysis, mention tracking, and crisis detection. Use when users need to monitor brand mentions, track customer sentiment, identify reputation risks, analyze brand perception, or measure social media presence and brand health across platforms.
---

# anysite Brand Reputation Monitoring

Monitor and protect your brand reputation across social media platforms. Track mentions, analyze sentiment, and identify issues before they escalate.

## Overview

- **Track brand mentions** across social platforms
- **Analyze sentiment** (positive, negative, neutral)
- **Monitor conversations** about your brand
- **Identify reputation risks** and crisis signals
- **Measure brand health** over time

**Coverage**: 65% - Pivoted from review platforms to social media monitoring; strong for Twitter, Reddit, Instagram, YouTube, LinkedIn

## v2 Tool Interface

All data fetching uses the anysite MCP v2 universal meta-tools:

- **`execute(source, category, endpoint, params)`** — fetch data from any source. Returns first page + `cache_key`.
- **`get_page(cache_key, offset, limit)`** — paginate through results when `next_offset` is returned.
- **`query_cache(cache_key, conditions, sort_by, aggregate, group_by)`** — filter, sort, or aggregate cached data without new API calls.
- **`export_data(cache_key, format)`** — export full dataset as CSV, JSON, or JSONL for reports.

Always call `discover(source, category)` first if unsure about endpoint names or params.

### Error Handling

v2 responses may include `llm_hint` fields with guidance on how to fix errors (e.g., wrong URN format, missing params). Always check `llm_hint` in error responses before retrying.

## Supported Platforms

- **Twitter/X**: Real-time mentions, sentiment, viral content
- **Reddit**: Community discussions, detailed feedback, sentiment
- **Instagram**: Visual brand mentions, hashtag tracking, influencer posts
- **YouTube**: Video mentions, comment sentiment, brand coverage
- **LinkedIn**: Professional mentions, company updates, B2B sentiment

## Quick Start

**Step 1: Set Up Monitoring**

Define:
- Brand keywords (company name, product names, misspellings)
- Platforms to monitor (Twitter, Reddit, Instagram, etc.)
- Monitoring frequency (real-time, daily, weekly)
- Alert thresholds (negative sentiment, volume spikes)

**Step 2: Search for Mentions**

Platform searches:
```
Twitter:    execute("twitter", "search", "search_posts", {"query": "brand name", "count": 100})
Reddit:     execute("reddit", "search", "search_posts", {"query": "brand name", "count": 100})
Instagram:  execute("instagram", "search", "search_posts", {"query": "#brandname", "count": 100})
LinkedIn:   execute("linkedin", "post", "search_posts", {"keywords": "brand name", "count": 50})
```

Each call returns a `cache_key` — use it for pagination, filtering, and export.

**Step 3: Analyze Sentiment**

For each mention:
- Classify: Positive, negative, neutral
- Categorize: Complaint, praise, question, general
- Prioritize: Urgency, reach, influence

Use `query_cache(cache_key, conditions=[...], sort_by=...)` to filter high-engagement or negative mentions without re-fetching.

**Step 4: Take Action**

Based on findings:
- Respond to negative mentions
- Amplify positive feedback
- Address product issues
- Engage with community

## Common Workflows

### Workflow 1: Daily Brand Monitoring

**Scenario**: Monitor brand mentions across all platforms daily

**Steps**:

1. **Search All Platforms**
```
# Twitter (real-time pulse)
execute("twitter", "search", "search_posts", {"query": "brand name OR @brandhandle", "count": 100})
→ Returns cache_key_twitter; filter last 24h with from_date param (timestamp)

# Reddit (detailed discussions)
execute("reddit", "search", "search_posts", {"query": "brand name", "count": 50, "time_filter": "day"})
→ Returns cache_key_reddit

# Instagram (visual mentions)
execute("instagram", "search", "search_posts", {"query": "#brandname OR brand name", "count": 50})
→ Returns cache_key_instagram

# LinkedIn (professional mentions)
execute("linkedin", "post", "search_posts", {"keywords": "brand name", "count": 20})
→ Returns cache_key_linkedin

# YouTube (video coverage)
execute("youtube", "search", "search_videos", {"query": "brand name review OR brand name unboxing", "count": 20})
→ Returns cache_key_youtube
```

If any result includes `next_offset`, fetch more with:
```
get_page(cache_key, offset=next_offset, limit=50)
```

2. **Classify Mentions**

Use `query_cache` to sort and filter cached results:
```
# Find high-engagement mentions across platforms
query_cache(cache_key_twitter, sort_by=[{"field": "favorite_count", "order": "desc"}])
query_cache(cache_key_reddit, sort_by=[{"field": "vote_count", "order": "desc"}])

For each mention:

Sentiment:
- Positive: Praise, recommendation, satisfaction
- Negative: Complaint, criticism, problem
- Neutral: Question, general mention, factual

Category:
- Product feedback
- Customer service issue
- Feature request
- General discussion
- Competitor comparison
```

3. **Prioritize Issues**
```
High Priority:
- Negative + High reach (viral potential)
- Multiple complaints about same issue
- Influencer negative mention
- Legal/safety concerns

Medium Priority:
- Individual complaints
- Feature requests
- Questions
- General feedback

Low Priority:
- Positive mentions
- Neutral discussions
- General brand awareness
```

4. **Generate Daily Report**

Export data for reporting:
```
export_data(cache_key_twitter, "csv")
export_data(cache_key_reddit, "csv")
→ Returns download URLs for each dataset

Summary:
- Total mentions (by platform)
- Sentiment breakdown (% positive/negative/neutral)
- Top issues identified
- Viral/trending mentions
- Recommended actions
```

**Expected Output**:
- Daily mention count: 50-200
- Sentiment distribution
- Top 5 issues to address
- Action items for team

### Workflow 2: Crisis Detection and Management

**Scenario**: Identify and track potential PR crises

**Steps**:

1. **Monitor for Anomalies**
```
Track baseline:
- Average mentions per day
- Average sentiment score
- Typical engagement levels

Alert triggers:
- Mentions >2x baseline
- Negative sentiment >50%
- Viral negative content (high engagement)
```

2. **Deep Dive on Spikes**
```
When alert triggered:

execute("twitter", "search", "search_posts", {"query": "brand name", "count": 500})
→ Identify what's driving spike; use get_page() to load all results

execute("reddit", "search", "search_posts", {"query": "brand name", "count": 200})
→ Check community discussions

For viral posts:
  # Get specific Reddit post details and comments
  execute("reddit", "posts", "posts", {"post_url": "<reddit_post_url>"})
  execute("reddit", "posts", "posts_comments", {"post_url": "<reddit_post_url>"})
  → Analyze reach and engagement, read comments for context

  # For viral tweets, scrape the tweet URL directly
  execute("webparser", "parse", "parse", {"url": "<tweet_url>"})
  → Get tweet details and engagement metrics
```

3. **Assess Crisis Severity**
```
Severity factors:
- Volume (how many mentions)
- Velocity (how fast growing)
- Reach (influencer involvement, media coverage)
- Sentiment (how negative)
- Validity (legitimate issue vs. misunderstanding)

Use query_cache to analyze cached data:
query_cache(cache_key, aggregate=[{"function": "count"}])
→ Total mention count without re-fetching
```

4. **Track Crisis Evolution**
```
Hourly monitoring:
- Mention volume trend
- Sentiment shifts
- Platform spread
- Media pickup
- Official response impact
```

5. **Measure Resolution**
```
Track until:
- Volume returns to baseline
- Sentiment improves
- No new negative mentions for 24-48h
```

**Expected Output**:
- Crisis timeline
- Mention volume graph
- Sentiment tracking
- Key influencers/posts
- Response effectiveness

### Workflow 3: Competitive Reputation Benchmarking

**Scenario**: Compare brand sentiment vs. competitors

**Steps**:

1. **Define Competitors**
```
List 3-5 main competitors
```

2. **Gather Mentions for All**
```
For brand + each competitor:
  execute("twitter", "search", "search_posts", {"query": "<brand>", "count": 200})
  execute("reddit", "search", "search_posts", {"query": "<brand>", "count": 100})
  execute("linkedin", "post", "search_posts", {"keywords": "<brand>", "count": 50})

Each returns a cache_key — use get_page() if next_offset indicates more data.
```

3. **Calculate Brand Health Scores**
```
For each brand:

Use query_cache to aggregate metrics from cached results:
  query_cache(cache_key, aggregate=[{"function": "count"}])
  → Total mention volume

  query_cache(cache_key, aggregate=[{"function": "avg", "field": "favorite_count"}])
  → Average engagement per mention

Mention Volume: Total mentions
Sentiment Score: (Positive - Negative) / Total
Engagement Rate: Avg engagement per mention
Share of Voice: Your mentions / Total category mentions
```

4. **Analyze Strengths/Weaknesses**
```
Compare:
- What are competitors praised for?
- What are competitors criticized for?
- Where do we excel?
- Where do we fall short?
```

5. **Identify Opportunities**
```
Look for:
- Unmet customer needs (complaints about competitors)
- Messaging gaps (what they're not saying)
- Product differentiation opportunities
- Customer service advantages
```

**Expected Output**:
- Competitive sentiment matrix
- Brand health scores comparison
- Strength/weakness analysis
- Strategic opportunities

## MCP Tools Reference (v2)

### Twitter/X
- `execute("twitter", "search", "search_posts", {"query": ..., "count": N})` — Find brand mentions. Supports `from_date`, `to_date`, `min_likes`, `min_retweets`, `language` filters.
- `execute("twitter", "user", "user", {"user": ...})` — Check brand profile stats
- `execute("twitter", "user", "user_posts", {"user": ..., "count": N})` — Monitor brand account posts

### Reddit
- `execute("reddit", "search", "search_posts", {"query": ..., "count": N})` — Find discussions. Supports `sort` (relevance/hot/top/new) and `time_filter` (day/week/month/year).
- `execute("reddit", "posts", "posts", {"post_url": ...})` — Get post details and sentiment
- `execute("reddit", "posts", "posts_comments", {"post_url": ...})` — Deep dive on discussions

### Instagram
- `execute("instagram", "search", "search_posts", {"query": ..., "count": N})` — Find visual mentions
- `execute("instagram", "post", "post", {"post": ...})` — Analyze mention engagement
- `execute("instagram", "post", "post_comments", {"post": ..., "count": N})` — Read feedback

### YouTube
- `execute("youtube", "search", "search_videos", {"query": ..., "count": N})` — Find video mentions
- `execute("youtube", "video", "video", {"video": ...})` — Get video details
- `execute("youtube", "video", "video_comments", {"video": ..., "count": N})` — Analyze sentiment

### LinkedIn
- `execute("linkedin", "post", "search_posts", {"keywords": ..., "count": N})` — Professional mentions
- `execute("linkedin", "company", "company_posts", {"urn": {"type": "company", "value": "<id>"}, "count": N})` — Monitor own company posts. Requires company URN from `execute("linkedin", "company", "company", {"company": "<alias>"})`.

### Pagination, Caching & Export
- `get_page(cache_key, offset, limit)` — Load next page of results from any execute() call
- `query_cache(cache_key, conditions, sort_by, aggregate, group_by)` — Filter/sort/aggregate cached data without new API calls
- `export_data(cache_key, "csv"|"json"|"jsonl")` — Export full dataset as downloadable file

## Sentiment Analysis Framework

**Manual Sentiment Classification**:

**Positive Indicators**:
- "Love", "great", "amazing", "best"
- Recommendations ("highly recommend")
- Repeat purchase ("buying again")
- Comparisons ("better than X")

**Negative Indicators**:
- "Disappointed", "worst", "terrible", "awful"
- Problems ("doesn't work", "broken")
- Comparisons ("X is better")
- Demands ("need refund", "fix this")

**Neutral Indicators**:
- Questions without sentiment
- Factual statements
- General mentions
- Informational content

**Sentiment Score**:
```
Score = (Positive mentions - Negative mentions) / Total mentions x 100

+50 to +100: Excellent
+20 to +49: Good
-19 to +19: Neutral/Mixed
-20 to -49: Poor
-50 to -100: Critical
```

## Monitoring Metrics

**Volume Metrics**:
- Total mentions per day/week/month
- Mentions by platform
- Trend over time

**Sentiment Metrics**:
- Sentiment distribution (% positive/negative/neutral)
- Sentiment score (net promoter style)
- Sentiment trend over time

**Engagement Metrics**:
- Average likes/shares per mention
- Viral mentions (>1000 engagements)
- Influencer mentions

**Issue Tracking**:
- Top complaints (by frequency)
- Product/service issues mentioned
- Feature requests
- Customer service mentions

## Output Formats

**Chat Summary**:
- Daily mention highlights
- Sentiment overview
- Top issues identified
- Recommended actions

**CSV Export** (via `export_data(cache_key, "csv")`):
- Mention list with sentiment
- Platform, date, reach
- Issue categorization

**JSON Export** (via `export_data(cache_key, "json")`):
- Complete mention data
- Time-series sentiment
- Engagement metrics

## Reference Documentation

- **[MONITORING_GUIDE.md](references/MONITORING_GUIDE.md)** - Best practices for brand monitoring, crisis response protocols, and sentiment analysis techniques

---

**Ready to monitor your brand?** Ask Claude to help you track mentions, analyze sentiment, or identify reputation risks across social platforms!
