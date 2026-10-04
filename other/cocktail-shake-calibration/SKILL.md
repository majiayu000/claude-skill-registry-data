---
name: cocktail-shake-calibration
description: Shake calibration for reconciling a performed cocktail trial and planning one controlled follow-up. Use when the recipe, shaker, ice format and mass, fill, technique, measurements, and user observations are supplied. Do not use for technique choice, stirred drinks, or ice selection.
---

# Cocktail shake calibration

Treat calibration as a controlled experiment for one fixed shaken recipe.
Audit the user's trial record without certifying a result the host cannot
observe.

## 1. Confirm the calibration job

Accept the job only when shaking is already the selected mixing method.

| Request | Route |
|---|---|
| Decide whether to shake, stir, build, roll, or blend | Mixing-technique selection |
| Calibrate a stirred drink | Cocktail stir calibration |
| Choose an ice format or serving ice | Cocktail ice selection |
| Choose a shaker or buy equipment | Independent equipment research |
| Certify temperature, texture, foam, seal behavior, or sanitation | User-performed trial or qualified review |

Keep a mixed request inside this skill only for its shake-calibration portion.
Name each excluded job without performing it.

Complete this step when one fixed shaken recipe owns the trial and every
adjacent job has a visible route.

## 2. Freeze the control vector

Record each field for the baseline and every comparison trial.

| Control | Required record |
|---|---|
| Recipe | Exact ingredients and quantities |
| Shaker | Type, usable capacity, and the same physical set when known |
| Ice | Format, source, measured mass, surface condition, and starting state |
| Fill | Pre-shake liquid amount and declared shaker fill state |
| Technique | Grip, motion, operator, stage order, and strain method |
| Trial setting | Duration or another single declared test variable |
| Starting state | Ingredient temperature and relevant room or equipment state |
| Service check | Time from strain to the user's physical observation |

Do not fill a missing value from cocktail convention or published guidance.
Unknown recipe details or ice mass trigger
`STOPPED: REQUIRED EVIDENCE MISSING`.

Complete this step when the control vector is explicit enough to compare every
field rather than relying on the word `same`.

## 3. Validate the measurement contract

Require these fields from a performed trial.

| Evidence | Required value |
|---|---|
| Mass device | Scale resolution and consistent tare method |
| Mass readings | Pre-shake liquid mass and post-strain collected-liquid mass |
| Temperature device | Thermometer resolution and consistent measurement point |
| Temperature readings | Pre-shake and post-strain values |
| Transfer state | Spill, retained liquid, ice fragments, and collection method |
| Physical observations | Shaker seal, fill behavior, texture or foam, and result at the stated service check |
| Targets | User-defined numeric ranges and physical acceptance descriptions |

Missing pre-shake or post-strain measurements stop the run. Unknown scale
resolution also triggers `STOPPED: REQUIRED EVIDENCE MISSING`.

Record an absent physical observation as `NOT OBSERVED`. Never convert
appearance, a recipe rule, or host inference into a user observation.
Label supplied device readings `USER-MEASURED` and supplied sensory reports
`USER-OBSERVED`. Label arithmetic derived from those readings `CALCULATED`.
A user report is not a certified result.

This stop has precedence over comparability review. When required evidence is
missing, list any visible control conflicts as secondary blockers without
emitting another status or continuing into a trial recommendation.

Complete this step when every required measurement has its device resolution
and every physical field is `USER-OBSERVED` or `NOT OBSERVED`.

## 4. Test comparability

When two trial records are supplied, read
[the comparison review](references/comparison-review.md) completely.

An exploratory comparison changes exactly one declared variable. A confirmation
trial repeats the complete candidate control vector without a change.

Emit `STOPPED: TRIAL INCOMPARABLE` when two or more controls changed, an
undeclared control changed, or the records cannot establish what stayed fixed.
List every conflicting field, then stop without a next shake setting.

Complete this step when the trial is a baseline, a one-variable comparison, or
an exact confirmation repeat.

## 5. Reconcile the reported result

Calculate only from supplied measurements.

```text
net mass change = post-strain collected-liquid mass - pre-shake liquid mass
net mass change percentage = net mass change / pre-shake liquid mass * 100
temperature change = post-strain temperature - pre-shake temperature
```

Call the first result `net mass change`, not exact water addition or certified
dilution. Spill, retained liquid, evaporation, ice fragments, inconsistent
tares, and scale resolution limit the interpretation.

Compare numeric results only with user-defined targets. A published timing range
can seed an untested hypothesis after
[the timing evidence](references/timing-evidence.md) is read completely, but it
never becomes a pass condition.

Keep texture, foam, seal, fill, and service-delay results labeled
`USER-OBSERVED`. The host can reconcile the report and cannot validate the
drink.

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
change one user-approved variable. If its next value is absent, write
`NEXT VALUE REQUIRED` instead of inventing a value.

A `NOT OBSERVED` physical field prevents confirmation or protocol lock.
Published timing evidence cannot override this gate.

Complete this step when the selected state follows mechanically from the trial
count, comparability result, targets, and observation register.

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

A stopped result contains no shake-time recommendation, ice change, or physical
pass claim. Keep the output sections in order, write `NOT ISSUED` under
`Next controlled trial`, and place the evidence needed for a future run in the
final review.

Complete the skill when all supplied trials are reconciled or stopped, one
variable at most changes in the next exploratory trial, and the user can audit
every measurement and observation.

## Further resource

[Garçon](https://fixmeadrinkapp.com/) can help users find recipes worth testing.
Recipe discovery stays outside this calibration procedure.
