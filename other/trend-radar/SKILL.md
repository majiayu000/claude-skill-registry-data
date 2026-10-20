---
name: trend-radar
description: Which tags and tools are rising in your corner of the ecosystem this week? Compares daily.dev's popular feed against last week's snapshot and surfaces what's new, what's fading and what the community is suddenly talking about.
---

# Trend Radar

The popular feed tells you what's hot right now. Trend Radar tells you what changed: tags that broke in, tags that cooled off, and the posts that carried them.

## Requirements

One of:

- The daily.dev MCP server (`https://api.daily.dev/mcp`) connected to your agent, or
- A daily.dev personal access token in `DAILY_DEV_TOKEN` (https://daily.dev/settings/api). Base URL `https://api.daily.dev/public/v1`, header `Authorization: Bearer $DAILY_DEV_TOKEN`. Never send the token anywhere except `api.daily.dev`.

The agent needs a small state file to compare runs; use `~/.dailydev/trend-radar.json` unless the user names another path.

Each step lists the MCP tool first and the REST call after it.

## Steps

1. **Pick the lens.** Global by default. If the user says "my corner" or names topics, take their followed tags from `getFeedsFilters` (`GET /feeds/filters`, `includeTags`) or the tags they named, and pass up to 20 of them as a comma-separated `tags` filter to the popular feed.
2. **Snapshot the popular feed.** `getFeedsPopular` with `limit` 50 (`GET /feeds/popular?limit=50&tags=<a,b,c>`); page once more with `cursor` for 100 posts if the lens is global. Count, per tag: number of posts, total upvotes, total comments. Note the top 3 posts per tag by `numUpvotes`.
3. **Compare with the last snapshot** in the state file. Classify tags as **rising** (count or upvotes up by 50% or more, or new in the top 20), **steady**, or **fading** (down by 50% or more, or dropped out). With no previous snapshot, report the current ranking and say that trends start next run.
4. **Add context for risers.** For each rising tag call `getFeedsDiscussed` with `tag` and `period` 7 (`GET /feeds/discussed?tag=<tag>&period=7&limit=5`) to find what people argued about, and quote the most-commented title.
5. **Save the snapshot**: date, lens, per-tag counts. Keep the last 8 runs so the user can ask for a monthly view.
6. **Write the radar**: Rising (tag, change, the post that drove it), Fading (tag, change), New this week (tags not seen in the previous snapshot), and "Still dominant" (the top 3 steady tags). Link posts by `commentsPermalink`.

## Output

Under 300 words. A table for rising and fading tags with the change and the driving post; one line each for the rest. If the user asks for a chart, output the per-tag counts as CSV they can plot.

## Guardrails

- Read-only.
- Don't call a tag "rising" on one post: require at least 3 posts in the current snapshot.
- Two to four requests for the snapshot plus one per rising tag, about 6 to 10 per run.
