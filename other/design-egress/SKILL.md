---
name: design-egress
description: "Checks a floor or a tenancy against the means-of-egress items every building code regulates: egress capacity per occupant, number of exits required, single-exit allowance, common path of travel, exit separation, travel distance, corridor width, dead-end length, door clear width, and door swing threshold. Trigger on \"check egress\", \"egress review\", \"exit count\", \"travel distance\", \"common path\", \"exit separation\", \"dead end corridor\", \"design-egress\", \"IBC 1006\", \"IBC 1017\", \"OBC 3.4\", or a pasted plan with occupant load and exit positions. Works in any jurisdiction. The user names the governing code and edition and supplies each limit by typing it, pasting the clause, or naming a file to read. The skill never supplies a limit from memory or from web search, and any item without a supplied limit is reported as unverified rather than assumed. Does not compute occupant load, and does not replace the Architect of Record or the AHJ."
license: MIT
metadata:
  title: "Design Egress"
  summary: "Verify exit counts, widths, separation, and travel distance"
  discipline: "code-life-safety"
  tags: "Design, Compliance, Pre-Design"
---

# Design Egress

Run a floor or a tenancy through the eleven means-of-egress items that codes
regulate, and report which pass, which fail, and which could not be checked.
The items are the same everywhere. The thresholds are not, so the thresholds
come from you.

## Scope and limits — read first

**What this does.** Takes your occupant load and plan dimensions, compares each
against the limit you supply, and returns a table with your citation beside your
own number. An item with no limit comes back as `unverified` and is counted, so
a partial check never reads as a clean one.

**What this does not do.**

- **It does not tell you what your code allows.** It has no thresholds in it.
  Every limit comes from you, and an item you do not supply a limit for stays
  unverified. That is the design, not a gap.
- It does not compute occupant load. Run `design-occupancy-load` first, or give
  the number.
- It does not measure your drawing. Travel distance, diagonals, and common path
  are distances you take off the plan and give it.
- It does not handle high-rise additions, atrium or smoke-control egress,
  existing-building provisions, or assembly aisle geometry. Each is flagged and
  stops that row.
- It does not check accessible means of egress in detail, stair dimensions (use
  `design-stair`), or fire resistance of the enclosure.
- It does not replace the Architect of Record or anticipate the AHJ.

**What you need before starting.** The governing code and edition, occupant
load, your plan dimensions, and the clause text for whichever items you want
checked.

## Workflow

### Step 1. Establish the code and the conditions

Ask, in one message:

> 1. Which code governs this project, and which edition?
> 2. What use or occupancy classification applies to the area being checked? If
>    mixed, list them.
> 3. Sprinkler condition, and which standard the system is designed to. Many
>    egress allowances change with it.
> 4. Any of these present: high-rise, atrium or smoke control, existing-building
>    provisions, assembly aisles? Each one takes its rows out of scope.
> 5. How will you supply the limits? Type them, paste the clause, or name a file
>    I should read.

Record the code and edition. They go on every output row.

**Read the profile first, if there is one.** If `docs/jurisdiction.md` exists,
read it before asking anything else and say which checklist items it already
answers, matching on the Key column so a row keyed to a different use or
sprinkler condition is not borrowed for this one. Those items are not asked
again. A row marked `not cited` stays `not cited` in the output. Where the file
is absent nothing changes. `jurisdiction-profile` writes and extends it.

### Step 2. Collect the numbers

Ask for these, per egress path or area being checked. Never substitute a
typical value.

- Area identifier
- Occupant load served, and where it came from
- Number of exits provided
- Straight-line distance between the two most remote exits
- Longest diagonal of the area served
- Common path of travel, from the most remote point until two paths become
  available
- Travel distance from the most remote point to the exit
- Dead-end corridor length, if any
- Clear width of the exit access corridor
- Clear width at the egress door
- Door swing direction, with or against the direction of travel

### Step 3. Collect one limit per item

Work through the checklist below. For each, accept exactly three kinds of
answer.

1. **A typed limit.** Record it, and ask which clause it came from, and which
   use and sprinkler condition it is the row for.
2. **Pasted clause or table row.** Read the threshold out of it and quote it
   back so it can be checked. Say which row you took, since most of these are
   tables keyed by use and sprinkler condition.
3. **A file to read.** Read it, quote the row, cite file and line.

If none arrives, mark the item `unverified` and continue. Do not offer a
threshold, do not search for one, and do not treat a familiar number as exempt.

When a threshold arrives that `docs/jurisdiction.md` did not hold, offer to
write it there with its clause and its key, so the next run does not ask. The
key is what makes the row reusable; without it the value is only correct for
this one project. Never write a row the user did not supply.

The checklist:

| # | Item | Compared against |
|---|------|------------------|
| 1 | Egress capacity per occupant, stairs | width provided vs load served |
| 2 | Egress capacity per occupant, level components | width provided vs load served |
| 3 | Number of exits required for the load | exits provided |
| 4 | Single exit allowance limit | load and travel where one exit is used |
| 5 | Common path of travel limit | common path measured |
| 6 | Exit separation, as a fraction of the diagonal | separation vs diagonal |
| 7 | Travel distance limit | travel distance measured |
| 8 | Corridor minimum width | corridor width provided |
| 9 | Dead-end corridor maximum | dead-end length measured |
| 10 | Door clear width minimum | door clear width provided |
| 11 | Door swing threshold by occupant load | load served and swing direction |

Items 1 and 2 need a capacity factor rather than a dimension. Ask for the factor
and what it is per occupant, then multiply.

### Step 4. Compare and report

| # | Item | Limit | Cited as | Row taken | Actual | Status |
|---|------|-------|----------|-----------|--------|--------|

- **Row taken**: the use and sprinkler condition the limit was read for. A limit
  read off the wrong row is the common failure here, and naming it makes that
  visible.
- **Cited as**: code, edition, clause, or file and line, or `not cited`.
- **Status**: `pass`, `fail`, `unverified` (no limit), `missing` (no dimension),
  or `out of scope` (flagged in Step 1).

Then a summary: passed, failed, unverified, out of scope, and what to supply to
close the unverified rows.

Close with:

> Limits in this table came from you, not from me. I compared numbers and
> supplied none. Unverified rows were not checked at all. Occupant load was
> taken as given and not verified here.

### Step 5. Save, if asked

Ask whether to write the table to a file, and where. Write it directly. There is
no template and no script.

## Rules

- **Never supply a threshold.** Not from memory, not from a search, not from a
  figure in this file. There are none in this file.
- **Always record which row a limit came from.** Use and sprinkler condition
  change most of these, and a right number off the wrong row looks identical to
  a right answer.
- **Never convert units.** If a limit and a dimension arrive in different units,
  say so and ask which to use.
- **An item is checked only with both a limit and a dimension.** Everything else
  is `unverified` or `missing`, and both appear in the summary.
- Stop the rows for high-rise, atrium and smoke control, existing-building
  provisions, and assembly aisles rather than checking the parts that fit.
- Say on every run that occupant load came from elsewhere and was not verified
  here.

## Anti-patterns

- Filling a threshold from recall because it is a well-known one. Those are the
  numbers that survive an edition change without anyone noticing.
- Searching the web for a clause and using it as the limit. Search finds which
  code governs; it does not quote it reliably.
- Taking a limit from the sprinklered row when the building is not sprinklered,
  or from a neighbouring use because it is close.
- Reporting only the rows that could be checked. The unverified rows are what
  tell the reader how much of the floor was actually looked at.
- Measuring travel distance or a diagonal off a description instead of asking
  for the number.
- Bundling a threshold table into this skill later. It has none on purpose, and
  a bundled table goes stale silently while still looking authoritative.

## Resources

None. This skill is one file. Output is written directly at the path you name.
