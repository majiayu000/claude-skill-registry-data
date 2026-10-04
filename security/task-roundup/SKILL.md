---
name: task-roundup
description: Refresh TODO.md from every action item in the vault (both-ways checkbox sync via ^t-id anchors), mark tasks done, and resolve the cases the maintenance tool cannot decide alone. Use when the user says "task roundup", "my todo", "what do I have to do", "I finished X", "sync tasks", or as the scheduled maintenance job.
version: 4.2.1
author: fbureau
license: MIT
metadata:
  hermes:
    tags: [second-brain, tasks, maintenance]
    related_skills: [daily-digest, knowledge-stub]
    requires_toolsets: [second_brain]
---

# Task roundup (Hermes edition)

The tool does the bookkeeping (scan, anchors, reconcile, buckets, hubs, staleness); you handle
the judgment calls it hands back in `needs_judgment`. Source notes stay the truth; TODO.md is a view.

1. `sb_brief`.
2. If the user reports completions ("I sent the QA plan"): `sb_search(text)` or `sb_read("TODO.md")` to find the
   line and its `^t-id`, then `sb_toggle_task(anchor, done=true)`. Ask when two lines could match.
3. `sb_maintain(scope="tasks")` — or `"all"` for the scheduled run (also rebuilds hubs, refreshes staleness
   flags, audits health). Read the report: tasks, new anchors, reconciled counts, buckets.
4. Resolve `needs_judgment`, one decision each, in the working language:
   - `unassigned-owner` → propose the likely owner from the meeting context; **ask** before writing; write via
     `sb_append_section` on the source note if the user confirms (never edit the original line).
   - `source-removed` → ask: drop the TODO entry or restore the line in its source note?
   - `zombie-task` → ask whether it is still relevant; if not, `sb_toggle_task(anchor, done=true)` with the user's ok.
   - `near-duplicate` (scope all) → compare the two pages with `sb_read`; propose a merge; never merge silently.
   - `new-hub` (scope all) → propose the hub with its member notes; create it only on the user's yes
     (`sb_create_note type=index fields={domain, tags:[domain], "auto-maintained": true}`), then `sb_maintain(scope="curator")`.
   - `curator-unstable` → report it as a bug signal, do not loop.
   In a scheduled run with nobody to ask, list the questions in the report and change nothing for them.
5. `sb_commit("task-roundup")`.
6. Report: ⏰ overdue · 📅 today · ⏳ waiting, what was reconciled, the open questions. Offer `sb_read("TODO.md")`
   if the user wants the full list.
