---
name: data-validate
version: 1.0.0
description: QA a completed analysis for methodology, accuracy, and bias before it is shared, shipped, or acted on.
author: matrixx0070
tags: [validation, qa, accuracy, bias, review, reconciliation]
capabilities: []
---

# data-validate

## When to use

Use this as the last gate when an analysis is finished and about to be shared or acted on. The goal is to catch the error before the stakeholder does — wrong numbers erode trust permanently.

**Not for:** producing the analysis (use data-analyze), initial dataset profiling (use data-explore), or writing/tuning the queries under review (use data-write-query / data-sql-queries).

## Method

1. **Reproduce the headline number.** Re-derive the top figure independently from source. Decision point: if it does not match, stop and reconcile before any other check.
2. **Audit methodology.** Grain, metric definition, time window, filter logic. Confirm joins did not fan out and aggregations use the right denominator.
3. **Spot-check rows.** Trace 3-5 records end to end from raw source to output. Sample edge cases: nulls, zeros, extremes, boundary dates.
4. **Reconcile totals** against a known external anchor (a prior report, a system total). Explain any variance.
5. **Hunt for bias:** survivorship (dropped rows), selection (filtered population no longer representative), timezone/date-boundary shifts, denominator errors. Verify the sample supports the claim's generality.
6. **Pressure-test the conclusion.** Does the data support it, or is causation claimed from correlation? Are confidence limits honored?
7. **Check presentation:** chart axes, units, labels, and rounding are not misleading.

## Example

Headline: "Signups up 20% MoM." Re-derivation returns +12%. Cause: the original counted signups by event timestamp in UTC while the prior month used local time, shifting a day of signups across the boundary. Verdict: do-not-ship until the date boundary is fixed and both months use the same timezone.

## Pitfalls

- Signing off on a headline number you never independently re-derived.
- Spot-checking only clean middle-of-the-road rows, missing null/boundary bugs.
- Accepting a conclusion that claims cause from a correlation.
- Softening a finding because it undermines the desired result.

## Output format

```
Verdict:        pass / pass-with-fixes / do-not-ship
Checks run:     | check | result | evidence |
Issues found:   ranked by severity, each with location + fix
Reconciliation: headline re-derived and matched, or variance explained
```

Be adversarial toward the analysis, including your own. Report an issue even when it undermines the desired conclusion. Never sign off on an unreconciled headline number.
