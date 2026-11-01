---
name: daylight-study
description: "Checks each room's depth against how far sidelight can reach it, from the window head heights, room depths, and glazing areas the user supplies: daylit depth by a stated convention, glazing-to-floor arithmetic held against a code minimum the user quotes, and the no-sky line when a facing building is in the way. Trigger on \"daylight study\", \"how deep does daylight reach\", \"is this room too deep for daylight\", \"no-sky line\", \"daylight-study\", or room depths paired with window head heights. The depth convention and the obstruction geometry are the only things this skill supplies itself; every dimension, glazing area, and code minimum comes from the user. It is a plan-stage tool for comparing layouts, not a daylighting simulation: no daylight factor, no illuminance, no glare, no LEED credit documentation, all of which come from a model. Exterior shadows on neighbors belong to shadow-study; energy-code glazing checks belong to test-glazing."
license: MIT
metadata:
  title: "Daylight Study"
  summary: "Work out how deep daylight reaches into each room, and which rooms stay dark"
  discipline: "design-building-types"
  tags: "Design, Analysis"
---

# Daylight Study

Give it each room's depth, its window head height, and its glazing area, and it
tells you how much of the room daylight actually reaches. The depth convention
and the obstruction geometry are worked out and shown step by step. Everything
about your rooms, and everything the code demands, is yours to supply.

## Scope and limits — read first

**What this does.** For each room you name, computes the daylit depth from the
window head height by a stated convention, compares it to the room's depth,
and reports the remainder that daylight does not reach. Computes the
glazing-to-floor-area ratio, held against a minimum only if you quote one. If
a facing building or wall is in the way, computes the no-sky line: the depth
past which no sky is visible from the working plane, from the geometry you
give. All of it lands in one table you can run across rooms and across layout
options.

**What this does not do.**

- **It is not a daylighting simulation.** No daylight factor, no illuminance,
  no lux, no glare, no annual metrics, no LEED daylight credit. Those come out
  of a model with a sky in it, run by whoever owns your energy and daylight
  modeling. This skill is the arithmetic you do before that model exists, to
  decide which rooms are worth modeling at all.
- **It does not know your code's light and ventilation minimums.** Whether a
  habitable room needs glazing at some percentage of its floor area, and what
  counts toward it, is code text and comes from you or `docs/jurisdiction.md`
  reading, never from memory. The skill does the division; you hold it against
  the rule.
- It handles sidelight only. Skylights and monitors light a plan differently,
  and their geometry is not in here.
- It ignores glass properties. Visible transmittance changes what a window
  delivers and is a spec decision, not plan arithmetic.
- Shadows this building casts on neighbors are `shadow-study`'s question.
  Whether the glazing passes the energy table is `test-glazing`'s.

**What you need before starting.** The room list with each room's depth from
the window wall and its floor area, the window head height in each room, the
glazing area per room, the code minimum quoted with its source if you want a
verdict against one, and, where a building faces the window, its height and
the distance to it.

## Workflow

### Step 1. Collect the rooms

Ask, in one message:

> 1. Which rooms, and for each: the depth from the window wall, and the floor
>    area.
> 2. The window head height in each room, measured from the floor.
> 3. The glazing area per room, and what you counted as glazing.
> 4. Is there a code minimum to check against? If so, quote it and name where
>    it is from. Without one I report ratios, not verdicts.
> 5. Does anything face the windows? If so, its height and the distance from
>    the window to it, and the sill or working-plane height you care about.

Confirm the units back before computing. Everything comes back in the units
given, and a study run with a metric head height against imperial depths is
wrong everywhere and looks fine.

### Step 2. Compute the daylit depth

State the convention before the arithmetic, every time:

```
convention      daylit depth ~ 2.0 x window head height for a sidelit room,
                ~ 2.5 x with a high transom or light shelf
                (a rule-of-thumb convention, not a code value; name your own
                multiplier and I will use it instead)
daylit depth    <multiplier x head height, arithmetic shown>
room depth      <as given>
remainder       <room depth - daylit depth, or "fully daylit">
```

Per room. A room deeper than its daylit depth is not a failure; it is a fact
about the plan, and the report says how much of the room is past the light.

### Step 3. Compute the glazing ratio

```
glazing area    <as given>
floor area      <as given>
ratio           <glazing / floor, arithmetic shown>
minimum         <quoted from the user, with their source, or "none supplied">
```

If a minimum was quoted, state each room against it in the user's own words.
If none was, report the ratio bare and say the rule to hold it against is
theirs to bring.

### Step 4. Compute the no-sky line, where something faces the window

Only for rooms where the user gave an obstruction. From the working plane, sky
is visible through the window head until the line of sight from a point in the
room, through the head, drops below the top of what faces it. Set the two
sight lines equal and solve for the depth, showing the triangles:

```
head above working plane         <arithmetic>
obstruction above working plane  <arithmetic>
distance to obstruction          <as given>
no-sky depth                     <similar triangles, arithmetic shown>
```

If the obstruction top sits below the window head as seen from the window, the
sky is clear and the row says so. If the geometry gets past one facing plane,
a court, a reveal, a sloped tower, say so and stop rather than approximating
silently.

### Step 5. Report

One table, rooms as rows, options side by side if there is more than one
layout:

| Room | Depth | Head height | Daylit depth | Past the light | Glazing : floor | No-sky depth |
|---|---|---|---|---|---|---|

Then, in prose: which rooms sit deepest past their daylight, and what moves
each one, since there are only three levers: raise the head, pull the depth,
or borrow light through the plan. If a code minimum was quoted, each room
stands against it, quoted as given. If layouts are being compared, say where
the options actually differ, not just what each scores.

Close every run with: sidelight only, glass properties not modeled, and
anything filed for a credit or a code alternative comes from a simulation,
not from this table.

### Step 6. Save, if asked

Ask whether to write the study to a file and where. Write it directly,
including the convention and arithmetic lines. There is no template and no
script.

## Rules

- **The depth convention and the obstruction geometry are the only things this
  skill knows.** Every dimension, area, and minimum comes from the user, and
  each carries its source in the output.
- Name the convention as a convention, with its multiplier, before using it.
  The user's own multiplier always replaces it.
- No verdict against a code without the code text quoted by the user, source
  named. Without it, ratios are measurements, not findings.
- Print the arithmetic per room. A daylit depth nobody can re-derive is not
  checkable.
- Never convert the user's units. Confirm them once, then keep them.
- Say on every run that this is plan-stage arithmetic, not a simulation.

## Anti-patterns

- Quoting a light-and-ventilation minimum from memory ("code wants glazing at
  8% of floor area") instead of asking for the text. Percentages and what
  counts toward them are code text and go stale; the user brings them.
- Reporting a daylight factor or an illuminance. That is a simulation's answer
  wearing arithmetic's clothes, and it will be wrong.
- Treating the 2-times-head-height convention as a limit a room passes or
  fails, or presenting it without saying it is a convention.
- Skipping a facing building the user mentioned because they left out its
  height. Ask; the no-sky line is often the whole answer.
- Calling a room compliant. A room meets the minimum the user quoted, in
  their words, or the question stays open.

## Resources

None. This skill is one file. Output is written directly at the path you
choose.
