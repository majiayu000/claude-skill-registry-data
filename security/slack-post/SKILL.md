---
name: slack-post
description: >-
  Post or send a message to Slack — a channel, DM, or thread reply. Triggers on "post / send /
  message / DM / reply / drop this in Slack", "tell #channel", "ping @someone on Slack", or any
  request to write into Slack (as opposed to reading/searching it). Governs posting IDENTITY:
  posts as YOU (user token) by default, and as the BOT only when the prompt says so ("as the bot",
  "use the bot", "post as the app"). Every Claude-sent message gets a "Sent using Claude" footer.
  Read-only Slack work (search, history, who's-in-a-channel) does NOT use this skill.
allowed-tools: mcp__plugin_adk_slack__conversations_add_message, mcp__plugin_adk_slack-bot__conversations_add_message, mcp__plugin_adk_slack__channels_list, mcp__plugin_adk_slack__conversations_search_messages, mcp__plugin_adk_slack__users_search, AskUserQuestion
argument-hint: "<message> --to <#channel|@user|channelID> [--as bot|user] [--thread <ts>]"
---

# slack-post — write a message to Slack with the right identity

Posting to Slack happens under **one of two identities**, and the choice is not cosmetic — it changes who the workspace sees as the author, what the message can @-mention, and which audit trail it lands in. This skill makes that choice explicit and consistent.

## The two identities

The plugin runs **two** Slack MCP servers, each pinned to one identity:

| Identity | Server | Tool | Posts as | When |
|---|---|---|---|---|
| **User** (default) | `slack` | `mcp__plugin_adk_slack__conversations_add_message` | **you** (your xoxp user token) | default — every post unless the prompt asks for the bot |
| **Bot** | `slack-bot` | `mcp__plugin_adk_slack-bot__conversations_add_message` | the Slack **app/bot** (xoxb token) | only when the prompt explicitly asks |

> Why two servers: the underlying `slack-mcp-server` cannot switch identity per call — with both tokens present it always prefers the user token. So the bot identity lives in its own server (`slack-bot`, launched with the bot token only, exposing just the post tool).

## Decision: which identity?

**Default to the user.** Post via `slack` unless the prompt clearly opts into the bot. Signals that mean *use the bot*:

- "post **as the bot** / **as the app** / **using the bot**"
- "**use the bot** to send this"
- an explicit `--as bot`

Anything else — including silence — means **post as you**. Do not ask which identity to use; the default is user. (If the prompt is genuinely ambiguous — e.g. "have the bot or me post, whichever" — then, and only then, ask with `AskUserQuestion`.)

When you post as the bot, the bot must already be a member of the target channel, or Slack rejects the post (`not_in_channel`). If that happens, say so and suggest inviting the app — don't silently fall back to the user identity.

## Always: the footer

**Every** message this skill sends — user or bot — ends with the footer:

```
_Sent using Claude_
```

Append it as the final line, separated by a blank line:

```
<the message body>

_Sent using Claude_
```

This is non-negotiable and applies to both identities. (To change the footer text, edit the line above — it is the single source of truth.)

## Steps

1. **Resolve the target.** Turn `--to` / "#channel" / "@user" into a channel or user ID if needed (`channels_list`, `users_search` on the `slack` server). A thread reply needs the parent `thread_ts`.
2. **Pick the identity** per the decision rule above. Default user; bot only on explicit request.
3. **Compose the body**, then append the `Sent using Claude` footer as the final line.
4. **Post** via the matching tool:
   - user → `mcp__plugin_adk_slack__conversations_add_message`
   - bot → `mcp__plugin_adk_slack-bot__conversations_add_message`
5. **Confirm back** to the human: which channel, which identity, and a link/ts if returned. If Slack rejected the post (e.g. `not_in_channel`, `channel_not_found`), report the raw error and the fix — never retry under a different identity to "make it work".

## Rules

- **Posting is outward-facing.** Show the human the exact message text and the resolved target+identity, and post only on a clear instruction to send. If they're still drafting, draft — don't send.
- **Never escalate identity to dodge an error.** A bot `not_in_channel` failure is reported, not worked around by quietly posting as the user (that changes the author the recipient sees).
- **No mass posting.** This skill sends the message the human asked for, to the target(s) they named — not a fan-out across channels.
- **Reads don't belong here.** Searching, fetching history, or listing members is the `slack` server's read tools directly — no skill, no footer, no identity decision.
