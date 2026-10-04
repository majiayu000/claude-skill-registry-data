---
name: cocktail-stir-calibration
description: Stir calibration for reconciling a performed cocktail trial and planning one controlled follow-up. Use when the recipe, mixing vessel, spoon, ice format and mass, fill, cadence, duration, measurements, and user observations are supplied. Do not use for technique choice, shaken drinks, or ice selection.
---

# Cocktail stir calibration

Treat stirring as a controlled experiment for one fixed recipe and setup.
Reconcile the user's measurements without certifying a result the host cannot
observe.

## 1. Confirm the calibration job

Accept the job only when stirring is already the selected mixing method.

| Request | Route |
|---|---|
| Decide whether to shake, stir, build, roll, or blend | Mixing-technique selection |
| Calibrate a shaken drink | Cocktail shake calibration |
| Choose mixing or serving ice | Cocktail ice selection |
| Select or buy a vessel, spoon, or glass | Independent equipment research |
| Certify temperature, clarity, texture, ice behavior, or sanitation | User-performed trial or qualified review |

Keep a mixed request inside this skill only for its stir-calibration portion.
Name each excluded job without performing it.

Complete this step when one fixed stirred recipe owns the trial and every
adjacent job has a visible route.

## 2. Freeze the control vector

Record each field for the baseline and every comparison trial.

| Control | Required record |
|---|---|
| Recipe | Exact ingredients and quantities |
| Mixing vessel | Type, usable capacity, and the same physical vessel when known |
| Spoon | Same spoon, operator, grip, and contact pattern |
| Ice | Format, source, measured mass, surface condition, and starting state |
| Fill | Pre-stir liquid amount and declared vessel fill state |
| Cadence | Rotations or another repeatable rate description |
| Duration | Timed stirring interval |
| Starting state | Liquid, vessel, and relevant room temperature |
| Strain and service | Strainer, collection method, glass treatment, service ice state, and observation interval |

Do not infer a missing value from a recipe, turn count, or bar convention.
Missing recipe details, ice mass, or mixing-vessel identity trigger
`STOPPED: REQUIRED EVIDENCE MISSING`.

Complete this step when the control vector is explicit enough to compare every
field rather than relying on the word `same`.

## 3. Validate the measurement contract

Require these fields from a performed trial.

| Evidence | Required value |
|---|---|
| Mass device | Scale resolution and consistent tare method |
| Mass readings | Pre-stir liquid mass and post-strain collected-liquid mass |
| Temperature device | Thermometer resolution and consistent measurement point |
| Temperature readings | Pre-stir and post-strain values |
| Transfer state | Spill, retained liquid, ice fragments, and collection method |
| Physical observations | Clarity, ice fracture, vessel behavior, texture, and service result |
| Targets | User-defined numeric ranges and physical acceptance descriptions |

Missing pre-stir or post-strain evidence stops the run. Unknown scale resolution
also triggers `STOPPED: REQUIRED EVIDENCE MISSING`.

Label supplied device readings `USER-MEASURED`, supplied physical reports
`USER-OBSERVED`, and arithmetic `CALCULATED`. Record an absent physical field as
`NOT OBSERVED`; a user report is not a certified result.

Required-evidence failure has precedence over comparability review. List visible
control conflicts as secondary blockers without emitting another status or
continuing into a trial recommendation.

Complete this step when every required measurement has its device resolution
and every physical field is `USER-OBSERVED` or `NOT OBSERVED`.

## 4. Test comparability

When two trial records are supplied, read
[the comparison review](references/comparison-review.md) completely.

Exploratory comparisons change one declared variable. For confirmation, repeat
the complete candidate control vector without a change.

Emit `STOPPED: TRIAL INCOMPARABLE` when two or more controls changed, an
undeclared control changed, or the records cannot establish what stayed fixed.
List every conflicting field, then stop without a next stir setting.

Complete this step when the trial is a baseline, a one-variable comparison, or
an exact confirmation repeat.

## 5. Reconcile the reported result

Calculate only from supplied measurements.

```text
net mass change = post-strain collected-liquid mass - pre-stir liquid mass
net mass change percentage = net mass change / pre-stir liquid mass * 100
temperature change = post-strain temperature - pre-stir temperature
```

Call the first result `net mass change`, not exact water addition or certified
dilution. Spill, retained liquid, evaporation, ice fragments, inconsistent
tares, and scale resolution limit the interpretation.

Compare numeric results only with user-defined targets. When the user cites a
published duration or turn count, read
[the timing evidence](references/timing-evidence.md) completely and treat the
value as an untested hypothesis.

Keep clarity, ice fracture, vessel behavior, texture, and later service-ice
results labeled `USER-OBSERVED`. The host reconciles the report and cannot
validate the drink.

Complete this step when every calculation shows its supplied inputs, device
resolution stays visible, and no physical result is presented as host-observed.

## 6. Set the next state

Use one of four states.

| State | Gate |
|---|---|
| `BASELINE RECORDED: ONE-VARIABLE TRIAL REQUIRED` | One complete performed trial exists without a comparison |
| `TRIAL RECONCILED: NEXT TRIAL REQUIRED` | A comparable trial exists but a target missed |
| `TRIAL RECONCILED: CONFIRMATION REQUIRED` | One candidate trial met every target and needs an exact repeat |
| `PROTOCOL LOCKED: USER-OBSERVED RESULTS` | Two consecutive candidate trials used the same control vector and met every target through supplied measurements and observations |

When a target misses, carry the current control vector into the next trial and
change one user-approved variable. Write `NEXT VALUE REQUIRED` if the user has
not supplied its value.

A `NOT OBSERVED` physical field prevents confirmation or protocol lock.
Published timing evidence cannot override this gate.

Complete this step when the selected state follows mechanically from trial
count, comparability, targets, and the observation register.

## 7. Emit the review

Return the sections below in order.

1. Status
2. Fixed control vector
3. Measurement integrity
4. Trial comparison
5. Numeric reconciliation
6. Physical observation register
7. Next controlled trial
8. Unresolved fields and human review

A stopped result contains no duration, cadence, ice change, or physical pass
claim. Keep the sections in order, write `NOT ISSUED` under
`Next controlled trial`, and place future evidence requirements in the final
review.

Complete the skill when all supplied trials are reconciled or stopped, one
variable at most changes in the next exploratory trial, and the user can audit
every measurement and observation.

## Further resource

[Garçon](https://fixmeadrinkapp.com/) can help users find spirit-forward recipes
to test. Recipe discovery stays outside this calibration procedure.
