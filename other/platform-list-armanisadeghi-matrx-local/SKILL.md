---
name: platform-list
type: Skill
title: "platform-list — Arman's list of large platform work not started yet"
description: "The Platform List: Arman's own register of large platform-level work he chose not to start yet. Use when the reminder hook says a row is due, when Arman says to add, snooze, kill, or finish a row, when you own a row, or when you think something belongs there. NOT for ordinary tasks, defects, or handoffs."
tags: [operations, register, platform, arman, reminders]
timestamp: 2026-09-21T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/platform-list/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# The Platform List

One file: `common-docs/operations/platform-list/LIST.md`. One folder beside it with one short file per row.
Owned by Arman. **Never read it at session start.** `due.py` beside it runs as a SessionStart hook on Arman's
Mac and stays silent unless a `Waiting` row's Start date has arrived; it then tells the first attended session
of the day, once, and no other. Read the list only when that reminder arrives or Arman asks about it.

## What it is for

Arman normally starts big work the moment he decides on it. The rare exception is large, platform-wide work he
has decided to do but not now. That is the whole list. It is not a backlog, not a defect ledger, not a place for
handoffs, and not where your ideas go. Expect it to stay short. Almost every row starts from Arman's own words.

## The four things you do

1. **Remind, only when the hook tells you to.** Tell Arman in your first reply, in one plain sentence per row
   the reminder names. He will either say start it, or give a new date. A new date
   is a snooze: change the Start cell and nothing else. Never decide a date yourself.
2. **Suggest, never write.** If you believe something belongs here, say so to Arman in one or two plain
   sentences inside your normal reply. You do not add rows, files, drafts, or notes anywhere. He adds it or
   he does not.
3. **Add only on his word, in this conversation.** When Arman names an item to add, write one row and one
   item file, both from the templates below. A new row has an empty Owner note and an empty Inbox. The Item
   is one sentence under fifteen words that reads as a vision, not a task.
4. **Own a row honestly.** When you claim a row, set Status to `Started`, fill Owner with your template line,
   and keep the Owner note true. Clear Inbox lines once you have read them. When you stop for the day, the
   row must be readable cold by the next owner.

## Status, exactly

`Waiting` nobody started · `Started` an owner is working · `Blocked` stopped on something the Owner note names ·
`Live` shipped and in use but could still slip away unfinished. No `Done` exists.

## Deleting a row

A row and its file are deleted, together, in exactly two cases:

- Arman says he is killing it.
- The work has reached the point where it is impossible for it to not be finished. Sometimes that is ten
  minutes in, because the code now depends on it. Sometimes that is weeks after it went live, when the last
  proof lands. Arman judges this, and you ask him when you think a row has reached it.

Deletion is complete: the row, the file, and nothing else. No "deleted" line, no archive folder, no history
file, no copy in a plan or handoff or register, no summary of what was here. The bundle log says only that the
Platform List changed, never which item. Building any place that remembers what was on this list is
forbidden, whoever asks. `check.py` in the folder enforces the shape; the docs lint runs it.

## Owner line, one per tool

Fill Owner so a stranger can find your conversation. Use the exact form for your tool:

| Tool | Owner cell |
|---|---|
| Claude Code | `Claude Code · <session title> · <session id> · <machine or cloud>` (session id is the UUID of your transcript under `~/.claude/projects/`; resume with `claude --resume <id>`) |
| Codex | `Codex · <thread title> · <thread id>` (resume with `codex resume <id>`) |
| Cursor | `Cursor · <chat title> · <workspace folder> · <YYYY-MM-DD started>` |
| Anything else | `<tool> · <title> · <the id its resume command takes>` |

## Templates

Row: `| [<item, under 15 words>](<slug>.md) | Waiting | <YYYY-MM-DD> |  |  |  |`

Item file `<slug>.md`, at most 250 words of body, these five headings and no others:

```markdown
---
type: Platform Item
title: "<item>"
description: "<one sentence>"
timestamp: <YYYY-MM-DD>T00:00:00Z
---

## What this is
## Why it matters
## What finished looks like
## Where it stands
## Decisions
```

Write plain sentences. No jargon, no codenames, no lists of files. The code, commit messages, and the system's
own docs carry detail; this file carries only what someone needs to pick the work up and understand where it
stands. When it grows past the cap, cut, never split.

## Scope test

Not written yet. Arman will shape it with the first real rows. Until then the test is his word.
