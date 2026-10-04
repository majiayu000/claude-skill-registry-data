---
name: pb-handover
description: >-
  Write a handover note for a colleague from the state of a project folder:
  what is done, what is open, what is risky, the next 3 steps and where
  things live. Sent only after your GO. Use for "handover note", "hand this
  project over", "I'm going on leave, brief my colleague".
category: bdb-core
kind: playbook
trigger: ["handover note", "hand this project over", "brief my colleague"]
inputs: [project_folder, colleague_name]
requires:
  skills: [quick-recap, memb-skill, github, "gh (external)"]
  agents: []
  mcps: []
  store: []
go_points: [send handover]
outputs: ["handover.md", "run-log.md"]
verify: "every open item cites a file, commit or PR"
difficulty: beginner
est_time: 10-20 min
---

# Handover note
What you get: a handover note for a colleague from the state of a project folder.

## Inputs
- A project folder
- The colleague's name
- A save folder — asked once; default `./pb-handover-<date>/`

## Steps
1. Ask once — save folder, project folder, colleague name → `run-log.md` — the folder exists
2. Read the folder and its git log (read-only); github — only if `gh (external)` is installed: your open pull requests for this repo → list of files, recent commits and open PRs in `run-log.md` — if gh is missing, skipped and logged
3. quick-recap — folder state and recent commits → what is done, what is in progress — each point cites a file or commit
4. memb-skill — search open commitments for this project → added tagged `[memB]` — skipped and logged if memB is not installed
5. Write `handover.md`: done, open, risks, next 3 steps, where things live — every open item cites a file, commit or PR; nothing invented, unknown is `?`
6. Show `handover.md` in full and apply your edits until you approve — approval logged
7. [GO] Send the handover through a connector you name, or send it yourself — show the recipient (name + address, `?` blocks sending until you fill it) and the full text first. The run stops here until the human types GO. The GO covers exactly the recipient and message shown and nothing else; a different or added recipient needs a fresh GO. The go-gate hook does not guard sending: this [GO] is the only guard.

Run log: `run-log.md` in the save folder. One line per step as it completes (`N. done|skipped|failed — file — check result`), and `WAITING FOR GO: <step>` at the gate. Anything other than the literal GO (case-insensitive) is not a GO. If a check fails, stop, write the failure into the log and tell the user.
