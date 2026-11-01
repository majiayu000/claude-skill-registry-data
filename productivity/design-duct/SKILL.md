---
name: design-duct
description: "Sizes a duct segment from an airflow and the limits you set: area from the velocity limit you state, rectangular dimensions within your aspect ratio, the equivalent-diameter arithmetic between round and rectangular, and a pressure-drop tally over a run when you supply the loss values, every step shown. Trigger on \"duct size\", \"duct sizing\", \"duct velocity\", \"equivalent diameter\", \"static pressure\", \"cfm to duct size\", \"design-duct\", or a pasted airflow with a size question. Works in either unit system, as given. The user supplies the airflow, the velocity or friction-rate limit with where it came from, aspect ratio limits, and any fitting loss values, cited; the skill never supplies a velocity limit, a friction rate, or a loss coefficient from memory or from web search. Geometry and arithmetic only: fan selection, system effect, acoustics, and leakage class are the mechanical engineer's calls. Preliminary, never a substitute for the mechanical Engineer of Record."
license: MIT
metadata:
  title: "Design Duct"
  summary: "Size a duct run from the airflow and the limits you set"
  discipline: "structure-mep"
  tags: "Design, Analysis"
---

# Design Duct

Duct sizing at the preliminary stage is arithmetic between an airflow, a
velocity, and a cross-section. The arithmetic is the same everywhere. The
velocity you find acceptable, and the friction and loss values you design
to, are choices and table rows, so they come from you.

## Scope and limits — read first

**What this does.** Takes an airflow and the limit you set, computes the
required area, proposes rectangular dimensions within the aspect ratio you
allow or checks the ones you give, converts between round and rectangular
through the equivalent-diameter arithmetic, and tallies pressure drop over
a run when you supply the per-segment and per-fitting values. Every step
printed.

**What this does not do.**

- **It does not know any limits or coefficients.** No velocity limits, no
  friction rates, no fitting loss coefficients, no roughness values. Every
  one comes from you, cited to your standard, your office criteria, or your
  chart reading. That is the design, not a gap.
- **The friction-rate method needs your chart reading.** It will not
  reproduce a friction chart from memory; you read the chart or the table
  and supply the value, and the arithmetic continues from there.
- One segment or one run at a time, as you describe it. It does not lay out
  systems, balance branches, or apportion airflow between diffusers.
- It does not select fans, compute system effect, check acoustics or
  velocity-generated noise, or assign leakage class and sealing.
- It does not decide the airflow. That number arrives from your load or
  ventilation calculation (`design-ventilation` computes the outdoor-air
  part).
- No insulation, clearance, or fire and smoke damper requirements; those
  are code and coordination questions outside this arithmetic.

**What you need before starting.** The airflow, the limit you are sizing
to (velocity, or a friction rate with your chart reading), the aspect
ratio you will accept, and, for a pressure tally, the loss values per
segment and fitting.

## Workflow

### Step 1. Establish the basis

Ask, in one message:

> 1. Sizing to a velocity limit or a friction rate? State the value and
>    where it came from: standard, office criteria, or a chart you read.
> 2. Unit system, as your documents use it.
> 3. Round, rectangular, or flat oval? For rectangular, the aspect ratio
>    you will accept and any dimension caps from the ceiling space.
> 4. One segment, or a run you want tallied for pressure drop?

### Step 2. Collect the segment

Airflow with its source. For a run: each segment's length and airflow, and
each fitting named with the loss value you supply for it.

Anything unstated is missing. Never substitute a typical velocity or a
familiar coefficient.

### Step 3. Compute, showing every step

```
Segment <name>
  airflow                  <as given>  [source]
  limit                    <as given>  [cited]
  required area            A = Q / V   <arithmetic>
  trial size               <as given, or proposed within your caps>
  actual velocity          <arithmetic>  — vs limit: <pass/fail>
  equivalent diameter      <formula, then arithmetic>
```

For a pressure tally, per segment and fitting, each with its supplied loss
value cited, then the running sum. Any segment missing a loss value shows
`unverified` and the total names what it excludes.

### Step 4. Report

Sizes and velocities per segment, the tally if run, the unverified list
first, and the criteria you supplied printed at the top. Then:

> Every limit, rate, and coefficient here came from you. I did the
> arithmetic and supplied no values. This is preliminary sizing; the
> mechanical Engineer of Record designs the system.

### Step 5. Save, if asked

Ask whether to write the calculation to a file and where. Write it
directly, including the arithmetic. There is no template and no script.

## Rules

- **Never supply a velocity limit, a friction rate, or a loss
  coefficient.** There are none in this file.
- **Proposed dimensions stay inside the caps you gave**, and the aspect
  ratio is printed beside them.
- **Show the arithmetic**, including the equivalent-diameter steps; a
  converted size without its steps cannot be checked.
- **A pressure tally names every value it is missing** before it reports a
  total.
- **Stop on a missing value** rather than proceeding with a placeholder.
- Never convert unit systems on your own; mismatched inputs stop the
  segment.
- Say on every run that this is preliminary.

## Anti-patterns

- Recalling a comfortable velocity for an office supply duct. The limit is
  a design choice the user owns.
- Reading a friction chart from memory because the flow is common.
- Filling a fitting coefficient because the fitting is ordinary.
- Balancing a branch by adjusting airflows nobody stated.
- Rounding a computed dimension to a neat size without saying the velocity
  moved.

## Resources

None. This skill is one file. Output is written directly at the path you
name.
