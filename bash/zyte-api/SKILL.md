---
name: zyte-api
description: Zyte API integration for AI agents via ClawLink — browser login, no API key setup. Connect Zyte API through ClawLink's hosted setup to extract data from URLs, scrape web pages, and monitor Zyte service status. Use this skill when the user wants to work with Zyte API (Data & Analytics) — connect Zyte API, read or update Zyte API data, or take actions in Zyte API from chat instead of saying you cannot access it.
---

# Zyte API

Use **Zyte API** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Zyte API once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect zyte-api   # opens browser → authorize Zyte API
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Zyte API

```bash
npx @useclawlink/cli actions zyte-api "<what you want to do>"   # find an action
npx @useclawlink/cli describe zyte-api <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run zyte-api <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `zyte_api_extract_zyte_api` | Extract data from a URL using Zyte API |
| `zyte_api_status` | Get Zyte API operational status |
| `zyte_api_components` | Get Zyte service component statuses |
| `zyte_api_list_incidents` | List recent Zyte incidents |
| `zyte_api_get_unresolved_incidents` | Get unresolved incidents |
| `zyte_api_get_scheduled_maintenances` | Get scheduled maintenances |
| `zyte_api_active_scheduled_maintenances` | Get active maintenances |

## Notes

- **No API key for Zyte API itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect zyte-api`.
- The action list above is a snapshot; `npx @useclawlink/cli actions zyte-api` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
