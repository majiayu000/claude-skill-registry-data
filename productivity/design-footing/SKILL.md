---
name: design-footing
description: "Checks a single isolated spread footing: bearing pressure under your loads against the allowable bearing value your geotechnical report gives, with every step of the arithmetic shown. Trigger on \"footing size\", \"spread footing\", \"bearing pressure\", \"bearing check\", \"pad footing\", \"footing check\", \"design-footing\", or a pasted column load with a bearing value. Works with any standard. The user supplies the loads, the allowable or factored bearing resistance with its source, the load combinations, and a trial plan size; the skill never supplies a bearing value, a soil property, or a frost depth from memory or from web search. Plan size and bearing only: the footing's thickness, shear, and reinforcement are concrete design and stop the run. Preliminary sizing, never a substitute for the Engineer of Record or the geotechnical engineer."
license: MIT
metadata:
  title: "Design Footing"
  summary: "Check a spread footing against the bearing value your report gives"
  discipline: "structure-mep"
  tags: "Design, Analysis"
---

# Design Footing

Take a column load, a bearing value from the geotechnical report, and a trial
footing size, and show the arithmetic that says whether the soil is
overloaded. The arithmetic is the same everywhere. The bearing value is the
one number in the calculation nobody should ever recall, so it comes from
your report, cited.

## Scope and limits — read first

**What this does.** Combines your loads under your combinations, adds the
weights you tell it to carry, computes the bearing pressure under a trial
plan size, including the linear distribution when you give a moment, and
compares it against the bearing value you cite. Shows every step. If you have
no trial size, it rearranges the check and reports the required area instead
of naming dimensions from nowhere.

**What this does not do.**

- **It does not know any soil or material values.** No allowable bearing, no
  unit weights, no frost depth, no groundwater assumption. Every one comes
  from your geotechnical report or from you, cited. That is the design, not a
  gap.
- **It checks bearing and plan size only.** Thickness, one-way shear,
  punching shear, and reinforcement are concrete design and stop the run;
  that is the Engineer of Record's calculation.
- One isolated spread footing, concentric load or moment about one axis at a
  time. Combined footings, strap footings, mats, and piles stop the run.
- Eccentricity beyond the kern (e greater than B/6 under a linear
  distribution) stops the run rather than switching to a partial-contact
  model silently.
- It does not estimate settlement, and it does not judge whether the bearing
  stratum in the report matches the site.
- It does not check overturning, sliding, or uplift as a stability system;
  a retaining structure is a different calculation.

**What you need before starting.** The geotechnical report's bearing value
and what kind of value it is, your standard's load combinations, the loads,
and a trial plan size if you have one.

## Workflow

### Step 1. Establish the basis

Ask, in one message:

> 1. What bearing value does your report give, and is it allowable
>    (service-level) or a factored resistance? Quote the report line,
>    including any condition attached (minimum width, embedment, stratum).
> 2. Which load combinations apply for a bearing check under your standard,
>    written out?
> 3. Does the check include the footing self-weight and soil overburden, and
>    at what unit weights, from your report?

If the answer to 1 is unclear, stop. Comparing factored loads against an
allowable value, or service loads against a factored resistance, is wrong by
the size of the factors and looks fine on the page.

### Step 2. Collect geometry and loads

Column load by source, unfactored: dead, live, snow, others as your standard
separates them. A moment or a horizontal load at the base if there is one,
with its source. Trial plan dimensions, embedment depth, and the footing
thickness only as a weight, if you told it to carry weights.

Anything unstated is missing. Never substitute a typical value, and never
assume a load is zero because it was not mentioned.

### Step 3. Compute, showing every step

```
Loads
  <each load, as given, with units and source>
Combination used            <written out, cited>
  load at base              <arithmetic>
Weights carried             <each, arithmetic, or "excluded, per user">
Trial footing               <B x L, as given>
Eccentricity (if moment)
  e = M / P                 <arithmetic>
  kern check e vs B/6       <arithmetic, stop if outside>
Bearing pressure
  q = P/A                   <arithmetic>
  q max, q min (if moment)  <formula, then arithmetic>
Bearing value               <as quoted, cited, with its conditions>
Ratio                       <q / value>
```

Every input line carries where it came from. If any input is unverified, the
result for that line reads `unverified`, not a number.

### Step 4. If no trial size was given

Rearrange: required area = load / bearing value, and say plainly that you
should pick plan dimensions that provide it, check the report's conditions
still hold at that size, and come back. Do not name dimensions.

### Step 5. Report

The governing pressure, the ratio, the report conditions restated next to
the result, and the list of anything unverified. Then:

> Every load, weight, and bearing value here came from you and your
> geotechnical report. I did the arithmetic and supplied no values. This is
> a preliminary bearing check of the plan size only; the Engineer of Record
> designs the footing.

### Step 6. Save, if asked

Ask whether to write the calculation to a file and where. Write it directly,
including the arithmetic. There is no template and no script.

## Rules

- **Never supply a bearing value, a unit weight, or a frost depth.** There
  are none in this file.
- **Confirm allowable versus factored before anything else**, and never mix
  the two.
- **Restate the report's conditions** (minimum width, embedment, stratum)
  beside every result; a bearing value stripped of its conditions is a
  different number.
- **Stop at the kern** rather than switching pressure models silently.
- **Show the arithmetic.** Stop on a missing value rather than proceeding
  with a placeholder.
- Never convert units, and never round an input to a neater figure.
- Say on every run that this is preliminary and not a design.

## Anti-patterns

- Recalling a "typical" allowable bearing for sand or clay. That is the one
  number this check exists to take from the report and nowhere else.
- Assuming frost depth or embedment from the project's location.
- Continuing past e > B/6 with a partial-contact distribution nobody asked
  for.
- Sizing the thickness or the rebar because the plan size passed.
- Treating a bearing value as unconditional when the report tied it to a
  width or a stratum.

## Resources

None. This skill is one file. Output is written directly at the path you
name.
