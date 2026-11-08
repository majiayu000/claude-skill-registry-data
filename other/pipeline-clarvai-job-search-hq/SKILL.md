---
name: pipeline
description: "Show the user's job board in chat (every application by stage, with next steps and due dates) and update it when they say what happened: applied, got a call, interview scheduled, rejected, offer. Use when the user says pipeline, board, my jobs, where do things stand, or reports a change to an application."
---

# Pipeline (chat version)

The chat version of the Claude Pipeline panel. `jobs/tracker.csv` is the only source of truth: read it fresh every time, and change it only in the rows the user is talking about. The file has no lock, so one writer at a time (the playbook's "One writer at a time" says why and what to tell the user).

## Show the board

Read `jobs/tracker.csv` (it may come from Excel: tolerate a byte-order mark, Windows line endings, quoted commas, and dates like `10/14/2026`; write dates back as `YYYY-MM-DD`). Read dates as AGENTS.md says ("Reading dates someone else wrote"); a date that is still unclear shows as "date unclear", never counts as due or overdue, and is never rewritten until the user says what it means. If the file is damaged (a semicolon-separated header, or a quoted value that never closes), don't edit it: say so and offer to repair it into a copy for them to check. If it has only the header, say "Nothing tracked yet" and offer `add-job` or `find-jobs`. If `profile/preferences.md` has a `search_status: closed` line, lead with "Search closed" (the user accepted a job) before showing anything.

Show a compact board, open stages first, in this order: Offer, Interviewing, Screening, Applied, Interested. One line per job:

`Example Co, Operations Analyst, next: onsite interview, Thu Oct 9`

Mark anything due today or overdue, and any application or offer `deadline` within 3 days, with the words "due" or "overdue" (no emoji) and put those first. A passed offer deadline is "offer deadline passed" (first); a passed application deadline on an `interested` job is "deadline passed" (suggest checking the posting or marking it skipped), not "overdue" forever. A row whose `notes` start with `Also: <what> YYYY-MM-DD` (e.g. `Also: Interview 2026-10-20`, `Also: Take-home due 2026-10-18`) has a second commitment: show it on its own line and count it by its own date. With `search_status: closed`, still show unsent withdrawal notes (`Send withdrawal note`). Under the board, one line of counts (e.g. "9 open · 2 due today · 1 deadline this week") and the weekly goal from `profile/preferences.md` if it helps. Closed jobs (accepted, rejected, withdrawn, skipped, ghosted): just a count, and list them only if they ask.

An `interested` job whose latest line in `history/posting-watch.md` (the posting watch) says `closed`: add "posting looks closed (checked <date>)" and offer to mark it `skipped`, with `Skipped: posting closed (checked <date>)` added to its notes (ask first).

On Mac or Linux (or Windows with Git Bash), `bash .claude/hooks/summary.sh long` prints the same counts; use it as a cross-check if it runs.

## Update it

When the user says what happened, change only that job's row. Check its current status first: if an application is already recorded (`applied`, `screening`, `interviewing`, `offer`, `accepted`, `rejected`, `withdrawn` or `ghosted`), "I applied" is not news. Keep its status, next step and `followups`; change `date_applied` only if the user says the recorded date is wrong. A second application to the same company needs its own posting and row.

| The user says | Change |
|---|---|
| "I applied to X" (today, yesterday, a date), row `interested` or `skipped` | `status=applied`, `date_applied` = the real date, `next_action=Follow up`, `next_action_date` = 7 business days after applying, `followups=0` |
| "They called / recruiter screen set" | `status=screening`, next step and date from what they said |
| "Interview scheduled for <date>" | `status=interviewing`, `next_action=Interview <date>`, `next_action_date` = that date; if the row already has a booked interview or `Take-home due <date>`, follow the playbook's "Two commitments at once" rule (`Also:` token); offer `interview-prep` |
| "Got an offer" | Whatever the old next step was: `status=offer`, `next_action=Respond to offer`, and ask for the answer-by date. Put it in `deadline` (replacing any old application deadline) with `next_action_date` 3 days before it (today if sooner); until they know it, `next_action_date` = today. Offer the `offer` skill |
| "Rejected" / "I withdrew" / "not applying" / "never heard back, give up" | `rejected` / `withdrawn` / `skipped` / `ghosted`; clear `next_action` and `next_action_date` |
| "Did the next step" | if `notes` start with an `Also:` item, that becomes the next step and the token is removed (date: the interview date, or for a take-home two days before it's due, or today if sooner); otherwise set `next_action` to the real next step if they know it, or "Decide next step" due today; an open job always keeps a next step |
| "Push it back a week" | move `next_action_date` 7 days later |
| "I accepted!" | `status=accepted`; clear `next_action` and `next_action_date`; congratulate them, then offer the "Closing the search" wrap-up in the `offer` skill |

Statuses and columns are in `knowledge/job-search-playbook.md` ("Tracker"). If a company has two rows (two postings), ask which one, or use the `folder` column to tell them apart.

After saving: re-read the row to confirm it saved, add one line to `history/activity.md`, and tell the user in one sentence what changed and when the next step is. If the save fails because the file is open in Excel, ask them to save and close Excel, then try again.

## Rules

- Re-read the tracker right before each change and edit only the affected row; never rewrite the file from an older copy (the other app may have changed it).
- Don't mark something applied or sent unless the user says it happened.
- If the dashboard page is published (`profile/published-pages.md`), offer to refresh it afterwards (in Codex: refresh the local file; republishing the link needs Claude).

## The Claude panel (Claude Code only; Codex: skip)

In Claude Code the board is the `/pipeline` panel. The user changes stage, next step and due date there; it writes `jobs/tracker.csv`, adds a line to `history/activity.md`, and leaves a `[Pipeline]` note. The change is already saved: don't re-apply it; take it into account, and republish the dashboard if the note asks. A saved job whose posting the posting watch found closed has a **Skip it: posting closed** button (same change as above). A one-line band above the prompt shows the pipeline summary, plus Contacts follow-ups due and new Job Inbox leads when there are any.
