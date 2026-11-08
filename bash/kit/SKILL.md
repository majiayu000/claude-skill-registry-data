---
name: kit
description: Kit integration for AI agents via ClawLink — browser login, no API key setup. Connect Kit through ClawLink's hosted setup to manage subscribers, broadcasts, tags, forms, and custom fields from your Kit account. Use this skill when the user wants to work with Kit (Marketing) — connect Kit, read or update Kit data, or take actions in Kit from chat instead of saying you cannot access it.
---

# Kit

Use **Kit** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Kit once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect kit   # opens browser → authorize Kit
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Kit

```bash
npx @useclawlink/cli actions kit "<what you want to do>"   # find an action
npx @useclawlink/cli describe kit <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run kit <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `kit_get_account` | Get the connected Kit account |
| `kit_get_subscriber` | Get a Kit subscriber by ID |
| `kit_create_subscriber` | Create a Kit subscriber |
| `kit_filter_subscribers` | Filter Kit subscribers |
| `kit_list_broadcasts` | List Kit broadcasts |
| `kit_get_broadcast` | Get a Kit broadcast by ID |
| `kit_create_broadcast` | Create a Kit broadcast |
| `kit_get_broadcast_stats` | Get Kit broadcast statistics |
| `kit_list_custom_fields` | List Kit custom fields |
| `kit_create_custom_field` | Create a Kit custom field |
| `kit_create_tag` | Create a Kit tag |
| `kit_list_tags` | List Kit tags |
| `kit_list_forms` | List Kit forms |
| `kit_get_email_stats` | Get Kit email statistics |
| `kit_get_growth_stats` | Get Kit growth statistics |

## Notes

- **No API key for Kit itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect kit`.
- The action list above is a snapshot; `npx @useclawlink/cli actions kit` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
