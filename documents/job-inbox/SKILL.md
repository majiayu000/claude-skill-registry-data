---
name: job-inbox
description: "Show the user's new job leads from find-jobs in chat and record their choices: save (then add-job), skip, or not for me with a reason. Use when the user says job inbox, leads, new jobs, what did you find, or answers a lead list like \"save 1,3; skip 2\"."
---

# Job Inbox (chat version)

The chat version of the Claude Job Inbox panel: same file, same rules. `jobs/leads.csv` holds every lead `find-jobs` found; read it fresh every time and change only the rows the user decides on.

## The file

Columns (follow the CSV rules in the playbook ("Tracker"; quoting, plain punctuation, and no cell starting with `=`, `+`, `-`, `@` or a tab); dates `YYYY-MM-DD`; it may come from Excel, so tolerate a byte-order mark, Windows line endings and dates like `10/14/2026`, read as AGENTS.md says in "Reading dates someone else wrote", asking the user when a date is still unclear and never rewriting it until they say):

```
id,found_date,company,role,location,remote,pay,posted,link,apply_link,job_id,source,fit_guess,why,concerns,status,reason,decided_date
```

- `status`: `new` (not looked at), `saved` (the user wants it; add-job pending), `added` (add-job made a job folder and tracker row), `skipped`, `not-for-me`.
- `reason`: only for `not-for-me`: `too-senior`, `too-junior`, `wrong-location`, `not-my-field`, `company`, `pay`, or `other: <their words>`.
- `fit_guess`: `A` strong fit, `B` good fit, `C` worth a look.

## 1. Show the list

Leads with `status: new` that are not already in `jobs/tracker.csv` (same company and job ID, or same link or apply link, ignoring `utm_` and similar tracking bits; same company and title at the same place only when a job ID is missing on either side. Two different job IDs are always separate openings). If a `new` lead is already tracked, set it to `added` quietly.

Number them, best fit first, one or two lines each:

`1. Example Co, Operations Analyst, Austin TX (hybrid), $65k-$75k. Strong fit: uses your SAP work`
`   Watch out: needs 2 years. Posting: https://example.com/jobs/123`

Leads found more than 30 days ago go last under "Older (may be filled)". Then any `saved` ones under "Saved, not added yet". Nothing new? Say so and offer `find-jobs`.

End with one line: "Tell me what to do, for example: save 1, 3; skip 2; 4 not for me, too senior."

## 2. Record what they say

Re-read the file right before each change. For each lead they name, change only its row:

| They say | Change |
|---|---|
| save / yes / keep | `status=saved`, `decided_date=today` |
| skip / pass / no | `status=skipped`, `decided_date=today` |
| not for me (+ why) | `status=not-for-me`, `reason` from the list above (ask once for a reason if they gave none; offer the choices: too senior, too junior, wrong location, not my field, the company, pay, something else), `decided_date=today` |
| undo / put it back | `status=new`, clear `reason` and `decided_date` |

Accept loose answers: "save 1,3; skip the rest", "all of them", "not 4, wrong city", and the same in the user's own language (match by meaning; the saved `status` and `reason` values stay in English, as listed). If a number is unclear, ask.

Then:
- Add **one** line to `history/activity.md` for the whole batch, e.g. `- 2026-10-06 14:05 · Codex · Job leads reviewed: saved 2 (Acme Corp - Data Analyst; Globex - Marketing Coordinator), skipped 1, not for me 1 (too senior)` (time from the computer).
- If they saved any, run `add-job` on those links now (all together), unless they say later. `add-job` sets each lead to `added`.
- If several `not-for-me` reasons repeat (say three "too senior"), mention that the next search will aim lower (find-jobs reads these reasons).

## Rules

- Never apply, sign in, or contact anyone from here. Saving a lead only adds it to the user's list.
- Don't delete rows; skipped and not-for-me rows keep `find-jobs` from suggesting the same posting again.

## The Claude panel (Claude Code only; Codex: skip)

In Claude Code the leads show as cards in the `/job-inbox` panel. The user presses Save, Skip, or Not for me (with a reason); it writes `jobs/leads.csv` and adds one line per sitting to `history/activity.md`. On each Save it leaves a `[Job Inbox]` note: run `add-job` on the saved leads (together) when the user next talks to you; `add-job` marks each lead added.
