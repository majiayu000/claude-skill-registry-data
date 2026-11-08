---
name: intercom
description: Intercom integration for AI agents via ClawLink — browser login, no API key setup. Connect Intercom through ClawLink's hosted setup to manage conversations, contacts, companies, tags, articles, and data events. Use this skill when the user wants to work with Intercom (Support) — connect Intercom, read or update Intercom data, or take actions in Intercom from chat instead of saying you cannot access it.
---

# Intercom

Use **Intercom** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Intercom once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect intercom   # opens browser → authorize Intercom
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Intercom

```bash
npx @useclawlink/cli actions intercom "<what you want to do>"   # find an action
npx @useclawlink/cli describe intercom <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run intercom <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `intercom_create_contact` | Create a new contact in Intercom |
| `intercom_create_conversation` | Create a new conversation in Intercom |
| `intercom_assign_conversation` | Assign a conversation to an admin or team |
| `intercom_close_conversation` | Close a conversation in Intercom |
| `intercom_add_tag_to_contact` | Add a tag to a contact in Intercom |
| `intercom_attach_contact_to_company` | Attach a contact to a company in Intercom |
| `intercom_create_an_article` | Create a new article in Intercom |
| `intercom_create_data_event` | Submit a data event to Intercom |

## Notes

- **No API key for Intercom itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect intercom`.
- The action list above is a snapshot; `npx @useclawlink/cli actions intercom` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
