---
name: punch-list
description: "Maintains a project punch list in docs/construction/punch-list.md. Trigger on \"punch list\", \"punch item\", \"snag list\", \"deficiency list\", \"defect list\", \"punch walk\", \"punch-list\", or a pasted site visit report whose observations should become tracked items. Each item carries a location, a description, the responsible trade, the date raised, its source, and a status that separates completed from verified, because a contractor marking work done is not the same as the architect seeing it done. The skill never invents an item, a responsible party, or a completion; what it was not told stays open. Feeds on create-site-visit-report output. It does not decide substantial completion and does not certify anything; those are contract acts."
license: MIT
metadata:
  title: "Punch List"
  summary: "Keep a punch list with location, trade, owner, and status per item"
  discipline: "construction-admin"
  tags: "Construction"
---

# Punch List

At the end of a project the work that remains is a hundred small items spread
across every room, three trades, and two months of site visits. The list of
them is only useful if it is one list, every item says where and who, and
nothing falls off it silently. This keeps that list.

## Scope and limits — read first

**What this does.** Maintains `docs/construction/punch-list.md`: one table of
items, each with an ID, a location, a description, the responsible trade, the
date and source it was raised from, and a status. Turns site visit
observations into items in one pass, updates statuses as you report them, and
answers "what is still open in unit 3B" or "what does the drywall sub still
owe" by reading the list back.

**What this does not do.**

- **It does not invent items.** Every item comes from you or from a report you
  paste. It never walks the building.
- **It does not close items.** `completed` is what the contractor claims;
  `verified` is what you confirmed on site. Only you move an item to either,
  and the report counts the two separately.
- It does not assign responsibility on its own. If you did not name the trade,
  the item reads `unassigned` and the report says how many are.
- It does not decide substantial completion, does not certify payment, and
  does not interpret what the contract makes of the list. `explain-aia` reads
  clauses; the decisions are the Architect of Record's.
- It does not store photos. It records photo filenames you name, next to the
  item they document.

**What you need before starting.** A project folder this can write into, and
observations: typed, or pasted from a `create-site-visit-report` document.

## Workflow

### Step 1. Bootstrap if needed

Check whether `docs/construction/punch-list.md` exists. If not, copy
`assets/punch-list-template.md` there and fill in the project name and date.
If the project has no `docs/` folder at all, confirm before creating one.

### Step 2. Capture

One row per item, IDs sequential: `P-001`, `P-002`.

- **Location** as the project names it: floor, room number, grid line, unit.
  Ask rather than approximate; "near the lobby" is not a location a
  subcontractor can find.
- **Trade** exactly as stated. No guess from the work type.
- **Source**: the site visit report date, the walk, or the person who called
  it in. Items with no source are still logged, sourced to the user and dated.

If the user pastes a site visit report, list the observations you read in it
and ask which become punch items before writing any. A report also records
weather and progress; not every line is a deficiency.

### Step 3. Update

Statuses: `open`, `disputed`, `completed`, `verified`. Movement comes only
from the user. When the contractor's list comes back marked done, record
those as `completed`, never as `verified`, and say so. Append dated notes
under an item rather than rewriting its history.

### Step 4. Report

On "status", "what's open", or before a walk: totals by status, then open
items grouped by trade and by location, then the `unassigned` count, then
items `completed` awaiting verification, oldest first. Before a site visit,
offer the open-items list sorted by location, which is the order a walk
actually happens in.

### Step 5. Close out the list

When every item reads `verified`, say so plainly and stop. Whether that means
final completion is the contract's question, not this file's.

## Rules

- **Location, trade, date on every item.** An item missing any of the three
  gets logged anyway and counted as incomplete data, said first in reports.
- **`completed` is a claim; `verified` is a fact.** Never merge them.
- **Append, do not overwrite.** Disputes especially: record both positions,
  dated.
- **Nothing is deleted.** A withdrawn item is marked `withdrawn` with who and
  why.
- **One list.** If a second list arrives (the contractor's own), reconcile
  into this one and record where each new item came from.

## Anti-patterns

- Turning every site-report observation into a punch item without asking.
- Marking an item `verified` because the contractor's list says done.
- Guessing the responsible trade from the nature of the work.
- Summarizing locations ("various units") to keep the table short.
- Treating a fully-verified list as a completion certificate.

## Resources

- `assets/punch-list-template.md` — the file this creates, empty.

No reference files. The items come from your site, not from here.
