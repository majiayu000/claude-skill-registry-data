---
name: pb-todo
description: >-
  Turn one sentence into a task line in the right to-do list, with project,
  priority and optional due date. Use for "add a to-do", "remember to ...",
  "put this on my list", "quick task". Nothing leaves your computer.
category: bdb-core
kind: playbook
trigger: ["add a to-do", "put this on my list", "quick task"]
inputs: [sentence, "lists_folder?"]
requires:
  skills: [memb-skill]
  agents: []
  mcps: []
  store: []
go_points: []
outputs: ["<lists>/<project>.md", "run-log.md"]
verify: "the approved line appears exactly once, in one list file"
difficulty: beginner
est_time: 2-5 min
---

# Quick to-do
What you get: one sentence becomes a task line in the right list, with priority and project.

## Inputs
- One sentence describing the task
- A lists folder — asked once; default `./todo/`
- A save folder for the run log — default `./pb-todo-<date>/`

## Steps
1. Ask once — lists folder (and the sentence if not given) → `run-log.md` — the lists folder exists, or you confirm it may be created
2. Parse the sentence → task, project, priority (P1-P3), due date if one is named — anything not stated is `?`, never guessed
3. Pick the list file `<lists>/<project>.md` from the project — a new file only after you say yes → chosen file in `run-log.md`
4. Show the exact line, e.g. `- [ ] P2 task text (due 2026-10-05)`, and wait for your approval — approval logged
5. Append the approved line to the chosen list → the line appears exactly once in that file, and in no other list
6. memb-skill — optional, ask first: store the task — memory id logged; skipped and logged if memB is not installed

Nothing in this plan is sent anywhere, so there is no GO step. It only writes into the lists folder and the save folder, except the opt-in step 6 (writes memB).

Run log: `run-log.md` in the save folder. One line per step as it completes (`N. done|skipped|failed — file — check result`). If a check fails, stop, write the failure into the log and tell the user.
