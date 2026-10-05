---
name: quarter-rollover
description: Run the quarter-boundary ritual — roll the quarter-scoped project folders, archive finished projects, grade the closing quarter's GOALS/OKRs, and draft the new quarter's goals behind an approval gate. Trigger on /quarter-rollover, "quarter rollover", "roll the quarter", "close out Q2", "new quarter setup", or when tools/quarter_path.py --check reports drift. Distinct from /triage-tasks (daily gate) and /audit (repo health check).
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
model: opus
---

# Quarter Rollover — skill entry point

You are running the `quarter-rollover` skill. It executes the SOP at
[workflows/quarter_rollover.md](../../../workflows/quarter_rollover.md), which is
authoritative — read it first and follow its seven steps. Do not duplicate its
content here; consume it.

## What this skill does

Closes one calendar quarter and opens the next across the whole workspace:
project folders roll and go cold, finished work is archived, the closing
quarter's goals and OKRs are **graded against evidence**, and the new quarter's
goals are drafted for approval.

Start with `python3 tools/quarter_path.py --check` — its output is your todo
list. If it exits 0 and `projects/` has no dormant folders, say so and stop;
there is nothing to invent.

## Load-bearing rules (do not improvise)

- **Grade before you rewrite.** Step 4 (grade the closing quarter) comes before
  Step 5 (write the new one). A quarter overwritten un-graded destroys the track
  record and quietly ratchets down ambition. If the user pushes to skip straight
  to new goals, say plainly what gets lost, then follow their call.
- **Step 5 is a hard approval gate.** Draft the new quarter's goals from evidence
  and present them in chat. Do NOT write them into `areas/personal/GOALS.md`
  until the user approves or edits. Grading is evidence work you own; deciding
  what the next 90 days are for is a founder taste call you don't.
- **Grade from evidence, not vibes.** Every verdict cites something checkable —
  a shipped file, a `Closed` task row, a `daily/` note, a financial number.
  Docs drift optimistic *and* under-credit shipped work; check both directions
  and say when evidence is missing rather than guessing a grade.
- **Never hard-code a quarter path.** Pipelines resolve their folder via
  `python3 tools/quarter_path.py <slug>`. If you find a literal
  `projects/YYYY-QN-…` in a workflow, skill, or agent file, that's a regression —
  fix it and mention it.
- **Archive, never delete.** Closed project folders move to `archive/YYYY/` with
  `git mv`. Fix relative-link depth after the move (one level deeper) and leave a
  closing pointer to the successor folder in the archived README.
- **Respect the exceptions.** Living-document projects (files updated in place,
  not one-dated-file-per-run) do not roll even if their folder carries a legacy
  quarter prefix; daily notes never archive; areas never roll. See the SOP's
  Exceptions section before "fixing" any of them.

## Arguments

Optional `$ARGUMENTS`: a quarter to close (e.g. `2026-Q2`) when running late or
back-filling. Default: close the quarter that just ended relative to today.

## Start now

Read [workflows/quarter_rollover.md](../../../workflows/quarter_rollover.md),
run `python3 tools/quarter_path.py --check`, and begin at Step 1.
