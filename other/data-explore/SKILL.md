---
name: data-explore
version: 1.0.0
description: Profile an unfamiliar dataset — shape, grain, quality, nulls, distributions, and duplicates — before any analysis is trusted.
author: matrixx0070
tags: [profiling, eda, data-quality, exploration, grain, duplicates]
capabilities: []
---

# data-explore

## When to use

Use this the moment you are handed a dataset (file, table, query result) and need to understand it before trusting it. Run it before analysis — skipping profiling is how wrong numbers reach stakeholders.

**Not for:** answering the business question itself (use data-analyze), significance testing (use data-statistical-analysis), or QA of a finished analysis against stakeholder-readiness (use data-validate).

## Method

1. **Shape.** Rows, columns, and the grain — what one row represents. Confirm the grain explicitly; most errors trace to a wrong grain assumption.
2. **Schema and types.** Each column's stored type vs its semantic type (dates as strings, IDs as numbers).
3. **Completeness.** Per column: null count and percentage. Flag mostly-empty columns and columns that should never be null but are.
4. **Distributions.** Numeric: min, max, mean, median, outlier flags. Categorical: cardinality and top values with frequencies. Dates: range and gaps.
5. **Duplicates.** Check fully duplicated rows and duplicates on the presumed key. Decision point: if the key is not unique, the real grain is finer than assumed — stop and re-derive it.
6. **Integrity.** Orphan foreign keys, impossible values (negative ages, future dates), inconsistent categories ("US" vs "USA").
7. **Reconcile** one total against a known external value to confirm the extract is complete.

## Example

A 100k-row `orders` extract assumed one row per order. Duplicate check on `order_id`:

```sql
SELECT order_id, COUNT(*) c
FROM orders GROUP BY order_id HAVING COUNT(*) > 1;
```

Returns 12k keys with 2+ rows. The real grain is order-line, not order — any per-order SUM would have double-counted. Verdict: usable with caveats, aggregate to `order_id` first.

## Pitfalls

- Assuming the grain from the table name instead of proving it with a key-uniqueness check.
- Reading null percentage without asking which columns are *not allowed* to be null.
- Treating high-cardinality free-text ("USA", "U.S.A.", "us") as clean categories.
- Profiling a partial extract and never reconciling the total, so completeness is unknown.

## Output format

```
Overview:       rows, columns, grain, date range (first line = grain)
Column profile: | name | type | %null | cardinality/range | notable |
Quality flags:  ranked issues (dupes, nulls, impossible, inconsistent) + counts + severity
Verdict:        ready / ready-with-caveats / not-usable — and what to fix
```

Never proceed to analysis silently past a quality flag — surface it.
