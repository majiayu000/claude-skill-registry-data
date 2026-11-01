---
name: space-program
description: "Maintains a space program in docs/program/program.md: every space the project must contain, its required quantity and target area from the brief, the area the current plan gives it, and the delta. Trigger on \"space program\", \"program of requirements\", \"room list\", \"area program\", \"programming\", \"target area\", \"are we over program\", \"space-program\", or a pasted brief with a room schedule to capture. Targets come from the brief or the client, measured areas come from your plan, and the grossing factor comes from you; the skill supplies none of them and computes only the arithmetic between them, shown. Works in the unit system the brief uses. Reports name every space still missing a target or a measured area rather than hiding them in totals. Interrogating the brief itself is brief-review's job."
license: MIT
metadata:
  title: "Space Program"
  summary: "Track the room list, target areas, and designed areas as they move"
  discipline: "design-building-types"
  tags: "Pre-Design"
---

# Space Program

The brief says forty-two spaces and a total. The plan, six weeks later, says
something else, and the client meeting is about the difference. The program
document is where target and actual sit side by side, space by space, so the
difference has a location instead of being one alarming number. This keeps
that document.

## Scope and limits — read first

**What this does.** Maintains `docs/program/program.md`: one row per space
with quantity, target area, designed area, delta, and the source each target
came from. Captures targets from a brief you paste or type, records designed
areas as you measure them, computes deltas and grossing arithmetic with the
work shown, and reports where the plan stands against the program.

**What this does not do.**

- **It does not know how big anything should be.** No target areas, no
  planning ratios, no benchmarks per seat or per bed or per student. Every
  target comes from your brief or your client, with its source recorded. That
  is the design, not a gap.
- **It does not measure your plan.** Designed areas come from you or from a
  schedule you paste. It never estimates an area from a drawing.
- **It does not choose a grossing factor.** You state it; the net-to-gross
  arithmetic is shown with your number in it.
- It does not critique the brief. Gaps, contradictions, and unstated
  assumptions in the brief itself are `brief-review`'s job; this tracks what
  the brief settled.
- It does not compute occupant loads. `design-occupancy-load` does, and can
  read areas from this file.
- It does not do adjacency planning or generate layouts. It records the
  adjacency requirements you state, as text on the row.

**What you need before starting.** The brief or room schedule, in any form
you can paste, and the unit system it uses. Designed areas whenever you want
the comparison side filled.

## Workflow

### Step 1. Bootstrap if needed

Check whether `docs/program/program.md` exists. If not, copy
`assets/program-template.md` there and record the project name, the date, and
the unit system the brief uses. If the project has no `docs/` folder at all,
confirm before creating one.

### Step 2. Capture the program

One row per space type: name as the brief names it, quantity, target area
per unit, and the source (brief page, meeting date, email). A space the brief
names without an area gets a row with the target blank; the report counts
those. Group rows by department or zone as the brief groups them.

### Step 3. Record designed areas

When you supply measured areas, fill the designed column and compute the
delta per row and per department, shown as area and as percent. Areas pasted
from a schedule keep their stated precision; never re-round.

### Step 4. Compute the totals

Net total from the rows. Then, only if you have stated a grossing factor or a
target gross area:

```
Net program          <sum>        [from the rows above]
Grossing factor      <as stated>  [source: you]
Gross                <arithmetic> = <n>
Target gross         <as stated>  [source]
Difference           <n>, <n>%
```

No factor stated, no gross computed. The report says so instead.

### Step 5. Report

Spaces over and under target, largest deltas first, by department. Then the
gaps, stated before the totals: spaces with no target, spaces with no
designed area, rows whose source is missing. A program that is 96% resolved
reads very differently from one that is 96% of the spaces it happened to
have numbers for.

### Step 6. Track the movement

When a target changes, the old value moves to the row's history with the
date and who changed it, and the source updates. The program at any past
meeting stays reconstructible.

## Rules

- **Every target has a source.** A target with no source is recorded, marked
  `unsourced`, and counted in every report.
- **Show the arithmetic** on every total and every grossing computation.
- **Keep the brief's units and the brief's names.** Translation between the
  brief's language and the plan's room names is recorded on the row, not done
  silently.
- **State the gaps first** in every report.
- **Never fill a blank target** from a similar project, a rule of thumb, or a
  web search.

## Anti-patterns

- Supplying a target area because the space type is familiar. The familiar
  ones are the ones nobody checks.
- Estimating a designed area off a drawing instead of asking for the measured
  figure.
- Applying a default grossing factor.
- Reporting only the total delta when individual rows swing both ways under
  it.
- Overwriting a changed target so the history of the number disappears.

## Resources

- `assets/program-template.md` — the file this creates, empty.

No reference files. The areas come from your brief and your plan, not from
here.
