---
name: feed-builder
description: Describe a feed in plain English ("Rust backend and observability, 50+ upvotes, no videos") and get a daily.dev custom feed with the right tags, sources and thresholds. Creates, tunes and verifies the feed for you.
---

# Feed Builder

Turn a sentence into a daily.dev custom feed. You describe the topic, the quality bar and what to leave out; the agent resolves tags, creates the feed, applies the filters and shows you what it returns.

## Requirements

One of:

- The daily.dev MCP server (`https://api.daily.dev/mcp`) connected with the `write` scope, or
- A daily.dev personal access token in `DAILY_DEV_TOKEN` (https://daily.dev/settings/api). Base URL `https://api.daily.dev/public/v1`, header `Authorization: Bearer $DAILY_DEV_TOKEN`. Never send the token anywhere except `api.daily.dev`.

Custom feeds beyond the first may need daily.dev Plus. If the create call returns 403, say so and stop.

Each step lists the MCP tool first and the REST call after it.

## Steps

1. **Parse the request** into: topics (tags), sources to include or block, minimum upvotes, minimum views, a day range, content types to drop (videos, memes, listicles, …), and a name.
2. **Resolve tags.** For every topic call `getSearchTags` (`GET /search/tags?q=<word>`). Tags are lowercase slugs with hyphens: `claude-code`, not `claude code`. Multi-word topics usually map to several tags; pick the ones that match the intent and show the user the list before creating anything.
3. **Name the feed.** Names may only contain letters, numbers and spaces, max 50 characters. No punctuation, no emoji in the name (the icon is a separate field). `Rust backend observability` is valid; `Rust + observability (prod)` is rejected with "Feed name should not contain special characters".
4. **Create it.** `postFeedsCustom` (`POST /feeds/custom`) with `name`, optional `icon` (one emoji), `minUpvotes`, `minViews`, `minDayRange`, `orderBy` (`DATE`, `UPVOTES`, `COMMENTS`, …; leave it out for the default ranking). Keep the returned `id`.
5. **Follow the tags.** `postFeedsFiltersByFeedIdTagsFollow` with `feedId` and `tags` (`POST /feeds/filters/{feedId}/tags/follow`). Block tags with `…TagsBlock`, follow or block sources with `…SourcesFollow` / `…SourcesBlock` (source handles come from `getSearchSources`, `GET /search/sources?q=`).
6. **Drop content types.** Call `getFeedsCustomAdvancedSettings` (`GET /feeds/custom/advanced-settings`) once to get setting ids, then `patchFeedsCustomByFeedIdAdvanced` (`PATCH /feeds/custom/{feedId}/advanced`) with `settings: [{ id, enabled: false }]`. Common ids: Videos 7, Memes 16, Listicles 11, News 9, Opinions 10, Releases 15, Tutorials 14, Squads 17.
7. **Verify.** `getFeedsFiltersByFeedId` (`GET /feeds/filters/{feedId}`) to confirm tags and settings, then `getFeedsCustomByFeedId` with `limit` 5 (`GET /feeds/custom/{feedId}?limit=5`) and show the titles. If it's empty, loosen `minUpvotes` or add a broader tag and tell the user what you changed.
8. **Hand it over.** Link the feed: `https://daily.dev/feeds/<slug>` using the `slug` from the create response.

## Output

A short confirmation: feed name and link, the tags followed, the thresholds, the content types dropped, and the first five posts it returns.

## Guardrails

- Never delete or modify an existing feed unless the user named it. `deleteFeedsCustomByFeedId` (`DELETE /feeds/custom/{feedId}`) is only for undoing a feed you just created when the user asks.
- Show the resolved tags and ask before creating when the request is ambiguous.
- The whole flow is about 6–8 requests of the user's API quota.
