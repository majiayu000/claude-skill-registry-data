---
name: circulation-study
description: "Studies circulation as a set of named journeys rather than as corridor area: establishes who moves through the building and why, traces each journey door to door, finds the places two journeys cross that should not, and reports where a route depends on something being unlocked, staffed or explained. Separates the circulation a plan needs from the circulation it happens to have. Trigger on \"circulation study\", \"trace the routes\", \"do these flows cross\", \"clean and dirty separation\", \"public and staff routes\", \"wayfinding through the plan\", \"circulation-study\", or a plan handed over with a question about how people move through it. Carries no corridor widths, no efficiency ratios and no separation requirements; egress widths and distances belong to `design-egress` and accessibility to the accessibility standard you quote. It does not lay out a plan and does not replace the Architect of Record."
license: MIT
metadata:
  title: "Circulation Study"
  summary: "Trace each journey through the plan and find where two that should not meet do"
  discipline: "design-building-types"
  tags: "Design"
---

# Circulation Study

Circulation gets measured as a percentage and designed as what is left over
between rooms. The questions that decide whether a building works are different:
who is walking, where from, where to, and who do they meet on the way.

## Scope and limits — read first

**What this does.** Names the journeys, traces each one through the plan door by
door, and reports three things: where journeys cross that should not, where a
route depends on a person or a key rather than on the plan, and where the same
journey is long or unclear for one group and short for another.

**What this does not do.**

- **It carries no dimensions and no ratios.** Corridor widths, egress widths,
  travel distances, circulation percentages: none are here. `design-egress`
  holds the egress arithmetic and the accessibility standard you quote holds the
  rest.
- It is not an egress study. Egress is one journey among several and it has its
  own skill, its own arithmetic and its own code. This study includes the egress
  route as a journey and points at `design-egress` for whether it complies.
- It is not accessibility review. It traces the accessible route as a journey
  and flags breaks; `accessibility-specialist` reads it properly.
- It does not model. No pedestrian simulation, no queuing, no flow rates.
- It does not lay out a plan.
- It does not replace the Architect of Record.

**What you need before starting.** The plans, at a scale that shows doors. Who
uses the building and when. The programme, ideally with `adjacency-matrix` run.
Any separation that is required rather than preferred, and what requires it. The
operational hours and what changes outside them.

## Workflow

### Step 1. Name the journeys before looking at the plan

Ask, in one message:

> 1. Who moves through this building? List every group, including the ones that
>    are not people: goods, waste, laundry, food, records, specimens, plant,
>    money, prisoners, patients, animals, whatever this building has.
> 2. For each group: where do they arrive, where do they go, and what do they do
>    on the way?
> 3. Which pairs must not meet, and what requires the separation?
> 4. What changes out of hours: doors locked, desks unstaffed, entrances closed?
> 5. What happens on the busiest day rather than the average one?

Question 1 is where studies fail. A plan that works for staff and visitors can
be unworkable for waste, and waste is never on the list until somebody asks.

### Step 2. Trace each journey, door by door

One table per journey, not a summary:

| Step | From | To | Through | Doors | Depends on | Note |
|---|---|---|---|---|---|---|

`Depends on` is the column that earns the study: a door that has to be unlocked,
a desk that has to be staffed, a lift that has to be called, a sign that has to
be read, somebody who has to be asked. A route depending on any of those is a
route that fails at 7pm or on the first day.

Trace in both directions. Journeys are rarely symmetrical, and the return trip
is where people get lost.

### Step 3. Find the crossings

Lay the journeys over each other and report every place two share a space:

| Journey A | Journey B | Where | Required separate? | What separates them |
|---|---|---|---|---|

For each crossing that should not happen, say what would separate them: a
different route, a time separation, a door, a lobby, or a change to the plan.
Time separation is a legitimate answer and it is also an operational commitment,
so name who owns it.

Report crossings that are fine as well as crossings that are not. A study that
lists only problems does not show that the rest was looked at.

### Step 4. Compare the journeys against each other

- **Length and clarity by group.** Which group has the longest or least obvious
  route, and is that the group least able to cope with it? A visitor route
  longer than the staff route is normal; a patient route longer than the staff
  route usually is not.
- **Number of decisions.** Count the points where someone has to choose a
  direction. That count, not corridor width, is what makes a building feel
  confusing.
- **First-time versus daily.** Trace one journey as somebody who has never been
  here. Every route that works only with familiarity is flagged.

### Step 5. Report

The journeys, the crossings, the comparison, then:

- Every route depending on a person, a key or a sign, counted.
- Every required separation not achieved, listed individually with what requires
  it.
- Every journey that was named but not traced, and why.
- What was assumed about the operation rather than told.

Close by pointing at `design-egress` for the egress arithmetic and at the
accessibility standard for the accessible route.

### Step 6. Save, if asked

Ask whether to write the study to a file and where.

## Rules

- **Never supply a width, a distance, or a circulation percentage.**
- Name the journeys before opening the plan, and include the non-human ones.
- Trace door by door, in both directions.
- Every route dependency on a person, key or sign is recorded.
- Report crossings that are acceptable as well as those that are not.
- Never present this as egress compliance or accessibility review.

## Anti-patterns

- Measuring circulation as a percentage and calling it studied.
- Tracing only the routes the plan was designed around.
- Forgetting waste, goods, or anything that arrives at a back door.
- Tracing one direction and assuming the return is the same.
- Treating a time separation as achieved without naming who operates it.
- Calling a route clear because it is clear to someone who drew the plan.
- Doing the egress arithmetic here.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
