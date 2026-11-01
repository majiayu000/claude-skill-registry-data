---
name: project-tracker
description: "Keeps one dated log of a project's issues, decisions, risks, and action items in docs/project/tracker.md. Trigger on \"project tracker\", \"decision log\", \"issue log\", \"risk register\", \"action items\", \"track this\", \"log this decision\", \"what did we decide\", \"who owns this\", \"project-tracker\", or when meeting notes produce action items worth keeping past the meeting. Every entry carries a date and a person; closed items move to a closed section rather than being deleted, so the log is also the project's history. The skill never invents a status, an owner, or a deadline. What it was not told, it records as unassigned and says so. Feeds on meeting-notes-cleaner output and is what generate-weekly-report reads. Not a construction schedule and not a CA log; RFIs and submittals have their own logs."
license: MIT
metadata:
  title: "Project Tracker"
  summary: "Keep issues, decisions, risks, and action items in one dated log"
  discipline: "practice-contracts"
  tags: "Project Management"
---

# Project Tracker

Every project generates the same four kinds of loose ends: questions nobody has
answered, decisions somebody made, things that could go wrong, and work someone
promised to do. They live in emails, meeting notes, and memory, and the project
forgets them at exactly the moment they matter. This keeps all four in one
dated file in the project repo.

## Scope and limits — read first

**What this does.** Maintains `docs/project/tracker.md`: four tables (actions,
issues, decisions, risks) plus a closed-items section. Adds entries when you
tell it something worth keeping, updates status when you report movement, and
answers questions like "what is still open" or "when did we decide that" by
reading the file back.

**What this does not do.**

- **It does not invent content.** No owner, no due date, no status, no
  likelihood arrives unless you said it. A field you did not supply reads
  `unassigned`, and the report counts those rather than hiding them.
- It is not a schedule. No dependencies, no critical path, no dates it computes
  for you.
- It is not a CA log. RFIs, submittals, and change orders have their own logs
  and their own tools (`rfi-writer`, `submittal-log-builder`); this log may
  point at an entry there, but never duplicates it.
- It does not chase anyone. A due date passing changes nothing in the file
  until you say what happened.
- It does not decide anything, and it does not rank risks on its own judgment.
  You say the impact and the likelihood; it records them.

**What you need before starting.** A project folder this can write into, and
the habit of telling it things. The log is only as good as what reaches it.

## Workflow

### Step 1. Bootstrap if needed

Check whether `docs/project/tracker.md` exists. If not, copy
`assets/tracker-template.md` there and fill in the project name and today's
date. If the project has no `docs/` folder at all, confirm before creating one.

### Step 2. Capture

When something arrives worth keeping, one entry, in the right table:

- **Action**: work someone agreed to do. Owner and due date if stated.
- **Issue**: an open question or problem with no owner-committed fix yet.
- **Decision**: something settled. Record who decided, the date, and **why**,
  in one sentence. A decision without its why gets relitigated in three months.
- **Risk**: something that could go wrong. Impact and likelihood as the user
  states them, plus the mitigation if one exists.

IDs are sequential per table: `A-012`, `I-004`, `D-021`, `R-003`. Meeting
notes and weekly reports can then point at an entry unambiguously.

If the user pastes cleaned meeting notes (the `meeting-notes-cleaner` output),
offer to log the action items from it in one pass, and keep each item's owner
and due date exactly as the notes state them.

### Step 3. Update

When the user reports movement, find the entry by ID or by words, update the
status, and append a dated note to that entry rather than overwriting the old
one. Status values: `open`, `blocked`, `done`, `dropped` for actions and
issues; `open`, `mitigated`, `closed`, `occurred` for risks. Decisions do not
have a status; a reversed decision gets a new entry that names the one it
supersedes.

### Step 4. Close, never delete

`done` and `dropped` entries move to the closed section with their closing
date. Nothing is ever removed from the file. The closed section is the answer
to "why is this shaped this way" a year later.

### Step 5. Report

On "what's open", "status", or before a meeting, read the file and answer
with: open actions past due, open actions with no owner or no date (the
unassigned count, stated first), open issues, and risks not yet mitigated.
This is the same reading `generate-weekly-report` does; if the user wants the
formal weekly document, point there.

## Rules

- **Date and attribute every entry.** An undated log is a list of rumors.
- **Record the why on every decision**, in the words the decider used.
- **Say the unassigned count first** in every report. A log that hides its
  gaps reads healthier than it is.
- **Append, do not overwrite.** Status notes stack under the entry with dates.
- **One fact, one place.** If an item is an RFI, log the RFI number and stop;
  the RFI log owns the rest.

## Anti-patterns

- Filling in an owner or a due date because it seems obvious who or when.
- Marking an action `done` because its due date passed quietly.
- Deleting closed items to keep the file short. The file being long is the
  point.
- Rewording a decision's why into something more defensible than what was said.
- Turning the tracker into a schedule by adding computed dates or dependencies.

## Resources

- `assets/tracker-template.md` — the file this creates, empty.

No reference files. The content comes from your project, not from here.
