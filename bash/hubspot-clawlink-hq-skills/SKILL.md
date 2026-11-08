---
name: hubspot
description: HubSpot integration for AI agents via ClawLink — browser login, no API key setup. Connect HubSpot through ClawLink's hosted setup to manage contacts, companies, deals, tickets, marketing emails, workflows, and CRM objects from your HubSpot portal. Use this skill when the user wants to work with HubSpot (CRM & Sales) — connect HubSpot, read or update HubSpot data, or take actions in HubSpot from chat instead of saying you cannot access it.
---

# HubSpot

Use **HubSpot** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect HubSpot once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect hubspot   # opens browser → authorize HubSpot
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using HubSpot

```bash
npx @useclawlink/cli actions hubspot "<what you want to do>"   # find an action
npx @useclawlink/cli describe hubspot <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run hubspot <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `hubspot_search_contacts_by_criteria` | Search HubSpot contacts |
| `hubspot_read_contact` | Get a HubSpot contact by ID |
| `hubspot_create_contact` | Create a HubSpot contact |
| `hubspot_update_contact` | Update a HubSpot contact |
| `hubspot_search_companies` | Search HubSpot companies |
| `hubspot_get_company` | Get a HubSpot company by ID |
| `hubspot_create_company` | Create a HubSpot company |
| `hubspot_search_deals` | Search HubSpot deals |
| `hubspot_get_deal` | Get a HubSpot deal by ID |
| `hubspot_create_deal` | Create a HubSpot deal |
| `hubspot_search_tickets` | Search HubSpot tickets |
| `hubspot_get_ticket` | Get a HubSpot ticket by ID |
| `hubspot_create_task` | Create a HubSpot task |
| `hubspot_search_crm_objects_by_criteria` | Search HubSpot CRM objects |
| `hubspot_retrieve_owners` | List HubSpot owners and users |

## Notes

- **No API key for HubSpot itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect hubspot`.
- The action list above is a snapshot; `npx @useclawlink/cli actions hubspot` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
