---
name: notion
description: Notion integration for AI agents via ClawLink — browser login, no API key setup. Connect Notion through ClawLink's hosted setup to search, read, and manage pages, databases, and blocks in your workspace. Use this skill when the user wants to work with Notion (Productivity) — connect Notion, read or update Notion data, or take actions in Notion from chat instead of saying you cannot access it.
---

# Notion

Use **Notion** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Notion once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect notion   # opens browser → authorize Notion
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Notion

```bash
npx @useclawlink/cli actions notion "<what you want to do>"   # find an action
npx @useclawlink/cli describe notion <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run notion <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `notion_search` | Search pages and databases in Notion |
| `notion_retrieve_page` | Retrieve a Notion page by ID |
| `notion_retrieve_block` | Retrieve a Notion block by ID |
| `notion_create_page` | Create a new Notion page |
| `notion_create_page_from_database` | Create a page inside a Notion database |
| `notion_update_page` | Update properties on a Notion page |
| `notion_duplicate_page` | Duplicate a Notion page |
| `notion_query_database` | Query a Notion database |
| `notion_create_database` | Create a new Notion database |
| `notion_update_database` | Update a Notion database's schema |
| `notion_retrieve_database_schema` | Retrieve a Notion database schema |
| `notion_retrieve_database_content` | Retrieve a Notion database's content |
| `notion_append_block` | Append blocks to a Notion page or block |
| `notion_update_block` | Update a Notion block |
| `notion_delete_block` | Delete a Notion block |
| `notion_create_comment` | Create a comment on a Notion page or discussion |
| `notion_list_all_users` | List all users in the Notion workspace |
| `notion_get_current_user` | Get the connected Notion bot user |

## Notes

- **No API key for Notion itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect notion`.
- The action list above is a snapshot; `npx @useclawlink/cli actions notion` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
