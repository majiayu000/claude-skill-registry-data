---
name: gmail
description: Gmail integration for AI agents via ClawLink — browser login, no API key setup. Connect Gmail through ClawLink's hosted setup to send emails, read messages, manage drafts and labels, and search your inbox. Use this skill when the user wants to work with Gmail (Google Apps) — connect Gmail, read or update Gmail data, or take actions in Gmail from chat instead of saying you cannot access it.
---

# Gmail

Use **Gmail** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Gmail once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect gmail   # opens browser → authorize Gmail
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Gmail

```bash
npx @useclawlink/cli actions gmail "<what you want to do>"   # find an action
npx @useclawlink/cli describe gmail <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run gmail <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `gmail_send_email` | Send a Gmail message |
| `gmail_fetch_emails` | Search and fetch Gmail messages |
| `gmail_fetch_message_by_message_id` | Get a Gmail message by ID |
| `gmail_fetch_message_by_thread_id` | Get a Gmail message by thread ID |
| `gmail_create_email_draft` | Create a Gmail draft |
| `gmail_reply_to_thread` | Reply to a Gmail thread |
| `gmail_forward_message` | Forward a Gmail message |
| `gmail_get_profile` | Get the connected Gmail account profile |
| `gmail_list_labels` | List Gmail labels |
| `gmail_create_label` | Create a Gmail label |
| `gmail_add_label_to_email` | Add a label to a Gmail message |
| `gmail_list_drafts` | List Gmail drafts |
| `gmail_get_attachment` | Get a Gmail attachment |
| `gmail_list_threads` | List Gmail threads |
| `gmail_list_send_as` | List Gmail send-as aliases |

## Notes

- **No API key for Gmail itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect gmail`.
- The action list above is a snapshot; `npx @useclawlink/cli actions gmail` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
