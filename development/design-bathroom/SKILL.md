---
name: design-bathroom
description: "Lays out a domestic bathroom or ensuite from the two things that actually constrain it — where the waste can run and which way the door swings — rather than from the fixtures. Works ventilation, the wet area and its waterproofing, storage, and the reach and clearance around each fixture, and separates what is fixed by the building from what is a choice. Trigger on \"bathroom layout\", \"ensuite\", \"can we move the toilet\", \"powder room\", \"where does the shower drain go\", \"design-bathroom\", or a bathroom to be laid out or moved. Carries no clearances, no fixture dimensions and no ventilation rates; each comes from the code you quote, the accessibility standard, or the fixture's own data. For an accessible restroom to a standard use `design-accessible-restroom`; for commercial fixture counts use `/count-plumbing-fixtures`. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Design Bathroom"
  summary: "Lay out a bathroom around the plumbing wall and the door swing"
  discipline: "design-building-types"
  tags: "Design"
---

# Design Bathroom

A bathroom is a small room where four services, a door, a wet area and three
fixtures compete for the same few feet. It is laid out from a fixture catalogue
and then found to be impossible because the waste cannot get there or the door
hits the basin.

## Scope and limits — read first

**What this does.** Establishes what can physically be moved before laying
anything out, then works the layout around the waste, the door and the wet area,
which are the three things that decide it.

**What this does not do.**

- **It carries no dimensions.** No clearance in front of a fixture, no fixture
  sizes, no ceiling height, no ventilation rate, no fall on a waste run. Code
  from the jurisdiction you quote, accessible dimensions from the standard,
  fixture dimensions from the product.
- **It is not accessible design.** `design-accessible-restroom` lays out to an
  accessibility standard, where the overlapping clearances govern. Where this
  bathroom has to be accessible or adaptable, that skill takes it.
- It does not count fixtures for a commercial building.
  `/count-plumbing-fixtures` does.
- It does not detail the waterproofing build-up beyond naming what it has to do.
- It does not replace the Architect of Record.

**What you need before starting.** Where it is and what is around it. Where the
existing waste and vent are, in a renovation. What is above and below. Who uses
it and how many at once. Whether it has to be accessible or adaptable.

## Workflow

### Step 1. Find out what can actually move

Ask, in one message:

> 1. New build or renovation? In a renovation, where are the existing waste, vent
>    and water, and what is under the floor? Point at
>    `existing-conditions-survey`.
> 2. What is below this room, and can anything be run in that ceiling?
> 3. What direction do the joists run, and can they be drilled or notched? That
>    is the engineer's answer, not yours.
> 4. Who uses it, how many at once, and is it the only one?
> 5. Does it have to be accessible or adaptable now, or later? Quote the
>    standard if so.
> 6. Is there a window, and where does the ventilation go?

**Question 1 decides most of the layout in a renovation.** Moving a toilet a few
feet can mean opening a floor, and moving it to another wall can mean it cannot
be done at all. Establish that before drawing.

### Step 2. Fix the plumbing wall first

One wall carries the waste and the vent, and everything expensive follows it:

- Which wall can take the stack, and is it thick enough for it?
- Where does the toilet go, since it needs the largest waste and the shortest
  run? It effectively places itself, and the rest arranges around it.
- Where does the shower or bath drain, and can it fall to the same place? A
  shower on the far wall from the stack is a fall across the whole room.
- Can the basin share the wall, and if not what does its run cost?
- Is there a second wall option, and what does it cost to use it?

Say plainly when the desired layout requires the waste to run where it cannot.
**Moving the fixture is usually cheaper than moving the waste**, and that
sentence resolves most bathroom layouts.

### Step 3. Work the door, which is the other half

- Which way does it swing, and what does it hit: the basin, the toilet, a
  towel rail, another door?
- Can it swing out instead, and what does that hit in the room outside?
- **Can somebody who has fallen inside be reached if the door swings in?** This
  is a real consideration in bathrooms for older or unwell users and it is
  usually decided by habit.
- Is there a privacy sequence: is the toilet visible from outside when the door
  opens, and does it matter here?
- Is there space to stand and dry beside the shower without being in the door
  swing?
- Sliding or pocket doors: what does that do to the wall carrying services and
  switches?

### Step 4. Work the wet area

- Where the water actually goes: the shower, the splash zone at the basin, the
  floor beside the bath.
- What is waterproofed, how far up and how far out, and what the code requires,
  quoted.
- Where the floor falls to, and whether the whole floor falls or only the shower.
- **Whether the threshold at the shower is level**, which is what most clients
  want and what most renovations cannot do without dropping the structure.
- What the waterproofing does at the door and at the junction with the wall.
  Point at `design-below-grade-assembly` for the principle: a wet room is a tanked
  box with a hole in it.
- What is under the floor and what happens when it leaks. A wet room over a
  living room is a different specification from one over a slab.

### Step 5. Work ventilation, reach and storage

- **Ventilation.** Where the extract goes and how it gets out of the building.
  Same question as `design-kitchen`: it is a route and an elevation, not a fan.
  Whether the code allows the window or requires mechanical, quoted.
- **Reach.** What is reachable from the toilet, from the shower, and from the
  basin: paper, a towel, a control, a switch. These get placed last and get
  placed wrong.
- **Storage.** Where it goes, and whether there is room for the things people
  actually keep in a bathroom.
- **Heating**, and whether the room is warm when wet.
- **The mirror and the light on a face**, which is what people notice daily and
  which is usually an afterthought. Point at `senior-lighting-consultant`.

### Step 6. Report

- What can move and what cannot, from Step 1.
- The plumbing wall and where each fixture landed, with anything that required
  the waste to go where it cannot.
- Door swing and what it clears.
- The wet area strategy, and whether a level threshold is possible.
- The extract route and its termination.
- Every dimension still open, with who supplies it.
- What has to reach the engineer: joists, structure, extract.

Then ask whether to write it to a file and where.

## Rules

- **Establish what can move before laying anything out.**
- Fix the plumbing wall before the fixtures.
- Say when moving the fixture is cheaper than moving the waste.
- Work the door swing as a design decision, including whether it swings in.
- Name the extract route and its termination, every run.
- **Never supply a clearance, a fixture dimension, or a ventilation rate.**
- Point at `design-accessible-restroom` the moment accessibility governs.

## Anti-patterns

- Laying out from a fixture catalogue.
- Moving a toilet across the room in a renovation without asking about the
  waste.
- A door that swings onto the basin.
- Promising a level shower threshold without checking the structure.
- Treating a wet room over a living room like one over a slab.
- Assuming joists can be drilled where the waste needs to go.
- An extract fan with no route out of the building.
- Placing the paper holder and the towel rail last, from habit.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
