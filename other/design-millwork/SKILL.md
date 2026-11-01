---
name: design-millwork
description: "Details built-in joinery to the point a shop can price it without asking: what is fixed and what moves, how it meets a floor and a wall that are neither level nor straight, what it hangs off and whether that backing exists, where the services in it come from, and which decisions are the shop's rather than the drawing's. Trigger on \"millwork\", \"casework\", \"joinery detail\", \"built-in\", \"reception desk\", \"how does this cabinet meet the wall\", \"design-millwork\", or a built-in element that has to be drawn for tender. Carries no dimensions, no clearances, no material thicknesses and no hardware; ergonomic and accessible dimensions come from the standard you quote and every material figure from the fabricator or the data sheet. It is not shop drawing — `submittal-review` reads those when they come back — and does not replace the Architect of Record."
license: MIT
metadata:
  title: "Design Millwork"
  summary: "Detail built-in joinery so the shop can price it and the wall can hold it"
  discipline: "design-building-types"
  tags: "Design"
---

# Design Millwork

Joinery is where a small practice's drawings get tested, because the shop prices
exactly what is drawn and asks about everything that is not. The two things that
come back as questions are always the same: what it fixes to, and what happens
where it meets a building that is not straight.

## Scope and limits — read first

**What this does.** Takes one built-in element and works it to the point a shop
can price it: the function, the fixings, the tolerance at every junction with
the building, the services in it, and the boundary between what the drawing
decides and what the shop does.

**What this does not do.**

- **It carries no dimensions.** No counter heights, no reach ranges, no knee
  clearances, no shelf spans, no material thicknesses, no hardware. Ergonomic
  and accessible dimensions come from the standard you quote; material and span
  figures from the fabricator.
- **It is not a shop drawing.** The shop draws it; `submittal-review` reads what
  comes back. This is the design intent drawing they price and draw from.
- It does not specify products or finishes. `schedule-builder` holds the
  schedule and the specification names the materials.
- It does not do accessibility compliance. Point at `/test-ada` for one
  clearance and `accessibility-specialist` for the route.
- It does not do structure. Anything heavy, anything a person could climb, and
  anything hung from a partition rather than from structure is a question for
  the engineer.
- It does not replace the Architect of Record.

**What you need before starting.** What it is for and who uses it. Where it is,
and what it meets on every side. The wall construction behind it. What services
it needs. Whether it is fixed or loose. The accessibility standard, if anything
about it has to be reachable.

## Workflow

### Step 1. Take the use, and who uses it standing or sitting

Ask, in one message:

> 1. What is it for, and what happens at it? Standing, sitting, both, from one
>    side or two?
> 2. Who uses it: staff, public, children, someone seated in a wheelchair? Does
>    the accessibility standard apply, and can you quote the relevant part?
> 3. What goes in it, and how much? Weight and size, not "storage".
> 4. Where is it, and what does it meet on each side and above?
> 5. What is the wall behind it made of, and is there backing?
> 6. Does it need power, data, water, waste, or ventilation?
> 7. Is it fixed, or could it be loose furniture instead?

**Question 7 is asked first for a reason.** Built-in is expensive, permanent,
and often chosen by habit. If loose furniture would do it, say so; the saving is
real and it is a `budget-reconciliation` item.

### Step 2. Fix what it does before what it looks like

| Element | What it has to do | Dimension needed from you |
|---|---|---|

Work through the functional requirements: working height, reach, what has to be
seen over or not seen over, what has to be reached from a seated position, door
and drawer swings and what they hit, what has to be lockable, what has to be
cleanable underneath.

Leave every dimension as a question. Where the accessibility standard governs
one, name the provision to quote rather than the figure.

### Step 3. Work every junction with the building

This is the step that decides whether the shop can build it. The building is not
straight, not level, and not square, and the joinery is.

| Junction | What it meets | Tolerance strategy | Who takes up the difference |
|---|---|---|---|

- **Floor.** Is there a plinth, a recessed toe, a scribe? Existing floors slope;
  a long run against one shows it. Point at `existing-conditions-survey`.
- **Wall, each end.** Scribes, filler pieces, or a shadow gap. A shadow gap
  forgives everything and has to be drawn deliberately, not left as a gap.
- **Ceiling or the top.** Does it reach, and if it stops short what closes the
  gap and how is the top cleaned?
- **Adjacent joinery**, and whether it is the same shop.
- **Anything that passes through**: a column, a pipe, a sprinkler, a switch.

**Name who takes up the difference at every junction.** A drawing that shows a
joinery unit and a wall meeting with a line has not decided, and the answer will
be decided on site by whoever gets there first.

### Step 4. Work what holds it up

- What does it fix to: studs, blocking, masonry, floor?
- **Is the backing there?** Backing has to be located before the wall closes, so
  it belongs on the partition drawings and not only here. Point at
  `design-partition`.
- Anything wall-hung and heavy, anything a child could climb, anything with a
  drawer full of files: name it as a question for the engineer rather than
  assuming the wall takes it.
- Anti-tip and seismic restraint where required, quoted.

### Step 5. Work the services in it

Every built-in with power in it becomes a coordination item:

- Where power, data, water and waste come from, and whether they arrive in the
  wall or the floor.
- Whether anything needs ventilation: a fridge, a printer, equipment in a
  cupboard.
- Whether anything needs access for service, and what has to be removable.
- Where the switches, outlets and cutouts land, and whether they are visible.
- Sinks and taps: the plumbing has to be coordinated with the carcass, and the
  cutout is the shop's from a template.

### Step 6. Draw the line between the drawing and the shop

Say which decisions belong to which, explicitly, because leaving it implied
produces either an over-drawn detail nobody reads or an under-drawn one that
gets built wrong:

| Decision | Drawing's | Shop's |
|---|---|---|

Generally the drawing owns: what it does, the overall geometry, the material and
finish, the junctions with the building, the reveals and shadow gaps, and
anything visible. Generally the shop owns: carcass construction, joint methods,
hardware selection within a stated performance, and how it is broken down to fit
through the door.

**Say how it gets into the room.** A unit that cannot pass the door or the lift
comes in pieces, and where the joints fall is a design decision if any of them
are visible.

### Step 7. Report

The function table, the junctions with who takes up the difference, the fixings
with backing flagged, the services, and the drawing-versus-shop line. Then:

- Every dimension still open, with who supplies it.
- Every junction where nobody takes up the difference.
- Whether backing has reached the partition drawings.
- What is a question for the engineer.
- Whether loose furniture was considered.

Then ask whether to write it to a file and where.

## Rules

- **Never supply a dimension, a clearance, or a hardware selection.**
- Ask whether it could be loose furniture, every run.
- Every junction names who takes up the difference between straight joinery and
  a building that is not.
- Backing is located on the partition drawings, not only here.
- Say how the unit gets into the room.
- Draw the drawing-versus-shop line explicitly.
- Never assume a wall can carry something hung on it.

## Anti-patterns

- Drawing joinery meeting a wall with a single line.
- Assuming the floor is level along a long run.
- Specifying a counter height from memory.
- Leaving backing to the contractor to work out.
- Detailing the carcass, which is the shop's and better than yours.
- Under-drawing the visible junctions and over-drawing the hidden ones.
- Designing a unit that cannot get into the room.
- Building in what furniture would have done.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
