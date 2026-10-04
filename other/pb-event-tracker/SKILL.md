---
name: pb-event-tracker
description: >-
  Build one spreadsheet for an event covering guests, vendors, timeline and
  budget, from your event brief and vendor list, and draft the vendor
  messages for your GO. Use for "event tracker", "plan this event", "track
  vendors and budget", "event spreadsheet".
category: media-eventtech
kind: playbook
trigger: ["event tracker", "track my event", "vendor and budget sheet"]
inputs: [event_brief, vendor_list]
requires:
  skills: [bdb-eventagency-skill]
  agents: []
  mcps: []
  store: []
go_points: [send vendor or guest messages]
outputs: ["brief.md", "tracker.csv", "summary.md", "vendor-requests-draft.md", "run-log.md"]
verify: "summary.md total recomputed from tracker.csv matches"
difficulty: intermediate
est_time: 20-40 min
---

# Event tracker
What you get: guests, vendors, timeline and budget for one event in a single spreadsheet.

## Inputs
- An event brief — a text or document file describing the event
- A vendor list — a file with the vendors and what each provides
- A save folder — asked once; default `./pb-event-tracker-<date>/`

## Steps
1. Ask once — save folder, event brief, vendor list → `run-log.md` — the files are readable
2. bdb-eventagency-skill (section "2. Client & Project Intake") — brief → `brief.md` with date, venue, attendance estimate, budget range — missing fields listed as `?`
3. bdb-eventagency-skill (section "4. Vendor Management", status list) — vendor list → `tracker.csv`, columns section, item, owner, status, due, cost, notes; sections guest, vendor, timeline, budget (the budget section holds one budget line whose amount goes in `notes`, never in `cost`; costs sit on their rows; guest rows from a guest list if given, else one `?` row) — every vendor from your list is present
4. bdb-eventagency-skill (section "5.1 Pre-production", run-of-show and day-minus milestones) — event date → timeline rows in `tracker.csv` (date `?` → ask, else skip the timeline and log it) — no row dated after the event
5. Total = sum of `cost` over all rows except the budget row; budget = the amount in the budget row's `notes` → `summary.md` with total versus budget, over or under — the sum recomputed from `tracker.csv` matches; budget `?` is reported as "budget unknown"
6. Show `tracker.csv` and `summary.md` in full and apply your edits until you approve — approval logged
7. Write `vendor-requests-draft.md` (requests and confirmations), each recipient as name + address (`?` blocks sending until you fill it) — draft only, nothing is sent
8. [GO] Send the vendor or guest messages through a connector you name, or send them yourself — show every recipient and the full text of every message first. The run stops here until the human types GO. The GO covers exactly the recipients and messages shown and nothing else; a different or added recipient needs a fresh GO. Never send to anyone not listed in `vendor-requests-draft.md`.

The tracker is a CSV file that opens in any spreadsheet app.

Run log: `run-log.md` in the save folder. One line per step as it completes (`N. done|skipped|failed — file — check result`), and `WAITING FOR GO: <step>` at the gate. Anything other than the literal GO (case-insensitive) is not a GO. If a check fails, stop, write the failure into the log and tell the user.
