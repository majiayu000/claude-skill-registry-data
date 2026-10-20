---
name: hot-take-drafter
description: Finds the most-argued post on daily.dev this week, lays out both sides from the comment thread, and drafts a spicy-but-fair take you can post. For when you want to join the conversation with something better than "this".
---

# Hot Take Drafter

Every week there's one post the whole community piles onto. Hot Take Drafter finds it, reads the fight, and drafts your entry.

## Requirements

One of:

- The daily.dev MCP server (`https://api.daily.dev/mcp`) connected to your agent, or
- A daily.dev personal access token in `DAILY_DEV_TOKEN` (https://daily.dev/settings/api). Base URL `https://api.daily.dev/public/v1`, header `Authorization: Bearer $DAILY_DEV_TOKEN`. Never send the token anywhere except `api.daily.dev`.

Each step lists the MCP tool first and the REST call after it.

## Steps

1. **Find the fight.** `getFeedsDiscussed` with `period` 7 and `limit` 10 (`GET /feeds/discussed?period=7&limit=10`). The period is 7, 30 or 365 days; there is no "today" option, so this is always "this week". Add `tag` to stay inside a topic (`&tag=typescript`). Pick the post with the highest comments-to-upvotes ratio among the top 5 by `numComments`; that's where people disagree rather than applaud.
2. **Read the thread.** `getPostsByIdComments` with `limit` 50 (`GET /posts/{id}/comments?limit=50`), including `children`. Identify the two or three camps, the single most-upvoted comment per camp, and any factual correction that settles part of the argument.
3. **Lay it out** for the user: the post title, one paragraph of what's being argued, then each camp in two lines with its best quote attributed by `author.username`.
4. **Draft the take.** Three options, each under 80 words, in the user's voice if they gave examples:
   - **The contrarian**: disagrees with the majority camp, with one concrete reason.
   - **The synthesis**: "both sides are missing X".
   - **The question**: the sharpest unanswered question in the thread.
   Each must be defensible from the thread or the post itself. No insults, no dunking on a named commenter.
5. **Hand over the link** to `commentsPermalink` so the user can post the take themselves.

## Output

The layout from step 3, then the three drafts, then the link. Under 350 words total.

## Guardrails

- Read-only. This skill never posts, upvotes or comments; the user does.
- Fair means fair: if the majority camp is simply right, say so and offer the synthesis and the question only.
- Two requests per run.
