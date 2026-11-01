---
name: equipment-reader
description: "Reads any product or equipment data sheet and pulls out the six things a building has to provide for it: the space it occupies, the clearance it needs on each side to be serviced, the route to get it in and out, the services it needs and from where, what it weighs and what carries it, and what it does to the room around it in heat, noise and vibration. Works for a rooftop unit, a lift, a range, a transformer, a door closer or a light fitting. Trigger on \"read this cut sheet\", \"what does this unit need\", \"they sent product data\", \"will this fit\", \"equipment-reader\", or a data sheet handed over with a question about space. Carries no dimensions or clearances of its own: every figure comes off the sheet, and a figure absent from the sheet is reported missing rather than assumed from a similar product. It does not select or size equipment and does not replace the engineers or the Architect of Record."
license: MIT
metadata:
  title: "Equipment Reader"
  summary: "Read a cut sheet for what the building has to give the equipment"
  discipline: "structure-mep"
  tags: "Reference"
---

# Equipment Reader

A cut sheet is written to sell a product and read for one number, usually the
overall size. The building has to provide five other things, they are all on the
sheet somewhere, and the one that gets missed is the service clearance, which is
larger than the unit.

## Scope and limits — read first

**What this does.** Reads any data sheet and reports the six demands it makes on
the building, with every figure attributed to where on the sheet it came from.

**What this does not do.**

- **It carries no dimensions or clearances.** Every figure comes off this sheet
  for this model. **A figure from a similar product is not a figure**, because
  clearances and dimensions vary between models more than anyone expects.
- It does not select or size equipment. That is the engineer's or the
  operator's.
- It does not check the engineering.
- It does not lay out the room. `design-mechanical-room`,
  `design-electrical-room` and `design-kitchen` do, and this feeds them.
- It does not read a schedule of many items. `schedule-reader` does.
- It does not replace the engineers or the Architect of Record.

**What you need before starting.** The data sheet, complete, including the
dimensional drawing and the installation notes. The model actually specified,
not the family. Where it is intended to go.

## Workflow

### Step 1. Establish which product this actually is

Ask, or read off the sheet:

> 1. Which model exactly, and is this the model specified or a family sheet
>    covering several?
> 2. Which options or accessories are included? Many change the dimensions and
>    the clearances.
> 3. Where is it intended to go, and what is around it?
> 4. Is this a basis of design with substitutions permitted?

**A family sheet is not a product sheet.** If the sheet covers a range, say so
and say which figures are the worst case, because that is what has to be held.

Same for question 4: if substitutions are permitted, the space held has to suit
more than this unit.

### Step 2. Pull the six demands

| Demand | Figure | Where on the sheet | Missing? |
|---|---|---|---|

1. **Space.** Overall dimensions, including anything projecting: handles,
   controls, connections, doors, filters.
2. **Service clearance, per side.** Not a margin. Which side needs what, for
   what operation: a tube pull, a coil pull, a filter change, a door swing, a
   panel to open. This is the figure most often missed and it is usually the
   largest one.
3. **Route.** The dimension it has to pass through to get in, and whether it
   breaks down into pieces. Then the same question for getting it out at
   replacement.
4. **Services.** What it needs, at what connection size, and from which side.
   Water, waste, gas, power, data, drainage, condensate.
5. **Weight.** Operating weight, and shipping weight if they differ. Point
   anything structural at the engineer.
6. **What it does to the room.** Heat rejected, noise, vibration, and any
   clearance to combustibles.

Anything not on the sheet is `missing`, and the row says who to ask.

### Step 3. Read the installation notes, which is where the conditions hide

Data sheets carry requirements in prose that never reach a drawing:

- Required ventilation of the space it sits in.
- A level base, a housekeeping pad, or isolation.
- Minimum distance from a wall, a corner, another unit.
- Access required for a specific operation at a specific frequency.
- Anything voiding the warranty: an installation condition, a distance, a
  service interval.
- Whether it may be installed outdoors, and what that requires.

**The warranty conditions are worth reading in full.** They are the ones that
turn up at commissioning.

### Step 4. Say what the building has to change

Set the demands against where it is intended to go:

| Demand | Available | Difference |
|---|---|---|

Then say plainly whether it fits, does not fit, or cannot be told from what was
supplied. Where it does not fit, say which of the six is the binding one — it is
usually the service clearance or the route, not the unit.

### Step 5. Report

- Whether this is a specific model or a family, and whether substitutions are
  permitted.
- The six demands, with every missing figure counted and who to ask.
- The installation and warranty conditions that reach the drawings.
- Fits, does not fit, or cannot tell, with the binding demand named.
- What goes to the structural engineer.

### Step 6. Save, if asked

Ask whether to write the reading to a file and where.

## Rules

- **Never supply a dimension or a clearance from a similar product.**
- Establish whether the sheet is one model or a family, and hold the worst case
  if it is a family.
- Record the service clearance per side, with the operation it is for.
- Read the installation notes and the warranty conditions, every run.
- Ask about the route out, not only the route in.
- A missing figure is reported missing, with who to ask.

## Anti-patterns

- Taking the overall dimensions and stopping.
- Adding a percentage instead of the actual service clearances.
- Using a figure from another model in the same range.
- Ignoring the installation notes because they are prose.
- Planning the route in and not the replacement.
- Holding the drawn dimension when substitutions are permitted.
- Missing the projecting handle, control panel or connection.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
