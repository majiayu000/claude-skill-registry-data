---
name: inbox-zero
description: Summarizes your daily.dev notifications in one short briefing, grouped by what needs you (replies, mentions, squad reviews) versus what's just news, and marks them read when you say so.
---

# Inbox Zero

Notifications pile up faster than you read them. Inbox Zero turns the backlog into one briefing and clears it on your command.

## Requirements

One of:

- The daily.dev MCP server (`https://api.daily.dev/mcp`) connected to your agent (add the `write` scope to mark notifications read), or
- A daily.dev personal access token in `DAILY_DEV_TOKEN` (https://daily.dev/settings/api). Base URL `https://api.daily.dev/public/v1`, header `Authorization: Bearer $DAILY_DEV_TOKEN`. Never send the token anywhere except `api.daily.dev`.

Each step lists the MCP tool first and the REST call after it.

## Steps

1. **Count first.** `getNotificationsUnreadCount` (`GET /notifications/unread/count`). If it's zero, say so and stop.
2. **Fetch.** `getNotifications` with `limit` 50 (`GET /notifications?limit=50`); page with `cursor` while `readAt` is null and the count isn't covered yet. Each notification has `type`, `title` (may contain HTML tags, strip them), `description`, `targetUrl`, `avatars` and `attachments`.
3. **Triage by `type`** into three buckets:
   - **Needs you**: replies and mentions (`comment_reply`, `comment_mention`, `post_mention`), squad moderation (`source_post_submitted`, member requests), anything addressed to you personally.
   - **Social**: upvotes, awards, milestones, new followers.
   - **Content**: new posts in sources and squads you follow (`source_post_added`), agent and briefing digests (`interest_content_batch`), announcements.
   Unknown types go to **Other** with their raw `type` shown.
4. **Write the briefing.** Needs-you items one per line with a link (`targetUrl`) and who it's from. Social collapsed into one sentence with counts. Content as a short list of the most relevant titles (use `attachments[].title` when present), max 8, link each. Lead with the needs-you count.
5. **Offer to clear.** Ask: "Mark all N as read?" Only on a yes, call `postNotificationsRead` (`POST /notifications/read`). It marks every notification read; there is no per-item variant, so never call it before the user has seen the needs-you list.

## Output

Under 200 words for a typical backlog. Three headers, links on everything actionable, then the clear prompt.

## Guardrails

- Never mark read without an explicit yes in the same conversation.
- Don't act on notifications (no replying, approving or following); link them so the user can.
- Two or three requests to read, one to clear.
