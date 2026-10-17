---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: searching-x
description: >
  Search X (Twitter) for posts, users, and threads using the grok CLI's native
  X search tools. Use when the user wants to find tweets, search for what people
  are saying about a topic, look up X users, or read full threads. Covers
  x_keyword_search, x_semantic_search, x_user_search, and x_thread_fetch with
  precise prompt templates and the full set of X search operators.
---

# Searching X via grok CLI

The `grok` CLI has 4 native X search tools. You invoke them by running grok in single-turn mode with a precise prompt that names the tool and its parameters.

```bash
grok -p '<prompt>' --always-approve
```

`-p` runs a single-turn prompt and exits. `--always-approve` skips tool approval prompts (optional; native X tools auto-approve, but add it when combining with other tools). The default model (`grok-4.5` or whatever `grok models` shows) has native X search tools. Do **not** pass `-m grok-build`; that model ID was retired and causes an "unknown model id" error.

Ignore stderr noise from strada traces. Only stdout matters.

## Tools

### x_keyword_search

The most powerful search tool. Supports the full set of X advanced search operators in the query string.

**Parameters:**
- `query` (required) — search string with operators
- `limit` (optional) — max 10, default 3
- `mode` (optional) — `"Top"` (default) or `"Latest"`

**Prompt template:**

```
Use x_keyword_search to search "<QUERY>" with mode "<MODE>" and limit <N>.
For each result show: post ID, author handle, date, full post text quoted
verbatim, and engagement counts (likes, reposts, views).
```

**Search operators** you can put inside the query string:

#### Date and time

| Operator | Example | Effect |
|---|---|---|
| `since:` | `since:2026-06-20` | Posts on or after this date |
| `until:` | `until:2026-06-25` | Posts before this date (exclusive) |
| `since:` with time | `since:2026-06-20_23:59:59_UTC` | Date + time precision |
| `within_time:` | `within_time:24h` | Relative window (supports `Nd`, `Nh`, `Nm`, `Ns`) |
| `since_time:` | `since_time:1750000000` | Unix timestamp (seconds) |
| `until_time:` | `until_time:1750100000` | Unix timestamp (seconds) |

#### User and account

| Operator | Example | Effect |
|---|---|---|
| `from:` | `from:elonmusk` | Posts from a specific user (no `@`) |
| `to:` | `to:elonmusk` | Replies to a specific user |
| `@username` | `@elonmusk` | Posts mentioning user (combine with `-from:` for pure mentions) |
| `list:` | `list:1234567890` or `list:owner/slug` | Posts from a list's members |
| `filter:follows` | | Only from accounts you follow |
| `filter:verified` | | Only from verified accounts |
| `filter:blue_verified` | | Only from blue-verified accounts |

#### Post relationships (verified working)

| Operator | Example | Effect |
|---|---|---|
| `quoted_tweet_id:` | `quoted_tweet_id:2069798022695756059` | Find all posts that quote a specific post |
| `conversation_id:` | `conversation_id:2069798022695756059` | All replies in a thread/conversation |
| `in_reply_to_tweet_id:` | `in_reply_to_tweet_id:ID` | Direct replies to a post (can be flaky) |
| `since_id:` | `since_id:ID` | Posts after this snowflake ID |
| `max_id:` | `max_id:ID` | Posts at or before this snowflake ID |

#### Engagement

| Operator | Example | Effect |
|---|---|---|
| `min_faves:` | `min_faves:50` | Minimum likes |
| `min_replies:` | `min_replies:10` | Minimum replies |
| `min_retweets:` | `min_retweets:5` | Minimum reposts |
| `filter:has_engagement` | | Has any replies/likes/reposts |

#### Media and content type

| Operator | Example | Effect |
|---|---|---|
| `filter:images` | | Only posts with images |
| `filter:videos` | | Only posts with videos |
| `filter:media` | | Posts with any media (images or videos) |
| `filter:links` | | Posts with links |
| `filter:mentions` | | Posts with @mentions |
| `filter:hashtags` | | Posts with hashtags |
| `filter:cashtags` | | Posts with $cashtags |

#### Post type

| Operator | Example | Effect |
|---|---|---|
| `filter:replies` | | Only replies |
| `filter:quote` | | Only quote posts |
| `filter:nativeretweets` | | Only button retweets (recent ~7-10 days) |
| `filter:self_threads` | | Only self-reply threads |
| `include:nativeretweets` | | Include retweets (excluded by default) |
| `-filter:replies` | | Exclude replies |
| `-filter:retweets` | | Exclude retweets |

#### Content matching

| Operator | Example | Effect |
|---|---|---|
| `"exact phrase"` | `"cursor vs claude code"` | Exact phrase match |
| `(A OR B)` | `(tennis OR wimbledon)` | Boolean OR (must be uppercase) |
| `-word` | `-spam` | Exclude word or phrase |
| `#hashtag` | `#Wimbledon` | Hashtag match |
| `$CASHTAG` | `$TSLA` | Cashtag match |
| `url:` | `url:github.com` | Posts linking to domain |

#### Geo and location

| Operator | Example | Effect |
|---|---|---|
| `geocode:` | `geocode:37.77,-122.41,10km` | Posts near coordinates (lat,long,radius) |
| `near:` | `near:"London"` | Posts near a city |
| `within:` | `within:10km` | Radius (combine with `near:`) |
| `place:` | `place:PLACEID` | Posts tagged with a place |
| `place_country:` | `place_country:US` | Posts from a country |

#### Language

| Operator | Example | Effect |
|---|---|---|
| `lang:` | `lang:en` | Filter by BCP 47 language code |

Operators combine freely with spaces (implicit AND). Examples:

```
sinner since:2026-06-22 min_faves:50
from:__morse since:2026-06-01
"ai coding agents" min_faves:100 lang:en filter:has_engagement
(cursor OR "claude code") since:2026-06-20 -spam
quoted_tweet_id:2069798022695756059
conversation_id:2069798022695756059 filter:replies
sinner within_time:24h min_faves:20
filter:images from:janniksin
```

Always use `mode "Latest"` when searching for recent news or events. Use `mode "Top"` for popular/trending content on a topic.

### x_semantic_search

Relevance-based search. Good for conceptual queries like "what people think about X" or "news about Y". Returns posts ranked by semantic relevance (vector similarity) rather than recency.

**Parameters:**
- `query` (required) — natural language search query
- `limit` (optional) — max 10, default 3
- `from_date` (optional) — `YYYY-MM-DD`, posts from this date onward
- `to_date` (optional) — `YYYY-MM-DD`, posts up to this date
- `usernames` (optional) — array of usernames, restrict to these authors only
- `exclude_usernames` (optional) — array of usernames to exclude
- `min_score_threshold` (optional) — relevance cutoff, default 0.18. Raise to 0.3-0.5 for stricter matches, lower for broader but noisier results.

**How scoring works:** embedding-based similarity between query and post content. Results are ranked by internal relevance score. `min_score_threshold` filters out posts below that score. Date bounds narrow the pool before semantic ranking.

**Prompt template:**

```
Use x_semantic_search with query "<QUERY>", from_date "<YYYY-MM-DD>",
to_date "<YYYY-MM-DD>", and limit <N>. For each result show: post ID,
author handle, date, full post text quoted verbatim, and any URLs in the post.
```

Use semantic search when:
- You want conceptual matches, not just keyword hits
- The topic is broad ("what are people saying about AI agents")
- You want to filter by date range without learning operator syntax

Use keyword search when:
- You need precise/latest results
- You want to combine multiple filters (user + date + engagement)
- You need exact phrase matching

### x_user_search

Find X users by name or handle.

**Parameters:**
- `query` (required) — name or handle to search for
- `count` (optional) — number of results, default 3

**Return fields per user:** ID (snowflake), display name, handle, avatar URL, follower count, verified status ("Blue Verified" / "Verified Organization" / absent), bio (when present). Does not return following count, joined date, or post count.

**Prompt template:**

```
Use x_user_search to find "<NAME_OR_HANDLE>" with count <N>.
For each result show: display name, handle, bio, and follower count.
```

### x_thread_fetch

Read a full post with its conversation context (parent posts above it and replies below it).

**Parameters:**
- `post_id` (required) — the numeric post ID (get this from search results)

**What it returns:**
- The **root post** of the conversation (ancestor)
- The **requested post** (labeled explicitly when it differs from root)
- **Parent chain** between root and requested post
- **Replies** to the requested post (direct + some nested; limited window, not all replies)
- **Quoted posts** fully embedded with the same fields

**Fields per post:** ID, conversation ID, author (name, handle, avatar, bio), timestamp, engagement (likes, reposts, quotes, replies, bookmarks, views), media (type, URLs, video duration), full text, quoted post (nested).

**Prompt template:**

```
Use x_thread_fetch with post_id "<ID>". Show the full thread: for each post
in the conversation show the author handle, date, full text quoted verbatim,
and whether it is a parent, the target post, or a reply.
```

## Session minimization

xAI bills by **session**, not by tool call. Every `grok -p` invocation is one session. **Combine as many tool calls as possible into a single prompt.** Grok can chain multiple X tools in one turn: search, then fetch threads, then search again. Never split work across multiple `grok -p` calls when one call can do it all.

When you need multiple searches (e.g. keyword search + semantic search + user lookup + thread fetch), write **one prompt** that lists all the operations sequentially. Grok executes them in order and returns all results in one response.

```bash
# BAD: 3 sessions, 3x the cost
grok -p 'Use x_keyword_search to search "chiavari" ...'
grok -p 'Use x_semantic_search with query "chiavari news" ...'
grok -p 'Use x_thread_fetch with post_id "123" ...'

# GOOD: 1 session, all 3 operations
grok -p 'Do all of the following and show full results for each:
1. Use x_keyword_search to search "chiavari since:2026-06-20 min_faves:10" with mode "Latest" and limit 10. Show post ID, author handle, date, full text verbatim, engagement.
2. Use x_semantic_search with query "chiavari local news", from_date "2026-06-20", limit 5. Show post ID, author handle, date, full text verbatim.
3. Use x_thread_fetch with post_id "123". Show the full thread with author, date, full text verbatim for each post.' --always-approve
```

The only reason to use a second `grok -p` call is when the output of the first is needed to construct the second query (e.g. you don't know the post ID yet). Even then, prefer asking grok to chain: "search for X, then fetch the thread of the top result."

## Common workflows

### Latest news on a topic

```bash
grok -p 'Use x_keyword_search to search "<TOPIC> since:2026-06-20 min_faves:10" with mode "Latest" and limit 10. For each result show: post ID, author handle, date, full post text quoted verbatim, and engagement counts (likes, reposts, views).'
```

### What a specific user posted recently

```bash
grok -p 'Use x_keyword_search to search "from:<HANDLE> since:2026-06-01" with mode "Latest" and limit 5. For each result show: post ID, author handle, date, full post text quoted verbatim, and engagement counts.'
```

### Search + read the best thread

```bash
grok -p 'Use x_keyword_search to search "<QUERY>" with mode "Latest" and limit 5. For each result show: post ID, author handle, date, full text verbatim, engagement. Then use x_thread_fetch on the post with the most likes to show its full conversation context.' --always-approve
```

### Find a user then read their posts

```bash
grok -p 'Use x_user_search to find "<NAME>" with count 3. Show display name, handle, bio, follower count. Then use x_keyword_search to search "from:<BEST_HANDLE>" with mode "Latest" and limit 5, showing post ID, date, full text, and engagement for each.' --always-approve
```

### Multi-topic search in one session

When you need data on multiple topics, combine them into one prompt:

```bash
grok -p 'Do all of the following and show full results for each:
1. Use x_keyword_search to search "<TOPIC_1> since:2026-06-20" with mode "Latest" and limit 5. Show post ID, author handle, date, full text verbatim, engagement.
2. Use x_keyword_search to search "<TOPIC_2> since:2026-06-20" with mode "Latest" and limit 5. Show post ID, author handle, date, full text verbatim, engagement.
3. Use x_semantic_search with query "<BROAD_QUESTION>", from_date "2026-06-20", limit 5. Show post ID, author handle, date, full text verbatim.' --always-approve
```

## Exploring post relationships

### Find all quotes of a post

Use `quoted_tweet_id:` in `x_keyword_search`. Returns all posts that quote the target.

```bash
grok -p 'Use x_keyword_search to search "quoted_tweet_id:<POST_ID>" with mode "Latest" and limit 10. For each result show: post ID, author handle, date, full post text quoted verbatim, engagement.'
```

### Find all replies in a thread

Use `conversation_id:` to get all replies in a conversation. The conversation ID is the root post's ID.

```bash
grok -p 'Use x_keyword_search to search "conversation_id:<ROOT_POST_ID> filter:replies" with mode "Latest" and limit 10. For each result show: post ID, author handle, date, full post text quoted verbatim, engagement.'
```

Alternatively, use `x_thread_fetch` on the post ID to get the parent chain + replies in one call.

### Find posts with images/videos from a user

```bash
grok -p 'Use x_keyword_search to search "from:<HANDLE> filter:images since:2026-06-01" with mode "Latest" and limit 10. For each result show: post ID, author handle, date, full post text quoted verbatim, engagement, and direct image URLs from media attachments.'
```

### Find posts linking to a specific domain

```bash
grok -p 'Use x_keyword_search to search "url:github.com min_faves:50 since:2026-06-20" with mode "Latest" and limit 10. For each result show: post ID, author handle, date, full post text quoted verbatim, engagement.'
```

### Find posts near a location

```bash
grok -p 'Use x_keyword_search to search "tennis geocode:51.5074,-0.1278,25km since:2026-06-20" with mode "Latest" and limit 5. For each result show: post ID, author handle, date, full post text quoted verbatim, engagement.'
```

## Decision rule

- **Discover posts by keyword, operator, or filter** -> `x_keyword_search`
- **Conceptual / relevance search with date range** -> `x_semantic_search`
- **Find a user profile** -> `x_user_search`
- **Read full thread given a post ID** -> `x_thread_fetch`
- **Already have a tweet URL and just need text** -> use the `reading-x-posts` skill instead (oEmbed, no grok needed)

## Tips

- **Minimize sessions.** xAI bills per session. Combine all searches, lookups, and thread fetches into one `grok -p` call. Never run separate `grok -p` calls for things that can be chained in one prompt.
- Always ask grok to **quote the full post text verbatim**. Without this instruction it tends to summarize.
- Always ask for **post IDs** in search results so you can follow up with `x_thread_fetch` (in the same session).
- Always ask for **engagement counts** (likes, reposts, views) to gauge post quality.
- `x_keyword_search` limit max is 10. For broader searches, combine multiple queries with different `since:/until:` windows **in the same prompt**.
- `x_semantic_search` can return spam or low-quality results. Add `min_score_threshold` (e.g. 0.3) to filter.
- The `from:` operator in keyword search does not need the `@` prefix. Use `from:elonmusk` not `from:@elonmusk`.
- These are the **only 4 native X tools**. There is no direct "get post by ID", "get user timeline", "get followers", "get trends", or "get lists" tool. Use keyword search operators to approximate these (e.g. `from:user` for timeline).
- `in_reply_to_tweet_id:` can be flaky with upstream errors. Prefer `conversation_id:` or `x_thread_fetch` for replies.
- `filter:nativeretweets` only covers recent ~7-10 days.
- Always ask for **media URLs** when searching for images/videos. Without this instruction grok may note "media attached" without giving the direct URL.
