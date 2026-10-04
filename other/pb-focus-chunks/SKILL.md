---
name: pb-focus-chunks
description: >-
  Split one big task into chunks of at most 25 minutes, each with a
  done-check, and place the demanding ones in your high-energy hours. Use for
  "split this task", "break it into chunks", "I can't start this", "focus
  plan". Nothing leaves your computer.
category: bdb-core
kind: playbook
trigger: ["split this task", "break it into chunks", "focus plan"]
inputs: [task, energy_pattern]
requires:
  skills: [concise-planning]
  agents: []
  mcps: []
  store: []
go_points: []
outputs: ["chunks.md", "run-log.md"]
verify: "every chunk is <= 25 min and has a done-check; sum of chunks equals the estimate"
difficulty: beginner
est_time: 5-10 min
---

# Focus chunks
What you get: one big task split into 25-minute chunks, ordered by your energy level, each with a done-check.

## Inputs
- One task, in your own words, with your total time estimate
- Your energy pattern — asked once, e.g. morning high / afternoon low
- A save folder — asked once; default `./pb-focus-chunks-<date>/`

## Steps
1. Ask once — save folder, task, total estimate, energy pattern → `run-log.md` — all answered
2. concise-planning — task and estimate → `chunks.md`: numbered chunks of at most 25 minutes, each with minutes, a done-check and an energy tag (high / low) — every chunk is <= 25 min and has a done-check; the minutes add up to your estimate
3. Order `chunks.md` so high-energy chunks fall into your high-energy slots and low-energy chunks into the rest → slot named per chunk — no high-energy chunk sits in a low slot
4. Show `chunks.md` in full and apply your edits until you approve — approval logged

Nothing in this plan is sent anywhere, so there is no GO step. It only writes into the save folder.

Run log: `run-log.md` in the save folder. One line per step as it completes (`N. done|skipped|failed — file — check result`). If a check fails, stop, write the failure into the log and tell the user.
