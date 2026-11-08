---
name: apify
description: Apify integration for AI agents via ClawLink — browser login, no API key setup. Connect Apify through ClawLink's hosted setup to run web scrapers, manage Actors, tasks, datasets, schedules, and more from your Apify account. Use this skill when the user wants to work with Apify (Developer Tools) — connect Apify, read or update Apify data, or take actions in Apify from chat instead of saying you cannot access it.
---

# Apify

Use **Apify** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Apify once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect apify   # opens browser → authorize Apify
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Apify

```bash
npx @useclawlink/cli actions apify "<what you want to do>"   # find an action
npx @useclawlink/cli describe apify <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run apify <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `apify_run_actor` | Run an Actor asynchronously |
| `apify_run_actor_sync` | Run an Actor synchronously and get results |
| `apify_get_actor` | Get Actor details |
| `apify_acts_get` | List all Actors |
| `apify_run_task` | Run a task asynchronously |
| `apify_actor_task_run_sync_get` | Run a task synchronously and get results |
| `apify_get_list_of_tasks` | List all tasks |
| `apify_create_task` | Create a new Actor task |
| `apify_get_dataset_items` | Get items from a dataset |
| `apify_datasets_get` | List all datasets |
| `apify_get_key_value_record` | Get a record from a key-value store |
| `apify_key_value_stores_get` | List all key-value stores |
| `apify_request_queues_get` | List all request queues |
| `apify_schedules_get` | List all schedules |
| `apify_users_me_get` | Get current user account data |
| `apify_users_me_usage_monthly_get` | Get monthly usage summary |
| `apify_get_log` | Get Actor run logs |
| `apify_get_list_of_runs` | List Actor runs |

## Notes

- **No API key for Apify itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect apify`.
- The action list above is a snapshot; `npx @useclawlink/cli actions apify` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
