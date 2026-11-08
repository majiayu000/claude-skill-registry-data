---
name: routines
description: "Use when the user wants automatic checks: new jobs every morning, watching their inbox, daily follow-up drafts, a weekly review, checking saved postings are still open, or asks to 'automate', 'schedule' or 'run this every day'. Sets up opt-in routines on their own computer that only read, draft and track, and spots ones that stopped running."
---

# /routines: automatic checks

A routine is a check the app runs by itself on a schedule, on the user's own computer, while they do something else. Each run starts a fresh session, does one job, and leaves the results in the folder: new leads in the Job Inbox, drafts in the Outbox, a line in the tracker, a weekly review. **Routines only read, draft and track.** They never send, apply, publish, accept anything, or change `profile/`, and they ask no questions (anything that needs the user waits for them, listed). Nothing is set up without the user's yes, and they can pause or delete a routine any time.

## 1. Explain and recommend

Say it in two or three plain sentences (above), then where it runs (step 3), then the cost: **each run uses their Claude or ChatGPT plan like a short chat**, so once a day beats hourly, and the scans skip the heavy research. Recommend one to three, not all six, from what fits their search (on a small plan, see AGENTS.md "Cost and pace": at most two, and the morning scan and the weekly review first). The schedules below are the cheap defaults: two or three scans a week find nearly everything a daily one does (`find-jobs`), and `/today` covers follow-ups between runs. Each instruction line starts with a quick pre-check, so a run with nothing to do (setup not done, the search paused or closed, the review already done) stops after a few hundred tokens:

| Routine | Schedule | When it fits | Instructions (paste exactly) |
|---|---|---|---|
| morning scan | Mon, Wed, Fri, 8:00 | Almost everyone actively looking | `Job Search HQ morning scan: first run `bash .claude/skills/routines/scripts/precheck.sh "morning scan"` (Windows without bash: `powershell -NoProfile -ExecutionPolicy Bypass -File .claude\skills\routines\scripts\precheck.ps1 -Routine "morning scan"`); if it prints SKIP, stop. Otherwise follow the find-jobs skill in scheduled mode.` |
| inbox check | Weekdays, 7:30 | Gmail, or a Microsoft 365 mailbox, connected to this app | `Job Search HQ inbox check: first run `bash .claude/skills/routines/scripts/precheck.sh "inbox check"` (Windows without bash: `powershell -NoProfile -ExecutionPolicy Bypass -File .claude\skills\routines\scripts\precheck.ps1 -Routine "inbox check"`); if it prints SKIP, stop. Otherwise follow the sync-inbox skill in scheduled mode.` |
| follow-up drafts | Mon and Thu, 9:00 | Several applications or contacts in play | `Job Search HQ follow-up drafts: first run `bash .claude/skills/routines/scripts/precheck.sh "follow-up drafts"` (Windows without bash: `powershell -NoProfile -ExecutionPolicy Bypass -File .claude\skills\routines\scripts\precheck.ps1 -Routine "follow-up drafts"`); if it prints SKIP, stop. Otherwise follow the follow-up skill in scheduled mode.` |
| weekly review | Weekly, Friday 16:00 | Anyone; pairs well with the morning scan | `Job Search HQ weekly review: first run `bash .claude/skills/routines/scripts/precheck.sh "weekly review"` (Windows without bash: `powershell -NoProfile -ExecutionPolicy Bypass -File .claude\skills\routines\scripts\precheck.ps1 -Routine "weekly review"`); if it prints SKIP, stop. Otherwise follow the weekly-review skill in scheduled mode.` |
| posting watch | Weekly, Monday 8:30 | Several saved jobs (`interested`) not applied to yet | `Job Search HQ posting watch: first run `bash .claude/skills/routines/scripts/precheck.sh "posting watch"` (Windows without bash: `powershell -NoProfile -ExecutionPolicy Bypass -File .claude\skills\routines\scripts\precheck.ps1 -Routine "posting watch"`); if it prints SKIP, stop. Otherwise follow the routines skill's posting watch in scheduled mode.` |
| certification reminder | Weekly, on their certification day, 9:00 | Only if `benefits_cert_day:` is set in `profile/preferences.md` | `Job Search HQ certification reminder: first run `bash .claude/skills/routines/scripts/precheck.sh "certification reminder"` (Windows without bash: `powershell -NoProfile -ExecutionPolicy Bypass -File .claude\skills\routines\scripts\precheck.ps1 -Routine "certification reminder"`); if it prints SKIP, stop. Otherwise follow the routines skill's certification reminder in scheduled mode.` |

Use the user's own times if they give them (in their time format), and the names above so the startup note can report results. Read `profile/preferences.md` first: before setup is done, while the search is paused (a "search paused until" note with a future date) or closed (`search_status: closed`), suggest finishing setup or resuming the search first (only the certification reminder makes sense then). Ask which ones they want (one question), and go ahead only on a clear yes for each. If they say they don't want any ("no thanks", "not now"), log `routines · not wanted` (see "The routine log" below) so `/today` stops offering them; they can still ask any time.

## 2. Find out which app they're in

From this session (the Claude desktop app's Code tab, the Claude terminal, Codex in the ChatGPT desktop app, or the Codex terminal or editor); ask once if you can't tell. If they use both apps on this folder, set up each routine in one app only, so the same check doesn't run twice.

## 3. Set it up

**Claude desktop app (Code tab).** Needs Claude Desktop 1.1.5368 or later.
- If this session can create scheduled tasks (a tool for them is available), offer to make it: after the yes, create each one with the name, a one-line description, the instructions line from the table, its schedule, and this folder as the working folder, **not** in an isolated worktree, in Auto permission mode where the tool lets you choose. Then tell them to check those three settings on the routine's **Edit** page.
- Otherwise, walk them through it, one step at a time: **Routines** in the sidebar (or the sidebar's **More** menu) → **New routine** → **Local**. Fill in **Name** and **Description**, paste the instructions line into **Instructions**, pick **Auto** in the permission-mode picker under it (if Auto isn't offered, pick **Accept edits** and do the "Run now" step below carefully), choose **this folder** as the working folder, and leave the **isolated worktree** switch **off**. Pick the **Schedule**, then save.
- Why the worktree stays off: a worktree is a separate copy of the app without the user's own files (their tracker, profile and drafts are never copied into it), so the routine would find nothing and its results would vanish.
- Then **Run now** once and watch it. If it stops to ask permission for something, choose "always allow" so later runs don't stall (a run waiting for an answer just sits there until they come back). Each run appears under **Scheduled** in the sidebar with a desktop notification.
- It runs only while the Claude app is open and the computer is awake. A run missed while asleep happens once when the computer wakes (only the latest missed one). **Settings → This computer → System → Keep computer awake** prevents idle sleep; closing a laptop lid still sleeps it.

**Codex (ChatGPT desktop app).** Open **Scheduled** in the sidebar (or ask in a chat to schedule it) and create a task with the instructions line and schedule. Choose this folder's **local project**, **not** a new worktree (the same reason as above). The computer must stay on and the app running. Runs happen unattended with the default sandbox and no approval prompts, and results arrive in **Scheduled**, which works like an inbox. The Codex terminal and editor extension can't manage scheduled tasks: suggest the ChatGPT desktop app.

**Claude terminal.** There's no lasting scheduler here: a repeating task (`/loop`) only runs while that terminal session stays open, and stops after 7 days. Good for "watch for replies this afternoon" (for example `/loop 1h /sync-inbox`), not for every day; for daily checks, suggest the Claude desktop app on the same folder. Never suggest cloud routines (`/schedule`, claude.ai): they run on a fresh copy of a GitHub repository, can't see this folder's files, and would need the user's data on GitHub.

After setting up, add one line to `history/activity.md` (e.g. `Routine set up: morning scan, weekdays 8:00`), log `<name> · set up (<cadence> <time>)` in the routine log (below), and tell the user what they'll see: a short note when they next open the app ("Your morning scan found 4 new leads"), and the results in the Job Inbox, Outbox or `interviews/`. Set up in the Claude terminal with `/loop` is not a routine: log nothing for it.

## The routine log

`history/routines.md` (create it if missing, starting with the line `# Routine results` and a blank line) has one line per run, written by the runs themselves (`references/scheduled-mode.md`), plus these lines you add when the user tells you, so the startup note and `/health` can tell a routine that stopped running from one they turned off:
- `- <date time> · <name> · set up (<cadence> <time>)`, and `changed (<cadence> <time>)` when they change its schedule. `<cadence>` is exactly one of `daily`, `weekdays` (also Mon, Wed, Fri or Mon and Thu), `weekly` or `fortnightly` (every other week), in English like the CSV values, e.g. `- 2026-10-22 09:10 · morning scan · set up (weekdays 8:00)`. For a rarer schedule (monthly), say so and use `fortnightly`; it may be flagged between runs.
- `- <date time> · <name> · paused`, `resumed` or `deleted`. Only `set up` and `resumed` make a paused routine count as running again; a schedule change doesn't.
- `- <date time> · routines · offered` when `/today` offers routines, and `routines · not wanted` when they decline them; either one stops `/today` offering again.
Date and time from the computer, as in AGENTS.md. Never edit or remove earlier lines.

## When a routine stops running

The startup note and `/health` flag a routine with nothing in the log for longer than its schedule allows (more than 2 days for a daily one, 4 for weekdays, 9 for weekly, 16 for fortnightly; quiet for over 45 days counts as removed). Tell the user in one line, then help them check, one step at a time: the app (the Claude desktop app or the ChatGPT desktop app) must be open and the computer awake at that time; the routine must use **this folder** with the isolated worktree **off** (a run in a worktree logs into a copy that's thrown away); a run may be sitting there waiting for a permission answer (open it under **Scheduled** and choose "always allow"); and a moved or renamed folder leaves the routine pointing at the old place. Then **Run now** once and check that a new line appears. If they paused or deleted it on purpose, log `paused` or `deleted` so it isn't flagged again.

## Pause, change or delete

- **Claude desktop app:** **Routines** → click the routine → **Status** (Active / Paused), **Edit**, **Run now**, or **Delete** (tick **Also delete files on disk** to remove its saved instructions too). They can also ask Claude in any desktop session ("pause my morning scan").
- **Codex:** open the task in **Scheduled** to pause or remove it, or ask in a chat.
- Whichever way it happens, log it as "The routine log" says (`paused`, `resumed`, `deleted`, or `changed (...)` for a new schedule).
- When the user pauses their search, suggest pausing every routine except the certification reminder; when they accept a job, suggest deleting them, keeping the certification reminder until the new job starts if `benefits_cert_day:` is set (`my-data` and `offer` ask this). A paused or closed search makes runs skip on their own anyway, but each skipped run still starts a session. Also suggest it when they move or rename this folder (a routine keeps pointing at the old place).

## Show the routines

When the user asks how their routines are doing ("show my routines", "are my automatic checks working?"), list each one from the routine log by the same rules as the startup note (`scripts/routine-status.sh`, or `.ps1` on Windows without bash, prints them; its states mean running, seems to have stopped, paused or deleted, and unused for over 45 days): its name, schedule, when it last ran and its last result, stopped ones first. Then offer what fits: help with one that stopped ("When a routine stops running"), or setting some up if there are none.

**The Claude panel (Claude Code only; Codex: skip).** In Claude Code this is the `/routines-board` panel, and a note above the prompt appears while a routine seems to have stopped. Its "I paused it", "I deleted it" and "I turned it back on" buttons write that line in the routine log, add a line to `history/activity.md` and leave a `[Routines]` note: the change is already logged, so don't log it again; only remind the user that the routine itself is changed in the desktop app. "Help me fix it" writes a request in the prompt for the user to send.

## How scheduled runs behave

Every routine follows `references/scheduled-mode.md` plus the "Scheduled mode" section of its own skill. Results are logged to `history/routines.md`; the startup note shows the last day's results.

## Posting watch

Checks once a week whether the saved jobs the user hasn't applied to yet are still open, so they don't prepare an application for a posting that's gone. As a routine it runs in scheduled mode; the user can also ask any time ("are my saved jobs still open?"). Follow `references/posting-watch.md`.

## Certification reminder (scheduled mode)

Run only when the instructions say scheduled mode. Follow `references/scheduled-mode.md` (it keeps this reminder running on a paused or closed search). If `benefits_cert_day:` is blank (it's cleared when a new job starts), log `no certification day set; this routine can be deleted` and stop. If today isn't the user's certification day by `benefits_cert_day:` (a weekday, or "every other <weekday> from YYYY-MM-DD"), log `not certification day` and stop. Otherwise, read only: count the benefit week(s) being certified the way `today` does (records in `jobs/tracker.csv`, `contacts/contacts.csv`, sent Outbox files and `jobs/work-search-log.csv`; no drafts), applications and other activities separately, against the agency's number in `.claude/skills/work-search-log/references/requirements.md`. Don't write to `jobs/work-search-log.csv`. Log e.g. `certify today; 3 of 3 activities recorded` or `certify today; 1 of 3 recorded, open the app and say "work search log"`. The user certifies on the agency's site themselves.
