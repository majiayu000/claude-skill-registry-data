---
name: tweetclaw-twitter-automation
description: "Guide agents through approved TweetClaw workflows for X/Twitter automation, including tweet scraping, reply search, follower export, user lookup, media, DMs, monitors, webhooks, giveaway draws, and confirmation-gated posts or replies."
---

# TweetClaw Twitter Automation

Use TweetClaw when a user asks an agent to work with X/Twitter through Xquik or the TweetClaw OpenClaw plugin.

## When to Use

Use this skill when the user asks for:
- Scraping tweets, threads, replies, quotes, mentions, likes, or media
- Searching tweets or tweet replies
- Looking up users, followers, following, or verified followers
- Posting tweets, replying to tweets, or uploading media after approval
- Reading or sending direct messages after account authorization
- Creating monitors, webhooks, or giveaway draws
- Checking which TweetClaw or Xquik endpoint can perform a task

## Do not use

Do not use this skill for:
- Spam, harassment, deceptive engagement, impersonation, or platform evasion
- Bulk unsolicited DMs, mass follows, mass likes, mass retweets, or engagement farming
- X ads, analytics dashboards, or scheduling features that TweetClaw does not provide
- Writing actions when only read-only access is configured
- Accessing private or account-scoped data without clear user authorization
- Asking users to paste API keys, signing keys, cookies, or tokens into chat

## Instructions

1. Restate the user job as one workflow: read, extraction, write, media, DM, monitor, webhook, draw, or discovery.
2. Check current docs before install, configuration, limits, or API details matter:
   - [TweetClaw GitHub](https://github.com/Xquik-dev/tweetclaw)
   - [Xquik docs](https://docs.xquik.com)
   - [TweetClaw npm registry metadata](https://registry.npmjs.org/@xquik%2ftweetclaw)
3. For OpenClaw installs, prefer the explicit npm selector:

```bash
openclaw plugins install npm:@xquik/tweetclaw
```

4. After install or update, verify the runtime before live work:

```bash
openclaw plugins inspect tweetclaw --runtime --json
openclaw skills info tweetclaw
```

5. Keep credentials in the Xquik dashboard, OpenClaw plugin config, or environment-backed secret storage. Never print or echo credential values.
6. Use TweetClaw discovery or Xquik docs to choose the smallest endpoint and request limit that satisfies the user.
7. Before any visible, state-changing, private, paid, recurring, extraction, monitor, webhook, draw, or account-scoped action, summarize the target, account, action, limits, data handling, and usage impact if available. Wait for explicit confirmation.
8. For posting or replying, show the final text and media list before sending. Do not add links, mentions, hashtags, or claims the user did not request.
9. For monitors and webhooks, state the target, event types, delivery behavior, and how the user can stop the resource.
10. Return concise results with IDs, URLs, counts, and any partial failures.

## Common Workflows

### Search Tweets

Use TweetClaw when the user needs X/Twitter search from an agent. Keep the query narrow, choose a result limit, and summarize returned tweet IDs, URLs, authors, timestamps, and matched text.

### Export Followers

Confirm the account or profile, the requested limit, and whether the user needs raw rows or a summary. Keep private account data scoped to the user's authorization.

### Post a Tweet

Show the exact tweet text and attached media. Ask for confirmation before sending. Report the created tweet URL after the action succeeds.

### Monitor Activity

Create a monitor only after the user confirms the account, keyword, or event target. Explain what will be watched and how results will be delivered.
