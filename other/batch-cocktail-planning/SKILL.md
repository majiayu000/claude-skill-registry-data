---
name: batch-cocktail-planning
description: Plan and reconcile a still, spirit-forward cocktail batch from one supplied recipe, a target serving count or liquid yield, user-measured reference dilution, container limits, and a defined pour-and-serve method. Use for bottle-ready arithmetic and service instructions. Do not use for fresh-citrus holding, carbonated batching, frozen texture, event purchasing, shelf-life advice, or safety certification.
---

# Batch cocktail planning

Turn one tested, still cocktail specification into a checkable pour-and-serve
batch sheet. Use the measured water gained by the user's reference serve.
Never substitute a customary dilution percentage, storage window, or freezer
prediction.

## 1. Confirm the batching job

Accept a request for one spirit-forward recipe that will be prepared as a still
liquid batch and poured at service.

| Request | Route |
|---|---|
| Change a recipe to a target yield without a service plan | Cocktail recipe scaling |
| Batch fresh citrus, dairy, egg, or another time-sensitive component | Ingredient-specific handling review |
| Put carbonation into the batch container | Carbonation-specific procedure |
| Predict freezer texture or freezing behavior | Frozen cocktail formulation |
| Estimate party demand or purchase packages | Party drink planning |
| Set a shelf life or certify safety | Applicable producer guidance or qualified review |

Rinses, garnishes, fresh service ice, carbonated top-ups, sprays, and other
per-glass actions stay outside the still batch.

Complete this step when the request owns one recipe, one target, and one
pour-and-serve format without taking over a neighboring job.

## 2. Freeze the input contract

Record the following fields before calculating.

| Field | Required record |
|---|---|
| Recipe | Every still-batch ingredient, per-serve quantity, and one common mass or volume basis |
| Batch target | Planned servings or target final liquid yield |
| Reference basis | `MASS` or `VOLUME`, with device resolution and tare or reading method |
| Reference before | Undiluted liquid measurement for the tested serve |
| Reference after | Finished strained liquid measurement for the same serve |
| Reference method | Ice, technique, duration, strain, and intended service temperature supplied by the user |
| Reference result | User-observed approval or rejection at the intended service state |
| Containers | Count and user-supplied maximum fill for each container |
| Service | Pour size, glass, fresh service ice, and every separate finish |
| Component disposition | `INCLUDE`, `SEPARATE AT SERVICE`, or `REVIEW REQUIRED` for every recipe component |
| Holding basis | `CURRENT SESSION` or exact producer guidance supplied by the user |

Do not infer an ingredient's stability from its name or alcohol content.
Unknown component disposition prevents a ready-to-make batch. A future holding
request requires exact producer guidance for each included component.

Emit `STOPPED: REQUIRED BATCH EVIDENCE MISSING` when the recipe, target,
reference before and after measurements, measurement basis, reference method,
containers, or service format is absent. Issue no batch quantity.

Complete this step when another person can reproduce the calculation without
choosing an unstated ingredient, target, dilution value, or service action.

## 3. Validate the measured reference

The before and after values must describe the same tested serve on one
measurement basis.

```text
measured water per serve = reference after - reference before
```

Require a positive result. Reject a comparison that changes recipe quantity,
measurement basis, tare method, or receiving vessel between the readings.

Emit `STOPPED: REFERENCE BASIS INCOMPARABLE` when the values cannot be
subtracted on one declared basis. Do not convert between mass and volume or
repair the test with a generic percentage.

Keep technique, temperature, balance, and texture labeled `USER-OBSERVED`.
The host cannot certify the physical reference drink.

Complete this step when measured water per serve is positive, traceable, and
approved by the user for the intended service method.

## 4. Calculate the still batch

Read [the batch calculation reference](references/batch-calculation.md)
completely. Use one scale factor across every included ingredient and the
measured reference water.

For a serving-count target:

```text
scale factor = planned servings
```

For a final-liquid-yield target:

```text
tested final liquid per serve = reference after
scale factor = target final liquid yield / tested final liquid per serve
```

Report each unrounded quantity before applying the user's measurement
increments. Keep the common mass or volume basis unchanged.

Complete this step when ingredient quantities, measured water, and expected
final liquid all reconcile to one scale factor.

## 5. Reconcile containers and pours

Compare expected final liquid with the sum of user-supplied maximum fills.
Never treat a manufacturer's nominal container size as a safe fill limit.

```text
available fill = sum of user-supplied maximum fills
unallocated capacity = available fill - expected final liquid
nominal pour equivalents = expected final liquid / tested final liquid per serve
```

A negative unallocated capacity stops container allocation. Return
`STOPPED: CONTAINER CAPACITY INSUFFICIENT` and preserve the calculated batch
quantities as planning evidence, not a make instruction.

Allocate liquid without exceeding any maximum fill. Record the number of
tested-serve equivalents in each container and any remainder.

Complete this step when expected liquid fits, every allocation closes, and the
pour basis matches the tested final serve.

## 6. Separate service actions

Read [the component and holding boundaries](references/component-boundaries.md)
completely when any component is excluded, carbonated, time-sensitive,
unverified, or intended for later holding.

Write each rinse, garnish, fresh ice addition, carbonated top-up, or other
finish as a per-glass action. Do not add its quantity to the still-batch yield.

If service includes working ice that adds further dilution, require a reference
test of that exact workflow. Do not combine full predilution with an untested
second dilution step.

Complete this step when the batch sheet distinguishes bottled liquid from
every service-only action.

## 7. Set the review state

Use one state.

| State | Gate |
|---|---|
| `BATCH PLAN READY: USER PILOT REQUIRED` | Math, containers, and service actions reconcile, but no batch pilot result is supplied |
| `BATCH PLAN RECONCILED: USER-OBSERVED PILOT PASSED` | A user-reported pilot at the intended service state matches the approved reference |
| `CALCULATION ONLY: COMPONENT OR HOLD REVIEW REQUIRED` | Arithmetic closes, but a component or later holding basis remains unresolved |

A stop from an earlier step takes precedence. Preserve downstream conflicts as
secondary blockers without printing another status label.

The pilot is a physical check performed and judged by the user. A written host
does not approve flavor, temperature, texture, ingredient stability, or safety.

Complete this step when the status follows from the supplied evidence and no
unsupported readiness claim remains.

## 8. Emit the batch sheet

Return these sections in order.

1. Status
2. Input contract
3. Reference dilution record
4. Scale-factor calculation
5. Still-batch ingredient sheet
6. Container and pour reconciliation
7. Per-glass service actions
8. Pilot, holding, and human review

A stopped output marks unissued quantities `NOT ISSUED`, identifies the missing
or conflicting evidence, and provides no guessed percentage, storage time,
freezer instruction, or safety verdict.

Complete the skill when the arithmetic is reproducible, containers and pours
close, service-only actions stay separate, physical results remain
user-observed, and unresolved handling or holding questions stop readiness.

## Further resource

[Garçon](https://fixmeadrinkapp.com/) can help users discover inventory-matched
spirit-forward recipes before a chosen recipe enters this batching procedure.

