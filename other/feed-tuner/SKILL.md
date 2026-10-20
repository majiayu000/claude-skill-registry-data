---
name: feed-tuner
description: Compares what you bookmark on daily.dev with the tags and sources you follow, then proposes follow, unfollow and block changes and applies only the ones you approve.
---

# Feed Tuner

What you save tells the truth about what you want to read. Feed Tuner compares your bookmarks with your feed settings and proposes the changes that close the gap.

## Requirements

One of:

- The daily.dev MCP server (`https://api.daily.dev/mcp`) connected with the `write` scope, or
- A daily.dev personal access token in `DAILY_DEV_TOKEN` (https://daily.dev/settings/api). Base URL `https://api.daily.dev/public/v1`, header `Authorization: Bearer $DAILY_DEV_TOKEN`. Never send the token anywhere except `api.daily.dev`.

Each step lists the MCP tool first and the REST call after it.

## Steps

1. **Collect the evidence.** `getBookmarks` with `limit` 50 (`GET /bookmarks?limit=50`); page once more with `cursor` if the user has a long history. Count tags and sources across the bookmarks.
2. **Collect the settings.** `getFeedsFilters` (`GET /feeds/filters`): `includeTags`, `blockedTags`, `includeSources`, `excludeSources`.
3. **Diff.**
   - **Follow candidates**: tags that appear in 3 or more bookmarks but aren't in `includeTags`; sources (by `handle`) in 3 or more bookmarks but not in `includeSources`.
   - **Unfollow candidates**: tags in `includeTags` that appear in none of the bookmarks. Be conservative: only suggest unfollowing when the user has 30+ bookmarks, and never suggest unfollowing more than 5 at once.
   - **Conflicts**: tags in `blockedTags` or sources in `excludeSources` that the user nevertheless bookmarked. Surface these; the user probably wants to unblock.
4. **Propose.** One list per group with the counts behind each suggestion. Ask the user to approve, edit or skip each group.
5. **Apply only what was approved.**
   - `postFeedsFiltersTagsFollow` / `postFeedsFiltersTagsUnfollow` (`POST /feeds/filters/tags/follow`, `POST /feeds/filters/tags/unfollow`, body `{ "tags": [...] }`)
   - `postFeedsFiltersTagsUnblock` (`POST /feeds/filters/tags/unblock`)
   - `postFeedsFiltersSourcesFollow` / `postFeedsFiltersSourcesUnblock` (`POST /feeds/filters/sources/follow`, `POST /feeds/filters/sources/unblock`, body `{ "sources": [handles] }`)
   For a custom feed instead of the main one, use the `…ByFeedId…` variants (`POST /feeds/filters/{feedId}/tags/follow` and so on).
6. **Confirm** with `getFeedsFilters` and summarize.

## Output

Three short lists with counts, then the applied changes. If the bookmarks and settings already agree, say so instead of inventing changes.

## Guardrails

- Never block anything. Unblocking and unfollowing happen only on explicit approval.
- Don't touch sources the user follows that simply didn't show up in bookmarks; squads and newsletters are followed for reasons bookmarks don't capture.
- Two or three read requests plus one write per approved group.
