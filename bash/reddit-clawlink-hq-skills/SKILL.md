---
name: reddit
description: Reddit integration for AI agents via ClawLink — browser login, no API key setup. Connect reddit through ClawLink's hosted setup. Use this skill when the user wants to work with Reddit (Social Media) — connect Reddit, read or update Reddit data, or take actions in Reddit from chat instead of saying you cannot access it.
---

# Reddit

Use **Reddit** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Reddit once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect reddit   # opens browser → authorize Reddit
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Reddit

```bash
npx @useclawlink/cli actions reddit "<what you want to do>"   # find an action
npx @useclawlink/cli describe reddit <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run reddit <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `reddit_create_reddit_post` | Creates a new text or link post on a specified, existing Reddit subreddit, optionally applying a flair. Immediately publishes publicly visible content — confirm subreddit, title, and body with the user before executing. Posts may be silently removed post-submission by automoderator or subreddit rules (errors: SUBMIT_VALIDATION_BODY_BLACKLISTED_STRING, POST_GUIDANCE_VALIDATION_FAILED); verify visibility via the returned permalink. Rapid consecutive calls trigger RATELIMIT errors with cooldown hints. |
| `reddit_delete_reddit_comment` | Deletes a Reddit comment, identified by its fullname ID, if it was authored by the authenticated user. Deletion is permanent and irreversible. |
| `reddit_delete_reddit_post` | Permanently and irreversibly deletes a Reddit post by its ID. Confirm with the user before calling. Only works on posts authored by the authenticated account; attempting to delete another user's post will fail. |
| `reddit_edit_reddit_comment_or_post` | Edits the body text of the authenticated user's own existing comment or self-post on Reddit; cannot edit link posts or titles. |
| `reddit_get` | Tool to retrieve a listing of Reddit posts sorted by the specified criteria (hot, new, top, etc.). Use when you need to get posts from the Reddit front page or all of Reddit with a specific sort order. Supports pagination and time filtering for top/controversial sorts. |
| `reddit_get_controversial_posts` | Tool to retrieve controversial posts from all subreddits with time filters. Use when you need to find the most controversial posts across Reddit from a specific time period (hour, day, week, month, year, or all-time). Returns a paginated listing of posts ranked by controversy within the specified time frame. |
| `reddit_get_me_prefs` | Tool to retrieve preference settings of the logged in user. Use when you need to check user preferences or settings. |
| `reddit_get_r_top` | Tool to retrieve top-rated posts from a subreddit with time filters. Use when you need to find the most popular posts from a specific time period (hour, day, week, month, year, or all-time). Returns a paginated listing of posts ranked by score within the specified time frame. |
| `reddit_get_random` | Tool to retrieve a random public Reddit post from any subreddit. Use when you want to discover serendipitous content or need a random post for testing or entertainment purposes. |
| `reddit_get_reddit_user_about` | Retrieves information about a specified Reddit user account, including karma scores and gold status. Use when you need to get profile information for any public Reddit user. |
| `reddit_get_scopes` | Tool to retrieve all available OAuth scopes supported by the Reddit API. Use when you need to understand what permissions are available or check scope definitions. |
| `reddit_get_subreddit_rules` | Fetch the explicit posting rules for a subreddit to ensure compliance before posting or commenting. Use when you need to verify content meets community guidelines or explain subreddit requirements to users. |

## Notes

- **No API key for Reddit itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect reddit`.
- The action list above is a snapshot; `npx @useclawlink/cli actions reddit` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
