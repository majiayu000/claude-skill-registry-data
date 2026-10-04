---
name: anysite-audience-analysis
description: Analyze audience demographics, engagement patterns, and follower behavior across Instagram, YouTube, and LinkedIn using anysite MCP server. Understand who engages with content, track audience growth, analyze follower quality, identify engagement patterns, and profile audience characteristics. Supports Instagram audience analysis, YouTube subscriber research, and LinkedIn connection profiling. Use when users need to understand target audiences, validate influencer audiences, analyze follower demographics, track engagement patterns, or optimize content for specific audience segments.
---

# anysite Audience Analysis

Understand your audience through demographic analysis, engagement patterns, and follower behavior across Instagram, YouTube, and LinkedIn.

## Overview

- **Analyze follower demographics** and characteristics
- **Track engagement patterns** and behavior
- **Evaluate audience quality** and authenticity
- **Identify content preferences** by audience segment
- **Optimize targeting** based on audience insights

**Coverage**: 60% - Focused on Instagram, YouTube, LinkedIn

## Supported Platforms

- ✅ **Instagram**: Follower analysis, engagement patterns, audience location
- ✅ **YouTube**: Subscriber insights, comment demographics, viewer behavior
- ✅ **LinkedIn**: Connection analysis, professional demographics, engagement

## Quick Start

**Step 1: Identify Audience Source**

Choose platform:
- Instagram: `execute("instagram", "user", "user", {"user": "..."})` + `execute("instagram", "user", "user_friendships", {"user": "...", "count": 100, "type": "followers"})`
- YouTube: `execute("youtube", "channel", "channel_videos", {"channel": "...", "count": 50})` + comment analysis
- LinkedIn: `execute("linkedin", "post", "get_user_posts", {"user": "...", "count": 50})` + engagement analysis

**Step 2: Collect Audience Data**

Gather:
- Follower/subscriber counts
- Engagement metrics
- Demographics (from profiles)
- Behavior patterns

**Step 3: Analyze Patterns**

Look for:
- Audience segments
- Engagement drivers
- Content preferences
- Peak activity times

Use `query_cache()` to filter and aggregate cached data without re-fetching.

**Step 4: Generate Insights**

Deliver:
- Audience profile summary
- Engagement patterns
- Content recommendations
- Targeting suggestions

Use `export_data()` to provide downloadable CSV/JSON files.

## Common Workflows

### Workflow 1: Instagram Audience Analysis

**Steps**:

1. **Get Profile Overview**
```
execute("instagram", "user", "user", {"user": "username"})
→ Follower count (follower_count), post count (media_count), bio (description)
→ Fields: id, alias, name, url, image, follower_count, following_count, description, media_count, is_private, is_verified, is_business, category, external_url, email, location
```

2. **Analyze Followers** (sample)
```
execute("instagram", "user", "user_friendships", {
  "user": "username",
  "count": 100,
  "type": "followers"
})
→ Fields: id, name, alias, url, image, is_verified, is_private

For each follower (sample):
- Profile type (personal, business, creator)
- Bio indicators (interests, location)
- Follower count (influence level)

Use get_page(cache_key, offset=10, limit=10) to load more followers.
```

3. **Engagement Pattern Analysis**
```
execute("instagram", "user", "user_posts", {"user": "username", "count": 50})
→ Fields: id, code, url, image, text, created_at, like_count, comment_count, reshare_count, view_count, type, is_paid_partnership

For each post:
  execute("instagram", "post", "post_likes", {"post": "{id}", "count": 100})
  → Fields: id, name, alias, url, image, is_verified, is_private

  execute("instagram", "post", "post_comments", {"post": "{id}", "count": 50})
  → Fields: id, comment_index, created_at, text, like_count, reply_count, parent_id, user

Analyze:
- Who engages most (power users)
- When engagement happens (timing via created_at)
- What content drives engagement
- Comment quality and topics

Use query_cache(cache_key, sort_by={"field": "like_count", "order": "desc"})
to find top-performing posts without re-fetching.
```

4. **Audience Segmentation**
```
Group followers by:
- Engagement level (active, passive, ghost)
- Interests (from bios)
- Location (from profiles)
- Influence (follower counts)

Use query_cache(cache_key, conditions=[{"field": "is_verified", "op": "eq", "value": true}])
to filter verified followers.
```

**Expected Output**:
- Audience demographics summary
- Engagement patterns
- Top engaged followers
- Content preferences

Use `export_data(cache_key, "csv")` to provide a downloadable follower/engagement report.

### Workflow 2: YouTube Audience Insights

**Steps**:

1. **Channel Overview**
```
execute("youtube", "channel", "channel_videos", {"channel": "@channel_alias", "count": 50})
→ Fields: id, title, url, author, duration_seconds, view_count, published_at, image

Aggregate:
- Total views (sum view_count)
- Content mix (by duration, topic)
- Publishing frequency (by published_at)

Use query_cache(cache_key, aggregate={"field": "view_count", "op": "sum"})
to get total views.
```

2. **Viewer Engagement Analysis**
```
For recent videos:
  execute("youtube", "video", "video", {"video": "{video_id}"})
  → Fields: id, url, title, description, author, duration_seconds, view_count, subtitles

  execute("youtube", "video", "video_comments", {"video": "{video_id}", "count": 200})
  → Fields: id, text, author, published_at, like_count, reply_count, reply_level
  → Analyze commenter patterns

Use get_page(cache_key, offset=10, limit=10) to load more comments.
```

3. **Audience Demographics from Comments**
```
From comments analyze:
- Questions asked (knowledge level)
- Topics discussed (interests)
- Language and tone
- Technical depth

Use query_cache(cache_key, conditions=[{"field": "text", "op": "contains", "value": "?"}])
to filter questions from comments.

Use query_cache(cache_key, sort_by={"field": "like_count", "order": "desc"})
to find most popular comments.
```

4. **Content Performance by Audience**
```
Correlate:
- High-view videos → audience interests
- High-comment videos → engagement topics

Use query_cache(cache_key, sort_by={"field": "view_count", "order": "desc"})
to rank videos by performance metrics.
```

**Expected Output**:
- Viewer interest profile
- Engagement drivers
- Content optimization insights
- Audience knowledge level

### Workflow 3: LinkedIn Audience Profiling

**Steps**:

1. **Get Post History**
```
execute("linkedin", "post", "get_user_posts", {"user": "{alias}", "count": 50})
```

2. **Analyze Engagement**
```
For each post:
- Reaction count and types
- Comment depth
- Share count
- Post reach indicators

Use query_cache(cache_key, sort_by={"field": "reactions", "order": "desc"})
to find most engaging posts.
```

3. **Profile Engagers** (if accessible)
```
From reactions/comments:
- Job titles
- Industries
- Companies
- Seniority levels

Use execute("linkedin", "user", "get", {"user": "{engager_alias}"})
to get full profiles of top engagers.
```

4. **Content-Audience Mapping**
```
Correlate:
- Which topics get most engagement
- Which formats perform best
- Which audiences engage with what
- When different audiences are active

Use query_cache(cache_key, aggregate={"field": "reactions", "op": "avg"}, group_by="post_type")
to analyze performance by content type.
```

**Expected Output**:
- Professional audience profile
- Engagement patterns by topic
- Content-audience fit analysis
- Posting optimization recommendations

## MCP Tools Reference

### v2 Meta-Tools

| Tool | Purpose |
|------|---------|
| `discover(source, category)` | Learn available endpoints and params before execute |
| `execute(source, category, endpoint, params)` | Fetch data — replaces all v1 tools |
| `get_page(cache_key, offset, limit)` | Load more items from previous execute |
| `query_cache(cache_key, conditions, sort_by, aggregate, group_by)` | Filter/sort/aggregate cached data |
| `export_data(cache_key, format)` | Export dataset as CSV/JSON/JSONL |

### Instagram Endpoints

| Endpoint | Call | Key Params |
|----------|------|------------|
| Profile | `execute("instagram", "user", "user", {"user": "..."})` | `user` (alias/ID/URL) |
| Followers/Following | `execute("instagram", "user", "user_friendships", {"user": "...", "count": N, "type": "followers"})` | `user`, `count`, `type` (followers\|following) |
| User Posts | `execute("instagram", "user", "user_posts", {"user": "...", "count": N})` | `user`, `count` |
| User Reels | `execute("instagram", "user", "user_reels", {"user": "...", "count": N})` | `user`, `count` |
| Post Details | `execute("instagram", "post", "post", {"post": "{id}"})` | `post` (numeric post ID) |
| Post Likes | `execute("instagram", "post", "post_likes", {"post": "{id}", "count": N})` | `post`, `count` |
| Post Comments | `execute("instagram", "post", "post_comments", {"post": "{id}", "count": N})` | `post`, `count` |

### YouTube Endpoints

| Endpoint | Call | Key Params |
|----------|------|------------|
| Channel Videos | `execute("youtube", "channel", "channel_videos", {"channel": "...", "count": N})` | `channel` (URL/@alias/ID), `count` (max 1000) |
| Video Details | `execute("youtube", "video", "video", {"video": "..."})` | `video` (ID or URL) |
| Video Comments | `execute("youtube", "video", "video_comments", {"video": "...", "count": N})` | `video`, `count` (max 2000) |
| Video Subtitles | `execute("youtube", "video", "video_subtitles", {"video": "...", "lang": "en"})` | `video`, `lang` |

### LinkedIn Endpoints

| Endpoint | Call | Key Params |
|----------|------|------------|
| User Posts | `execute("linkedin", "post", "get_user_posts", {"user": "..."})` | `user` (alias) |
| User Profile | `execute("linkedin", "user", "get", {"user": "..."})` | `user` (alias) |

### Error Handling

- If `execute()` returns an error with `"llm_hint"`, follow the hint.
- If `execute()` returns `{"error": "Source not found", "available_sources": [...]}`, check source name.
- If `execute()` returns `{"error": "Endpoint not found", "available_endpoints": [...]}`, call `discover()` to find correct endpoint names.

## Audience Analysis Framework

**Demographic Analysis**:
```
- Age range (inferred from profiles)
- Location (from bio/profiles)
- Interests (from bio keywords)
- Professional level (LinkedIn titles)
```

**Behavioral Analysis**:
```
- Engagement frequency
- Content preferences
- Peak activity times
- Interaction patterns
```

**Quality Metrics**:
```
- Real vs. fake followers
- Engagement authenticity
- Audience overlap
- Influence distribution
```

## Output Formats

**Chat Summary**:
- Audience profile highlights
- Key engagement patterns
- Content recommendations
- Strategic insights

**CSV Export** via `export_data(cache_key, "csv")`:
- Follower sample data
- Engagement metrics
- Segment distribution

**JSON Export** via `export_data(cache_key, "json")`:
- Complete audience data
- Engagement time series
- Segmentation details

## Reference Documentation

- **[PLATFORM_COVERAGE.md](references/PLATFORM_COVERAGE.md)** - Platform-specific audience analysis capabilities
- **[TOOL_MAPPING.md](references/TOOL_MAPPING.md)** - Mapping analysis needs to MCP tools

---

**Ready to understand your audience?** Ask Claude to help you analyze followers, track engagement patterns, or profile audience characteristics!
