---
name: apollo
description: Apollo integration for AI agents via ClawLink — browser login, no API key setup. Connect Apollo through ClawLink's hosted setup to search prospects, enrich contacts, manage accounts and deals, and run sequences without manual API key handling. Use this skill when the user wants to work with Apollo (CRM & Sales) — connect Apollo, read or update Apollo data, or take actions in Apollo from chat instead of saying you cannot access it.
---

# Apollo

Use **Apollo** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Apollo once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect apollo   # opens browser → authorize Apollo
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Apollo

```bash
npx @useclawlink/cli actions apollo "<what you want to do>"   # find an action
npx @useclawlink/cli describe apollo <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run apollo <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `apollo_get_auth_status` | Get the connected Apollo user and team context |
| `apollo_search_contacts` | Search contacts already stored in Apollo CRM |
| `apollo_search_accounts` | Search company accounts in Apollo CRM |
| `apollo_people_search` | Search Apollo's people database |
| `apollo_people_enrichment` | Enrich a person from Apollo's contact database |
| `apollo_organization_search` | Search Apollo's organization database |
| `apollo_organization_enrichment` | Enrich a company from Apollo's database |
| `apollo_list_deals` | List Apollo deals/opportunities |
| `apollo_get_deal` | Get an Apollo deal by ID |
| `apollo_search_sequences` | Search Apollo email sequences |
| `apollo_search_tasks` | Search Apollo tasks |
| `apollo_create_contact` | Create a new contact in Apollo CRM |
| `apollo_create_account` | Create a company account in Apollo CRM |
| `apollo_create_deal` | Create a new deal in Apollo CRM |
| `apollo_add_contacts_to_sequence` | Enroll contacts into an Apollo email sequence |

## Notes

- **No API key for Apollo itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect apollo`.
- The action list above is a snapshot; `npx @useclawlink/cli actions apollo` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
