---
name: seekter-report
description: Summarise the job search from the markdown tracker - funnel, response rate, what's working, where applications come from, what's pending on the user. Use when the user runs /seekter-report or asks how the search is going, for weekly numbers, or what to change.
---

# /seekter-report — how is the search going

Read-only. Data comes from `applications/` via `scripts/seekter.py`, plus `runs/*.md` for per-day source tables.

1. `python3 scripts/seekter.py stats` (all time) and `python3 scripts/seekter.py stats --since <7 days ago>`.
2. `python3 scripts/seekter.py list --since <period start>`, then read the front matter of the rows you need (source, ats, location_fit, fit).
3. Compute, for the period and all time:
   - applications sent, skips, pending hand-offs;
   - replies: interviewing + offer + rejected, as a share of sent; median days from `applied` to the first log line after it;
   - by `source` (freehire, linkedin, board names, manual): sent and replies;
   - by `location_fit` (A/B/C): sent and replies. A track with many sends and no replies is a targeting signal;
   - top skip reasons (group the Reason column of `applications/<YYYY-MM>/skipped.md` by its first clause).
4. Every record with `status: pending` is a hand-off (`python3 scripts/seekter.py list --status pending`; also the "Needs you" table in `applications/README.md`): list each with its link and the exact action.
5. Write 3–5 plain observations with the number behind each ("C-track: 14 sent, 0 replies in 3 weeks"). Suggest at most two changes, each tied to a file (`profile/search.json` query, `profile/profile.md` rule). Don't change them without the user saying yes.

Save as `runs/report-<YYYY-MM-DD>.md` and show the user the short version.
