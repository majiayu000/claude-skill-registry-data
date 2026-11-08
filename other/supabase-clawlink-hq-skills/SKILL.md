---
name: supabase
description: Supabase integration for AI agents via ClawLink — browser login, no API key setup. Connect Supabase through ClawLink's hosted setup to manage projects, query databases, deploy Edge Functions, and configure auth and organizations. Use this skill when the user wants to work with Supabase (Storage & Databases) — connect Supabase, read or update Supabase data, or take actions in Supabase from chat instead of saying you cannot access it.
---

# Supabase

Use **Supabase** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Supabase once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect supabase   # opens browser → authorize Supabase
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Supabase

```bash
npx @useclawlink/cli actions supabase "<what you want to do>"   # find an action
npx @useclawlink/cli describe supabase <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run supabase <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `supabase_list_all_projects` | List all Supabase projects |
| `supabase_get_project` | Get a Supabase project by ref |
| `supabase_get_project_logs` | Get project logs |
| `supabase_get_health` | Get API health status |
| `supabase_list_all_organizations` | List all organizations |
| `supabase_get_organization` | Get organization information |
| `supabase_list_tables` | List database tables |
| `supabase_get_table_schemas` | Get table schemas |
| `supabase_select_from_table` | Select rows from a table |
| `supabase_run_read_only_query` | Execute a read-only SQL query |
| `supabase_beta_run_sql_query` | Execute a database SQL query |
| `supabase_list_functions` | List all Edge Functions |
| `supabase_get_function` | Retrieve an Edge Function |
| `supabase_create_function` | Create a new Edge Function |
| `supabase_deploy_function` | Deploy an Edge Function |
| `supabase_list_database_branches` | List database branches |
| `supabase_gets_project_s_auth_config` | Get project's auth config |
| `supabase_list_secrets` | List all project secrets |
| `supabase_list_migration_history` | List migration history |
| `supabase_list_backups` | List project database backups |

## Notes

- **No API key for Supabase itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect supabase`.
- The action list above is a snapshot; `npx @useclawlink/cli actions supabase` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
