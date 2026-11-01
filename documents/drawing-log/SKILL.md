---
name: drawing-log
description: "Maintains a drawing issue log in docs/drawings/log.md: every sheet in the set, its current revision, and every dated issuance with its purpose. Trigger on \"drawing log\", \"issue log\", \"sheet log\", \"revision log\", \"what rev is\", \"when did we issue\", \"drawing register\", \"drawing-log\", or a request to record that a set went out. The sheet list can be seeded from a drawing-set-bookmarker index or typed; revisions and issue dates come from you, never from a guess. Superseded sheets are marked, not deleted, so the log answers what was in force on any past date. It records what was issued to whom; the cover sheet for a package is create-transmittal's job, and what changed inside a sheet is drawing-diff's."
license: MIT
metadata:
  title: "Drawing Log"
  summary: "Track every sheet's revision and issue history in one log"
  discipline: "construction-admin"
  tags: "Project Management"
---

# Drawing Log

Six months in, the set has been issued nine times for four purposes, a third
of the sheets have been revised at least twice, and somebody on site is
building from the wrong one. The log is how you answer "what is current" and
"what did they have on March 12th" without archaeology. This keeps that log.

## Scope and limits — read first

**What this does.** Maintains `docs/drawings/log.md`: a sheet table (number,
title, current revision, status) and an issue table (date, purpose,
recipients, which sheets went at which revision). Records new sheets, new
revisions, and new issuances as you report them, and reads the log back to
answer what is current, what changed between issues, and what any recipient
holds.

**What this does not do.**

- **It does not know your revisions.** A sheet's revision changes only when
  you say it was revised, and an issue exists only when you say the set went
  out. It never marks a sheet revised because time passed or a PDF appeared.
- It does not read the drawings. What changed inside a sheet is
  `drawing-diff`'s job; this log records only that it changed and when.
- It does not write the transmittal. `create-transmittal` makes the cover
  sheet for a package; this records that the package went, to whom, and what
  was in it.
- It does not decide what sheets the set should contain.
  `drawing-checklist` answers what a phase expects; this records what exists.
- It does not manage CAD or BIM files, sheet numbering standards, or title
  blocks.

**What you need before starting.** The sheet list: typed, pasted, or read
from a `drawing-set-bookmarker` index file. After that, the habit of telling
the log when sheets are revised and sets go out.

## Workflow

### Step 1. Bootstrap if needed

Check whether `docs/drawings/log.md` exists. If not, copy
`assets/drawing-log-template.md` there. If a `drawing-set-bookmarker` index
exists in the project, offer to seed the sheet table from it; otherwise ask
for the sheet list. If the project has no `docs/` folder at all, confirm
before creating one.

### Step 2. Record sheets

One row per sheet: number and title exactly as the title block has them,
current revision as you state it, status `active` or `superseded`. A sheet
added mid-project records the date it entered the set.

### Step 3. Record an issue

Each time a set goes out, one entry: issue number sequential (`ISS-01`),
date, purpose in your words (pricing, permit, construction, addendum, ...),
recipients, and the list of sheets included with the revision each went at.
If a revision changed since the last issue, update the sheet table in the
same pass and note which issue carried the change. Offer `create-transmittal`
for the cover sheet; do not write one here.

### Step 4. Answer questions

From the log alone:

- **What is current**: the sheet table, active sheets, current revisions.
- **What does <recipient> hold**: the latest issue naming them, sheet by
  sheet.
- **What changed since <issue>**: sheets whose revision moved after that
  date, with the issues that carried each change.

If the log cannot answer, say what entry is missing rather than
reconstructing from memory.

### Step 5. Supersede, never delete

A sheet leaving the set is marked `superseded` with the date and, where one
exists, the sheet that replaced it. Every issuance it ever appeared in stays
intact.

## Rules

- **Every issue has a date and a purpose.** An undated issuance cannot answer
  the only question logs exist for.
- **Sheet numbers verbatim.** No normalizing `A-101` to `A101`; the log must
  match the title block, and mismatches are flagged, not fixed silently.
- **The log records; it does not conclude.** Whether the contractor built
  from a stale set is a dispute question (`dispute-advisor`), not a log entry.
- **One log per project.** Consultant sets get rows in this log, marked with
  their discipline, not a second file.

## Anti-patterns

- Bumping a revision because a newer PDF showed up in a folder.
- Recording an issue without its sheet list, "same as last time".
- Deleting superseded sheets to keep the table short.
- Reconstructing a missed issuance from memory instead of recording that the
  gap exists.
- Turning the log into a transmittal archive; the cover sheets live where
  `create-transmittal` put them.

## Resources

- `assets/drawing-log-template.md` — the file this creates, empty.

No reference files. The history comes from your project, not from here.
