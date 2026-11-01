---
name: design-balcony
description: "Works a balcony, terrace or projecting deck as the place where the envelope is deliberately broken: something structural passes through the insulation, the waterproofing has to turn up and drain away from a door, and a guard has to fix to whatever is left. Establishes the structural relationship first, since a cantilevered slab, a thermally broken connection and an independently supported balcony are three different buildings, then works the falls, the threshold, the drainage and the guard. Trigger on \"balcony detail\", \"cantilever slab thermal bridge\", \"terrace over occupied space\", \"balcony door threshold\", \"where does the balcony drain\", \"design-balcony\", or a projecting floor with a wall behind it. Carries no dimensions, no thermal values, no loads and no code requirements; guard and drainage requirements are code you quote and the structure is the engineer's. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Design Balcony"
  summary: "Carry structure, water, and insulation past the wall without losing any"
  discipline: "envelope-performance"
  tags: "Design"
---

# Design Balcony

A balcony is a hole punched deliberately through everything the wall was built
to do. Structure crosses the insulation, waterproofing has to turn up beside a
door that has to be level for accessibility, and a guard fixes into whatever is
left. It is a small element that fails in four ways at once.

## Scope and limits — read first

**What this does.** Settles the structural relationship, which decides
everything else, then works the falls, the threshold, the drainage, the guard
and what happens underneath.

**What this does not do.**

- **It carries no dimensions, values, loads or requirements.** Guard heights and
  loads, drainage sizing, thermal performance targets and accessible threshold
  limits are code and engineering you quote.
- **It does no structural work.** Cantilever design, thermal break connection
  selection, deflection and vibration: the engineer's. This names where those
  decisions land and what each choice costs the architecture.
- It does not build the wall or the roof. `design-wall-assembly` and
  `design-roof-assembly` do, and a terrace over occupied space is a roof before
  it is a balcony.
- It does not run the thermal arithmetic. Point at `condensation-check`, and say
  plainly that a balcony is usually the worst thermal bridge on the building.
- It does not replace the Architect of Record.

**What you need before starting.** What is under it: outside, occupied space, or
another balcony. The wall assembly behind it. The structure, or the options. The
door type and where the accessible route runs. The code's guard and drainage
provisions, quoted.

## Workflow

### Step 1. Establish what is underneath, first

Ask, in one message:

> 1. What is under the balcony: open air, occupied space, a garage, another
>    balcony?
> 2. What is the wall behind it? Point at `design-wall-assembly`.
> 3. What structure is proposed or possible?
> 4. What door, and is it on the accessible route? Quote the threshold
>    provision if so.
> 5. Quote the code's guard requirements and its drainage provisions.
> 6. Who uses it, and for what: standing, sitting, planting, storage, a barbecue?
> 7. How is it maintained and cleaned, and can the underside be reached? Point at
>    `facade-access-study`.

**Question 1 changes what this is.** Over occupied space it is a roof with a
guard on it, and it gets `design-roof-assembly` and
`design-below-grade-assembly`'s level of care. Over open air a leak is a
nuisance; over a bedroom it is a claim.

### Step 2. Settle the structural relationship, because everything follows it

Three options and they are different buildings:

| Relationship | What it means | What it costs |
|---|---|---|
| Continuous slab | The floor slab runs straight out | Cheapest to build, worst thermal bridge on the building, and the slab edge is cold inside |
| Thermally broken connection | A proprietary connector at the line of insulation | Continuity kept, a structural component with a lead time, and the engineer specifies it |
| Independently supported | Posts, hangers, or a separate frame | The envelope stays whole, and there is now a second structure with its own foundation and its own movement |

State which and why. Then say what it does to the four control layers, because
the answer is different for each. Point at `design-wall-assembly` for the layers
and to the engineer for the connection.

**If the answer is a continuous slab, say plainly that the thermal bridge is
unquantified and that `condensation-check` should run on the slab edge inside.**
That is where the condensation and the mould appear, in the corner of the room
behind it.

### Step 3. Work the falls and the threshold together

They fight each other and both are non-negotiable:

- The surface has to fall away from the building.
- The door threshold has to be low, and on an accessible route it has to be very
  low, quoted from the standard.
- The waterproofing has to turn up behind the door, high enough to matter.

Those three demands meet at one line. Report the strategy: a recessed structure
so the finished level drops, a drainage channel across the door, a raised
pedestal system over the waterproofing, or a combination. Say what each costs in
structure and in build-up depth.

A balcony detailed with the threshold as an afterthought is the single most
common source of water inside.

### Step 4. Work the drainage and where the water goes

- Where does the water leave: a drain, a scupper, an open edge?
- **An open edge means water runs down the facade below.** Say so; it stains,
  and on a multi-storey building it stains the same place repeatedly.
- If there is a drain, where does the pipe go, does it pass through occupied
  space, and what happens if it blocks? Point at `design-roof-drainage`.
- What happens in a freeze: standing water, ice at the door, a blocked outlet.
- Where the water goes at the bottom of the building.

### Step 5. Work the guard, which fixes into the weakest place

- What the guard fixes to: the slab top, the slab edge, the face, or a separate
  post. Each is a different penetration of the waterproofing.
- **Every fixing through a waterproof surface is a hole.** Name what closes each
  one, and prefer a fixing that does not pass through the membrane at all.
- Whether the guard is structural to a load quoted from the code, which is the
  engineer's.
- What the guard does to the elevation and to the view from inside, sitting.
- Drainage at the base of the guard, so water does not pond against it.

### Step 6. Work the underside and the edges

- What the soffit is, and whether it is insulated. Over occupied space it has to
  be.
- Where the balcony meets the wall at each end, and what the control layers do
  there. Point at `design-window-perimeter` for the door.
- Where it meets the balcony above and below.
- Any planter, which is a permanently wet weight over the waterproofing.
- Anything fixed to it later by an occupant: an awning, a light, a hook.

### Step 7. Report

- What is underneath, and therefore what standard of care applies.
- The structural relationship, with what it costs the envelope.
- The falls and threshold strategy, and what it costs in depth.
- The drainage and where water goes, including the blocked case.
- Every guard fixing and what closes it.
- Every open value, with who supplies it.
- The hand-offs: engineer for the structure and the guard load,
  `condensation-check` for the slab edge, `facade-access-study` for maintenance.

Close by saying the thermal bridge has not been quantified.

### Step 8. Save, if asked

Ask whether to write the detail to a file and where.

## Rules

- **Never supply a dimension, a load, a thermal value, or a guard height.**
- Ask what is underneath before anything else.
- Settle the structural relationship before detailing.
- Work the falls and the threshold as one problem, never in sequence.
- Name what closes every fixing that passes through the waterproofing.
- Say where water goes at an open edge, and that it stains.
- Say on every run that the thermal bridge is unquantified.

## Anti-patterns

- Detailing the threshold after the levels are set.
- A continuous slab with no mention of the cold slab edge inside.
- Guard posts through the membrane with the closure left to the contractor.
- An open drainage edge over an entrance or a principal elevation.
- Treating a terrace over occupied space as a balcony rather than as a roof.
- Recalling a guard height.
- A planter over waterproofing with no thought to weight, drainage, or the day
  it has to be lifted to find a leak.
- Forgetting that the underside is a soffit somebody sees.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
