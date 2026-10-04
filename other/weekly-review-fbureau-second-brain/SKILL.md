---
name: weekly-review
description: Synthesize the week from the daily notes into a weekly review note — themes, decisions, people focus, patterns, energy, and a plan for next week. Use when the user says "weekly review", "recap of the week", "how did the week go", or as the Monday scheduled job.
version: 4.2.1
author: fbureau
license: MIT
metadata:
  hermes:
    tags: [second-brain, synthesis, review]
    related_skills: [daily-digest, prioritize]
    requires_toolsets: [second_brain]
---

# Weekly review (Hermes edition)

The daily notes already say what happened. A weekly review that repeats them is worthless. Its job is
to say what the week **meant** — the pattern across days that no single day shows.

1. `sb_brief`, then `sb_vault_activity(since_hours=168)` for everything the week touched.
2. `sb_read` each `01-daily/` note of the week. Read them all before writing anything: the pattern is
   only visible once.
3. `sb_agenda()` for the state the week ends in, and `sb_maintain(scope="staleness", apply=false)` for
   the relationships that cooled while the week was busy.
4. Synthesize, in the working language. Three or four themes, not ten. For each: what happened, what
   it cost, what it means. A theme that is just a list of meetings is not a theme.
5. Cover explicitly, because these are what a week hides:
   - **Decisions** made and, more usefully, the ones deferred again. Name what deferring costs.
   - **People** — who took most of the week, and who should have but did not.
   - **Patterns** — what repeated. Compare with the previous weekly note if one exists (`sb_search`).
   - **Energy** — from the braindumps' `energy` field, what drained and what did not.
   - **Weak signals** — things mentioned once that would matter if true.
6. Plan next week in at most five items, each tied to a theme. Not a task list: `/prioritize` does that.
7. `sb_create_note(type="daily", fields={date, tags:["weekly"]}, preamble=<2-3 English sentences: what
   week this covers, why, when>, sections={...}, slug=<"YYYY-WNN weekly">)`, then
   `sb_daily_append(section="Thinking", line="- Weekly review: [[<path>]]")`.
8. `sb_commit("weekly-review: <week>")`.
9. Report the review itself in the reply, not just its path — for the scheduled run, the reply is the
   deliverable. Keep it to one screen.
