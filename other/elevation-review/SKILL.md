---
name: elevation-review
description: "Reads any elevation for the two things it is doing at once: composing a facade, and hiding the depth that makes it buildable. An elevation is a flat drawing of something that is not flat, so joints, reveals, returns, thicknesses and everything behind the surface are all drawn as lines of equal weight or not at all. Checks what it commits to, what it leaves to a section, and where it disagrees with the plan. Trigger on \"read this elevation\", \"does this facade work\", \"they sent elevations\", \"check this elevation against the plan\", \"elevation-review\", or any elevation handed over. Carries no dimensions or module sizes; anything measured is read at the stated scale. `facade-module` divides an elevation into panels and `design-envelope` decides what each face has to be; this reads the drawing. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Elevation Review"
  summary: "Read an elevation for what it decides and what it flattens away"
  discipline: "design-building-types"
  tags: "Review"
---

# Elevation Review

An elevation is the drawing clients look at and the drawing that lies most, not
out of dishonesty but because it is flat. Everything with depth — a reveal, a
return, a sill, a shadow gap, a jamb — becomes a line the same weight as every
other line, and everything behind the surface disappears.

Read for composition it is one drawing. Read for what it commits the building to
it is another, and the second reading is the one nobody does.

## Scope and limits — read first

**What this does.** Reads any elevation for what it commits to, what it has
flattened away, and whether it agrees with the plan and the section it was drawn
from.

**What this does not do.**

- **It carries no dimensions or module sizes.** Anything measured is read at the
  stated scale and reported as read.
- It does not judge the composition. `design-critic` does, and it reads better
  after this.
- It does not divide the facade into panels. `facade-module` does.
- It does not decide what the wall has to be. `design-envelope` and
  `design-wall-assembly` do.
- It does not do daylight or shadow. `daylight-study` and `shadow-study` do.
- It does not replace the Architect of Record.

**What you need before starting.** The elevation, at a stated scale. The plan
and any section it relates to. Which face it is and what it faces. What phase
the drawing is.

## Workflow

### Step 1. Establish which face this is and what is behind it

Ask, in one message:

> 1. Which face, facing which way, and onto what: a street, a boundary, a
>    courtyard, a neighbour?
> 2. Whose drawing, at what revision and scale, at what phase?
> 3. Do you have the plan and a section for the same face?
> 4. Is the ground drawn as measured or assumed? Point at `survey-review`.
> 5. Is this a design elevation or a construction one?

**Question 3 decides how much of this is possible.** An elevation on its own can
be read for what it commits to; it cannot be checked against anything.

### Step 2. Read what it commits the building to

Whatever it was drawn for, an elevation decides:

- The number of storeys and roughly the floor-to-floor rhythm.
- Where the openings are, how big, and in what pattern.
- Where the entrance is, and whether it reads as one.
- The overall height and the profile against the sky.
- What material the building is, if it shows any.
- How the building meets the ground along its whole length.

Report each as committed or not yet, and note which of them a client who has
seen this drawing now believes.

### Step 3. Find what has been flattened away

The pass that earns the exercise. In every case, ask whether the drawing says or
merely implies:

- **Depth.** Is the facade flush, or does it have reveals and returns? An
  elevation of a flush wall and one of a deeply modelled wall can be the same
  drawing.
- **Joints.** Where does the material actually break: panel joints, movement
  joints, sheet sizes? Point at `facade-module` and `design-expansion-joint`.
- **The window in the wall depth.** Set forward, set back, and by how much. This
  single dimension changes the whole reading of a facade and never appears on an
  elevation.
- **Sills, heads, jambs, copings**, and whether any of them project.
- **What happens at the ends.** Where the elevation stops, and what the return
  looks like. Corners are where facades are actually judged and they are on
  neither elevation.
- **What is behind.** Is that window in front of a room, a riser, a plant space,
  a stair, or a blank wall?

### Step 4. Check it against the plan and the section

| Item | Elevation shows | Plan or section shows | Agree? |
|---|---|---|---|

- Do the openings line up with the rooms and the structure?
- Does the floor line on the elevation match the section's levels?
- Does the ground line match the survey and the civil grading?
- Does the height match what the plan's storey count implies?
- Are there openings on the elevation with no room behind them, or rooms with no
  opening?
- Does anything on the roof appear here: plant, a parapet, a stair bulkhead,
  a lift overrun? Point at `design-elevator`, whose overrun is drawn here or
  discovered later.

**An opening on an elevation with a riser behind it** is the classic finding and
it appears on almost every scheme once.

### Step 5. Report

- What the elevation commits to, and which of those a viewer now believes.
- Everything flattened away, with what would resolve each: usually a section or
  a detail.
- Disagreements with the plan and the section, with both values.
- What is at the corners and the ends, or that neither drawing shows it.
- What was read at scale rather than dimensioned.

Then name the next: `section-review` for the depth, `facade-module` for the
joints, `design-envelope` for what the face has to be, `design-critic` for
whether it is any good.

### Step 6. Save, if asked

Ask whether to write the reading to a file and where.

## Rules

- **Ask which face it is and what is behind it**, before reading.
- Report what the drawing commits to, and what a viewer will believe.
- Name everything flattened: depth, joints, window position in the wall,
  returns, corners.
- Check the openings against the plan and the levels against the section.
- Ask what is behind every opening.
- Never judge the composition here.

## Anti-patterns

- Reading an elevation for composition and stopping.
- Assuming a flush facade because the drawing is flat.
- Ignoring where the window sits in the wall depth.
- Not looking at the corner, which is on neither elevation.
- Missing an opening with a riser behind it.
- Treating a drawn ground line as a surveyed one.
- Forgetting the lift overrun and the roof plant, which appear here first.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
