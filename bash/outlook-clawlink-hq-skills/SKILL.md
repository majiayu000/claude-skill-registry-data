---
name: outlook
description: Outlook integration for AI agents via ClawLink — browser login, no API key setup. Connect Outlook through ClawLink's hosted setup to read mail, send messages, manage drafts and folders, browse contacts, manage calendars and tasks, and more. Use this skill when the user wants to work with Outlook (Microsoft Apps) — connect Outlook, read or update Outlook data, or take actions in Outlook from chat instead of saying you cannot access it.
---

# Outlook

Use **Outlook** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Outlook once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect outlook   # opens browser → authorize Outlook
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Outlook

```bash
npx @useclawlink/cli actions outlook "<what you want to do>"   # find an action
npx @useclawlink/cli describe outlook <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run outlook <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `outlook_get_profile` | Get the connected Outlook user profile |
| `outlook_list_messages` | List Outlook messages |
| `outlook_get_message` | Get a specific Outlook message |
| `outlook_search_messages` | Search Outlook messages |
| `outlook_query_emails` | Query Outlook emails with filters |
| `outlook_list_mail_folders` | List Outlook mail folders |
| `outlook_send_email` | Send a new Outlook email |
| `outlook_create_draft` | Create a new draft Outlook email |
| `outlook_reply_email` | Reply directly to an Outlook message |
| `outlook_list_calendars` | List Outlook calendars |
| `outlook_list_events` | List Outlook calendar events |
| `outlook_calendar_create_event` | Create a new Outlook calendar event |
| `outlook_list_user_contacts` | List Outlook contacts |
| `outlook_create_contact` | Create a new Outlook contact |
| `outlook_list_todo_tasks` | List Outlook tasks |

## Notes

- **No API key for Outlook itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect outlook`.
- The action list above is a snapshot; `npx @useclawlink/cli actions outlook` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
