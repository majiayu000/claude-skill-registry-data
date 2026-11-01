---
name: design-core
description: "Aggregates the pieces of a building core (elevator shafts, stairs, toilets, mechanical and electrical shafts and rooms) from dimensions the user supplies, applies the user's own wall-and-circulation factor, and reports total core area and core-to-floor-plate ratio against the user's benchmark, showing every step. Trigger on \"core sizing\", \"how big is my core\", \"core-to-floor ratio\", \"core efficiency\", \"design-core\", or a floor plate paired with a list of core components. Every dimension comes from the user: shaft sizes from manufacturer cut sheets, stair footprints from the user's stair layout, room sizes from the user's plans, the grossing factor and the target ratio from the user's own benchmarks. The skill never supplies a typical shaft size, fixture count, or target ratio. It does not decide elevator count (the elevator consultant's traffic analysis does), does not check stair or fixture code compliance, and is not a substitute for the Architect of Record."
license: MIT
metadata:
  title: "Design Core"
  summary: "Add up the core from your own dimensions and check its share of the plate"
  discipline: "design-building-types"
  tags: "Design, Analysis"
---

# Design Core

List what goes in the core, with the dimensions from your own sources, and get
back the total, the ratio, and the piece that is driving it. The arithmetic is
addition and one division; the value of the run is that every line carries
where it came from.

## Scope and limits — read first

**What this does.** Collects the core components you name with the dimensions
you supply, sums them, applies your wall-and-circulation factor, divides by
your floor plate, and compares the ratio to your own target, per floor type if
the core changes over the height. Then it names the largest contributor, so
the conversation about trimming the core starts in the right place.

**What this does not do.**

- **It does not know any dimensions.** No typical elevator shaft, no standard
  stair footprint, no usual toilet room, no default grossing factor, no
  industry target ratio. Every one of them comes from you, with its source.
  That is the design, not a gap.
- **It does not decide how many elevators you need.** That is a traffic
  analysis, and it belongs to the elevator consultant. The count is an input
  here, never a finding.
- It does not check code. Stair geometry is `design-stair`, egress capacity is
  `design-egress`, and fixture counts come from your plumbing code analysis.
  This skill takes the areas those exercises produced.
- It does not lay the core out. Whether the pieces fit together, where the
  core sits on the plate, and what that does to the structure are design and
  engineering judgment.
- It is a planning-stage aggregation, not a substitute for the Architect of
  Record.

**What you need before starting.** The floor plate area, the list of what is
in the core, a dimension for each piece with its source (manufacturer cut
sheet, your stair layout, your plans), your wall-and-circulation factor, and
the target ratio you are holding yourself to, with where it came from.

## Workflow

### Step 1. Establish the plate and the floor types

Ask, in one message:

> 1. The floor plate area, and its source. Gross plate, measured how?
> 2. Does the core change over the height (a low-rise and high-rise bank, a
>    mechanical floor, a different toilet count)? If so, name the floor types
>    and I will run each.
> 3. Your target core-to-plate ratio, and where it comes from: your own past
>    projects, a developer's proforma, a leasing standard. If you have none,
>    the run still works; the ratio just reports without a verdict.

### Step 2. Collect the components

For each component, a dimension and a source. Accept typed values, a pasted
table, or a file. The usual list, offered as a prompt and not a requirement:

- Elevator shafts: count times shaft plan size, from the manufacturer's cut
  sheet or the elevator consultant. Machine room if the system has one.
- Stairs: count times footprint, from your own stair layout.
- Toilet rooms, from your plans, with the count your code analysis produced.
- Mechanical, electrical, and telecom shafts and rooms, from your engineers.
- Janitor, service, and anything else your core carries.

If a component has no dimension yet, it goes in the table as `no dimension
yet` and the total is reported as incomplete. Do not fill it with a typical
value, and do not drop it silently.

### Step 3. Apply your factor and compute

```
<component>        <count> x <dimensions>   = <area>    (<source>)
...
subtotal, components                        = <area>
walls and internal circulation   x <factor> (<your factor, its source>)
core total                                  = <area>
core-to-plate      <core> / <plate>         = <ratio>
vs your target     <target, its source>     = <over / under, by how much>
```

Every line shows its arithmetic and its source. If the factor was not
supplied, stop and ask for it; a core summed without walls looks better than
any core that can be built.

### Step 4. Name the driver

One or two sentences: which component moves the ratio most, and what a change
there would do to the total, arithmetically. Do not recommend the change. Cut
the elevator bank and the building may not elevator; that call belongs to the
consultant and to you.

### Step 5. Report, and save if asked

The table, the ratio per floor type, the incomplete lines counted on the face
of the output, and the driver. Then ask whether to write it to a file and
where. Write it directly; there is no template and no script.

## Rules

- **Never supply a dimension, a factor, or a target.** There are none in this
  file, and none arrive from memory during a run.
- Every line carries its source. A subtotal over unsourced lines reports as
  unsourced.
- A missing component dimension makes the total incomplete, stated plainly,
  rather than a guess.
- Elevator count is an input. If the user asks whether it is enough, the
  answer is the elevator consultant, by name.
- Never convert units, and never round the user's dimensions to neater
  figures.
- Ratios compare only against a target the user supplied, with its source
  named. No target, no verdict.

## Anti-patterns

- Filling in a shaft size because the elevator is a common model. Cut sheets
  differ by capacity, speed, and code edition, and the recalled one is
  exactly the wrong one.
- Offering an industry-standard core ratio as the benchmark. Whose industry,
  which building type, measured how? The user's own number or none.
- Treating the wall-and-circulation factor as optional detail. It is
  routinely a fifth of the core.
- Recommending a component to shrink. The skill points at the arithmetic
  driver; the design move is the user's.
- Summing a core with one component silently missing.

## Resources

None. This skill is one file. Output is written directly at the path you
choose.
