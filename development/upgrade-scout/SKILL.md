---
name: upgrade-scout
description: Before you bump a dependency or review a PR that touches one, find out what broke for other people. Pulls migration guides, gotchas and community reactions from daily.dev for the library and version in question.
---

# Upgrade Scout

A dependency bump looks like a one-line diff until it isn't. Upgrade Scout reads what the daily.dev community wrote about the library and version before you run the upgrade, or while you review the PR that does.

## Requirements

One of:

- The daily.dev MCP server (`https://api.daily.dev/mcp`) connected to your agent, or
- A daily.dev personal access token in `DAILY_DEV_TOKEN` (https://daily.dev/settings/api). Base URL `https://api.daily.dev/public/v1`, header `Authorization: Bearer $DAILY_DEV_TOKEN`. Never send the token anywhere except `api.daily.dev`.

Each step lists the MCP tool first and the REST call after it.

## Steps

1. **Work out what changed.** From the user's request, the lockfile diff or the PR diff, list the libraries with a version change, as `name`, `from`, `to`. For a PR review, also list libraries the diff starts using for the first time.
2. **Search with short queries.** For each library call `getSearchPosts` (`GET /search/posts?q=<query>&limit=10`) with two or three words at most: the library name plus the major version, for example `Next.js 16`, then the name plus `migration` or `breaking`. Don't use `/recommend/*` for this: it matches keywords only and returns nothing for natural-language questions.
3. **Widen when thin.** If search gives fewer than 3 relevant posts, resolve the tag with `getSearchTags` (`GET /search/tags?q=<library>`) and read the tag feed with `getFeedsTagByTag` and `limit` 30 (`GET /feeds/tag/{tag}?limit=30`), keeping posts whose summary mentions the version.
4. **Read the arguments.** For the 2 or 3 posts with the most `numComments`, call `getPostsByIdComments` with `limit` 20 (`GET /posts/{id}/comments?limit=20`). Production stories live in the comments.
5. **Write the brief**, per library:
   - **Breaking changes and migration steps** reported, with the version they apply to
   - **Gotchas** people hit after upgrading, especially anything about build tooling, types, runtime behaviour or performance
   - **Verdict**: upgrade now, wait for a patch release, or needs a dedicated migration PR, with the reason
   - **Sources**: post titles linked to `commentsPermalink`, with upvotes and comments
   If the search found nothing substantive, say "no community signal yet" instead of padding.

## Output

Under 150 words per library. Lead with the verdict. For a PR review, end with the two or three questions worth asking the author.

## Guardrails

- Read-only.
- Prefer posts from the last 12 months; flag older material as such because migration advice ages fast.
- Two to five requests per library.
