---
name: notes-and-tasks
description: >
    Create, read, update, and delete manually-logged activities (notes, calls, meetings) and tasks/to-dos
    on table & object records via the Frontline CLI, and READ the full synced record timeline
    (`frontline object timeline` — emails, conversations, WhatsApp, audit changes, permission-redacted).
    Covers record-scoped to-dos (`frontline object task` — the record's "To-do's" tab, which shows EVERY
    user's to-dos on that record) and the personal to-dos inbox (`frontline user-tasks`, filtered by
    assignee). NOT `max tasks` — those are Max's own scheduled/event automations (see the max-tasks skill).
    Best practice: assign new to-dos to their owner and let created time default to now.
allowed-tools: Bash(frontline:*)
---

# Activities, Tasks & To-dos

Activities and tasks are sub-resources attached to individual rows. They let you
track follow-ups, comments, interactions, and to-do items without polluting row fields.

> **Three different "tasks" — don't confuse them:**
>
> | Command                                  | What it is                                   | Scope                                                          |
> | ---------------------------------------- | -------------------------------------------- | -------------------------------------------------------------- |
> | `frontline object task …`                | A record's **To-do's** (the tab on a record) | Record-scoped — returns **every** user's to-dos on that record |
> | `frontline user-tasks …` (alias `tasks`) | The personal **To-dos inbox**                | Assignee-scoped — `--mine` = assigned to you                   |
> | `max tasks …`                            | Max's own scheduled/event **automations**    | Not a to-do at all — see the `max-tasks` skill                 |

> **Two different "activity" surfaces — don't confuse them:**
>
> | Command                          | Reads                                                                              | Writable?       |
> | -------------------------------- | ---------------------------------------------------------------------------------- | --------------- |
> | `frontline object activity …`    | **Manually-logged** activities only (notes, calls, meetings, logged emails)        | Create/edit/del |
> | `frontline object timeline list` | The **full record timeline** — synced inbox emails, conversations, WhatsApp, audit | Read-only       |
>
> `object activity` does **not** return synced inbox/chat history; that lives on the timeline
> (see the [Timeline](#timeline) section). The timeline is permission-redacted server-side.

## Activities

An **activity** is a manually-logged interaction on a record. Each has a **type**:

| Type         | Description                    |
| ------------ | ------------------------------ |
| `NOTE`       | Free-form note (default)       |
| `EMAIL`      | Manually logged email exchange |
| `PHONE_CALL` | Phone call                     |
| `MEETING`    | In-person or video meeting     |
| `WHATSAPP`   | WhatsApp thread                |

> **Pick the type that matches the interaction — don't default everything to `NOTE`.** A meeting
> is `MEETING`, a call is `PHONE_CALL`, etc. Use `NOTE` only for free-form commentary that isn't a
> concrete interaction (a reminder, an observation, context). Backdate with `--activity-date` when
> logging something that already happened. You generally only need to log **offline** interactions
> (calls, in-person meetings) — synced inbox emails and chats already appear on the timeline.

> `object activity` only lists what was **manually logged**. Synced emails, conversation
> history, WhatsApp threads, audit changes and file events are part of the **timeline**, not
> here — read them with `frontline object timeline` (see below).

### Key fields

| Field            | Notes                                                                                |
| ---------------- | ------------------------------------------------------------------------------------ |
| `content`        | The body text. Required.                                                             |
| `activityDate`   | When the interaction actually happened (ISO datetime). Defaults to now if omitted.   |
| `userIds`        | Comma-separated (CLI) or array (API) of user IDs to tag as attendees/participants.   |
| `additionalData` | Freeform JSON for structured extras (e.g. `{"duration":30,"outcome":"interested"}`). |
| `relatedTableId` | Table/object numeric ID to cross-link to another record. Pair with `relatedRowId`.   |
| `relatedRowId`   | Row ID of the linked record.                                                         |

### List Activities

```bash
frontline object activity list <object> <row-id>
frontline object activity list <object> <row-id> --table
```

### Create an Activity

```bash
# Simple note (default type)
frontline object activity create <object> <row-id> --content "Follow up next week"

# Phone call with date and participants
frontline object activity create deals 6625abc \
  --content "30-min call, very interested" \
  --type PHONE_CALL \
  --activity-date 2026-06-01T15:00:00Z \
  --user-ids 12,34

# Meeting with extra metadata
frontline object activity create deals 6625abc \
  --content "Kickoff meeting" \
  --type MEETING \
  --additional-data '{"duration":60,"location":"Zoom"}'

# Linked to another record (cross-reference)
frontline object activity create contacts 6625abc \
  --content "Called about Acme deal" \
  --type PHONE_CALL \
  --related-table-id 5 \
  --related-row-id 6626def000aabb112233
```

### Get an Activity by ID

```bash
frontline object activity get <object> <activity-id>
frontline object activity get <object> <activity-id> --pretty
```

### Update an Activity

```bash
frontline object activity update <object> <activity-id> --content "Updated: follow up Friday"
frontline object activity update deals 42 --activity-date 2026-06-02 --user-ids 12,34
```

### Delete an Activity

```bash
frontline object activity delete <object> <activity-id>
```

Only manually-created activities can be deleted. Only the owner or an account admin can delete.

---

## Timeline

`frontline object timeline` reads the **full activity timeline** for a record — the same feed
the in-app record view shows. It is **read-only** and merges:

- Synced **inbox emails** (Gmail/Outlook), with subject/summary
- **Conversation** history (Max chats, agent threads)
- **WhatsApp** personal threads
- **Audit** changes (field edits, stage moves)
- Manually-logged activities, tasks and files

> **Permissions:** share-gated content (emails, WhatsApp) is **redacted server-side** based on
> your account's sharing settings — identical to the in-app timeline. You only see detail you're
> allowed to see. This is why synced communication lives here and not under `object activity`.

Timeline activity **types** (use with `--type`, comma-separated):
`EMAIL`, `CONVERSATION`, `WHATSAPP_PERSONAL`, `AUDIT_LOG`, `NOTE`, `TASK`, `FILE`, `MANUAL_ACTIVITY`.

### List the timeline

```bash
frontline object timeline list <object> <row-id>
frontline object timeline list people 6625abc --type EMAIL,CONVERSATION --table
frontline object timeline list deals 6625abc --search "pricing" --from 2026-01-01 --to 2026-06-30
frontline object timeline list people 6625abc --page 2 --page-size 50
```

### Get one timeline activity

```bash
frontline object timeline get <object> <row-id> <activity-id>
frontline object timeline get people 6625abc 42 --pretty
```

> Use `object timeline` to **answer "what's the history with this person/company?"** Use
> `object activity` only to **log** a new note/call/meeting.

---

## Tasks (a record's To-do's)

`frontline object task` manages the **record's "To-do's" tab**. It is record-scoped: listing returns
**all** to-dos on that record regardless of who created or is assigned to them (e.g. if Alvaro and
Esteban each add a to-do on the same person, both show up here). Tasks have content, optional due
dates, assignees, and a completion state.

### Best practice — ownership & timing

- **Created-by + timestamp are automatic.** The authenticated user is recorded as the creator and the
  created time is set to now — you don't pass these.
- **Assign new to-dos to their owner.** Assignees are NOT auto-set. When you create a to-do for
  someone, pass `--assignees <userId>` (their ID from `frontline users list`) so it also lands in
  their personal To-dos inbox (`frontline user-tasks --mine`). Without an assignee it appears only on
  the record's To-do's tab. Default to the user you're acting for; change it to delegate.
- **Due date:** set `--due-date` only when there's a real deadline.
- **Same idea for notes/activities:** they're attributed to the current user and `activityDate`
  defaults to now — only pass `--activity-date` to backdate a previously-happened interaction.

### List Tasks

```bash
frontline object task list <object> <row-id>
```

### Create a Task

```bash
# Recommended: assign the to-do to its owner so it also shows in their inbox
frontline object task create <object> <row-id> \
  --content "Call the client" \
  --assignees 42

# With a due date
frontline object task create <object> <row-id> \
  --content "Send proposal" \
  --assignees 42 \
  --due-date 2026-05-01

# Multiple assignees (comma-separated user IDs from `frontline users list`)
frontline object task create <object> <row-id> \
  --content "Review contract" \
  --assignees 12,34

# Unassigned: still visible on the record's To-do's tab, but in nobody's inbox
frontline object task create <object> <row-id> --content "Call the client"
```

### Get a Task by ID

```bash
frontline object task get <object> <task-id>
```

### Update a Task

```bash
frontline object task update <object> <task-id> --data '{"content":"Revised task","dueDate":"2026-06-01"}'
```

### Complete / Uncomplete a Task

```bash
frontline object task complete <object> <task-id>
frontline object task uncomplete <object> <task-id>
```

### Delete a Task

```bash
frontline object task delete <object> <task-id>
```

---

## To-dos inbox — `frontline user-tasks`

The account **"To-dos" inbox** (alias `frontline tasks`). Same underlying to-dos as `object task`, but
listed by **assignee** rather than by record, and a to-do can optionally be linked to a record with
`--object`/`--row`. Use this for "what's on my plate" views; use `object task` for "everything on this
record".

```bash
# My open to-dos
frontline user-tasks list --mine --pending --table

# Create a to-do assigned to user 42, due next week, linked to a record
frontline user-tasks create --content "Email David about renewal" \
  --due 2026-06-25 --assignees 42 --object people --row 6625abc

frontline user-tasks complete 101
```

> `list` filters by assignee (`--mine`, `--people`, `--teams`) and **cannot** scope to a single
> record's row. To see all to-dos on one record (the UI "To-do's" tab), use
> `frontline object task list <object> <row-id>`.

---

## Typical Workflow

```bash
# 1. Find the row you want to annotate
frontline object record list deals --search "Acme"
# → row ID = 6625abc123def456

# 2. Log a phone call
frontline object activity create deals 6625abc123def456 \
  --content "Discussed pricing" \
  --type PHONE_CALL \
  --activity-date 2026-06-01T15:00:00Z \
  --user-ids 12

# 3. Add a follow-up to-do, assigned to its owner (so it hits their inbox too)
frontline object task create deals 6625abc123def456 \
  --content "Send revised proposal" \
  --assignees 42 \
  --due-date 2026-06-05

# 4. Later, mark it complete
frontline object task complete deals 7
```

---

## See also

- Concept reference: [Activities](https://docs.getfrontline.ai/docs/concepts/activities)
- Full CLI reference: <https://docs.getfrontline.ai/cli>
- `max-tasks` skill — Max's own scheduled/event automations (a different "tasks", on the `max` CLI).
