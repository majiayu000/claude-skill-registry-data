---
name: phasing-study
description: "Works out the phasing for construction in and around a building that stays occupied: which functions must never close, where each one lives during each phase, the swing space that makes the moves possible, and the sequence that gets everyone home without a circular dependency. Builds the occupancy ledger, the move list, and the per-phase checklist of what must be true before a phase can start. Trigger on \"phasing study\", \"occupied renovation\", \"how do we renovate without closing\", \"swing space\", \"decant plan\", \"phasing-study\", or a renovation scope paired with functions that cannot stop. The sequencing logic is the skill's; every duration, cost, and code determination comes from elsewhere: the contractor owns means, methods, and the schedule, and whether egress and separations hold during each phase is a code and AHJ question this skill raises and never answers. It is the design-side plan that makes those conversations possible, not a construction schedule and not a logistics plan."
license: MIT
metadata:
  title: "Phasing Study"
  summary: "Plan construction phases around a building that stays open through them"
  discipline: "design-building-types"
  tags: "Design, Analysis"
---

# Phasing Study

An occupied renovation is a puzzle with one rule: everyone has somewhere to be
during every phase, and the building still works at every step. The puzzle is
usually solved late, by the contractor, on the contractor's terms. Solved
early, on the design side, it changes the design: where the phase lines fall,
what gets built first, and how much swing space the project actually needs.

## Scope and limits — read first

**What this does.** Takes the functions in the building, which of them must
stay open, the spaces available to host them temporarily, and the end state,
and works out a phase sequence: an occupancy ledger showing where every
function lives in every phase, a move list with a count per function, phase
boundaries as physical facts, and a checklist per phase of what must be true
before it starts.

**What this does not do.**

- **It does not rule on life safety during construction.** Whether egress
  holds in each phase, what separates occupied space from work, and what the
  fire marshal will require are code and AHJ questions. This skill raises
  them, per phase, by name, and never answers them. `design-egress` and the
  jurisdiction hold the answers.
- It does not schedule. Durations, crew logic, procurement, and means and
  methods are the contractor's. `schedule-review` reads the contractor's CPM
  once it exists; this study is what the design team brings to that
  conversation.
- It does not carry costs. Each extra move and each square foot of swing
  space costs something, and the figures come from the owner and the
  estimator.
- It does not design the temporary works: partitions, protection, shoring,
  temporary systems are designed by whoever stamps them.

**What you need before starting.** The functions in the building and which
must not close, the spaces that could host functions temporarily, the scope
of work by area, the end state, and anything with a fixed date attached.

## Workflow

### Step 1. Collect the pieces

Ask, in one message:

> 1. Every function in the building, and for each: can it close, move once,
>    move more than once, or must it stay exactly where it is? Hours matter:
>    a function that runs nights changes what can happen near it.
> 2. The scope of work, by area: what is being renovated, and does any of it
>    have to happen in a fixed order for technical reasons?
> 3. What space exists to host functions temporarily: empty floors, leased
>    space nearby, trailers, the phase-one area once it finishes.
> 4. The end state: where everything lives when it is over.
> 5. Fixed dates, if any: a school year, a fiscal year, a lease expiry.
> 6. The systems: does anything serving occupied areas run through work
>    areas? Air, power, data, water, egress paths.

### Step 2. Build the occupancy ledger

One table, functions as rows, phases as columns, a location in every cell.
The rule that makes it a method: **no function is ever homeless, and every
cell is filled before any phase is called workable.**

| Function | Now | Phase 1 | Phase 2 | ... | End state | Moves |
|---|---|---|---|---|---|---|

Count the moves per function in the last column. Each move costs money,
downtime, and goodwill, and the count is the first thing the owner should
see. A ledger with a function moving three times is legal; it is also a
question.

### Step 3. Test the sequence for circular dependencies

The classic failure: phase 2 needs the space phase 1 occupies, and phase 1
cannot finish until phase 2's space is ready. Walk the chain of moves
explicitly and show it:

```
who moves first        <function, from, to>
what that frees        <space, and which phase needs it>
what has to be true    <the work finished, the systems live, the approval in hand>
```

If the chain does not close, the study's answer is that it does not close,
plus the two ways out: more swing space, or a scope split into smaller
phases. Both are owner decisions with costs attached; name them, do not pick.

### Step 4. Draw the phase boundaries as physical facts

Per phase, in a table:

- Where the line between occupied and work actually is, wall by wall, floor
  by floor.
- How construction reaches the work without crossing occupied space: access,
  hoisting, deliveries, workers.
- What crosses the line anyway: systems serving occupied areas through work
  areas, egress paths, the elevator everyone shares. Each one is a named
  problem for the engineer, the contractor, or the AHJ.
- The noise-and-vibration adjacency: what loud work sits next to, and when
  that function operates.

### Step 5. Write the per-phase checklist

For each phase, what must be true before it starts:

| Phase | Space empty | Systems live | Separations in place | Approvals | Moves done |
|---|---|---|---|---|---|

Every cell is a fact somebody has to confirm, with the somebody named: the
owner empties, the engineer confirms systems, the AHJ rules on separations
and egress, the contractor builds the protection.

### Step 6. Report

The ledger, the move count, the phase boundaries, the checklists, and then in
prose: the phase the whole plan hinges on, the function that constrains
everything, and the swing-space decision the owner has to make. Close every
run with: durations and logistics are the contractor's, life safety during
construction is the AHJ's, and this study is the design side's opening
position for both conversations.

### Step 7. Save, if asked

Ask whether to write the study to a file and where. Write it directly. There
is no template and no script.

## Rules

- **The sequencing logic is the only thing this skill supplies.** Durations,
  costs, and code determinations come from the contractor, the estimator,
  and the AHJ, and each open question carries its owner's name.
- No function is ever homeless. A ledger with an empty cell is unfinished,
  not flexible.
- Count the moves and report the count before the sequence's elegance.
- Every phase boundary is stated as a physical fact, not a schedule concept.
- Life safety during each phase is raised by name, every run, and never
  answered.
- Never present the sequence as the schedule. It is the design-side logic
  the schedule has to satisfy.

## Anti-patterns

- Solving the puzzle with swing space the owner never agreed to pay for.
- A ledger cell that says "TBD" surviving into the report.
- Declaring egress "maintained" because a path exists on the plan. That is
  the AHJ's call, made against code text, during each phase.
- Sequencing by construction logic alone and discovering the nightshift
  function next to the demolition.
- Treating the move count as free because the distances are short.
- Writing durations into the phases. The moment it has dates it reads as a
  schedule, and it is not one.

## Resources

None. This skill is one file. Output is written directly at the path you
choose.
