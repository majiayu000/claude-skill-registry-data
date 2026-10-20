---
name: bookmark-recap
description: Turns what you bookmarked on daily.dev this week into a short reading report you can paste into standup, Slack or a newsletter. Groups your saves by topic, pulls the one-line summaries, and tells you what's worth reading first.
---

# Bookmark Recap

What did you save this week, and what should you actually read? This skill reads your recent daily.dev bookmarks, groups them by topic and writes a recap you can share.

## Requirements

One of:

- The daily.dev MCP server (`https://api.daily.dev/mcp`) connected to your agent, or
- A daily.dev personal access token in `DAILY_DEV_TOKEN` (https://daily.dev/settings/api). Base URL `https://api.daily.dev/public/v1`, header `Authorization: Bearer $DAILY_DEV_TOKEN`. Never send the token anywhere except `api.daily.dev`.

Each step lists the MCP tool first and the REST call after it.

## Steps

1. **Fetch bookmarks.** `getBookmarks` with `limit` 30 (`GET /bookmarks?limit=30`). Bookmarks come newest-saved first and each carries `bookmarkedAt`, the time the user saved it. Pass `unreadOnly: true` to recap only what the user hasn't opened yet, or `listId` (from `getBookmarksLists`, `GET /bookmarks/lists`) for one folder.
2. **Scope by date.** Default to the last 7 days using `bookmarkedAt`. If the user asks for a longer period, keep paging with `cursor` until `bookmarkedAt` falls outside the window. If nothing was saved in the window, say so and offer the latest 10 instead.
3. **Group.** Cluster by `tags`. Pick the two or three biggest clusters as sections; the rest goes under "Also saved".
4. **Rank within a group** by `numUpvotes`, and flag long reads (`readTime` ≥ 10 minutes).
5. **Write it.** For each post: title linked to `url` (fall back to `commentsPermalink`), the source name, read time, and one line taken from `summary`. Finish with a "Read first" pick: the post with the best upvotes-to-read-time ratio, in one sentence.

## Output

Markdown, under 300 words for a week of bookmarks. Sections by topic, bullets per post, "Read first" at the end. If the user asked for Slack, use Slack markdown (no headings, `*bold*`, one link per line).

## Guardrails

- Read-only. Don't mark bookmarks read or move them unless asked.
- One or two requests of the user's API quota for a week; one more per extra page.
