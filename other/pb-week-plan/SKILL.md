---
name: pb-week-plan
description: >-
  Turn your scattered to-do lists and notes into one prioritised plan for the
  week, with at most 3 must-do items per day. Use for "plan my week", "what
  should I do this week", "sort my to-dos", "weekly plan from my notes".
  Nothing leaves your computer unless you opt in to steps 4 or 8.
category: bdb-core
kind: playbook
trigger: ["plan my week", "sort my to-dos", "weekly plan"]
inputs: [todo_folders, "calendar_file?"]
requires:
  skills: [memb-skill, github, concise-planning, "gh (external)"]
  agents: []
  mcps: []
  store: []
go_points: []
outputs: ["inbox.md", "calendar.md", "week-plan.md", "run-log.md"]
verify: "every line in week-plan.md points to a line in inbox.md"
difficulty: beginner
est_time: 10-20 min
---

# Plan my week
What you get: one prioritised plan for this week, built from your scattered to-do lists and notes.

## Inputs
- Folders with your to-dos and notes — you name them
- A calendar file (.ics) — optional, exported from your calendar app
- A save folder — asked once; default `./pb-week-plan-<date>/`

## Steps
1. Ask once — save folder, folders with to-dos and notes, optional calendar file → `run-log.md` — the folders exist
2. Read the to-dos and notes → `inbox.md`, every open item with its source file and line — at least one item, otherwise stop and ask
3. memb-skill — search open commitments and deadlines → added to `inbox.md` tagged `[memB]` — skipped and logged if memB is not installed
4. github — only if you opt in and `gh (external)` is installed: your own open pull requests → added to `inbox.md` — your choice recorded
5. Read the calendar file → `calendar.md` with the fixed appointments — skipped if none was given
6. concise-planning — `inbox.md` and `calendar.md` → `week-plan.md`, per day Must (max 3), Should, Could — every line traces to a line in `inbox.md` or `calendar.md`; nothing invented
7. Show `week-plan.md` in full and apply your edits until you approve — approval logged
8. memb-skill — optional, ask first: store the approved Must items — memory ids logged

Nothing in this plan is sent anywhere, so there is no GO step. It only reads the files you named and writes into the save folder, except the opt-in steps 4 (gh queries GitHub) and 8 (writes memB).

Run log: `run-log.md` in the save folder. One line per step as it completes (`N. done|skipped|failed — file — check result`). If a check fails, stop, write the failure into the log and tell the user.
