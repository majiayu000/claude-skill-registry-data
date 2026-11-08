---
name: airtable
description: Airtable integration for AI agents via ClawLink — browser login, no API key setup. Connect Airtable through ClawLink's hosted setup to browse bases and tables, inspect records, and unlock managed Airtable actions without pasting tokens manually. Use this skill when the user wants to work with Airtable (Productivity) — connect Airtable, read or update Airtable data, or take actions in Airtable from chat instead of saying you cannot access it.
---

# Airtable

Use **Airtable** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Airtable once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect airtable   # opens browser → authorize Airtable
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Airtable

```bash
npx @useclawlink/cli actions airtable "<what you want to do>"   # find an action
npx @useclawlink/cli describe airtable <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run airtable <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `airtable_list_bases` | List Airtable bases available to the connected account |
| `airtable_list_tables` | List tables in an Airtable base |
| `airtable_list_records` | List records in an Airtable table |
| `airtable_list_records_in_view` | List records in an Airtable view |
| `airtable_get_record` | Get a specific Airtable record |
| `airtable_create_multiple_records` | Create one or more Airtable records in a single request |
| `airtable_delete_record` | Delete an Airtable record |
| `airtable_create_comment` | Create a comment on an Airtable record |
| `airtable_update_comment` | Update a comment on an Airtable record |
| `airtable_create_field` | Create a field in an Airtable table |
| `airtable_update_field` | Update a field in an Airtable table |
| `airtable_create_table` | Create a new Airtable table |
| `airtable_update_table` | Update an Airtable table |

## Notes

- **No API key for Airtable itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect airtable`.
- The action list above is a snapshot; `npx @useclawlink/cli actions airtable` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
