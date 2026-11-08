---
name: todoist
description: Todoist integration for AI agents via ClawLink — browser login, no API key setup. Connect Todoist through ClawLink's hosted setup to create and manage tasks, projects, and comments. Use this skill when the user wants to work with Todoist (Productivity) — connect Todoist, read or update Todoist data, or take actions in Todoist from chat instead of saying you cannot access it.
---

# Todoist

Use **Todoist** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Todoist once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect todoist   # opens browser → authorize Todoist
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Todoist

```bash
npx @useclawlink/cli actions todoist "<what you want to do>"   # find an action
npx @useclawlink/cli describe todoist <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run todoist <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `todoist_get_all_tasks` | Fetches all incomplete tasks from Todoist |
| `todoist_get_all_projects` | Get all projects from a Todoist account |
| `todoist_filter_tasks` | Get all tasks matching a filter |
| `todoist_get_all_comments` | Retrieve all comments for a task or project |
| `todoist_bulk_create_tasks` | Create many tasks in one request |
| `todoist_close_task_v1` | Close (complete) a task in Todoist |
| `todoist_archive_project2` | Archive a project in Todoist |
| `todoist_add_workspace` | Create a new workspace in Todoist |

## Notes

- **No API key for Todoist itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect todoist`.
- The action list above is a snapshot; `npx @useclawlink/cli actions todoist` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
