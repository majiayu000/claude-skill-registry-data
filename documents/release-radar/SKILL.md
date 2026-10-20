---
name: release-radar
description: A weekly changelog for your stack from daily.dev. Finds release notes, breaking changes and migration posts for the tags you follow, writes a digest, and saves the posts to a bookmark list.
---

# Release Radar

Release notes scatter across dozens of blogs and repos. Release Radar collects the ones that matter for your stack from daily.dev and turns them into one weekly digest.

## Requirements

One of:

- The daily.dev MCP server (`https://api.daily.dev/mcp`) connected to your agent (add the `write` scope if you want posts bookmarked), or
- A daily.dev personal access token in `DAILY_DEV_TOKEN` (https://daily.dev/settings/api). Base URL `https://api.daily.dev/public/v1`, header `Authorization: Bearer $DAILY_DEV_TOKEN`. Never send the token anywhere except `api.daily.dev`.

Each step lists the MCP tool first and the REST call after it.

## Steps

1. **Decide the stack.** Use the tags the user names, or `getFeedsFilters` (`GET /feeds/filters`) and take `includeTags`. Cap at 8 tags; more than that makes the digest noise.
2. **Pull the tag feeds.** For each tag, `getFeedsTagByTag` with `limit` 30 (`GET /feeds/tag/{tag}?limit=30`). These feeds are unranked and include tweets and zero-upvote posts, so filter:
   - keep posts whose `title` or `summary` mentions a version or a release: matches like `v\d`, `\d+\.\d+`, `release`, `released`, `changelog`, `breaking`, `deprecat`, `migrat`, `end of life`, `GA`, `beta`, `RC`
   - keep `createdAt` within the last 7 days (or the period the user asked for)
   - drop posts with `type` starting with `social:` unless they have 10 or more upvotes
3. **Fill gaps with search.** For tags with few hits, `getSearchPosts` with `q` set to `<tag> release` (`GET /search/posts?q=<tag>+release&limit=10`) and apply the same filters.
4. **Classify** each kept post into **Breaking changes**, **Releases**, **Deprecations and end of life**, or **Migration guides**, using the summary. Within each group sort by `numUpvotes`.
5. **Write the digest.** Per post: title linked to `url` (fall back to `commentsPermalink`), the project or source, the version if visible, one line from `summary`, and upvotes. Lead with breaking changes.
6. **Optional: save them.** If the user wants the posts kept, `postBookmarks` with the post ids (`POST /bookmarks`, body `{ "postIds": [...] }`). To file them in a dedicated list, find or create one with `getBookmarksLists` / `postBookmarksLists` (`GET /bookmarks/lists`, `POST /bookmarks/lists`, body `{ "name": "Releases", "icon": "🚀" }`) and pass its id as `listId`. Bookmark lists are a daily.dev Plus feature; on a free account `listId` is ignored and the posts land in the main bookmarks, so say that rather than failing.

## Output

A digest under 400 words for 8 tags, grouped as in step 4, with a one-line "nothing new" for tags that had no releases. Markdown by default; Slack formatting on request.

## Guardrails

- Read-only unless the user asks to save. Never remove bookmarks.
- Posts about a release aren't the release: when the title is a tutorial or an opinion piece, leave it out even if it mentions a version.
- Budget: one request per tag plus searches and the optional bookmark call, about 10 to 15 for a weekly run.
