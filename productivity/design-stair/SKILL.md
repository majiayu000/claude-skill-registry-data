---
name: design-stair
description: "Checks one stair flight item by item: width, headroom, riser, tread, uniformity, nosing, landing, vertical rise between landings, handrail height, wall clearance, cross section, extensions, both-sides requirement, and open risers. Trigger on \"check stair\", \"stair compliance\", \"stair dimension check\", \"riser tread check\", \"handrail extension\", \"stair code check\", \"IBC 1011\", \"ADA stair\", \"OBC stair\", \"NBC stair\", or pasted stair geometry. Works in any jurisdiction. The user names the governing code and edition, then supplies each limit by typing it, pasting the clause, or naming a file to read. The skill never supplies a code value from memory or from web search, and any row without a supplied limit is reported as unverified rather than guessed. Does not replace the Architect or Engineer of Record, and does not cover curved, spiral, winder, or alternating tread stairs."
license: MIT
metadata:
  title: "Design Stair"
  summary: "Check a stair flight against the limits your code sets"
  discipline: "code-life-safety"
  tags: "Design, Compliance, Pre-Design"
---

# Design Stair

Walk one stair flight through the fifteen dimensional items that stair codes
regulate, and report which ones pass, which fail, and which could not be
checked. The checklist is the same everywhere. The numbers are not, so the
numbers come from you.

## Scope and limits — read first

**What this does.** Runs a stair flight against a fixed checklist, compares each
item to the limit you supply, and returns a table with the clause you cited next
to your own dimension. Nothing is skipped silently: an item with no limit comes
back as `unverified` and is counted in the summary.

**What this does not do.**

- **It does not tell you what your code requires.** It has no code values in it.
  Every limit comes from you, and a row you do not supply a limit for stays
  unverified. This is the whole design of the skill, not a gap in it.
- It does not read your code for you, look it up on the web, or recall it. A
  number that arrives any of those three ways is wrong often enough to be
  useless, and a wrong limit that looks checked is worse than a blank.
- It does not cover curved, spiral, winder, or alternating tread stairs, ladders,
  or stepped ramps. Geometry outside a straight flight stops the run.
- It does not sweep the rest of the plan. For the wide pass across all eight
  egress and accessibility axes, run `code-compliance-review` and come back here when the
  stair itself is the question. Flight geometry is the one thing `code-compliance-review`
  does not cover.
- It does not check guards, fire rating or enclosure, egress capacity, or
  structural adequacy. Those are separate questions.
- It does not replace the Architect or Engineer of Record, and it does not
  anticipate what an AHJ will say.

**What you need before starting.** The governing code and its edition, your
stair geometry, and access to the clause text for whichever items you want
checked. Without the third one the run still works, it just returns unverified
rows.

## Workflow

### Step 1. Establish the code

Ask, in one message:

> 1. Which code governs this project, and which edition? (for example IBC 2021,
>    OBC 2024, NBC 2020, or your national code)
> 2. Is there a separate accessibility standard in play? (for example 2010 ADA,
>    CSA B651, or an annex of the same code)
> 3. Is this stair on an accessible route? If no, the accessibility rows are
>    dropped.
> 4. How will you supply the limits? Type them as we go, paste the clause text,
>    or name a file I should read.

Record the answers verbatim. Every output row carries the code name and edition,
so a table can be read a year later without guessing which cycle it came from.

**Read the profile first, if there is one.** If `docs/jurisdiction.md` exists,
read it before asking anything else and say which of the checklist rows it
already answers. Those are not asked again. A row it holds with `not cited` in
the Clause column stays `not cited` in the output and is never promoted on the
way through. Where the file is absent nothing changes: every limit is asked for
exactly as below. `jurisdiction-profile` is the skill that writes and extends
that file.

If the geometry is curved, spiral, winder, or alternating tread, stop here and
say so.

### Step 2. Collect the geometry

Ask for these. Treat anything unstated as missing, and never fill one in with a
typical value.

- Clear width, and the occupant load the stair serves if width depends on it
- Headroom
- Riser height, giving max and min across the flight if they differ
- Tread depth, giving max and min if they differ
- Nosing projection, radius, and underside angle
- Landing depth
- Number of risers, or vertical rise between landings
- Handrail height above the nosing line
- Handrail clearance from the wall
- Handrail cross section: diameter if circular, perimeter and maximum dimension
  if not
- Handrail extension beyond the top riser, and beyond the bottom riser
- Handrails on both sides, yes or no
- Open risers, yes or no
- Slip resistance provided, yes or no, and whether the stair is exposed to wet
  conditions

### Step 3. Collect the limits, one item at a time

For each row in the checklist below, ask for the limit and how it is cited.
Accept any of three answers, and take nothing beyond them.

1. **A typed limit.** "Riser max 180 mm." Record it, and ask which clause it
   came from.
2. **Pasted clause text.** Read the value out of what was pasted and quote the
   sentence back so it can be checked.
3. **A file to read.** Read it, quote the sentence, and cite the file and line.

If none of the three arrives, mark the row `unverified` and move on. Do not
offer a value, do not search for one, and do not treat a commonly known number
as exempt from this.

When a limit arrives that `docs/jurisdiction.md` did not already hold, offer to
write it there with its clause, so the next run does not ask for it again. Never
write a row the user did not supply.

The checklist:

| # | Item | Applies to |
|---|------|------------|
| 1 | Clear width | all |
| 2 | Headroom | all |
| 3 | Riser height | all |
| 4 | Tread depth | all |
| 5 | Riser and tread uniformity tolerance | all |
| 6 | Nosing profile and projection | all |
| 7 | Landing depth | all |
| 8 | Vertical rise between landings | all |
| 9 | Handrail height | all |
| 10 | Handrail clearance from wall | all |
| 11 | Handrail cross section and graspability | all |
| 12 | Handrail extensions, top and bottom | all |
| 13 | Handrails required on both sides | all |
| 14 | Open risers permitted | accessible route |
| 15 | Slip resistance | wet conditions |

Rows 14 and 15 drop out when they do not apply. Rows 1 through 13 always appear,
even if every one of them ends up unverified, because an empty row is the useful
part of the output.

### Step 4. Compare and report

One table, in the chat:

| Item | Limit | Cited as | Actual | Status |
|------|-------|----------|--------|--------|

- **Limit**: what was supplied, in the units it was supplied in. Do not convert.
- **Cited as**: code, edition, and clause, or the file and line, or `not cited`
  if a bare number was given.
- **Actual**: the dimension provided.
- **Status**: `pass`, `fail`, `unverified` (no limit supplied), `missing` (no
  dimension supplied), or `n/a`.

Then a four line summary: how many passed, how many failed, how many are
unverified, and what to supply to close the unverified rows.

End with the sentence that makes the table safe to hand to someone else:

> Limits in this table came from you, not from me. I compared numbers and did
> not supply any. Unverified rows were not checked at all.

### Step 5. Save, if asked

Ask whether to write the table to a file, and where. Write it directly. There is
no template and no script.

## Rules

- **Never supply a code value.** Not from memory, not from a search, not from a
  figure that appears in this file. There are none in this file.
- **Never convert units.** If a limit arrives in millimetres and a dimension in
  inches, say so and ask which to use. A silent conversion is a wrong number
  with the rounding hidden.
- **A row is only checked if it has both a limit and a dimension.** Anything else
  is `unverified` or `missing`, and both are counted in the summary.
- **Every limit carries its citation** through to the output, or is marked
  `not cited` so the reader knows.
- Stop the run for curved, spiral, winder, and alternating tread geometry rather
  than checking the rows that happen to fit.

## Anti-patterns

- Filling a limit from recall because it is well known. Well known values are
  exactly the ones that get carried across an edition change without anyone
  noticing.
- Searching the web for a clause and quoting it as the limit. Search is reliable
  for finding which code governs and unreliable for quoting it correctly, and a
  quote that is 95% right reads identically to one that is right.
- Reporting only the rows that could be checked. The unverified rows are what
  tell the reader how much of the stair was actually looked at.
- Converting inches to millimetres, or rounding a supplied limit to a neater
  number.
- Bundling a table of values into this skill later. It has none on purpose, and
  a bundled table goes stale silently while continuing to look authoritative.
- Continuing past Step 1 without an edition. A clause number without an edition
  is not a citation.

## Resources

None. This skill is one file. Output is written directly at the path you name.
