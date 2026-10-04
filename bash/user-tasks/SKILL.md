---
name: user-tasks
allowed-tools: Bash(frontline:*)
description: Create, list, inspect, update, complete, and delete user tasks (the account "To-dos" inbox) from the CLI. Use when the user asks about their to-dos, task inbox, follow-ups, reminders, or tasks assigned to a user — optionally linked to a CRM record. These are user tasks, distinct from Max tasks.
---

## What these are

`frontline user-tasks` manages **user tasks** — the "To-dos" inbox in the app. A task has
content, an optional due date, assignees (account users), and may optionally be **linked to an
object record** (e.g. a Company or Person). Completing a task requires you to be one of its
assignees.

The CLI command is `frontline user-tasks`. The older alias `frontline tasks` still works for
back-compat, but prefer `user-tasks`.

These are NOT:

- **Object-row tasks** (`frontline object task *`) — tasks that live on a specific record's
  timeline. (A user task _can_ link to a record, but it lives in the global inbox.)
- **Max tasks** — Max's own scheduled/periodic jobs.

## Prerequisites

- Authenticate with `frontline auth login <api-key>`.
- All user-task commands require a **USER API key** (tasks are user-scoped within the account).
- Assignee IDs come from `frontline users list`.

## List

```bash
frontline user-tasks list                       # all user tasks
frontline user-tasks list --mine --pending      # your open tasks
frontline user-tasks list --completed --table
frontline user-tasks list --object companies    # tasks linked to a Company record
frontline user-tasks list --people 12,15        # tasks whose assignees are these People IDs
frontline user-tasks list --teams 3
```

Flags: `--mine` (assigned to you), `--completed` / `--pending` (completion state),
`--object <name>` (linked object slug, e.g. `companies`), `--people <csv>`, `--teams <csv>`.
`--table` renders a flat summary; default output is JSON.

Each task includes `assignees`, `created_by`, `completed`/`completed_at`, and `related`
(the linked object record, or `null`).

## Create

```bash
# Simple to-do
frontline user-tasks create --content "Email David about the Q3 renewal" --due 2026-06-25 --assignees 42

# Linked to a CRM record
frontline user-tasks create --content "Send onboarding deck" --object companies --row abc123 --assignees 42,57
```

- `--content` is required.
- `--due` is a date (`YYYY-MM-DD`).
- `--assignees` is a comma-separated list of **user IDs** (`frontline users list`).
- `--object <name>` + `--row <rowId>` link the task to an object record. **Both are required
  together** — `--object` is the object slug (e.g. `companies`, `people`); `--row` is the record ID.

## Inspect / Update

```bash
frontline user-tasks get 101

frontline user-tasks update 101 --content "Email David today"
frontline user-tasks update 101 --due 2026-07-01
frontline user-tasks update 101 --clear-due            # remove the due date
frontline user-tasks update 101 --assignees 42,57      # REPLACES the assignee list
frontline user-tasks update 101 --object people --row p_9   # (re)link to a record
frontline user-tasks update 101 --unlink               # remove the linked record
```

Update only touches the fields you pass. `--assignees` **replaces** the whole assignee list
(it is not additive). Use `--clear-due` to null the due date and `--unlink` to detach the
linked object record.

## Complete / Reopen / Delete

```bash
frontline user-tasks complete 101      # you must be an assignee; errors if already completed
frontline user-tasks uncomplete 101    # reopen
frontline user-tasks delete 101        # permanent
```

---

## See also

- Per-record tasks on a CRM row: the `notes-and-tasks` skill (`frontline object task *`).
- Resolve assignee user IDs: the `users` skill (`frontline users list`).
- Full reference: <https://docs.getfrontline.ai/docs> and <https://docs.getfrontline.ai/cli>.
