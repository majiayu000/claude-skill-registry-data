---
name: program-reader
description: "Reads any brief or programme document — a client's schedule of accommodation, a spreadsheet from a user group, a consultant's brief, a previous architect's programme — and establishes what its numbers actually are before anybody designs against them: which are measured, which are standards, which are wishes, what area basis they are on, whether the total is the sum of the parts, and what the document counts that a building would not. Trigger on \"read this brief\", \"they sent a schedule of accommodation\", \"what does this programme actually say\", \"is this area realistic\", \"program-reader\", or a brief handed over. Carries no area standards and no benchmarks; the basis comes from the document or from `area-measurement`. `brief-review` interrogates a brief for gaps and contradictions; this reads one for what its figures rest on, and it runs first. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Program Reader"
  summary: "Read a brief or programme document for what its numbers rest on"
  discipline: "design-building-types"
  tags: "Pre-Design, Review"
---

# Program Reader

A programme arrives as a spreadsheet and gets designed against as though every
number in it were the same kind of number. They are not. Some were measured in
a building somebody works in now, some came from a standard, some are what a
department head asked for, and some are the previous row plus ten percent.

The total at the bottom is the sum of all four and is treated as a requirement.

## Scope and limits — read first

**What this does.** Reads any brief or programme document and establishes what
each figure rests on, what area basis it is on, whether the arithmetic closes,
and what the document counts that a building does not.

**What this does not do.**

- **It carries no area standards and no benchmarks.** What a room type "should"
  be is not here. The basis comes from the document or from `area-measurement`.
- It does not interrogate the brief for gaps and contradictions.
  `brief-review` does that, and it should run after this: a brief cannot be
  interrogated usefully until its numbers are understood.
- It does not track the programme through design. `space-program` does.
- It does not test what fits. `test-fit` and `stacking-diagram` do.
- It does not replace the Architect of Record.

**What you need before starting.** The document, complete, including its notes
and any second sheet. Who produced it and when. Whether it is a requirement or
a proposal.

## Workflow

### Step 1. Establish what kind of document it is

Ask, in one message:

> 1. Who produced it: the client, a user group, a consultant, a previous
>    architect, or assembled from several?
> 2. When, and has anything changed since?
> 3. Is it a requirement, a proposal, or a wish list? Has anybody agreed it?
> 4. Is there a budget attached, and was it tested against this?
> 5. Are there notes, a second sheet, or a covering document?

**Question 3 matters most.** A programme that has been agreed is a contract of
sorts; one assembled from user group requests has not been reconciled with
anything, including itself.

### Step 2. Mark what each figure rests on

The core of the reading. Row by row:

| Space | Area | Rests on | Confidence |
|---|---|---|---|

`Rests on` is one of:

- **Measured.** Somebody measured an existing space and this is it.
- **Standard.** From a published or institutional standard, named.
- **Asked for.** A user or a department said this.
- **Derived.** Calculated from a count: people, beds, seats, stations.
- **Unknown.** Nobody can say, and it has been in the spreadsheet for two
  years.

Report the counts. **A programme that is mostly `asked for` and `unknown` is a
wish list**, and knowing that before designing against it changes the
conversation entirely.

### Step 3. Find the area basis, or the absence of one

- Is the figure net, usable, gross, or unstated? Point at `area-measurement`.
- Is a circulation, structure or services allowance included in each row, added
  at the end, or missing?
- Is there a net-to-gross factor stated, and where did it come from?
- Are different rows on different bases? This happens whenever a programme was
  assembled from several sources, which is most of them.

**A programme with no stated basis is not a number a building can be designed
to**, and saying so is the most useful thing this produces.

### Step 4. Check whether the arithmetic closes

- Do the rows sum to the stated subtotals, and the subtotals to the total?
- Are quantities multiplied correctly: room count times area?
- Is anything double-counted, especially shared or support spaces?
- Is anything counted that a building does not have: a role rather than a room,
  a function that lives in another space, an item of furniture?
- Is anything missing that every building has: circulation, plant, risers,
  toilets, storage, cleaning, waste, arrival?

That last list is where programmes are quietly short, and the shortfall lands on
the gross factor nobody set.

### Step 5. Read what the programme implies but does not say

- What the counts imply about occupancy, and therefore about egress and fixture
  counts. Point at `design-occupancy-load` and `/count-plumbing-fixtures`.
- What any room demands that is not an area: height, daylight, acoustic
  separation, a service, a floor loading, an adjacency.
- Whether any single space is large enough to decide the building's shape.
- What the programme assumes about how the organisation works, which is a
  claim and is often out of date.

### Step 6. Report

- What kind of document it is and whether it has been agreed.
- The `rests on` counts, with `asked for` and `unknown` named.
- The area basis, per row where it differs, or that it is unstated.
- Where the arithmetic does not close.
- What is counted that is not a room, and what every building has that is
  missing.
- What the programme implies for code and services.
- What to ask, and of whom.

Then name `brief-review` for the interrogation, `area-measurement` for the
basis, `space-program` to track it from here.

### Step 7. Save, if asked

Ask whether to write the reading to a file and where.

## Rules

- **Mark what every figure rests on**, and count the categories.
- **Establish the area basis, per row if it differs**, or say there is none.
- Check that the arithmetic closes.
- Name what is counted that is not a room, and what a building has that is
  missing.
- Ask whether it has been agreed and by whom.
- Never supply an area standard or a benchmark.

## Anti-patterns

- Designing against the total.
- Treating a measured area and a department's request as the same kind of
  number.
- Assuming one area basis across a document assembled from several.
- Missing that the rows do not sum.
- Accepting a net-to-gross factor with no source.
- Overlooking plant, risers, circulation and storage because the programme did.
- Interrogating the brief before its numbers are understood.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
