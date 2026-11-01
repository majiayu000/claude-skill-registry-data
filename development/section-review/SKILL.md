---
name: section-review
description: "Reads any section — a sketch section, a building section, a wall section, a consultant's, an inherited one — for the thing a section exists to settle: whether the vertical dimensions actually add up, and what has been drawn around rather than resolved. A section is the only drawing where the structure, the services, the ceiling, the floor build-up and the envelope have to agree in the same line, which is why it is the drawing most often cut where the conflicts are not. Trigger on \"read this section\", \"does this section work\", \"they sent a wall section\", \"check this section\", \"section-review\", or any section handed over. Carries no dimensions or depths; anything measured is read off the drawing at its stated scale. `plan-review` reads a plan and `assembly-review` reads a stack; this reads the drawing where the vertical dimensions meet. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Section Review"
  summary: "Read a section for what it resolves and what it draws around"
  discipline: "design-building-types"
  tags: "Review"
---

# Section Review

A plan can be wrong for years without anybody noticing. A section cannot,
because it is the one drawing where the floor-to-floor, the structure, the
services, the ceiling and the envelope all have to occupy the same vertical
line and add up.

Which is exactly why sections get cut through the corridor rather than through
the place where they would not.

## Scope and limits — read first

**What this does.** Reads any section for whether the vertical dimensions close,
what the cut avoids, and what has been drawn as poché or as "typical" rather
than resolved.

**What this does not do.**

- **It carries no dimensions or depths.** Anything measured is read at the
  stated scale and reported as read, or marked unmeasurable.
- It does not read a plan. `plan-review` does.
- It does not read an assembly's layers. `assembly-review` does, and a wall
  section is usually both drawings at once — say which part is being read.
- It does not check code, structure or services. `code-compliance-review`,
  `structural-drawing-review` and `mep-review` do.
- It does not replace the Architect of Record.

**What you need before starting.** The section, at a stated scale. Where the cut
is taken, on a plan. The floor-to-floor. What phase the drawing is.

## Workflow

### Step 1. Find out where the cut is, and where it is not

Ask, in one message:

> 1. Where is this section cut, on the plan? Is there a section marker?
> 2. Whose drawing, at what revision, at what scale?
> 3. What phase: sketch, developed, wall section, construction?
> 4. Is this the only section, or one of several?
> 5. Is the floor-to-floor stated anywhere?

**Then ask where it is not cut.** A single section through a building shows one
line, and the conflicts are almost always somewhere else: at the deepest beam,
at the corridor where the main duct crosses, at the stair, at the level change,
where the plate steps.

Name the places that ought to have a section and do not. That list is usually
the most useful thing this produces.

### Step 2. Check that the vertical dimensions close

The one arithmetic a section has to survive:

```
floor to floor
  - structure depth at this line
  - services below it
  - ceiling void and the ceiling itself
  - floor build-up above
= clear height
```

Run it with whatever is on the drawing, and report each term as `dimensioned`,
`scaled`, or `not shown`. Point at `design-ceiling`, which does this properly
with values from the engineers.

**Say plainly when the terms do not add up**, and say which term is missing
rather than which is wrong. Most sections do not close because something was
never in them, not because a number is incorrect.

### Step 3. Find what has been drawn around

The heart of it. Sections resolve things or avoid them, and both look like
drawing:

- **Poché with nothing in it.** A solid black or hatched zone standing in for a
  build-up nobody has decided.
- **"Typical" or "similar".** Which condition is it typical of, and is this one
  of them?
- **A break line.** What is behind it, and was it broken because it repeats or
  because it changes?
- **A cut that stops.** A section that ends at a wall rather than continuing to
  the ground or the sky.
- **Services shown as a rectangle.** A duct symbol with no size is a hope.
- **Ground drawn flat** where the site slopes. Point at `civil-drawing-review`.
- **A ceiling drawn as one line** where there is a plenum full of things.

Report each with what it is standing in for and who resolves it.

### Step 4. Check the places a section is for

The conditions a section exists to settle, and whether this one settles them:

- Every threshold and level change, inside and out.
- Where the roof meets the wall, and where the wall meets the ground. Point at
  `design-parapet` and `design-below-grade-assembly`.
- Head and sill of every opening in the cut.
- Where the structure lands and what it lands on.
- Stairs and any change in floor level.
- Where the ceiling changes height.
- What is above the highest point and below the lowest.

Anything in that list absent from the section is not necessarily wrong; it is
another section.

### Step 5. Report

- Where it is cut, and the sections that are missing.
- Whether the vertical dimensions close, with the missing terms named.
- Everything drawn around: poché, typical, break lines, symbol services.
- Which of the conditions a section settles are settled here.
- What was read at scale rather than dimensioned.
- What could not be read.

Then name the next: `design-ceiling` for the plenum arithmetic,
`assembly-review` for the build-up, `plan-review` for the plan it was cut from.

### Step 6. Save, if asked

Ask whether to write the reading to a file and where.

## Rules

- **Ask where it is cut, and name the places that are not cut.**
- Run the vertical arithmetic, and mark every term dimensioned, scaled, or not
  shown.
- Say which term is missing rather than which is wrong.
- Report poché, "typical", break lines and symbol services as things drawn
  around.
- Never measure something the scale cannot support.
- Judge a sketch section as a sketch section.

## Anti-patterns

- Reading the section and never asking where it was cut from.
- Accepting poché as a build-up.
- Treating "typical" as an answer.
- Assuming a duct symbol has a size behind it.
- Reporting a section as fine because it draws well.
- Missing that the one place needing a section has none.
- Scaling a dimension off a sketch.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
