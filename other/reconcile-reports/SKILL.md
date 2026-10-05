---
name: reconcile-reports
description: Explain why two or more reports, spreadsheets, or metric totals disagree by aligning definitions and quantifying the difference. Use for reconciliation of existing results, not general data cleaning or choosing new KPIs.
---

# Reconcile reports

Produce an inspectable explanation of the disagreement. Preserve the distinction between different legitimate definitions, demonstrated errors, and differences that cannot be resolved with available evidence.

## Establish the comparison

Identify each report's version, as-of time, headline value, source, unit, population, and intended meaning. Reproduce the reported values from available detail where possible. If only summaries or screenshots are supplied, check supported arithmetic and definitions, but do not claim row-level reconciliation.

Agree or clearly state the comparison direction, for example B minus A. Do not automatically treat the newer, larger, or more official-looking number as correct. Use the governing business definition for the relevant period when available; if it is unknown, compare the definitions without declaring a winner.

## Align before explaining

Inspect only differences that could materially affect the result:

- Period boundaries, timezone, event date versus posting date, and refresh or backfill timing.
- Population, status filters, exclusions, units, currencies, and rounding.
- Row grain, distinct-count keys, aggregation, joins, duplicates, and missing records.
- For rates, the numerator and denominator separately; for averages, the weighting and underlying counts.
- Formula values, subtotal scope, and displayed versus underlying precision where relevant.

Preserve original files. Normalize in a working copy or code, keeping original values and source pointers. Do not silently strip leading zeros from identifiers, collapse distinct entities, treat missing values as zero, or delete apparent duplicates without a justified matching rule.

When matching rows, establish key uniqueness first. Check unmatched records and join expansion so a many-to-many match cannot silently inflate totals. If there is no reliable key, report matching ambiguity and its potential effect instead of presenting a fuzzy match as exact.

## Build the reconciliation

Use inspectable formulas, queries, or code for nontrivial calculations. State the formula and inputs for small manual comparisons. Separate observed corrections from hypothetical adjustments.

For additive amounts, build a bridge from A to B with signed, mutually exclusive adjustments where possible. Show the residual: B minus A minus the sum of explained adjustments. Check that the bridge actually reconciles using precision appropriate to the source, with any tolerance stated and justified.

If differences interact, define the order of a sequential bridge and explain that attribution may depend on that order. Do not count a record once as a date difference and again as a status difference. For nonadditive metrics, reconcile underlying counts or recompute under aligned definitions rather than summing percentages.

Distinguish a bookkeeping explanation from a causal explanation. A reconciled report difference does not establish why real-world performance changed. A zero residual is insufficient if the adjustment rules lack evidence.

## Deliver the answer

Lead with the size of the disagreement and the supported explanation. Include the original totals, material definition differences, quantified adjustments, residual, and remaining limitations. Use source locations and runnable calculations when they help another person reproduce the result.

If resolution is incomplete, state how much remains unexplained and the specific evidence needed next. Recommend a correction only when justified; report changes to source files only if actually authorized and performed. Do not turn a narrow reconciliation into a broad data-quality audit.
