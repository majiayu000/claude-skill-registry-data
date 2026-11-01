---
name: design-envelope
description: "The door into envelope work, and the step usually skipped: before any assembly is built up, decide how many envelope types the building actually has, which face gets which, where the junctions between them fall, and what each one has to achieve. Produces the schedule of types and junctions that the assembly and junction skills then execute against, and hands each part off by name. Trigger on \"design the envelope\", \"how many wall types do we need\", \"what should this facade be\", \"envelope strategy\", \"where do the assemblies change\", \"design-envelope\", or an envelope scope with no strategy behind it. Carries no R-values, no assemblies and no code minimums; performance requirements come from the code and the brief you quote. It builds nothing itself — `design-wall-assembly`, `design-roof-assembly` and the junction skills do — and does not replace the enclosure consultant or the Architect of Record."
license: MIT
metadata:
  title: "Design Envelope"
  summary: "Decide what each face of the building has to be, before detailing any"
  discipline: "envelope-performance"
  tags: "Design"
---

# Design Envelope

Envelope work starts at a wall section, and by the time anyone looks up there
are eleven wall types, four of which differ from each other by an inch of
insulation nobody can defend, and a set of junctions that were never scheduled
because each one was drawn when it came up.

This is the step before the sections. It decides how many types there are and
where they change.

## Scope and limits — read first

**What this does.** Establishes what each face has to achieve, how many distinct
envelope types that actually requires, where the junctions between them fall,
and what the whole thing has to be maintained and accessed for. Hands every
build-up and every junction to the skill that does it.

**What this does not do.**

- **It builds nothing.** `design-wall-assembly`, `design-roof-assembly`,
  `design-below-grade-assembly` build the stacks; `design-parapet`,
  `design-window-perimeter`, `design-expansion-joint`, `design-balcony` work the
  junctions. This says how many of each there are and what each is for.
- **It carries no values.** No R-values, no permeance, no air leakage targets,
  no code minimums. All from the code and the brief you quote.
- It runs no arithmetic. `condensation-check` does, on each assembly.
- It does not audit continuity. `air-barrier-trace` does, once the types exist.
- It does not select products.
- It does not replace the enclosure consultant or the Architect of Record.

**What you need before starting.** The building: its shape, its levels, what is
inside each part. The climate zone and its source. The code's envelope
requirements, quoted. Any certification being pursued. The budget position.

## Workflow

### Step 1. Take what the building is, not what it should look like

Ask, in one message:

> 1. What is inside, behind each face? A heated office, a garage, a warehouse, a
>    plant room and a stair have different demands on the wall in front of them.
> 2. What is the climate zone, and from what source?
> 3. Quote the code's envelope requirements. Is a certification being pursued?
>    Point at `leed-tracker`, `passive-house-tracker`.
> 4. What is fixed already: a structure, a floor-to-floor, a facade module, a
>    material the client has chosen? Point at `facade-module`.
> 5. What does each face see: sun, driving rain, a neighbour, a street, a
>    boundary line with a fire separation on it?
> 6. What is below grade, and what is under it? Point at
>    `design-below-grade-assembly`.
> 7. How will it be reached after it is built? Point at `facade-access-study`.

### Step 2. Work out how many types the building actually needs

The decision that keeps the set honest. Two forces pull against each other:

- **Fewer types is cheaper, faster to draw, and easier to build correctly.** A
  trade that builds one wall three hundred times gets good at it.
- **More types means each face gets what it needs**, and a single type applied
  everywhere is over-specified somewhere and under-specified somewhere else.

Work the demands into a table and see how many genuinely distinct answers there
are:

| Face / zone | What is behind | Thermal | Water exposure | Fire | Acoustic | Appearance | Type |
|---|---|---|---|---|---|---|---|

**Two rows with the same answers are the same type.** Merge them. Two rows
differing in one column may still be one type built to the stricter demand, and
that is usually cheaper than a second type.

Report the count, and report every type that exists for appearance alone, since
that is a legitimate reason and it should be a decision rather than a
by-product.

### Step 3. Schedule the junctions, which is the part nobody does

Every place two types meet, or a type stops, is a junction, and each is a detail
somebody has to draw. Listing them now is what stops them being discovered one
at a time in production.

| # | Junction | Between | Skill that takes it | Drawn? |
|---|---|---|---|---|

Work systematically rather than from the elevation: base of every type, top of
every type, every corner inside and out, every change of type in plan and in
section, every opening condition, every floor line, every movement joint, every
projection, every penetration the programme already knows about, and every place
the envelope meets the ground or the roof.

**Count them.** A building with four types usually has twenty to forty junction
conditions, and a set that has drawn six is a set with thirty questions in it.

### Step 4. Decide the strategy questions that cut across every type

Answer once, for the building, rather than four times in four sections:

- **Where the air barrier plane sits** across the whole building, and how it
  gets from one type to the next. This is the single decision that most affects
  whether the building performs. Point at `air-barrier-trace`.
- **Where the insulation sits** relative to structure: outboard everywhere,
  cavity everywhere, or mixed. Mixed means every junction between the two is a
  thermal bridge.
- **Drained or face-sealed**, and whether it is consistent.
- **Which direction the building dries**, and whether it is the same everywhere.
- **What is buried and what is replaceable**, which sets what has to be right
  first time.

Inconsistency in any of these is allowed and has to be deliberate. Name each
place the strategy changes and why.

### Step 5. Report and hand off

- The type count, with what distinguishes each and which exist for appearance.
- The junction schedule with its count, and which are drawn.
- The five cross-cutting decisions, with every place the strategy changes.
- Every requirement that came from an assumption rather than a quoted source.
- The hand-off list: each type to its assembly skill, each junction kind to its
  junction skill, then `condensation-check` and `air-barrier-trace` on the
  result, and `facade-access-study` for maintenance.

Close by saying no assembly was built and no arithmetic was run here.

### Step 6. Save, if asked

Ask whether to write the strategy to a file and where. It is read back every
time one of the assembly skills runs.

## Rules

- **Build nothing.** Every assembly and every junction names the skill that owns
  it.
- **Never supply an R-value, a permeance, or a code minimum.**
- Merge two types with the same demands, and say when a type exists for
  appearance.
- Schedule the junctions systematically and report the count.
- Answer the five cross-cutting questions once for the building.
- Name every place the strategy deliberately changes.

## Anti-patterns

- Starting at a wall section.
- Eleven wall types, four of which differ by an inch.
- A junction schedule discovered one detail at a time in production.
- Deciding the air barrier plane separately in each assembly.
- Mixing outboard and cavity insulation without naming the junctions between
  them.
- Choosing the cladding first and working the wall backwards from it.
- Leaving maintenance access until after the elevation is agreed.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
