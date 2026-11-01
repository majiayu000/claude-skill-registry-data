---
name: plan-review
description: "Reads any floor plan you hand it and reports three things separately: what is drawn, what a plan of this kind should show and does not, and what the plan commits to without saying so. Works whatever the project type, whatever the phase, and whether the plan is yours, a consultant's, a client's previous architect's, or one found in a property listing. Trigger on \"read this plan\", \"what do you make of this floor plan\", \"review this layout\", \"they sent us a plan\", \"plan-review\", or a plan handed over with no particular question attached. Carries no dimensions and no standards; anything measured comes from what is on the drawing. `design-critic` judges a design, `code-compliance-review` audits against eight code axes, and `circulation-study` traces the journeys; this reads the drawing first, which is what the other three assume has happened. It does not replace the Architect of Record."
license: MIT
metadata:
  title: "Plan Review"
  summary: "Read a plan for what is on it, what is missing, and what it implies"
  discipline: "design-building-types"
  tags: "Review"
---

# Plan Review

The first thing anybody does with a plan is form an opinion about it. The useful
first step is duller and it is skipped: work out what is actually drawn, what a
plan like this should show and does not, and what it has quietly committed to.

## Scope and limits — read first

**What this does.** Reads the plan and separates three things that get merged:
what is on it, what is missing from it, and what it implies without stating.
Works on any plan, at any phase, from anyone.

**What this does not do.**

- **It carries no dimensions or standards.** Anything measured is read off the
  drawing and reported with the scale it was read at, or marked unmeasurable.
- It does not judge the design. `design-critic` and `independent-critic` do, and
  they read better after this has run.
- It does not check code. `code-compliance-review` audits eight axes; `compliance-check`
  holds it against text you paste.
- It does not trace journeys or study circulation. `circulation-study` does.
- It does not read a whole set. `set-reader` does.
- It does not replace the Architect of Record.

**What you need before starting.** The plan. Its scale, its date and its
revision if they are on it. What kind of project it is, if known. Whose plan it
is and why you have it.

## Workflow

### Step 1. Establish what the drawing is before reading it

Ask, or read off the sheet:

> 1. Whose plan, from when, at what revision, and at what scale?
> 2. What phase does it appear to be: a sketch, concept, schematic, developed,
>    or construction?
> 3. Is it one of a set, or on its own?
> 4. Why do you have it: your own work, a consultant's, a previous architect's,
>    a client's existing building, a property listing?
> 5. Is there a north point and a scale bar?

**Question 4 changes everything about how it is read.** A listing plan is drawn
to sell and is often wrong. A previous architect's plan carries decisions nobody
on this team made. Your own plan is being checked against intentions you can
still state.

If there is no scale and no dimensions, say so and read it as a diagram. A plan
without either cannot support any of what follows and pretending otherwise is
the fastest way to a wrong finding.

### Step 2. Read what is drawn

Work systematically rather than by eye:

- The boundary of the building, and what is inside versus outside.
- Every room or space, and whether each is named and dimensioned.
- Every door and its swing. Every window.
- Structure: what is shown, what direction it spans, what is a wall and what is
  a column.
- Vertical: stairs, lifts, shafts, and where they go.
- Services: what is shown at all, and what has been left out.
- Levels and changes of level, including thresholds.
- What is fixed and what is furniture.
- The scale bar, north point, and anything on the sheet that is not the plan.

### Step 3. Say what is missing for a plan of this kind

Against the phase established in Step 1, not against a construction set:

| Missing | Would matter for | Late for this phase? |
|---|---|---|

The ones that are usually absent and always matter: door swings, level changes,
structure, shaft sizes, wall thicknesses, and whether the dimensions given
actually add up to the overall.

**Check that the parts add to the whole.** Room dimensions that do not sum to
the overall is the most common thing on a plan and it is silent.

### Step 4. Say what the plan commits to without saying so

The part nobody does, and where the value is:

- **Structure.** A long span, a column in the wrong place, a wall that has to be
  load-bearing for the plan to work.
- **Services.** A wet room far from any riser, a kitchen with nowhere for an
  extract to go, a room with a load and no plant space.
- **Code.** A dead-end corridor, a single exit, a door that swings the wrong
  way, a route that is not accessible.
- **Cost.** A shape with more envelope than it needs, a small number of very
  large spans, a level change that means a lift.
- **Programme.** Anything requiring something that has a lead time.

Report each as an implication with what would confirm it, not as a fault. The
plan may be right and somebody may have already resolved it.

### Step 5. Report

- What the drawing is, and whether it can support the reading (scale,
  dimensions, revision).
- What is drawn, briefly.
- What is missing, with whether it is late for the phase.
- Where the dimensions do not add up.
- What the plan commits to without saying, with what would confirm each.
- What could not be read, and why.

Close by naming the next skill: `design-critic` for judgement, `code-compliance-review` for
code, `circulation-study` for the journeys.

### Step 6. Save, if asked

Ask whether to write the reading to a file and where.

## Rules

- **Ask whose plan it is and why you have it**, before reading it.
- Say plainly when there is no scale and no dimensions, and read it as a diagram
  from then on.
- Judge missing items against the phase, not against a construction set.
- Check that the dimensions add up.
- Report implications with what would confirm them, never as faults.
- Never judge the design here. Name the skill that does.

## Anti-patterns

- Forming an opinion before reading what is drawn.
- Reading a property listing plan as though it were measured.
- Marking a schematic plan down for missing what a schematic plan does not show.
- Measuring off an unscaled drawing.
- Reporting an implication as a mistake.
- Skipping door swings and level changes, which is where most of it hides.
- Critiquing. Different skill, and separate on purpose.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
