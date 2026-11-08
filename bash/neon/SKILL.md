---
name: neon
description: Neon integration for AI agents via ClawLink — browser login, no API key setup. Connect Neon through ClawLink's hosted setup to manage serverless Postgres projects, branches, and databases. Use this skill when the user wants to work with Neon (Storage & Databases) — connect Neon, read or update Neon data, or take actions in Neon from chat instead of saying you cannot access it.
---

# Neon

Use **Neon** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Neon once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect neon   # opens browser → authorize Neon
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Neon

```bash
npx @useclawlink/cli actions neon "<what you want to do>"   # find an action
npx @useclawlink/cli describe neon <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run neon <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `neon_access_project_details_by_id` | Retrieve detailed information about a Neon project |
| `neon_count_project_branches` | Get the total number of branches in a project |
| `neon_fetch_database_for_branch` | List databases for a project branch |
| `neon_get_auth` | Retrieve authentication information |
| `neon_accept_projects_transfer_requests` | Accept a transfer request for a project |
| `neon_add_role_to_branch` | Create a new PostgreSQL role within a branch |
| `neon_add_new_jwks_to_project_endpoint` | Add a new JWKS URL to a project |
| `neon_add_project_email_permission` | Add email permissions to a project |

## Notes

- **No API key for Neon itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect neon`.
- The action list above is a snapshot; `npx @useclawlink/cli actions neon` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
