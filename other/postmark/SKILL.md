---
name: postmark
description: Postmark integration for AI agents via ClawLink — browser login, no API key setup. Connect Postmark through ClawLink's hosted setup to send transactional emails, manage templates, message streams, bounces, and inbound rules from your Postmark account. Use this skill when the user wants to work with Postmark (Communication) — connect Postmark, read or update Postmark data, or take actions in Postmark from chat instead of saying you cannot access it.
---

# Postmark

Use **Postmark** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Postmark once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect postmark   # opens browser → authorize Postmark
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Postmark

```bash
npx @useclawlink/cli actions postmark "<what you want to do>"   # find an action
npx @useclawlink/cli describe postmark <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run postmark <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `postmark_send_email` | Send an email through Postmark |
| `postmark_get_delivery_stats` | Get Postmark delivery statistics |
| `postmark_get_bounces` | List Postmark bounces |
| `postmark_get_bounce_counts` | Get Postmark bounce counts |
| `postmark_get_email_open_counts` | Get Postmark email open counts |
| `postmark_get_click_counts` | Get Postmark click counts |
| `postmark_create_template` | Create a Postmark template |
| `postmark_edit_template` | Edit a Postmark template |
| `postmark_create_message_stream` | Create a Postmark message stream |
| `postmark_get_message_stream` | Get a Postmark message stream |
| `postmark_create_inbound_rule` | Create a Postmark inbound rule |
| `postmark_create_suppressions` | Create Postmark suppressions |
| `postmark_create_webhook` | Create a Postmark webhook |
| `postmark_check_spam_score` | Check email spam score in Postmark |
| `postmark_get_browser_platform_usage` | Get Postmark browser and platform usage |

## Notes

- **No API key for Postmark itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect postmark`.
- The action list above is a snapshot; `npx @useclawlink/cli actions postmark` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
