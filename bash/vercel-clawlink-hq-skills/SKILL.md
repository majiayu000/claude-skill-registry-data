---
name: vercel
description: Vercel integration for AI agents via ClawLink — browser login, no API key setup. Connect Vercel through ClawLink's hosted setup to manage projects, deployments, domains, environment variables, and team resources. Use this skill when the user wants to work with Vercel (Developer Tools) — connect Vercel, read or update Vercel data, or take actions in Vercel from chat instead of saying you cannot access it.
---

# Vercel

Use **Vercel** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Vercel once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect vercel   # opens browser → authorize Vercel
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Vercel

```bash
npx @useclawlink/cli actions vercel "<what you want to do>"   # find an action
npx @useclawlink/cli describe vercel <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run vercel <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `vercel_get_auth_user` | Get the authenticated Vercel user |
| `vercel_get_teams` | List teams accessible to the connected Vercel account |
| `vercel_get_projects` | List Vercel projects |
| `vercel_get_project2` | Get details for a specific Vercel project |
| `vercel_get_deployments` | List Vercel deployments |
| `vercel_get_deployment` | Get details for a specific deployment |
| `vercel_list_domains` | List domains in the connected Vercel account |
| `vercel_get_project_domains` | List domains attached to a Vercel project |
| `vercel_filter_project_envs` | List environment variables for a Vercel project |
| `vercel_add_environment_variable` | Add an environment variable to a Vercel project |
| `vercel_create_project2` | Create a new Vercel project |
| `vercel_create_new_deployment` | Create a new deployment in Vercel |
| `vercel_add_project_domain` | Attach a domain to a Vercel project |
| `vercel_update_project2` | Update project settings for a Vercel project |

## Notes

- **No API key for Vercel itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect vercel`.
- The action list above is a snapshot; `npx @useclawlink/cli actions vercel` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
