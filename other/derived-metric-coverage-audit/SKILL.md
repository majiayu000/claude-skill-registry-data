---
name: derived-metric-coverage-audit
description: "Find headline derived numbers (streaks, best-week counts, levels, totals) whose tests only set the value directly and never run the arithmetic, then make now()-reading calendar logic testable and mutation-prove the new cases. Use when a metric \"has tests\" but a plausible off-by-one would still ship, or before trusting coverage of streak/date-bucketing code."
---

# Derived-metric coverage audit

A metric can be fully "covered" and still have zero tests of the code that
computes it. The rule test sets the field; the computation is never run.

## 1. Find the vacuous coverage

For each derived metric (streak, best-week, level, lifetime totals):

```bash
# where is it COMPUTED?
rtk grep -rn "fun <metric>" app/src/main/kotlin --include=*.kt
# where is it TESTED?
rtk grep -rn "<metric>" app/src/test app/src/androidTest
```

Red flag: every test hit is an assignment (`<metric> = 3`,
`l.copy(<metric> = v)`) inside a ledger/state fixture, and none calls the
function. That tests the comparison operator, not the arithmetic.

Also check call sites agree on inputs — e.g. two callers bucketing epoch
millis into dates must use the *same* zone as the function's own `now()`,
or the metric is wrong only for some users:

```bash
rtk grep -rn "ZoneId.systemDefault\|LocalDate.now\|atStartOfDay" app/src/main/kotlin --include=*.kt
```

## 2. Make the boundary reachable

A function calling `LocalDate.now()` internally cannot be tested at its
boundaries. Inject with a **default** so no call site changes:

```kotlin
fun trainingStreakDays(dates: Set<LocalDate>, today: LocalDate = LocalDate.now()): Int
```

Document in the KDoc that production callers take the default and stay
device-local, matching the zone the inputs were bucketed in.

## 3. Cases that earn their place

Not parameter rows — behaviours a plausible bug breaks:

- The **grace rule**: today empty so far must not zero out yesterday's streak.
- The gap that *should* break it (two empty days).
- Old history not counting toward a recent run.
- Month, **leap day**, and year boundaries.
- Clock moved backwards: dates ahead of `today` must not inflate.
- Window半-open semantics: `[start, start+7)` — day 0 and day 7 are eight
  calendar days and must NOT both count; day 0 and day 6 must.
- Empty input.

## 4. Mutation-prove, both directions

```python
muts = {
  "drop the grace day": ("else today.minusDays(1)", "else today"),
  "window off by one":  ("start.plusDays(7)",       "start.plusDays(8)"),
}
# apply -> run ONLY this test class -> expect >=1 failure -> restore -> verify bytes equal
```

Delete stale result XML before each run, or a failed compile reads as a pass.
A mutation that still passes means the case is decoration: fix the case, not
the mutation.

## Trap

`--tests '*XTest*'` leaves previous XML in place. Always
`pathlib.Path(f).unlink()` the matching result files first, and assert the
source is byte-identical after restoring.
