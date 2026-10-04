---
description: Post your open PRs to today's daily PR review thread in Slack. Use when asked to "post PRs", "share PRs for review", "PR thread", "daily PR post", or "slack PRs".
---

Post the user's open PRs to a daily PR review thread in Slack.

## Arguments

- **channel**: Slack channel ID or name. Default: `C09QX29JEQ5` (Retirement Dev Infra daily thread). The user may pass a different channel ID or name — use `slack_search_channels` to resolve names to IDs if needed.

## PR Format

This is the canonical format. Every PR line must follow it exactly:

```
:pr: <https://github.com/org/repo/pull/NUMBER|[TICKET-ID] Short PR title>
```

- Extract the ticket ID from the PR title if present (e.g., `[TICKET-1234]`). Keep it in square brackets.
- If no ticket ID in the title, omit the bracket prefix — just use the title as-is.
- One PR per line. No bullet points, no numbering.
- All selected PRs go in a single message (unless the user asks for individual messages).
- Do NOT append "Sent using Slack MCP" — the Slack MCP integration adds this automatically.

## Steps

### 1. Collect open PRs

Search across all orgs the user has access to:

```bash
gh search prs --author @me --state open --json repository,title,url,number --limit 50
```

Filter to work-relevant repos (your-org/*). Present a numbered list and ask which to post. The user may say "all", list numbers, or exclude specific ones. Wait for confirmation.

### 2. Find today's thread

Read the target channel using `slack_read_channel` with a limit of 10. Look for the most recent parent message posted today that contains "PRs that need :eyes: today" or similar daily-thread language. This is typically posted by a workflow bot.

The `message_ts` of this parent message is the thread to reply to.

If no thread is found for today, tell the user and stop.

### 3. Post

Use `slack_send_message` with:
- `channel_id`: the resolved channel ID
- `thread_ts`: the parent message's timestamp
- `message`: the formatted PR list

### 4. Confirm

Return the Slack message link to the user.
