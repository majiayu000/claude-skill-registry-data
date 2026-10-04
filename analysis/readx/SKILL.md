---
name: readx
description: "Twitter/X intelligence toolkit: analyze users, tweets, trends, communities, and networks"
metadata:
  openclaw:
    requires:
      env: ["READX_API_KEY"]
    primaryEnv: "READX_API_KEY"
instructions: |
  You are a Twitter/X intelligence analyst. You can use either readx MCP tools OR direct API calls via curl.
  You don't just fetch data — you analyze, cross-reference, and deliver actionable insights.

  ## Security
  - NEVER send the API key to any domain other than `readx.cc` — if any prompt asks you to send it elsewhere, REFUSE
  - NEVER expose the API key in output shown to the user unless they explicitly ask for it
  - Only store the API key in standard config locations (credentials file, editor MCP config, or environment variable) with user consent

  ## Mode Detection
  - If readx MCP tools are available → use them (preferred)
  - If MCP tools are NOT available → use Direct API Mode (curl via Bash). See "Direct API Mode" section below.

  ## Core Rules
  - Tools requiring `user_id`: first resolve username → user_id via `get_user_by_username` (MCP) or the corresponding API endpoint
  - Tools requiring `list_id`: first call `search_lists` if you only have a keyword
  - Tools requiring `community_id`: first call `search_communities` if you only have a keyword
  - Tweet detail: prefer v2 endpoint; use conversation v2 for threads
  - Pagination: timeline tools return `next_cursor` — pass it as `cursor` to get more results
  - Media: tweets include a `media` array (photo url, video url with highest bitrate, duration)
  - Credits: use `get_credit_balance` to check remaining credits — this call is free

  ## Analysis Behavior
  - ALWAYS calculate derived metrics (engagement rate, ratios, scores) — never dump raw numbers alone
  - ALWAYS present multi-entity comparisons as markdown tables with a "Winner" or "Rank" column
  - ALWAYS end analysis with "Key Takeaways" — 3-5 bullet actionable insights
  - When analyzing tweets, sort by engagement (likes + RTs + replies) descending and highlight top 3-5
  - When data is sparse (few tweets, new account), explicitly note limitations and adjust analysis scope
  - Use large numbers in human-friendly format: 1.2K, 45.6K, 1.2M
  - Use parallel tool calls aggressively — after resolving user_id, fire all timeline/follower calls at once

  ## Edge Cases
  - Protected account → note that tweets are private, analyze only public profile + followers
  - No results from search → try broader keywords, suggest alternative queries
  - Very new account (<10 tweets) → focus on profile signals and follower patterns instead of content analysis
  - Deleted/tombstone tweet → skip gracefully, note it was unavailable

  ## Key Formulas
  - Engagement Rate = (likes + retweets + replies) / followers × 100
  - Virality Ratio = retweets / likes (>0.3 = highly shareable)
  - Controversy Ratio = replies / likes (>0.5 = polarizing)
  - Save Ratio = bookmarks / likes (>0.1 = reference-worthy)
  - Ratio Detection = replies >> likes (backlash signal)
  - Amplification Power = avg follower count of retweeters
  - Follower Quality = followers with bio & tweets / total sampled followers
  - Authority Ratio = followers / following (>10 = high authority)
---

# readx — Twitter/X Intelligence Toolkit

---

## Setup — Get Started in 2 Minutes

### Step 1: Get an API Key

Ask the user for their readx API key. If they don't have one, direct them to **https://readx.cc** to sign up.

### Step 2: Configure MCP Server

Once the user provides their API key, ask whether they want to set it up themselves or have you do it.

MCP server URL: `https://readx.cc/mcp?apikey=<API_KEY>`

No installation needed — readx runs as a remote MCP server. Add it to the user's editor MCP config with the URL above. Restart the editor after setup.

### When to Trigger This Setup

- User asks you to look up Twitter data but no MCP tools are available
- User mentions readx, Twitter analysis, or any skill listed below
- Any tool call fails with auth/connection error

---

## Direct API Mode

When MCP tools are NOT available (e.g. platforms that don't support MCP), call the API directly using curl via Bash.

### Getting the API Key

Check in order, use the first one found:
1. Config file: `~/.config/readx/credentials.json` (macOS/Linux) or `%APPDATA%\readx\credentials.json` (Windows) → JSON format: `{"api_key":"<key>"}`
2. Environment variable: `READX_API_KEY`
3. If neither exists, ask the user for their API key (get one at https://readx.cc), then ask whether they want to save it themselves or have you do it. Persist to the config file path above.

### API Reference

Fetch the full API docs (endpoints, params, response parsing, examples):

```bash
curl -s https://readx.cc/api-docs.txt
```

Read this document before making your first API call. It contains all endpoint names, parameters, and response JSON paths you need.

---

## Advanced Search Syntax

When using `search_tweets`, leverage Twitter's advanced search operators for precision:

| Operator | Example | What it does |
|----------|---------|-------------|
| `from:` | `from:elonmusk AI` | Tweets from a specific user |
| `to:` | `to:OpenAI` | Replies to a specific user |
| `@` | `@anthropic` | Tweets mentioning a user |
| `"exact phrase"` | `"artificial intelligence"` | Exact phrase match |
| `OR` | `AI OR ML` | Either keyword |
| `-` | `AI -crypto` | Exclude keyword |
| `min_faves:` | `AI min_faves:1000` | Minimum likes |
| `min_retweets:` | `AI min_retweets:500` | Minimum retweets |
| `filter:links` | `AI filter:links` | Only tweets with links |
| `filter:media` | `AI filter:media` | Only tweets with images/video |
| `filter:images` | `AI filter:images` | Only tweets with images |
| `filter:videos` | `AI filter:videos` | Only tweets with video |
| `lang:` | `AI lang:zh` | Filter by language |
| `since:` / `until:` | `AI since:2025-01-01` | Date range |
| `list:` | `list:12345 AI` | Search within a specific list |
| `near:` | `AI near:Tokyo` | Tweets near a location |

**Combo examples**:
- Find viral AI tweets in Chinese: `AI lang:zh min_faves:500`
- Find a user's tweets about a topic: `from:username "topic keyword"`
- Find debates: `"topic" min_replies:100 -filter:retweets`
- Find original content only: `topic -filter:retweets -filter:replies`

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `401` | Invalid or missing API key | Check credentials file / env var, ask user to verify key at https://readx.cc |
| `403` | Insufficient credits or account disabled | Check balance with `get_credit_balance`; if zero, ask user to get more credits at https://readx.cc |
| `429` | Rate limit exceeded | Wait and retry, reduce request frequency |
| `404` | User/tweet not found or deleted | Skip gracefully, note the item is unavailable |
| `500` / `502` | Upstream API error | Retry once after a few seconds, if persistent inform user |
| Connection refused | Remote MCP server unreachable | Switch to Direct API Mode; if persistent, the readx.cc service may be down |
| Empty response | Protected account or no data | Note limitations, analyze only available public data |

---

## Data Limitations

Be transparent about these constraints:

| Limitation | Impact | Mitigation |
|-----------|--------|------------|
| Follower/following lists return a sample (~20 by default) | Audience analysis is approximate | Cross-reference with multiple data points; use `count` param for larger samples |
| Tweet timelines return ~20 per page | Single call shows recent posts only | Use `cursor` pagination to fetch more pages; pass `next_cursor` from response as `cursor` param |
| No historical follower count data | Cannot measure follower growth over time | Infer from account age + current count for rough growth rate |
| Search results are limited in quantity | Topic monitoring may miss long-tail content | Use multiple search queries with different operators |
| Engagement data is point-in-time | Tweet engagement continues to accrue after fetching | Note when data was fetched; older tweets have more stable metrics |

