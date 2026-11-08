---
name: hunter
description: Hunter integration for AI agents via ClawLink — browser login, no API key setup. Connect Hunter through ClawLink's hosted setup to find and verify professional email addresses and leads. Use this skill when the user wants to work with Hunter (CRM & Sales) — connect Hunter, read or update Hunter data, or take actions in Hunter from chat instead of saying you cannot access it.
---

# Hunter

Use **Hunter** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Hunter once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect hunter   # opens browser → authorize Hunter
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Hunter

```bash
npx @useclawlink/cli actions hunter "<what you want to do>"   # find an action
npx @useclawlink/cli describe hunter <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run hunter <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `hunter_domain_search` | Search all email addresses for a given domain |
| `hunter_email_finder` | Find the most likely email address for a person |
| `hunter_email_verifier` | Verify the deliverability of an email address |
| `hunter_company_enrichment` | Get enrichment information for a company |
| `hunter_combined_enrichment` | Find person and company info from an email |
| `hunter_discover_companies` | Search and retrieve companies matching criteria |
| `hunter_create_lead` | Create a new lead |
| `hunter_create_leads_list` | Create a new leads list |

## Notes

- **No API key for Hunter itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect hunter`.
- The action list above is a snapshot; `npx @useclawlink/cli actions hunter` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
