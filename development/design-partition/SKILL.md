---
name: design-partition
description: "Builds an interior partition type from what the partition has to do rather than from a wall type legend copied forward: takes the acoustic separation, the fire rating, the structural condition above and what has to be fixed to it, then works the build-up and the two decisions that decide whether it performs — how far up it goes, and what happens at the head where the structure above moves. Trigger on \"partition type\", \"interior wall build-up\", \"does this wall go to deck\", \"STC between these rooms\", \"deflection head detail\", \"wall type legend\", \"design-partition\", or a room adjacency with a question about the wall between. Carries no ratings, no STC values, no stud spacings and no listings; performance comes from the specification or the acoustician and every rated assembly is a tested system you cite. For an exterior wall use `design-wall-assembly`; for a rated assembly's continuity use `design-fire-barrier`. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Design Partition"
  summary: "Build up an interior partition and decide where it stops"
  discipline: "design-building-types"
  tags: "Design"
---

# Design Partition

A drawing set carries fifteen wall types and most of them arrived from the last
project. The two things that decide whether a partition works are not in the
build-up at all: how far up it goes, and what happens where it meets a structure
that moves.

## Scope and limits — read first

**What this does.** Takes the demands on one partition type, works the build-up
against them, then works the head and the extent, which is where partitions
actually fail. Names what each layer is for and removes any that has no job.

**What this does not do.**

- **It carries no numbers or listings.** No fire rating, no acoustic value, no
  stud gauge or spacing, no insulation thickness, no deflection allowance.
  Performance requirements come from the specification, the acoustician and the
  code analysis; every rated assembly is a tested system you cite by number.
- It does not trace a rated assembly around the building.
  `design-fire-barrier` does, and a partition type is one section of that
  surface.
- It does not do the acoustic design. `design-acoustic-separation` works the
  separation as a whole including flanking, and this holds one wall in it.
- It does no structural work. Deflection of the structure above, the partition's
  own lateral stability, and anything heavy fixed to it are the engineer's.
- It does not lay out the plan or decide which rooms need which type.
- It does not replace the Architect of Record.

**What you need before starting.** What is on each side of it and what that
demands. The rating required and what requires it, quoted. The acoustic
separation required and its source. What is above: structure, and how much it
moves. What has to be fixed to the wall. The ceiling condition on both sides.

## Workflow

### Step 1. Take the demands, not the build-up

Ask, in one message:

> 1. What is on each side, and what is the worst pair this type will separate?
>    A type gets used everywhere it fits, so design it for the worst case it
>    will be drawn against.
> 2. What rating is required, and what requires it? Quote it.
> 3. What acoustic separation is required, from the specification or the
>    acoustician?
> 4. What is directly above: a structural slab, a beam, a joist, another
>    partition, a roof? How much does it move, and who told you?
> 5. What is fixed to it: cabinets, equipment, grab bars, televisions, doors,
>    glazing?
> 6. Is there a ceiling on each side, at what height, and is it the same on
>    both?
> 7. What passes through it, and is the MEP set available?

If the user offers a wall type instead, take it as a proposal to test against
the demands.

### Step 2. Work the two decisions that decide the wall

Before the layers, answer these two and say why:

**How far up does it go?** To the underside of the ceiling, to the underside of
the structure, or somewhere between. This decides the acoustic performance more
than the build-up does, it decides whether the rating is continuous, and it
decides the cost. A partition stopping at the ceiling with a continuous plenum
over it separates nothing acoustically, whatever the assembly is rated at.

**What happens at the head?** The structure above moves, and a partition built
tight to it either carries load it was not designed for or cracks. A deflection
head is a detail with a movement allowance from the engineer, and it has to
maintain the rating and the acoustic seal while moving. State that all three
have to hold at once.

Present both as decisions with reasons, not as details.

### Step 3. Build up the layers, and read the gaps between rows

| # | Layer | Its job | Value needed from you |
|---|---|---|---|

**A layer with no job comes out.** Insulation in a partition with no acoustic or
fire requirement is a cost with no purpose; say so and ask what it is for.

Then read between the rows:

- Are the layers on both faces the same, and should they be? Asymmetry is
  sometimes deliberate and sometimes a drafting accident.
- Does anything need a service void, and on which side?
- Does a fixing pass through a layer that has to stay continuous?
- Is the assembly a tested system, and does the proposed build-up still match
  the listing? A layer added for another reason can invalidate it.

### Step 4. Work the edges: head, base, jambs and junctions

- **Head**, as decided in Step 2, with the movement, the rating and the seal all
  named.
- **Base**: what it sits on, whether the finish runs under it, and what the
  acoustic seal is at the floor. A partition sealed at the head and not at the
  base leaks sound at the base.
- **Jambs and door openings**: doors are the acoustic weak point in almost every
  partition, and a rated door in a rated wall is a separate listed assembly.
- **Junctions with the exterior wall**, where the partition meets the facade and
  the mullion. Point at `design-wall-assembly`.
- **Junctions with other partitions**, and where a type changes along its length.
- **Corners and terminations**, including where a partition stops in open space.

### Step 5. Work what goes through it and what hangs on it

- Every penetration: services, boxes, and whether back-to-back boxes are
  offset. Point at `penetration-review`.
- What is fixed to it and whether the wall can take it. Anything heavy needs
  backing, and backing has to be located before the wall is closed.
- Whether a ceiling is supported off it, which makes it structural in a small
  way.

### Step 6. Report

The two decisions, the build-up table, the edges, the penetrations. Then:

- Every value still open, counted, with who supplies it.
- Whether the assembly is a tested system and whether the listing was cited.
- Whether the acoustic performance depends on something outside this wall, and
  the pointer to `design-acoustic-separation`.
- What has to reach the engineer: the movement allowance, anything heavy.

Then ask whether to write the type to a file and where.

## Rules

- **Never supply a rating, an acoustic value, a spacing, or a movement
  allowance.**
- Answer the extent and the head before the layers, every run.
- Design the type for the worst pair it will be used between.
- Every layer carries a job, or it comes out.
- Name the head condition as holding movement, rating and seal at once.
- Never assert a tested assembly's number.

## Anti-patterns

- Carrying a wall type legend forward from the last project.
- Stopping an acoustic partition at the ceiling and reporting the assembly's
  rated value as the separation achieved.
- Drawing the head tight to the structure.
- Sealing the head and not the base.
- Adding a layer to a listed assembly without checking the listing still holds.
- Insulation in a partition with no requirement behind it.
- Leaving backing for wall-hung items to the contractor.
- Treating a rated door as covered by the wall's rating.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
