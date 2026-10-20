---
name: community-check
description: Before you adopt a tool or technique, find out what the daily.dev community actually thinks. Reads the most-discussed posts and their comment threads on a topic and summarizes the consensus, the dissent, and the gotchas, with sources.
---

# Community Check

Answer the question "what do developers on daily.dev actually think about X?" by reading discussions, not just articles. Articles tell you what authors claim; comment threads tell you what happened in production.

## Requirements

One of:

- The daily.dev MCP server (`https://api.daily.dev/mcp`) connected to your agent, or
- A daily.dev personal access token in `DAILY_DEV_TOKEN` (create one at https://daily.dev/settings/api). Base URL `https://api.daily.dev/public/v1`, header `Authorization: Bearer $DAILY_DEV_TOKEN`. Never send the token anywhere except `api.daily.dev`.

Each step below lists the MCP tool first and the REST call after it.

## Steps

1. **Find the posts.** Run both and merge:
   - `getSearchPosts` with `q` set to the topic and `limit` 15 (REST: `GET /search/posts?q=<topic>&limit=15`).
   - `getFeedsDiscussed` with `limit` 20 and `period` 30, filtered with `tag` when the topic is a known tag (REST: `GET /feeds/discussed?limit=20&period=30&tag=<tag>`). Use `getSearchTags` (`GET /search/tags?q=`) to confirm the tag name first.
2. **Pick the conversations.** From the merged list keep the 4–6 posts with the most `numComments`. Ignore posts with fewer than 3 comments.
3. **Read the threads.** For each kept post call `getPostsByIdComments` with `limit` 30 (REST: `GET /posts/{id}/comments?limit=30`). Read replies too, they are nested under `children`.
4. **Synthesize.** Group what you read into:
   - **Consensus**: claims repeated across threads by different people.
   - **Dissent**: credible disagreement, with the strongest version of the argument.
   - **Gotchas from production**: specific failures, migrations, costs, performance numbers.
   - **Open questions**: things people asked that nobody answered well.
5. **Cite.** Every claim gets the post title linked to its `commentsPermalink`. Quote comments sparingly and attribute them by `author.username`.

## Output

Keep it under 400 words unless asked for more. Lead with a one-sentence verdict, then the four groups, then a "Sources" list. Include upvote and comment counts next to each source so the reader can judge weight.

## Guardrails

- Read-only. Don't upvote, bookmark or comment.
- If fewer than two posts have real discussion, say so instead of inventing a consensus.
- Each call uses one request of the user's daily.dev API quota. Stay under ~10 calls per check.
