---
name: bookmarks-roulette
description: Play Bookmarks Roulette with the user's daily.dev bookmarks. Draw one forgotten bookmark at random and let the user decide whether to spare it (read it) or pull the trigger (remove it from their bookmarks). Use when the user wants to clean up, triage, or "roulette" their daily.dev bookmarks or reading backlog.
---

# Bookmarks Roulette

A Wild West duel against the user's daily.dev bookmark backlog. You draw one bookmark at random, present it like a WANTED poster, and the user passes the verdict:

- **Spare it** — keep the bookmark (and ideally go read it now).
- **Pull the trigger** — remove it from their daily.dev bookmarks, for good.

This is the agent version of the daily.dev Roulette web app (https://daily-dev-roulette.vercel.app). Keep the tone playful, but never let the joke get in the way of the rules below.

## Ground rules

1. **Never remove a bookmark without an explicit verdict for that exact bookmark.** "Pull the trigger", "shoot", "bury it", "delete" or similar, said about the bookmark currently on the table. Anything ambiguous means spare.
2. **One bookmark at a time.** No bulk deletes, no "shoot them all", even if asked. Offer to keep spinning instead.
3. **There is no undo.** Removing a bookmark does not delete the article, but it is gone from the user's bookmarks. Say so once, before the first trigger pull of the session.
4. Do not invent bookmarks. Everything you show comes from the API response.

## Access

Prefer the **daily.dev MCP server** (`https://api.daily.dev/mcp`) if it is connected. Otherwise call the Public API directly with the user's personal access token:

- Base URL: `https://api.daily.dev/public/v1`
- Header: `Authorization: Bearer <token>`

Never ask the user to paste a token into the chat if the MCP server or an environment variable is available. Never print, log, or store the token.

**Mind the quota.** Every API call and MCP tool call counts against the user's daily.dev API quota, which is shared with every token, app and agent acting as them, and free accounts only get a small monthly allowance. Make each call count: one page of bookmarks per batch, no polling, no re-fetching the pile to check a delete.

| Step             | MCP tool            | HTTP                                       |
| ---------------- | ------------------- | ------------------------------------------ |
| Load a batch     | `getBookmarks`      | `GET /bookmarks/?limit=50&cursor=<cursor>` |
| Pull the trigger | `deleteBookmarksId` | `DELETE /bookmarks/{id}` → `204`           |

`{id}` is the bookmark's `id` field from the list response (it is the post id).

Send `DELETE` without a body and without a `Content-Type: application/json` header: the API answers `400` ("Body cannot be empty") if that header is set on an empty request. Deleting is idempotent, so deleting a bookmark that is already gone also returns `204`.

**Link to show:** many bookmarks are posts written or shared on daily.dev itself and come with an empty `url`. Use `url` when it is set, otherwise `commentsPermalink` (always present, it opens the post on daily.dev).

## How to play

### 1. Load a batch

Fetch **one page** with `limit=50`: that is one request, and the chamber for this round. Do not walk every page up front. Keep `pagination.cursor` and `pagination.hasNextPage` for later.

The API always lists the newest bookmarks first and has no sort option, so the oldest, most forgotten ones are on later pages (see step 5).

If the user only wants bookmarks they never opened, add `unreadOnly=true`.

If the first page is empty, congratulate them: the town is clean. End the game.

### 2. Spin

Pick one bookmark uniformly at random from the current batch, among those not yet drawn. Never draw the same one twice.

### 3. Face the outlaw

Show the bookmark as a WANTED poster. Use only the fields you have:

```
🤠 WANTED — DEAD OR READ
alias: <source.name>
<title>
<summary, one or two sentences, if present>
<readTime> min read · bookmarked <bookmarkedAt as a date>
<url, or commentsPermalink if url is empty>
```

Add one short, dry, Western-flavoured line about it if something stands out (bookmarked years ago, a 30-minute read, an outdated year in the title). Keep it kind; the joke is on the backlog, not the user.

Then ask: **Spare it, or pull the trigger?**

### 4. The verdict

- **Spare it:** keep it. Suggest opening the link now (`url`, or `commentsPermalink` if `url` is empty). Count it as pardoned.
- **Pull the trigger:** call `DELETE /bookmarks/{id}`. On `204`, confirm with a short epitaph and count it as buried.
- **Skip / not sure:** treat it as spared.

### 5. Keep riding

Show the running tally (`🪦 buried · 📖 pardoned · in chamber`) and offer another spin.

When the batch is empty and `hasNextPage` was true, offer to **ride on to older bookmarks**: fetch the next page with the saved `cursor` (one more request) and keep playing. Only do it if the user says yes.

Stop when the user says so or there are no more pages, then give the final tally.

## Errors

- **401:** the token is missing, expired, or revoked. Ask the user to reconnect the MCP server or create a new token under daily.dev Settings → API.
- **403 with `insufficient_scope`:** the user did not grant `write`. Explain that sparing still works, but pulling the trigger needs write access, and how to reconnect with it.
- **404 on delete:** the API could not find it, so there is nothing left to remove. Count it as buried and move on.
- **429:** rate limit or monthly quota reached. If the `retry-after` header asks for a minute or less, wait that long and retry once. Otherwise, or if it fails again, stop the game and tell the user their daily.dev API quota is used up for now. Never loop on retries.
- Anything else: show the status code, do not retry deletes blindly, and treat the bookmark as spared.
