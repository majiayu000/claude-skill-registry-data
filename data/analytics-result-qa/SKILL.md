---
name: analytics-result-qa
category: quality
description: Use when you are about to hand off any number, table, chart or analysis someone will act on (a metric query, a dbt mart, a report, an experiment readout) — the pre-delivery checklist for data quality, calculation, reasonableness and presentation, and the pitfalls that produce plausible wrong numbers
tech_stack: SQL & dbt
source: anthropics/knowledge-work-plugins validate-data (Apache-2.0), adapted
---
# Analytics Result QA

## Overview

The dangerous analytics bug is not the query that fails — it is the one that returns a plausible number. A fan-out join, a partial month, a shifted denominator: each produces a result that looks fine and is wrong by 20%. This checklist runs before any number leaves your run, and the checks that can be automated become tests.

**Core principle:** recompute every headline number a second way, and turn every check you did by hand into a test or a dbt test that keeps doing it.

## 1. Before computing: the question and the definitions

- Is the analysis answering the question asked, for the population asked? Write the population definition down (who is in, who is excluded and why).
- Is each metric defined the way the people who will read it define it ("active", "churned", "revenue" net or gross)? Where the task is silent, record your definition in the closing message.
- Are the comparison periods and cohorts comparable — same length, same definition, both complete?

## 2. Pre-delivery checklist

### Data quality
- [ ] The source tables are the right ones, and you know their as-of date.
- [ ] No unexpected gaps in the time range or missing segments.
- [ ] Null rates in the columns you use are known and handled on purpose.
- [ ] No double counting from duplicate source rows or a join.
- [ ] Every filter is intentional; none silently drops a segment.

### Calculation
- [ ] Aggregation grain matches the question; every non-aggregated column is in the GROUP BY.
- [ ] Rates use the right denominator, and the denominator cannot be zero.
- [ ] Compared periods have the same length; partial periods are excluded or labelled.
- [ ] Join types are right (INNER vs LEFT) and row counts were checked before and after each join.
- [ ] Parts sum to the whole, or the difference is explained (overlap, unknown bucket).

### Reasonableness
- [ ] Magnitudes are plausible (no negative revenue, rates within 0–100%).
- [ ] No unexplained jumps in a time series.
- [ ] Headline numbers match a known reference (an existing dashboard, finance figures, a previous report) or the gap is explained.
- [ ] Edge cases behave: an empty segment, a zero-activity period, a brand-new entity.

### Presentation
- [ ] Bar charts start at zero; axes are labelled; panels share scales where compared.
- [ ] Precision matches the evidence; units and currencies are explicit.
- [ ] Titles state the date range; caveats and assumptions are written down.
- [ ] Someone else can reproduce it from the code in the diff.

## 3. Pitfalls that produce plausible wrong numbers

| Pitfall | How it happens | Detect / prevent |
|---|---|---|
| Join fan-out | one-to-many join before aggregating | row counts before and after; aggregate before joining; `count(distinct key)` |
| Survivorship | only entities that still exist are analysed | ask who is missing (churned, deleted, failed) |
| Incomplete period | current month compared with a full one | complete periods only, or same-number-of-days comparisons |
| Denominator shift | the definition of "eligible" changed between periods | one definition across compared periods; note any change |
| Average of averages | pre-aggregated means averaged across unequal groups | aggregate from rows or weight by group size |
| Timezone mismatch | UTC events bucketed against local-time days | convert to one timezone before truncating; state it |
| Selection by outcome | segment defined by the result being measured | segment on pre-treatment attributes |
| Look-ahead | a later fact used to explain an earlier event | as-of joins; only information available at the time |
| Simpson's paradox | mix shift reverses the trend in the aggregate | check the key segments |

## 4. Recompute it another way

1. Compute the headline number by a second route (from a different table, bottom-up vs top-down, SQL vs pandas) and compare.
2. Trace three individual entities by hand through every step.
3. Reverse-check: per-unit value × count ≈ total.
4. Boundary slices: one day, one customer, one category — do the micro-results make sense?

## 5. Red-flag values

- A metric moved more than ~50% period over period with no known cause.
- Exact round numbers, or rates of exactly 0% or 100%.
- Identical values across periods or segments (a dimension is being ignored).
- A result that confirms the hypothesis perfectly.

Each one is investigated before delivery, not footnoted after.

## 6. Make the checks permanent

| Manual check | Permanent form |
|---|---|
| Key is unique after the join | dbt `unique` test / `merge(validate="many_to_one")` |
| Parts sum to the total | a singular dbt test or a pytest assertion on the fixture |
| Rate within 0–1 | dbt `accepted_range` (if dbt_utils is installed) or a pandera `Field(ge=0, le=1)` |
| Matches the finance figure within 1% | a reconciliation test against a fixture, or a monitored check in the pipeline |

## 7. Your verdict, in the closing message

State one of:

- **Ready** — checks passed, numbers reconciled, caveats noted.
- **Ready with caveats** — correct, but the reader must know: list each caveat (partial period, excluded segment, definition choice).
- **Not ready** — a check failed that you could not resolve in this run: what failed and what it would take; that is also a card comment for a person (concise-board-comments).

Include the reconciliation you did ("total revenue 1.284M matches the finance export within 0.3%").

## Common Mistakes

- Trusting a number because the query ran without error.
- Checking the total but not the segments that sum to it.
- Comparing this partial month with last full month.
- Leaving the reconciliation in your head instead of in a test.

## Red Flags

- No reference figure anywhere to compare the headline number with.
- `select distinct` used to make counts "look right".
- A definition decided silently in SQL that the reader will interpret differently.
