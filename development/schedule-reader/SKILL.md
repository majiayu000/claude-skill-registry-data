---
name: schedule-reader
description: "Reads any engineer's or consultant's schedule — mechanical equipment, plumbing fixtures, electrical panels, lighting, fire protection devices, structural members — and translates it into the architectural consequences: what has to fit somewhere, what needs a room, what needs access, what needs a route, what lands on a wall or a ceiling, and what weighs something the structure has to carry. Trigger on \"read this equipment schedule\", \"what does this mechanical schedule mean for us\", \"they sent a schedule\", \"schedule-reader\", or any consultant's schedule handed over. Carries no dimensions, capacities or clearances; every figure comes from the schedule or the product data. Not to be confused with `schedule-review`, which reads a contractor's construction programme — a different document entirely. `explain-panel-schedule` goes deeper on one electrical panel. It does not check the engineering and does not replace the engineers or the Architect of Record."
license: MIT
metadata:
  title: "Schedule Reader"
  summary: "Read an engineer's schedule for what it means to the architecture"
  discipline: "structure-mep"
  tags: "Reference, Review"
---

# Schedule Reader

An engineer's schedule is issued as a coordination document and read as a wall
of numbers. Every row of it is something that has to physically exist somewhere
in the building, be reached for service, and be carried by something.

## Scope and limits — read first

**What this does.** Reads any consultant's schedule and turns each row into what
the architecture has to provide: space, access, a route, a surface, or a load.

**What this does not do.**

- **It checks no engineering.** Whether the equipment is correctly selected or
  sized is the engineer's.
- **It carries no dimensions, capacities or clearances.** Every figure comes
  from the schedule, the product data, or the code you quote.
- **It is not `schedule-review`.** That skill reads a contractor's construction
  programme. This reads an equipment or element schedule. The two share a word
  and nothing else, and the near-miss is why this says so here.
- It does not go deep on one panel. `explain-panel-schedule` does.
- It does not build a schedule. `schedule-builder` does that for the
  architectural ones.
- It does not replace the engineers or the Architect of Record.

**What you need before starting.** The schedule, complete, with its header, its
notes and its legend. The plans showing where the items are. The product data,
if any is referenced.

## Workflow

### Step 1. Establish what kind of schedule it is

Ask, or read off the sheet:

> 1. Which discipline, which consultant, what revision and date?
> 2. What are the columns, and is there a legend or notes block?
> 3. Are the items located on a plan, or only scheduled?
> 4. Is this design intent, or has it been through a submittal?
> 5. Does it reference product data, and do you have it?

**Read the notes before the rows.** Schedule notes carry the requirements that
do not fit in a column, and they are where the access, clearance and sequencing
demands live.

### Step 2. Turn every row into what the architecture has to provide

| Item | Where | Needs space | Needs access | Needs a route | Lands on | Weighs |
|---|---|---|---|---|---|---|

For each row, ask the six:

- **Space.** Its own dimensions plus the service clearance the data sheet
  requires. Point at `equipment-reader` for the cut sheet, and
  `design-mechanical-room` or `design-electrical-room` if it lives in a room.
- **Access.** What has to be reached, from where, how often, and whether it is
  above a hard ceiling. Point at `design-ceiling`.
- **A route.** How it gets in during construction and out at replacement.
- **Lands on.** A wall, a ceiling, a floor, a roof, a plinth — and whether that
  surface exists in the architectural drawings.
- **Weighs.** Anything the structure has to carry, hang, or isolate. To the
  engineer.
- **Serves.** Where the thing it serves is, and whether the connection between
  them is drawn anywhere.

Where a column is blank on the schedule, it is `not supplied` and never assumed.

### Step 3. Find what the schedule implies that no drawing shows

The output that earns the exercise:

- Items with no location on any plan.
- Items requiring a room that does not exist.
- Items requiring access through a ceiling or a wall that has no panel.
- Items on an exterior wall or a roof that will be visible, which is an
  elevation decision made in a schedule. Point at `size-louver` and
  `design-roof-drainage`.
- Items that need power, water or drainage that another discipline's schedule
  does not show.
- Anything marked future, spare, or by others.

### Step 4. Read the header and the notes for what binds

- Design conditions and assumptions stated at the top.
- Anything the notes require of the architecture: clearances, finishes,
  drainage, ventilation, fire rating, acoustic isolation.
- Whether any item is specified as a basis of design with substitutions allowed,
  which means the dimensions may change after tender.

That last one matters: **a schedule that permits substitutions is a schedule
whose dimensions are provisional**, and the space held for it has to be the
worst case rather than the drawn one.

### Step 5. Report

- Items with no location, first.
- The six-column table, with every `not supplied` counted.
- Everything the schedule implies that no drawing shows.
- What has to go to the structural engineer: weights, hangers, openings.
- What has to go on an elevation.
- Whether substitutions are permitted, and therefore which dimensions are
  provisional.

Close by saying no engineering was checked.

### Step 6. Save, if asked

Ask whether to write the reading to a file and where. CSV where it becomes a
coordination list; point at `coordination-log`.

## Rules

- **Read the notes before the rows.**
- **Never check the engineering.**
- Turn every row into space, access, route, surface, load and what it serves.
- A blank column is `not supplied`, never assumed.
- Say when substitutions are permitted and the dimensions are therefore
  provisional.
- Name the near-miss with `schedule-review` where confusion is possible.

## Anti-patterns

- Reading the rows and not the notes.
- Assuming a clearance because the schedule did not give one.
- Treating a scheduled item as located because it is scheduled.
- Missing that an item lands on an elevation.
- Holding space to the drawn dimension when substitutions are allowed.
- Checking whether the selection is correct.
- Confusing this with reading a contractor's programme.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
