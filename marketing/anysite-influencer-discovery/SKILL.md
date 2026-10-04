---
name: anysite-influencer-discovery
description: Discover and analyze influencers across Instagram, Twitter/X, LinkedIn, YouTube, and Reddit using anysite MCP server. Find content creators by niche, analyze engagement metrics, evaluate audience quality, track influencer activity, and identify partnership opportunities. Supports multi-platform influencer search, profile enrichment, follower analysis, and engagement tracking. Use when users need to find brand ambassadors, research content creators, identify thought leaders, build influencer lists, or evaluate influencer partnerships for marketing campaigns.
---

# anysite Influencer Discovery

Find and analyze influencers across social platforms using anysite MCP. Discover content creators, evaluate their reach and engagement, and identify partnership opportunities.

## Overview

- **Discover influencers** across Instagram, Twitter, LinkedIn, YouTube
- **Analyze engagement** and audience quality
- **Track activity** and content patterns
- **Evaluate partnership fit** based on niche and metrics
- **Build influencer lists** with contact information

**Coverage**: 85% - Excellent for Instagram, Twitter, LinkedIn, YouTube influencers.

## v2 Tool Interface

All data fetching uses the anysite v2 meta-tools:

- **execute(source, category, endpoint, params)** - Fetch data. Returns first page + `cache_key`.
- **get_page(cache_key, offset, limit)** - Load more items from a previous execute (when `next_offset` is returned).
- **query_cache(cache_key, conditions, sort_by, aggregate, group_by)** - Filter, sort, or aggregate cached data without new API calls.
- **export_data(cache_key, format)** - Export full dataset as CSV, JSON, or JSONL. Returns a download URL.

**Error handling**: Check responses for `llm_hint` fields that provide actionable guidance on failures (e.g., alias not found, URN required).

## Supported Platforms

- ✅ **Instagram**: Profile stats, posts, followers, engagement, Reels
- ✅ **Twitter/X**: User search, followers, tweets, engagement
- ✅ **LinkedIn**: B2B influencers, thought leaders, professional content
- ✅ **YouTube**: Channel search, subscribers, views, video performance
- ✅ **Reddit**: Community influencers, karma, post quality

## Quick Start

**Step 1: Search for Influencers**

By platform:
- Instagram: `execute("instagram", "search", "search_posts", {"query": "niche keywords", "count": 50})` with niche keywords + hashtags
- Twitter: `execute("twitter", "search", "search_users", {"query": "niche keywords", "count": 50})` with niche keywords
- LinkedIn: `execute("linkedin", "search", "search_users", {"keywords": "industry thought leader", "count": 50})` with industry + "thought leader"
- YouTube: `execute("youtube", "search", "search_videos", {"query": "niche", "count": 50})` with niche, then analyze channels

**Step 2: Analyze Profiles**

Get detailed metrics:
- Instagram: `execute("instagram", "user", "user", {"user": "username"})` -> followers, posts, engagement rate
- Twitter: `execute("twitter", "user", "get", {"username": "handle"})` -> followers, tweet frequency
- YouTube: `execute("youtube", "channel", "channel_videos", {"channel": "...", "count": 30})` -> subscribers, views, growth
- LinkedIn: `execute("linkedin", "user", "user", {"user": "alias"})` -> connections, post engagement

**Step 3: Evaluate Engagement**

Check engagement quality:
- Post likes, comments, shares
- Engagement rate (engagement / followers)
- Audience authenticity (comment quality)
- Content consistency (posts per week)

Use `query_cache(cache_key, sort_by=[{"field": "like_count", "order": "desc"}])` to rank posts by engagement without re-fetching.

**Step 4: Build Influencer List**

Export with `export_data(cache_key, "csv")`:
- Name, handle, platform
- Follower count, engagement rate
- Niche/topics, content type
- Contact info (if available)
- Partnership fit score

## Common Workflows

### Workflow 1: Instagram Influencer Discovery

**Scenario**: Find Instagram influencers in sustainable fashion (10k-100k followers)

**Steps**:

1. **Search by Hashtag/Keywords**
```
execute("instagram", "search", "search_posts", {
  "query": "sustainable fashion OR eco friendly fashion",
  "count": 100
})
-> Extract unique user handles from results
-> Use get_page(cache_key, offset, 50) if next_offset returned for more results
```

2. **Analyze Each Creator**
```
For each unique handle:
  execute("instagram", "user", "user", {"user": "username"})
  -> Follower count, bio, profile type

Filter for:
- 10k-100k followers
- Business/Creator account
- Bio mentioning sustainability
```

3. **Evaluate Content**
```
For qualified creators:
  execute("instagram", "user", "user_posts", {"user": "username", "count": 30})

Analyze:
- Post frequency (consistency)
- Engagement rate per post
- Content quality and style
- Brand partnerships visible

Use query_cache(cache_key, sort_by=[{"field": "like_count", "order": "desc"}]) to find top posts
Use query_cache(cache_key, aggregate=[{"field": "like_count", "function": "avg"}]) for average engagement
```

4. **Check Audience Quality**
```
execute("instagram", "post", "post_likes", {"post": "post_id", "count": 100})
execute("instagram", "post", "post_comments", {"post": "post_id", "count": 50})

Look for:
- Real comments (not just emojis)
- Engaged community (questions, discussions)
- Geographic relevance
```

5. **Get Contact Information**
```
From Instagram bio:
- Email addresses
- Website links

If LinkedIn mentioned:
  execute("linkedin", "search", "search_users", {"keywords": "first_name last_name"})
  execute("linkedin", "user", "user", {"user": "alias_from_search"})
```

**Expected Output**:
- 20-40 qualified influencers
- Engagement metrics for each
- Contact information for 60-70%
- Partnership fit scores

Use `export_data(cache_key, "csv")` to generate a downloadable influencer list.

### Workflow 2: LinkedIn Thought Leader Identification

**Scenario**: Find B2B thought leaders in SaaS/sales

**Steps**:

1. **Search for Active Posters**
```
execute("linkedin", "search", "search_users", {
  "keywords": "SaaS sales thought leader",
  "title": "VP Sales OR Head of Sales OR Chief Revenue Officer",
  "count": 100
})
```

2. **Analyze Post Activity**
```
For each candidate:
  execute("linkedin", "post", "get_user_posts", {"user": "urn", "count": 50})

Filter for:
- Posts 2-3x per week minimum
- High engagement (100+ reactions)
- Original content (not just shares)

Use query_cache(cache_key, conditions=[{"field": "comment_count", "operator": ">", "value": 10}])
to filter for high-engagement posts
```

3. **Evaluate Influence**
```
Check post engagement:
- Average reactions per post
- Comment quality and quantity
- Share count
- Follower growth signals

Use query_cache(cache_key, aggregate=[
  {"field": "comment_count", "function": "avg"},
  {"field": "share_count", "function": "avg"}
]) for average metrics
```

4. **Assess Content Quality**
```
Review posts for:
- Expertise demonstration
- Original insights
- Engagement with comments
- Consistency of messaging
```

**Expected Output**:
- 15-25 active thought leaders
- Content themes and topics
- Engagement metrics
- Partnership opportunities (guest posts, quotes, etc.)

Use `export_data(cache_key, "csv")` to export the thought leader list.

### Workflow 3: YouTube Creator Research

**Scenario**: Find YouTube creators in tech reviews

**Steps**:

1. **Search for Niche Content**
```
execute("youtube", "search", "search_videos", {
  "query": "tech review 2026",
  "count": 100
})
-> Extract unique channel names
-> Use get_page(cache_key, offset, 50) if more results needed
```

2. **Analyze Channels**
```
For each channel:
  execute("youtube", "channel", "channel_videos", {"channel": "channel_id", "count": 30})

Check:
- Subscriber count
- Upload frequency
- Average views per video
- Video length (long-form vs shorts)

Use query_cache(cache_key, aggregate=[{"field": "view_count", "function": "avg"}]) for average views
```

3. **Evaluate Video Performance**
```
For top videos:
  execute("youtube", "video", "video", {"video": "video_id"})

Metrics:
- View count
- Like/dislike ratio
- Comments count
- Watch time signals (retention)
```

4. **Analyze Audience Engagement**
```
execute("youtube", "video", "video_comments", {"video": "video_id", "count": 100})

Look for:
- Active community
- Technical discussions
- Purchase decisions influenced
```

**Expected Output**:
- 10-20 relevant channels
- Subscriber and view metrics
- Engagement analysis
- Partnership fit assessment

Use `export_data(cache_key, "csv")` to export channel data.

## MCP Tools Reference (v2)

### Instagram
- `execute("instagram", "search", "search_posts", {"query": ..., "count": N})` - Find posts by keywords/hashtags
- `execute("instagram", "user", "user", {"user": ...})` - Get profile with followers, bio
- `execute("instagram", "user", "user_posts", {"user": ..., "count": N})` - Get recent posts with engagement
- `execute("instagram", "post", "post_likes", {"post": ..., "count": N})` - Check audience authenticity
- `execute("instagram", "post", "post_comments", {"post": ..., "count": N})` - Analyze engagement quality
- `execute("instagram", "user", "user_friendships", {"user": ..., "count": N, "type": "followers"})` - Get followers list (for analysis)

### Twitter/X
- `execute("twitter", "search", "search_users", {"query": ..., "count": N})` - Find users by keywords/bio
- `execute("twitter", "user", "get", {"username": ...})` - Get profile with followers, tweets
- `execute("twitter", "user_tweets", "get", {"username": ...})` - Get recent tweets with engagement
- `execute("twitter", "search", "search_posts", {"query": ..., "count": N})` - Find influential tweets in niche

### LinkedIn
- `execute("linkedin", "search", "search_users", {"keywords": ..., "count": N})` - Find professionals by keywords/title
- `execute("linkedin", "user", "user", {"user": ...})` - Get complete profile (includes skills with `with_skills: true`)
- `execute("linkedin", "post", "get_user_posts", {"user": "urn", "count": N})` - Get post history and engagement
- `execute("linkedin", "user", "user_skills", {"urn": ..., "count": N})` - Verify expertise (requires URN from profile)

Note: LinkedIn connection count is returned in the profile response (`connection_count` field). No separate endpoint needed.

### YouTube
- `execute("youtube", "search", "search_videos", {"query": ..., "count": N})` - Find videos by keywords
- `execute("youtube", "channel", "channel_videos", {"channel": ..., "count": N})` - Get all videos from channel
- `execute("youtube", "video", "video", {"video": ...})` - Get video metrics (views, likes)
- `execute("youtube", "video", "video_comments", {"video": ..., "count": N})` - Analyze audience engagement

### Reddit
- `execute("reddit", "search", "search_posts", {"query": ..., "count": N})` - Find influential posts in subreddits
- `execute("reddit", "user", "user_posts", {"username": ..., "count": N})` - Get user's post history
- `execute("reddit", "user", "user_comments", {"username": ..., "count": N})` - Analyze community engagement

### Web Scraping
- `execute("webparser", "parse", "parse", {"url": ...})` - Scrape any webpage for contact info, media kits, etc.

### Pagination, Caching & Export
- `get_page(cache_key, offset, limit)` - Fetch additional pages from any execute() result
- `query_cache(cache_key, conditions, sort_by, aggregate, group_by)` - Filter/sort/aggregate cached data
- `export_data(cache_key, "csv"|"json"|"jsonl")` - Export full dataset as downloadable file

## Output Formats

**Chat Summary**:
- Top 10 influencers with key metrics
- Engagement rate comparison
- Partnership recommendations
- Contact information found

**CSV Export** (via `export_data(cache_key, "csv")`):
- Influencer name, handle, platform
- Followers, engagement rate
- Niche, content type
- Email, website
- Fit score (1-100)

**JSON Export** (via `export_data(cache_key, "json")`):
- Complete profile data
- All posts with engagement
- Audience demographics (if available)
- Historical metrics

## Influencer Evaluation Framework

### Reach Metrics
- **Followers**: Total audience size
- **Views**: Average content views
- **Growth**: Follower growth rate

### Engagement Metrics
- **Rate**: Engagement / Followers
- **Quality**: Comment depth and relevance
- **Consistency**: Regular engagement patterns

### Authenticity Indicators
- **Audience Quality**: Real vs. fake followers
- **Comment Quality**: Meaningful discussions
- **Growth Pattern**: Organic vs. purchased
- **Engagement Distribution**: Consistent vs. spiky

### Content Quality
- **Production Value**: Visual/audio quality
- **Originality**: Unique vs. repurposed
- **Consistency**: Regular posting schedule
- **Niche Alignment**: On-brand content

### Partnership Fit
- **Audience Overlap**: Match with target market
- **Brand Alignment**: Values and messaging
- **Professionalism**: Past partnerships, disclosure
- **Availability**: Contact information, responsiveness

## Advanced Features

### Micro-Influencer Strategy

Focus on 10k-50k followers for higher engagement:
```
Benefits:
- Higher engagement rates (5-10% vs. 1-3%)
- More authentic audience connections
- Lower partnership costs
- Niche expertise

Discovery approach:
- Use hashtag searches via execute("instagram", "search", "search_posts", ...)
- Use query_cache() to filter by engagement rate vs. reach
- Prioritize niche relevance over size
```

### Multi-Platform Presence Analysis

Identify influencers active across platforms:
```
1. Find on Instagram/Twitter
2. Search LinkedIn for professional presence:
   execute("linkedin", "search", "search_users", {"keywords": "name"})
3. Check for YouTube channel:
   execute("youtube", "search", "search_videos", {"query": "creator name", "count": 10})
4. Look for website/blog:
   execute("webparser", "parse", "parse", {"url": "website_url"})

Benefits:
- Multiple touchpoints
- Diverse content formats
- Professional credibility
- Larger total reach
```

### Audience Demographics Research

Analyze who follows the influencer:
```
Instagram:
- execute("instagram", "user", "user_friendships", {"user": "username", "count": 100, "type": "followers"})
- Analyze follower profiles for patterns
- Use query_cache(cache_key, group_by="location") to segment by geography

LinkedIn:
- Check who engages with posts
- Identify follower job titles/industries from post comments

YouTube:
- Analyze comment demographics via execute("youtube", "video", "video_comments", ...)
- Check subscriber locations (if available)
```

## Reference Documentation

- **[DISCOVERY_CRITERIA.md](references/DISCOVERY_CRITERIA.md)** - Influencer evaluation criteria, scoring frameworks, and niche identification strategies

## Troubleshooting

**No Influencers Found**:
- Broaden search keywords
- Try multiple hashtags
- Search across multiple platforms
- Reduce minimum follower requirements

**Low Engagement Rates**:
- Use `query_cache(cache_key, conditions=[{"field": "engagement_rate", "operator": ">", "value": 0.03}])` to filter
- Focus on micro-influencers (smaller = higher engagement)
- Check for bot followers (sudden spikes)

**No Contact Information**:
- Check bio for email/website
- Look for LinkedIn profile via `execute("linkedin", "search", "search_users", {"keywords": "name"})`
- Try website domain: `execute("webparser", "parse", "parse", {"url": "domain"})`
- Search for media kit or press page

**API Errors**:
- Check `llm_hint` in error responses for actionable guidance
- LinkedIn endpoints requiring URN: get URN from profile response first, do not guess aliases
- Use `execute("linkedin", "search", "search_users", ...)` to find correct aliases before fetching profiles

---

**Ready to discover influencers?** Ask Claude to help you find content creators, analyze engagement, or build influencer lists for your marketing campaigns!
