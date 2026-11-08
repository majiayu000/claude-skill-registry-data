---
name: motion
description: Motion integration for AI agents via ClawLink — browser login, no API key setup. Connect Motion through ClawLink's hosted setup to manage workspaces, projects, tasks, recurring tasks, schedules, comments, and custom fields from your Motion account. Use this skill when the user wants to work with Motion (Productivity) — connect Motion, read or update Motion data, or take actions in Motion from chat instead of saying you cannot access it.
---

# Motion

Use **Motion** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect Motion once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect motion   # opens browser → authorize Motion
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using Motion

```bash
npx @useclawlink/cli actions motion "<what you want to do>"   # find an action
npx @useclawlink/cli describe motion <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run motion <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `motion_get_my_user` | Get the connected Motion user |
| `motion_list_users` | List Motion workspace users |
| `motion_list_workspaces` | List Motion workspaces |
| `motion_list_projects` | List Motion projects |
| `motion_get_project` | Get a Motion project by ID |
| `motion_create_project` | Create a new Motion project |
| `motion_list_tasks` | List Motion tasks |
| `motion_get_task` | Get a Motion task by ID |
| `motion_create_task` | Create a new Motion task |
| `motion_update_task` | Update a Motion task |
| `motion_move_task` | Move a Motion task to another project or status |
| `motion_list_recurring_tasks` | List Motion recurring tasks |
| `motion_list_schedules` | List Motion schedules |
| `motion_list_comments` | List Motion comments |
| `motion_create_comment` | Create a comment on a Motion task |

## Notes

- **No API key for Motion itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect motion`.
- The action list above is a snapshot; `npx @useclawlink/cli actions motion` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
