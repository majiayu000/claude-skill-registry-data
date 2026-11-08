---
name: sendgrid
description: SendGrid integration for AI agents via ClawLink — browser login, no API key setup. Connect SendGrid through ClawLink's hosted setup to manage contacts, lists, campaigns, templates, and send transactional and marketing emails without manual API key setup. Use this skill when the user wants to work with SendGrid (Communication) — connect SendGrid, read or update SendGrid data, or take actions in SendGrid from chat instead of saying you cannot access it.
---

# SendGrid

Use **SendGrid** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect SendGrid once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect sendgrid   # opens browser → authorize SendGrid
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using SendGrid

```bash
npx @useclawlink/cli actions sendgrid "<what you want to do>"   # find an action
npx @useclawlink/cli describe sendgrid <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run sendgrid <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `sendgrid_get_a_user_s_account_information` | Get SendGrid account information |
| `sendgrid_get_all_single_sends` | List SendGrid single sends |
| `sendgrid_create_a_campaign` | Create a SendGrid campaign |
| `sendgrid_send_a_single_send` | Send a SendGrid single send email |
| `sendgrid_get_all_contacts` | List SendGrid contacts |
| `sendgrid_add_or_update_a_contact` | Add or update a SendGrid contact |
| `sendgrid_create_a_list` | Create a SendGrid contact list |
| `sendgrid_get_all_field_definitions` | List SendGrid custom field definitions |
| `sendgrid_get_all_sender_identities` | List SendGrid sender identities |
| `sendgrid_send_mail` | Send an email through SendGrid |
| `sendgrid_create_a_custom_field` | Create a SendGrid custom field |
| `sendgrid_get_all_categories` | List SendGrid email categories |
| `sendgrid_create_a_transactional_template` | Create a SendGrid transactional email template |
| `sendgrid_get_all_email_templates` | List SendGrid email templates |
| `sendgrid_get_all_automation_stats` | Get SendGrid automation statistics |

## Notes

- **No API key for SendGrid itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect sendgrid`.
- The action list above is a snapshot; `npx @useclawlink/cli actions sendgrid` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
