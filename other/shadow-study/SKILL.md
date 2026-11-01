---
name: shadow-study
description: "Computes solar altitude and azimuth from latitude, date, and time, then the shadow a massing casts: length, direction, and, if the user supplies the distance, whether it reaches a neighboring line. Trigger on \"shadow study\", \"how far does the shadow go\", \"solstice shadows\", \"will my building shade the neighbor\", \"shadow-study\", or a massing height paired with a date and a place. The solar geometry is computed from published astronomy formulas, the one thing this skill works out itself; everything else comes from the user: heights, distances, grades, and any shadow criteria the jurisdiction enforces. Flat ground is assumed unless the user supplies grades. It is a design-stage tool for comparing massing options, not a submission-grade shadow study, and it does not know which hours or open spaces any city protects."
license: MIT
metadata:
  title: "Shadow Study"
  summary: "Compute sun angles and shadow reach for a massing, date, and place"
  discipline: "design-building-types"
  tags: "Design, Analysis"
---

# Shadow Study

Give it a height, a place, and a date, and it computes where the shadow falls.
The sun's position is geometry, worked out from formulas and shown step by
step. Everything about your site, and everything the jurisdiction demands, is
yours to supply.

## Scope and limits — read first

**What this does.** Computes solar declination, altitude, and azimuth for the
latitude, dates, and times you name, then shadow length and direction for each
massing height you give. If you supply the distance to a property line, an
open space, or a neighbor's window line, it reports whether the shadow reaches
it at each time, in a table you can run across massing options.

**What this does not do.**

- **It does not know your jurisdiction's shadow criteria.** Which hours matter,
  which parks or streets are protected, what counts as an adverse impact: that
  is zoning and design-guideline text, and it comes from you or the AHJ, never
  from memory. The skill computes geometry; you hold it against the rule.
- It assumes flat ground. Sloped sites, terraces, and shadows on facades
  rather than ground need the grades and geometry from you, or a 3D model.
- It ignores context: existing buildings, trees, and terrain that already
  shade the site are not in the arithmetic unless you put them there.
- **It is not a submission document.** A shadow study filed with an AHJ comes
  out of a 3D model with the site survey in it. This skill is for deciding
  between massing options before that model exists.
- It does not design the massing. Pair it with `test-massing` for the options
  and their heights.

**What you need before starting.** The place (a latitude, or a city to confirm
one against), the dates and local times that matter to you, the height of each
massing option, and, for an impact question, the distance and bearing from the
building face to the line you care about.

## Workflow

### Step 1. Establish place, time, and heights

Ask, in one message:

> 1. Where is the site? A latitude and longitude, or a city and the latitude
>    you want used. I will state the value I am computing with so you can
>    check it.
> 2. Which dates and local times? Solstices and equinox at morning, noon, and
>    afternoon are the usual set, but your jurisdiction or your question may
>    name others.
> 3. The time zone, and whether daylight saving applies on those dates.
> 4. The massing heights, per option, and the face each height belongs to.
> 5. Is there a line the shadow must not cross? If so, its distance and
>    direction from the building face.

Confirm the latitude and time zone back before computing. A shadow study run
in the wrong time zone is wrong by an hour of sun and looks fine.

### Step 2. Compute the sun position, showing the formulas

For each date and time, compute and print, with the formula named on each
line:

```
declination     <formula, then arithmetic>
hour angle      <from local solar time, arithmetic shown>
solar altitude  <formula, then arithmetic>
solar azimuth   <formula, then arithmetic>
```

These are the published astronomy relations, and they are the one thing this
skill supplies itself. State that plainly in the output, and state the
approximation: minute-level precision is not the point at massing stage, and
anyone needing better runs the model.

If the altitude comes out at or below zero, the sun is down at that time and
the row says so instead of printing a shadow length.

### Step 3. Compute the shadows

Per option, per time:

```
shadow length    = height / tan(altitude)     <arithmetic>
shadow direction = azimuth + 180 degrees      <stated as a bearing>
reach            <length compared to the distance you gave, if any>
```

Flat ground, stated on every run. If the user gave grades, apply them, showing
the arithmetic; if the geometry gets beyond a plane and a slope, say so and
stop rather than approximating silently.

### Step 4. Report

One table, options as rows or columns as fits:

| Option | Date, time | Altitude | Shadow length | Direction | Reaches your line? |
|---|---|---|---|---|---|

Then, in prose: which option casts the longest shadow at the times you named,
and where the differences between options actually show up. If a jurisdiction
criterion was supplied, state each option against it, quoting the criterion as
you gave it. If none was supplied, say that reach is geometry, not a verdict,
and the rule to hold it against is yours to bring.

Close every run with: flat ground assumed, context not modeled, and a
submission-grade study comes from a 3D model with the survey in it.

### Step 5. Save, if asked

Ask whether to write the study to a file and where. Write it directly,
including the formula lines. There is no template and no script.

## Rules

- **The solar formulas are the only thing this skill knows.** Every height,
  distance, grade, and criterion comes from you, and each carries its source
  in the output.
- Print the formula before the arithmetic, every time. A sun angle nobody can
  re-derive is not checkable.
- Confirm latitude and time zone back to the user before computing.
- A shadow reaching a line is a measurement. Whether that is a problem is the
  jurisdiction's rule, quoted from what you supplied, or stated as an open
  question.
- Never convert the user's units. Heights in, shadow lengths out, in the same
  unit.
- Say on every run that this is a massing-stage study, not a submission.

## Anti-patterns

- Recalling a city's shadow ordinance ("Toronto protects parks from
  10am to 4pm") instead of asking for the criterion. Named hours and protected
  places are zoning text and go stale; the user brings them.
- Silently assuming solar noon when the user said noon. Clock noon and solar
  noon differ, and the difference is part of the arithmetic to show.
- Printing a shadow length for a sun below the horizon.
- Modeling a sloped site as flat without saying so.
- Presenting the table as proof of no impact. It is geometry for a decision,
  not a finding for a filing.

## Resources

None. This skill is one file. Output is written directly at the path you
choose.
