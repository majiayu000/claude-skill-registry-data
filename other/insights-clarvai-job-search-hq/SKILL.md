---
name: insights
description: "Show how the user's search is going, read-only: where applications stall, which sources bring replies, whether higher fit scores get more replies, applications per week, and why they passed on leads. Use when the user says insights, stats, numbers, what's working, where am I stuck, or asks whether their fit scores are any good."
---

# Insights (chat version)

The chat version of the Claude Insights panel: the same numbers, read from the same files. Read-only: change nothing. For what to change next week, offer `weekly-review`, which reads more (the activity log, interview notes, the Outbox).

## Read

`jobs/tracker.csv` (tolerate a byte-order mark, Windows line endings, quoted commas; read dates as AGENTS.md says, "Reading dates someone else wrote": an unclear date isn't counted in any week), `jobs/leads.csv` and `profile/preferences.md` (`date_order:`, `search_status:`). If the tracker's header is separated by semicolons or a quote never closes, it's damaged: say so and offer to repair it into a copy (the playbook's "Tracker"); show no numbers.

## Count (each job once, by its current stage and its notes)

- **Applied:** status `applied`, `screening`, `interviewing`, `offer`, `accepted`, `rejected`, `withdrawn` or `ghosted`, or a real `date_applied`.
- **Heard back:** applied, and `screening`, `interviewing`, `offer`, `accepted` or `rejected`, or it reached an interview.
- **Interview:** `interviewing`, `offer` or `accepted`, or `rejected`, `withdrawn` or `ghosted` whose `notes` or `next_action` clearly say it got that far (a dated "Interview 2026-10-10", or "interviewed"); "rejected before interview" or "no interview" doesn't count.
- **Offer:** `offer` or `accepted`, or `withdrawn` whose notes say it declined an offer ("declined the offer", "offer received"); "withdrew after accepting another offer" doesn't count.
- **Steps:** applied to heard back, heard back to interview, interview to offer, as "got of had". Give a percentage only when "had" is 10 or more, and name the lowest such step as "your lowest step so far"; with none at 10, say it's too early to name a weak spot.
- **Per week:** applications by `date_applied` in each of the last 8 weeks (Monday to Sunday).
- **Outcomes:** waiting (`applied`), rejected (and how many after an interview), no response (`ghosted`), withdrawn.
- **What seems to help:** heard back for jobs with a contact named (or a referral in the notes) against those without, and for jobs applied to within 3 days of finding them (`date_found` to `date_applied`) against later ones.
- **Do fit scores hold up?** Heard back among fit 5 against fit 1-4 (most applications are fit 4 or 5). Only with 10 or more applications in each: say whether fit 5 has been getting more replies; if not, offer to look at how jobs are being scored. Otherwise "too early to tell".
- **On request (or if they ask what's working):** the same three numbers by `source` (blank is "not recorded"; the 6 biggest), by fit score and by priority, and the top `not-for-me` reasons in `jobs/leads.csv` (`other: ...` counts as other).

## Show

A short block in plain words, numbers first, no charts or emoji: the headline ("20 applied, 10 heard back, 6 interviews, 1 offer"), the three steps, the lowest step, the weekly counts, outcomes, and the fit check. End with one line: "Want a weekly review with what to change?" Small numbers are noise: never call a stage weak below about 10 jobs, and never grade the user.

## The Claude panel (Claude Code only; Codex: skip)

In Claude Code this is the `/job-insights` panel. It only reads; its "Ask Claude for a weekly review" button writes `/weekly-review` in the prompt for the user to send.
