---
name: zendesk
description: Zendesk integration for AI agents via ClawLink — browser login, no API key setup. Connect Zendesk through ClawLink's hosted setup to manage tickets, users, organizations, automations, macros, and custom objects. Use this skill when the user wants to work with Zendesk (Support) — connect Zendesk, read or update Zendesk data, or take actions in Zendesk from chat instead of saying you cannot access it.
---

# Zendesk

Use **Zendesk** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Zendesk once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect zendesk   # opens browser → authorize Zendesk
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Zendesk

```bash
npx @useclawlink/cli actions zendesk "<what you want to do>"   # find an action
npx @useclawlink/cli describe zendesk <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run zendesk <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `zendesk_create_zendesk_ticket` | Create a new Zendesk ticket |
| `zendesk_create_many_tickets` | Create multiple Zendesk tickets in bulk |
| `zendesk_apply_zendesk_macro` | Preview how a Zendesk macro would affect a ticket |
| `zendesk_autocomplete_users` | Search for Zendesk users by name prefix |
| `zendesk_create_automation` | Create a new automation in Zendesk |
| `zendesk_create_custom_object_record` | Create a new custom object record |
| `zendesk_count_zendesk_organizations` | Count the number of organizations in Zendesk |

## Notes

- **No API key for Zendesk itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect zendesk`.
- The action list above is a snapshot; `npx @useclawlink/cli actions zendesk` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
