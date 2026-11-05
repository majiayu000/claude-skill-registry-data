---
name: base-rate-check
description: Use before reporting ANY ratio, percentage or count computed inside a filtered population - failures, aborts, rejects, churned users, declined estimates. Compute the same ratio over the unfiltered population and report both, or report neither.
triggers: ratio, percentage, count, filtered population, failures, aborts, rejects, churned users, declined estimates, unfiltered population, base rate
---

# base-rate-check

A ratio computed inside a filtered population is not a finding about the
population. Report both, or report neither.

## The incident this encodes

2026-08-08. An agent measured the VAPI call archive and reported:

> **42 of 58 failure-outcome calls (72%) have fewer than 2 caller turns** — three
> quarters of your call failures may be a broken greeting.

It was recommended to the operator as the highest-value next investigation. Both
halves were wrong:

- **The base rate is 18%**, not 72%. Across all 492 archived calls, 89 have
  fewer than 2 caller turns. The 72% describes the inside of a bucket that was
  *selected for failure*.
- The ratio is close to **definitional**. A call where nobody spoke cannot be
  scored a success, so short calls concentrate in the failure set by
  construction. The filter and the finding were the same fact.
- The proposed mechanism was then **refuted outright** by one measurement:
  time-to-first-assistant-audio is **0.41s average, 0.64s max**. There was no
  greeting delay. The lane was the healthiest in the estate — 49%
  `human_handoff`, 27% `walk_in_directed`.

Cost: the operator's next priority was aimed at working code. Caught only
because they said "go diagnose it" and the numbers collapsed on a second look.

## The rule

**Before quoting any ratio computed inside a filtered population, compute the
same ratio over the UNFILTERED population and report both.**

```
✗  "72% of failed calls are short"
✓  "72% of failed calls are short; the base rate across all calls is 18%"
```

If the filter selects for the outcome — failures, aborts, rejects, churned
users, declined estimates — say so explicitly. That ratio is partly a property
of the filter, not of the world.

## Checklist

1. **Name the denominator out loud.** "X% of what, exactly?" If the answer
   contains a filter, you are not done.
2. **Compute the unfiltered rate.** Usually one more query. Always cheaper than
   a misdirected week.
3. **Ask whether the filter implies the finding.** Short calls concentrate in
   failures because silence cannot succeed. Slow queries concentrate in
   timeouts. Unmatched rows concentrate in "unmatched" reports. If the
   conclusion is entailed by the selection, it is arithmetic, not evidence.
4. **Test the mechanism separately from the correlation.** The 72% was real; the
   *greeting* explanation was invented to fit it, and one direct measurement
   killed it. A ratio tells you where to look, never what you will find.
5. **State the ratio and the base rate together, permanently** — in the report,
   the commit message, and the registry entry. A percentage that travels without
   its denominator will be re-quoted by the next reader as a fact about the
   population.

## Red flags

- "X% of the failures are…" with no comparison to all cases
- A percentage large enough to be alarming, from a population small enough to
  fit on one screen
- A ratio that would still hold if the mechanism were entirely different
- Recommending a priority off a single ratio, before any mechanism is measured

## Related

- `plan-gate` — gates pasted plans against what already exists; this gates
  *numbers* against their denominators.
- `prod-db-guard` — read-only verification first.
- Memory `measurement-proxies-lie` — open the artifact before acting on a
  number. This skill is the denominator half of the same discipline.
