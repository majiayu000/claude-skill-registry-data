---
name: resend
description: Resend integration for AI agents via ClawLink — browser login, no API key setup. Connect Resend through ClawLink's hosted setup to send emails, manage audiences, contacts, templates, and domains without manual API key setup. Use this skill when the user wants to work with Resend (Communication) — connect Resend, read or update Resend data, or take actions in Resend from chat instead of saying you cannot access it.
---

# Resend

Use **Resend** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Resend once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect resend   # opens browser → authorize Resend
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Resend

```bash
npx @useclawlink/cli actions resend "<what you want to do>"   # find an action
npx @useclawlink/cli describe resend <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run resend <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `resend_send_email` | Send an email through Resend |
| `resend_get_email` | Get a Resend email by ID |
| `resend_create_audience` | Create a Resend audience |
| `resend_get_audience` | Get a Resend audience by ID |
| `resend_list_audiences` | List Resend audiences |
| `resend_create_contact` | Create a Resend contact |
| `resend_get_contact` | Get a Resend contact by ID |
| `resend_list_contacts` | List Resend contacts in an audience |
| `resend_delete_contact` | Delete a Resend contact |
| `resend_create_domain` | Create a Resend domain |
| `resend_get_domain` | Get a Resend domain by ID |
| `resend_list_domains` | List Resend domains |
| `resend_create_template` | Create a Resend email template |
| `resend_get_template` | Get a Resend email template |
| `resend_list_templates` | List Resend email templates |

## Notes

- **No API key for Resend itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect resend`.
- The action list above is a snapshot; `npx @useclawlink/cli actions resend` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
