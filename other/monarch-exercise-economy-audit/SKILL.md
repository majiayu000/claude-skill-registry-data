---
name: monarch-exercise-economy-audit
description: "Use when adding, renaming or re-tiering a movement in the Ironvellum (formerly Monarch, D:/Monarch) exercise catalogue, changing an XP constant there, or when a movement scores wrongly: holds or attempts counted as reps, NEW PR on every climbing set, a classification key that names nothing."
---

# Ironvellum exercise economy audit

Project `D:/Monarch` (Ironvellum, formerly Monarch). The catalogue is hand-edited
data, so it fails **silently** (generic invariants: `hand-edited-catalogue-invariants`).
This skill holds the app's scoring model and the traps it has hit. The change
procedure is `score-economy-rework-safety`; a whole-economy payout audit is
`game-economy-ground-truth-audit`.

## The model (read these five, they are small)

| file | role |
|---|---|
| `data/Seed.kt` | `allExercises` = `baseExercises` + every `Skills.ALL` movement not already there + `activities`. `withMetric()` stamps `HOLD` from the map — a hold must be **recognised**, never given an explicit metric in its row |
| `domain/MovementDifficulty.kt` | tier: `loadPricedTiers` → skill tree → `catalogueTiers` → `DEFAULT_TIER = 2`. `intensity() = 2^(tier-1)` |
| `domain/Xp.kt` | `effortUnits = taperedVolume(reps or seconds/5) * intensity * loadMultiplier * modifierFactor` |
| `domain/Skills.kt` | tree data; `metric` and `target` are **inferred from the standard's prose** |
| `domain/StrengthIndex.kt` | body-scaled; applies XP's `taperedVolume` and a sqrt-damped `MovementDifficulty.strengthWeight`, so cheap volume cannot farm the leaderboard's lifetime sum |

`val ExerciseMetric.isStrength` (`Models.kt:26-27`) is the existing REPS/HOLD vs
activity predicate. Reuse it; never write a second one.

## Pricing rule for any new movement (settles most tier arguments)

**A tier states UNLOADED difficulty only.** `Xp.loadMultiplier` already pays for
the kilos, so a tier that prices the load pays for the plate twice (the load
double-count trap in `score-economy-rework-safety`). `loadPricedTiers` scores
loaded names as their unloaded parent: `weighted pull-up` and `weighted dip` at
3, and rungs II-V of the Squat, Bench, Press and Deadlift ladders at 1, their
line root. Back Squat, Bench Press, Overhead Press and Deadlift are tier I
skill-tree rows; isolation is tier 1 (`bicep curl`, `wrist curl`).

Leaving a new movement unclassified is not neutral: it falls to
`DEFAULT_TIER = 2`, intensity 2, double a tier-I barbell root. Classify it
explicitly; `isClassified` backs the test that holds the seeded catalogue to full
coverage. (verified 2026-09-24)

## Audit axes that actually find bugs

1. **Reverse classification direction.** The forward test ("every seeded
   movement is classified") cannot see a key that names *nothing*. `"plank"` was
   priced tier 1 and marked a hold for months while only `Weighted Plank` was
   seeded. Walk the public `catalogueOnlyKeys` accessor back to the catalogue;
   keep the maps `private` rather than reflecting or widening them.
2. **Forward test's own blind spot:** it filtered `metric == REPS.name`, so an
   unclassified **HOLD** passed. Filter on `isStrength`.
3. **Prose-inferred metrics.** `Skills` infers metric/target from the standard
   text. Minute-denominated standards broke it: *"Hold 3 minutes"* → SECONDS
   target **3**; *"10-minute routine"* → REPS target **10**. Fix the inference,
   not the strings. `minute` and `metre` are one regex slip apart — pin
   `Handstand Walk` ("10 metres unbroken") as METRES in the same test.
4. **Activity metrics scored as reps.** An ATTEMPTS_GRADE set carries its
   *attempt count* in the `reps` column. `SetRecords`, `ExerciseHistoryCalculator`
   and `SessionScreen`'s block-strength sum all branched only on hold-vs-not, so
   seven boulder attempts minted a seven-bodyweight-rep PR.
5. **Progression gates.** The bypass was HOLD-only, so a `DISTANCE_TIME` preset
   entry was told to hit N reps and add 2.5 kg.

## The regression that follows fix 4 — do not ship without it

`SetRecords.delta` returns `isRecord = true` when **no record exists**
(`SetRecords.kt:~120`). Excluding activity sets from records therefore makes
every climbing set read **NEW PR** forever. Plumb a `scoresStrength` flag to the
set row and gate both the badge and the block strength line.

## Two claims to distrust

- *"Every prerequisite tier is strictly below its dependent."* **False.** A tier
  is a difficulty **band** holding ordered chains — Muscle-up (III) requires
  Pull-up (III); ~12 such pairs. The true invariant is *never **harder***.
  Acyclicity already stops a band chain closing on itself.
- *"`isWeighted` contradicts the presets."* It is **UI-only** — the picker's
  equipment facet and labels (`ExercisePicker.kt:295`,
  `ExerciseExplorerScreen.kt:196`); no scoring code reads it. A +10 kg pull-up is
  genuinely bodyweight-with-added-load. Not a defect.

## Wiring a new row touches

- `Repository.ensureSeeded` inserts by **exact** name every launch, so upgrades
  pick rows up; a lifter's same-named custom row is kept (merge, not duplicate),
  and classification is case-insensitive so it still gets the right tier.
- `Progression.weightStepKg` is substring/muscleGroup heuristics, **no** per-name
  table — new movements inherit sensibly.
- `TitleEngine` hard-codes **category strings** (`"Cardio"`, `"Water"`, `"Sport"`),
  never movement names. Adding is safe; **renaming** breaks skill badge, hold
  detection and tier, which all key on the display name.

## Verification

Mutation-prove every invariant (break the real data once, confirm the *matching*
test fires; commit first and revert as `score-economy-rework-safety` says). Then
on the emulator — never the owner's phone, where logged sets bank XP that is
never restated — with a bodyweight logged (without one the badge path is null
and the check is vacuous), log an activity set **and a lifting set in the same
session**. Expect the lifting one to show `N STR` and `NEW PR` and the activity
one to show neither. Without that control, "no badge" only proves badges are
broken.

Pin every Gradle run to the emulator from Git Bash:
`ANDROID_SERIAL=emulator-5554 ./gradlew.bat <task>` (see `monarch-session-context`).
