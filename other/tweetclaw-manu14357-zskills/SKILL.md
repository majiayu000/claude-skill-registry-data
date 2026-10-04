---
name: tweetclaw
description: Use TweetClaw through OpenClaw for X/Twitter automation workflows, including tweet search, reply search, follower export, media handling, monitors, webhooks, giveaway draws, and approval-gated posting.
category: automation
agents:
  - openclaw
  - codex
  - claude-code
author: Xquik
---

# TweetClaw

TweetClaw is the Xquik OpenClaw plugin for structured X/Twitter automation. Use it when an agent needs a reviewed tool path for tweet scraper workflows, tweet search, reply search, user lookup, follower export, media upload, media download, direct messages, monitors, webhooks, giveaway draws, or approved posting.

## When to Use

Use this skill when the user asks to:

- Search tweets, search tweet replies, or inspect tweet threads
- Look up X/Twitter users, export followers, or review account activity
- Upload media, download tweet media, or prepare media for a post
- Monitor accounts or keywords and send webhook notifications
- Run a giveaway draw from tweet replies or engagement rules
- Post tweets, post replies, send DMs, or update profiles after explicit approval
- Use the TweetClaw OpenClaw plugin or `@xquik/tweetclaw` package from an agent

## When NOT to Use

- Do not use TweetClaw for spam, harassment, deceptive engagement, impersonation, credential collection, platform evasion, mass unsolicited DMs, or bulk follow, like, or retweet campaigns.
- Do not use it for unapproved posting, profile edits, DMs, webhooks, monitors, or recurring actions.
- Do not use read-only pay-per-use mode for writes, uploads, DMs, profile changes, monitors, webhooks, or account-backed actions.
- Do not paste API keys, signing keys, cookies, passwords, or account credentials into chat, docs, logs, or skill files.

## Setup

Install the OpenClaw plugin:

```bash
openclaw plugins install npm:@xquik/tweetclaw
```

Verify the runtime before live work:

```bash
openclaw plugins inspect tweetclaw --runtime --json
openclaw skills info tweetclaw
```

Store credentials in OpenClaw plugin config. Treat all API keys and signing keys as sensitive config. If credentials are missing, use setup guidance instead of asking the user to reveal secrets in chat.

## Workflow

1. Clarify the user's X/Twitter goal, account, target, limits, and expected output.
2. Use TweetClaw docs at https://docs.xquik.com when endpoint parameters, response shapes, limits, or billing details matter.
3. Use `explore` first when you need to find the relevant endpoint family.
4. Before any visible, state-changing, private, paid, extraction, recurring, monitor, webhook, or write action, summarize:
   - target account or resource
   - action to perform
   - final text and media when relevant
   - requested limit or recurring behavior
   - estimated credit usage or account effect
5. Wait for explicit confirmation before invoking the action.
6. Redact credentials and avoid exposing sensitive personal data unless the user explicitly requests that specific data and is authorized to access it.

## Tooling Notes

- `explore` lists available endpoint descriptors without credentials or network calls.
- `tweetclaw` invokes one allowed Xquik API endpoint through the configured OpenClaw plugin runtime.
- MPP mode is read-only and suitable only for supported read endpoints.
- Account-backed mode is required for posting, DMs, uploads, profile updates, monitors, webhooks, and other write-like workflows.

## Examples

**User:** "Search tweets about OpenClaw plugins from the last week."

**AI behavior:** Use `explore` to find tweet search, confirm search scope and limit if needed, then use TweetClaw to return concise results.

**User:** "Post this launch tweet from my connected account."

**AI behavior:** Show the exact account, final tweet text, media list, and estimated credit usage. Wait for explicit approval before posting.

**User:** "Monitor @example for new posts and call my webhook."

**AI behavior:** Explain the monitor target, webhook behavior, event scope, and recurrence. Wait for explicit approval before creating the monitor.

## Origin

https://github.com/Xquik-dev/tweetclaw/tree/master/skills/tweetclaw
