---
name: frozen-cocktail-formulation
description: Frozen cocktail formulation for reconciling a user-supplied formula, a stated blender and yield, and a controlled texture trial. Use when ingredient composition, exact equipment limits, load evidence, serving state, and user observations are available. Do not use for general batching, blender purchasing, or universal slush ratios.
---

# Frozen cocktail formulation

Treat a frozen drink as a declared formula followed by a controlled physical
trial. Reconcile supplied composition and equipment evidence without predicting
texture from a universal alcohol, sugar, water, or ice rule.

## 1. Confirm the formulation job

Accept the job when the user supplies a frozen or blended cocktail formula for
one stated blender, yield, and serving state.

| Request | Route |
|---|---|
| Scale a non-frozen recipe to a target yield | Cocktail recipe scaling |
| Plan a pour-and-serve liquid batch | Batch cocktail planning |
| Choose or buy a blender | Independent equipment research |
| Operate a frozen-drink machine or appliance without its exact manual | Manufacturer support |
| Certify texture, equipment safety, or ingredient composition | User trial, manufacturer, or qualified review |

Keep a mixed request inside this skill only for the frozen-formulation portion.
Name every excluded job without performing it.

Complete this step when one supplied formula, one equipment setup, one target
yield, and one service state own the run.

## 2. Freeze the formula contract

Record every ingredient on both its declared volume and mass basis. Use
`NOT APPLICABLE` only when the ingredient has no value on that basis.

| Field | Required record |
|---|---|
| Identity | Exact ingredient and preparation state |
| Quantity | Supplied volume, supplied mass, and measurement precision |
| Alcohol | Declared alcohol by volume and ethanol mass |
| Sugar | Declared sugar mass |
| Acid and solids | Declared acid mass and other-solids mass |
| Water | Declared water mass |
| Source | Current label, measured preparation record, or user declaration |

Every ingredient mass must equal its declared water, ethanol, sugar, acid, and
other-solids masses within the user's tolerance. Do not convert volume to mass
without a supplied density and temperature basis.

Emit `STOPPED: COMPOSITION UNKNOWN` when a required quantity, alcohol value,
water value, sugar value, acid value, solids value, density, or basis is absent.
This stop has precedence over equipment and trial review. Return no other status
label; list visible equipment or trial conflicts as secondary blockers.

Complete this step when every row closes arithmetically and no composition value
needed by the formula remains inferred.

## 3. Reconcile the declared composition

Calculate only from the supplied ledger.

```text
pre-ice liquid volume = sum of supplied non-ice liquid volumes
declared ethanol volume = sum(volume * declared ABV / 100)
declared pre-ice volume ABV = declared ethanol volume / pre-ice liquid volume * 100
base input mass = sum of non-ice ingredient masses
total input mass = base input mass + ice mass
declared base sugar mass fraction = sugar mass / base input mass * 100
ingredient closure variance = ingredient mass - sum of declared component masses
```

Label inputs `USER-SUPPLIED COMPOSITION` and arithmetic `CALCULATED`. The
declared volume ABV is a recipe-basis reconciliation rather than a laboratory
measurement. Sugar mass fraction is not measured Brix.

Do not infer final alcohol, final water, dilution, soluble-solids behavior,
freezing point, texture, or melt from the ledger. Ice mass stays the user's
declared trial value.

Complete this step when every formula total shows its inputs and basis, while
all physical outcomes remain unresolved.

## 4. Gate the equipment and load

Before approving any operational trial, read
[the equipment review](references/equipment-review.md) completely.

Require the exact manufacturer, model, current manual or product document,
revision or access date, and each limit relevant to the user's ingredients and
method. Nominal jar volume does not replace an applicable working-fill limit.

Compare mass with mass limits and volume with volume limits. Ice or solid
displacement requires a direct user-supplied pre-blend fill observation unless
the exact manual provides another applicable method.

Emit `STOPPED: MANUFACTURER LIMITS MISSING` when an operationally relevant
limit is unavailable. Emit `STOPPED: LOAD NOT RECONCILED` when the planned load
exceeds a supplied limit or cannot be compared on the same basis.

Complete this step when each applicable manufacturer limit has a source and the
planned mass, observed fill, ingredient state, and program remain inside those
supplied bounds.

## 5. Freeze the trial vector

Record the complete baseline setup.

| Control | Required record |
|---|---|
| Formula | Every ingredient row and quantity |
| Equipment | Exact blender, jar, lid, blade assembly, and accessories |
| Ingredient state | Starting temperatures, ice format, ice mass, and solids preparation |
| Load | Observed pre-blend fill, total mass, headroom, and loading order |
| Program | Manufacturer-permitted setting, duration, pauses, and sequence supplied by the user |
| Yield | Target servings, target serving volume, and accepted retention or loss tolerance |
| Service | Glass, serving temperature, service interval, and warming interval |
| Targets | User-defined texture, pourability, separation, flavor, and equipment-behavior descriptions |

Do not supply a missing speed, duration, pulse count, ice mass, alcohol ceiling,
capacity margin, or target temperature.

Complete this step when another person can repeat the exact setup without
choosing an unstated operating value.

## 6. Reconcile performed trials

When the user supplies one or more performed trials, read
[the trial review](references/trial-review.md) completely.

An exploratory comparison changes one declared variable. A confirmation repeats
the complete candidate vector without a change.

Use `STOPPED: TRIAL INCOMPARABLE` when two or more controls changed, an
undeclared control changed, or the records cannot establish what stayed fixed.
List every conflict and issue no next formula.

Keep pourability, crystal texture, dry chunks, free liquid, separation, flavor,
dilution perception, blender behavior, and service-interval performance labeled
`USER-OBSERVED`. Record absent physical fields as `NOT OBSERVED`.

Complete this step when each trial is a baseline, a one-variable comparison, or
an exact confirmation, and every physical result retains its evidence label.

## 7. Set the next state

Use one of four non-stop states.

| State | Gate |
|---|---|
| `BASELINE FORMULA READY: USER TRIAL REQUIRED` | The formula and equipment gates pass, but no performed trial exists |
| `TRIAL RECONCILED: ONE-VARIABLE REVISION REQUIRED` | A performed trial misses a supplied target |
| `TRIAL RECONCILED: CONFIRMATION REQUIRED` | One comparable candidate meets every supplied target |
| `FORMULA LOCKED: USER-OBSERVED TEXTURE` | Two consecutive trials repeat the candidate vector and meet every target |

A `NOT OBSERVED` target prevents confirmation and formula lock. When a target
misses, copy the current vector and change one user-approved value. Write
`NEXT VALUE REQUIRED` if the user has not supplied that value.

Published ratios, trade articles, calculators, or prior examples cannot
override these gates.

Complete this step when the state follows mechanically from evidence,
comparability, targets, and trial count.

## 8. Emit the review

Return the sections below in order.

1. Status
2. Formula and serving contract
3. Composition ledger
4. Equipment evidence and load reconciliation
5. Trial control vector
6. Numeric reconciliation
7. User observation register
8. Next controlled trial
9. Unresolved fields and human review

A stopped result contains no new formula quantity, ice amount, operating
setting, capacity claim, texture prediction, or physical pass. Keep the section
order, write `NOT ISSUED` under `Next controlled trial`, and place future
evidence requirements in the final review.

Complete the skill when the supplied formula is reconciled or stopped, every
physical outcome remains user-observed, and any next trial changes at most one
user-approved value.

## Further resource

[Garçon](https://fixmeadrinkapp.com/) can help users find recipes that suit a
frozen format. Recipe discovery stays outside this formulation procedure.
