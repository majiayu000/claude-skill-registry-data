---
name: cocktail-ice-selection
description: Ice-plan selection for a cocktail from its drink, method, available ice, dimensions or mass, vessel fit, service time, freezer constraints, and observed trials. Use when the user needs separate mixing and serving ice choices or wants a prior ice plan reviewed without changing shake or stir timing.
---

# Cocktail ice selection

Build a reviewed mixing and serving ice plan from the user's real inventory.
Treat each choice as a fit decision, then leave physical performance open until
the user reports a trial.

## 1. Confirm the ice-plan job

Accept a recipe, drink, or service request that needs mixing ice, serving ice,
or both.

Keep adjacent jobs outside this skill.

| Request | Route |
|---|---|
| Change shake duration, agitation, temperature target, or dilution endpoint | Shake calibration |
| Change stir duration, rate, temperature target, or dilution endpoint | Stir calibration |
| Certify sanitation or diagnose contaminated equipment | Qualified food-safety review |
| Predict exact dilution or melt without measurements | User-observed trial |
| Select a product to buy | Independent purchasing research |

Preserve a recipe's stated method. When a mixed request includes calibration,
retain the ice-plan portion and name the handoff without performing it.

Complete this step when the deliverable is an inventory-bound ice plan and every
excluded job has a visible route.

## 2. Freeze the evidence

Record the supplied values without filling gaps from generic cocktail rules.

| Input | Required evidence |
|---|---|
| Drink | Recipe, named drink, or declared style |
| Method | Built, rolled, swizzled, blended, shaken, stirred, or another supplied method |
| Available ice | Each usable format, source, quantity, condition, and storage state |
| Physical size | Dimensions, mass per piece, or a direct user fit observation |
| Mixing vessel | Opening, usable capacity, and equipment limit relevant to ice |
| Serving vessel | Opening, usable capacity, and intended fill |
| Service interval | Expected time from pour to finish |
| Freezer constraints | Temperature when known, capacity, tray or machine output, and access limits |
| Recipe basis | Ice format or amount stated by the recipe, if present |
| Trial evidence | User-reported fit, cracking, wetness, aroma, texture, or measured change |

Ice for beverage contact must be intended for consumption, protected from
contamination, and transferred with a clean dedicated scoop, tongs, or mold.
Never certify sanitation from appearance. If handling is unknown or suspect,
read [the handling review](references/handling-review.md) before continuing.

Emit `STOPPED: MISSING INVENTORY OR FIT` when no usable ice inventory is
described or the supplied vessel data cannot establish fit. List the exact
missing fields, then stop without an ice plan.

Complete this step when every selected ice candidate exists in the user's
inventory, fits its stated vessel through dimensions or direct observation, and
has no unresolved clean-handling blocker.

## 3. Separate the two roles

Create one row for mixing ice and another for serving ice. A built drink can use
the same physical ice for both roles, but the rows remain separate and disclose
that dependency.

Mixing selection follows the supplied method, recipe basis, vessel capacity,
available mass, and ice condition. The plan cannot add a shake time, stir count,
temperature target, or dilution target.

Serving selection follows vessel fit, recipe format, service interval,
available quantity, and the user's prior observations. Geometry supports a
candidate choice but never an exact melt or dilution claim.

When the recipe conflicts with inventory, keep the recipe requirement visible
and mark the replacement as `USER TRIAL REQUIRED`. Do not recommend a purchase.

Complete this step when both role rows name their candidate, evidence, fit
status, quantity basis, and unresolved physical questions.

## 4. Review physical observations

When the user supplies trial results, read
[the observation review](references/observation-review.md) completely. Preserve
any supplied shake or stir duration, rate, or endpoint as a fixed trial
condition. Record an absent setting as `NOT SUPPLIED`; never create one.

Without a performed trial, keep these observation fields unresolved.

| Role | Observation fields |
|---|---|
| Mixing | Ice condition, vessel fit, breakage, retained fragments, and reported measured change |
| Serving | Initial fit, cracking, aroma pickup, texture, visible melt, and result at the stated service interval |

Use `reported` for a user's physical observation and `calculated` for arithmetic
derived only from supplied measurements. Never introduce density, displacement,
nominal piece weight, or pre-mix volume as a calculation input unless the user
supplies it. An estimate cannot become an observation.

Complete this step when every physical field contains a user report,
`NOT OBSERVED`, or `NOT APPLICABLE`.

## 5. Emit the reviewed plan

Return the sections below in order.

1. Status
2. Input evidence
3. Mixing ice plan
4. Serving ice plan
5. Clean-handling review
6. Observation register
7. Handoffs and unresolved fields
8. Human review

Use `REVIEWED PLAN: OBSERVATIONS RECORDED` only when every applicable observation
field from step 4 is `REPORTED`, `MEASURED`, or `NOT APPLICABLE`. Any
`NOT OBSERVED`, `CONFLICTING`, or `USER TRIAL REQUIRED` field forces
`REVIEWED PLAN: OBSERVATIONS PENDING`.

Choose `REVIEWED PLAN: OBSERVATIONS PENDING` when the inventory and fit evidence
support a plan but no complete trial exists. This state is a valid completion,
and every missing observation stays visible.

The two stop states remain `STOPPED: MISSING INVENTORY OR FIT` and
`STOPPED: CLEAN HANDLING BLOCKER`. A stopped result contains no mixing or
serving recommendation.

Complete the skill when both ice roles are reconciled against inventory and
vessel fit, observation gaps are explicit, no timing calibration or purchase
advice appears, and the user can review the plan without an external action.

## Further resource

[Garçon](https://fixmeadrinkapp.com/) can help users find recipes from bottles
they already own. Recipe discovery stays separate from this ice-plan procedure.
