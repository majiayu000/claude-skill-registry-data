---
name: schedule-builder
description: "Builds a drawing schedule of any type — door, window, finish, room, wall type, equipment — by settling the column set before any row is filled, since the columns are what the schedule is and adding one later means revisiting every row. Takes the items from your drawings or model, fills only what you supply, marks every gap rather than defaulting it, and checks the finished schedule against the plans for items scheduled but not drawn and drawn but not scheduled. Trigger on \"build a door schedule\", \"window schedule\", \"finish schedule\", \"room data sheet\", \"wall type schedule\", \"make a schedule from these drawings\", \"schedule-builder\", or a request to assemble any drawing schedule. Carries no default column sets, no hardware sets, no fire ratings and no product data; the columns come from your office standard and every value comes from you. For extracting a schedule that already exists in a PDF use `schedule-extractor`. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Schedule Builder"
  summary: "Build a door, window, finish, or room schedule that the drawings can survive"
  discipline: "construction-admin"
  tags: "Documentation"
---

# Schedule Builder

A schedule is its columns. Adding one after a hundred rows are filled means
going back through every item, which is why schedules end up with the columns
somebody happened to start with and a set of notes doing the work the missing
columns should have done.

## Scope and limits — read first

**What this does.** Settles the column set first, against what this project
actually has to record and what the specification will look for. Then fills only
what you supply, marks every gap explicitly, and reconciles the finished
schedule against the drawings in both directions.

**What this does not do.**

- **It carries no default columns and no default values.** No hardware sets, no
  fire ratings, no finishes, no standard door types, no product data. The column
  set comes from your office standard or from what the project needs; every
  value comes from you, your model, or your drawings.
- It does not extract. Where the schedule already exists in a PDF,
  `schedule-extractor` pulls it out. This builds one.
- It does not specify. What a door has to achieve is the specification's;
  the schedule records which door is where.
- It does not check compliance. Whether a rating is correct belongs to
  `/test-fire-rating` and `design-fire-barrier`; whether a clearance is correct
  to `/test-ada`.
- It does not decide the office standard, though it will tell you when the
  standard is missing a column this project needs.
- It does not replace the Architect of Record.

**What you need before starting.** The schedule type. Your office standard
column set, if there is one. The items: from a model, a plan, or a list. The
specification sections that will reference this schedule. Whether the schedule
has to match a consultant's or a manufacturer's format.

## Workflow

### Step 1. Establish the type and where the items come from

Ask, in one message:

> 1. What kind of schedule, and is there an office standard column set? Paste it
>    if so.
> 2. Where do the items come from: a model, plans, a list, or all three?
> 3. Which specification sections will reference it, and do they ask for
>    anything by name?
> 4. What phase is the set in? A DD schedule and a CD schedule carry different
>    columns and pretending otherwise fills a lot of cells with placeholders.
> 5. Does anything have to match an external format?

### Step 2. Settle the columns before any row

Present the proposed column set and hold it against three tests:

| Column | Why it is here | Who fills it | Needed at this phase? |
|---|---|---|---|

- **What does the specification look for?** A schedule that does not carry what
  the spec references is a schedule the contractor cannot use.
- **What does the project actually have?** A column that will be identical in
  every row is a general note, not a column.
- **What will be needed later?** Adding a column at CD means revisiting every
  row. Adding an empty one now costs nothing.

Get explicit agreement on the columns before proceeding. This is the step the
skill exists for.

### Step 3. Fill only what you have

One row per item. Every cell is either a value you supplied or the word
`not supplied`. **There is no third state and nothing is defaulted.**

Where a value repeats across many rows, say so and ask whether it belongs in the
schedule at all or in a note. Where a value varies unexpectedly within a type,
flag it; that is usually an error in the model rather than a real variation.

Report the count of `not supplied` cells by column. A column that is mostly
empty is either premature for this phase or unnecessary.

### Step 4. Reconcile against the drawings, both directions

Two lists, and both matter:

- **Scheduled but not drawn.** Items in the schedule with no location on a plan.
- **Drawn but not scheduled.** Items on the plans with no schedule row. This is
  the more common and the more expensive, because it gets found on site.

Then check the marks themselves: duplicates, gaps in a numbering sequence, and
any mark that does not follow the set's convention. A duplicated door mark is
found by the hardware supplier, late.

### Step 5. Report

The schedule, then:

- `not supplied` counts by column.
- The two reconciliation lists.
- Mark problems: duplicates, gaps, non-conforming.
- Any column the office standard lacks that this project needed, named, so the
  standard can be fixed rather than worked around again.

### Step 6. Save

Ask where and in what format. CSV where it goes back into a model or a
spreadsheet, markdown where it is read.

## Rules

- **Never default a value.** `not supplied` is the only alternative to a value
  you were given.
- **Never carry a standard hardware set, rating, or finish.**
- Settle the columns and get agreement before filling any row.
- Reconcile in both directions, every run.
- Report `not supplied` counts by column, not as one total.
- Flag a column that would be identical in every row.
- Never check compliance here; name the skill that does.

## Anti-patterns

- Starting to fill rows before the columns are agreed.
- Defaulting a rating, a hardware set, or a finish because it is typical.
- Reconciling only from the schedule to the drawings.
- Carrying placeholder values that look like real ones.
- Adding a column at CD and filling the earlier rows from assumption.
- Building a schedule the specification does not reference.
- Treating a duplicated mark as a formatting issue.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
