---
name: clickup
description: ClickUp integration for AI agents via ClawLink — browser login, no API key setup. Connect ClickUp through ClawLink's hosted setup to manage tasks, lists, folders, spaces, comments, checklists, and time tracking from your ClickUp workspace. Use this skill when the user wants to work with ClickUp (Productivity) — connect ClickUp, read or update ClickUp data, or take actions in ClickUp from chat instead of saying you cannot access it.
---

# ClickUp

Use **ClickUp** from your AI agent through [ClawLink](https://claw-link.dev) — browser login, no API key to paste, no config to edit. Connect ClickUp once and the agent can read and act on it. Works in any agent that can run shell commands (Claude Code, Cursor, Codex, Cline, and more).

## Setup

Run these once — the agent can run them for you:

```bash
npx @useclawlink/cli login              # opens browser → approve (mints + stores a key)
npx @useclawlink/cli connect clickup   # opens browser → authorize ClickUp
```

No API key to create or paste — `login` stores the credential at `~/.clawlink/credentials.json`.

## Using ClickUp

```bash
npx @useclawlink/cli actions clickup "<what you want to do>"   # find an action
npx @useclawlink/cli describe clickup <action-id>             # see its inputs (before writes)
npx @useclawlink/cli run clickup <action-id> --input '<json>' # execute
```

Reads first; confirm with the user before any write.

## Available actions

| Action | Description |
|--------|-------------|
| `clickup_get_task` | Get a ClickUp task by ID |
| `clickup_get_tasks` | List ClickUp tasks with optional filters |
| `clickup_create_task` | Create a new ClickUp task |
| `clickup_update_task` | Update an existing ClickUp task |
| `clickup_delete_task` | Delete a ClickUp task |
| `clickup_get_list` | Get a ClickUp list by ID |
| `clickup_get_lists` | List ClickUp lists |
| `clickup_create_list` | Create a new ClickUp list |
| `clickup_update_list` | Update a ClickUp list |
| `clickup_delete_list` | Delete a ClickUp list |
| `clickup_get_folder` | Get a ClickUp folder by ID |
| `clickup_get_folders` | List ClickUp folders |
| `clickup_create_folder` | Create a new ClickUp folder |
| `clickup_update_folder` | Update a ClickUp folder |
| `clickup_delete_folder` | Delete a ClickUp folder |
| `clickup_get_space` | Get a ClickUp space by ID |
| `clickup_get_spaces` | List ClickUp spaces |
| `clickup_create_space` | Create a new ClickUp space |
| `clickup_update_space` | Update a ClickUp space |
| `clickup_delete_space` | Delete a ClickUp space |
| `clickup_get_task_comments` | List comments on a ClickUp task |
| `clickup_get_list_comments` | List comments on a ClickUp list |
| `clickup_create_task_comment` | Add a comment to a ClickUp task |
| `clickup_create_list_comment` | Add a comment to a ClickUp list |
| `clickup_update_comment` | Update a ClickUp comment |
| `clickup_delete_comment` | Delete a ClickUp comment |
| `clickup_get_custom_fields` | List custom fields for a ClickUp list |
| `clickup_update_task_custom_field` | Update a custom field value on a ClickUp task |
| `clickup_remove_task_custom_field` | Remove a custom field value from a ClickUp task |
| `clickup_get_task_templates` | List ClickUp task templates |
| `clickup_create_checklist` | Create a checklist in a ClickUp task |
| `clickup_update_checklist` | Update a ClickUp checklist |
| `clickup_delete_checklist` | Delete a ClickUp checklist |
| `clickup_create_checklist_item` | Create an item in a ClickUp checklist |
| `clickup_update_checklist_item` | Update a ClickUp checklist item |
| `clickup_delete_checklist_item` | Delete a ClickUp checklist item |
| `clickup_create_time_entry` | Create a time entry in ClickUp |
| `clickup_start_time_entry` | Start a time entry for a ClickUp task |
| `clickup_stop_time_entry` | Stop the current time entry in ClickUp |
| `clickup_get_view` | Get a ClickUp view by ID |
| `clickup_get_view_tasks` | List tasks from a ClickUp view |
| `clickup_get_view_comments` | List comments from a ClickUp view |
| `clickup_get_team_views` | List ClickUp team views |
| `clickup_get_space_views` | List ClickUp space views |
| `clickup_get_folder_views` | List ClickUp folder views |
| `clickup_get_list_views` | List ClickUp list views |

## Notes

- **No API key for ClickUp itself** — ClawLink holds the OAuth token; the agent only holds your ClawLink credential.
- Not connected yet, or access expired? Re-run `npx @useclawlink/cli connect clickup`.
- The action list above is a snapshot; `npx @useclawlink/cli actions clickup` is always current.

## Resources

- ClawLink: https://claw-link.dev
- Docs: https://docs.claw-link.dev
- CLI: https://www.npmjs.com/package/@useclawlink/cli

---

**Powered by [ClawLink](https://claw-link.dev)** — connect 1,000+ apps to any AI agent.
