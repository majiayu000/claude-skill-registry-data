---
name: lemlist
description: Lemlist integration for AI agents via ClawLink — browser login, no API key setup. Connect Lemlist through ClawLink's hosted setup to manage campaigns, leads, teams, and automation from your Lemlist account. Use this skill when the user wants to work with Lemlist (Marketing) — connect Lemlist, read or update Lemlist data, or take actions in Lemlist from chat instead of saying you cannot access it.
---

# Lemlist

Use **Lemlist** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Lemlist once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect lemlist   # opens browser → authorize Lemlist
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Lemlist

```bash
npx @useclawlink/cli actions lemlist "<what you want to do>"   # find an action
npx @useclawlink/cli describe lemlist <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run lemlist <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `lemlist_get_list_campaigns` | List Lemlist campaigns |
| `lemlist_get_campaign_by_id` | Get a Lemlist campaign by ID |
| `lemlist_get_campaign_stats` | Get Lemlist campaign statistics |
| `lemlist_get_campaign_sequences` | List Lemlist campaign sequences |
| `lemlist_get_retrieve_lead_by_email` | Get a Lemlist lead by email |
| `lemlist_get_contact_messages` | List Lemlist contact messages |
| `lemlist_get_retrieve_activities` | List Lemlist activities |
| `lemlist_get_list_team_senders` | List Lemlist team senders |
| `lemlist_get_list_tasks` | List Lemlist tasks |
| `lemlist_get_all_webhooks` | List Lemlist webhooks |
| `lemlist_create_campaign` | Create a Lemlist campaign |
| `lemlist_add_lead_to_campaign` | Add a lead to a Lemlist campaign |
| `lemlist_unsubscribe_lead_from_campaign` | Unsubscribe a lead from a Lemlist campaign |
| `lemlist_create_company` | Create a Lemlist company |
| `lemlist_get_label` | Get a Lemlist label |

## Notes

- **No API key for Lemlist itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect lemlist`.
- The action list above is a snapshot; `npx @useclawlink/cli actions lemlist` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
