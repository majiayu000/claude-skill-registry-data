---
name: numbers-style
description: "Use when writing any number in prose, a table, a chart label or a KPI tile: rounding and significant figures, percent vs percentage points, relative vs absolute change, growth wording, small bases, units and currency, VAT, nominal vs real, locale formatting (English vs Finnish fi-FI separators), ranges, minus signs, dates, ISO weeks and timezones, and naming the kind of average."
license: CC-BY-4.0
---

# Numbers style

A number is read once, quickly. It must be unambiguous, no more precise than
the evidence, and formatted the same way everywhere in a report.

## Precision

- **Two or three significant figures in prose.** "€182,400" in a table;
  "€182,000" or "€0.18 million" in a sentence. Never more precise than the
  uncertainty: if the interval is ±3 pp, "24%" not "24.37%".
- **Round at the end.** Keep full precision through calculations; round only
  for display. Shares that are rounded need not sum to 100%; say so in a
  note rather than fudging a component.
- **Consistent decimals within a column, axis or comparison.**

## Change

- **Percentage points for differences between rates; percent for relative
  change.** "Conversion rose 3 percentage points, from 21% to 24% (a 14%
  relative increase)." Never "conversion rose 3%" for that change.
- **Give both levels.** "from 188 to 212 orders (+13%)", not only "+13%".
- **Growth from zero or a negative base is undefined.** Write the levels.
- **Decreases cannot exceed 100%.** Use "fell to a third", not "fell 300%".
  Avoid "three times less".
- **Small bases: counts first.** "2 of 10 East-region orders were cancelled", not
  "20% cancellation". When a rate on a small base must be shown, give n and
  an interval (`uncertainty-display`).

## Units and money

- **Every number has a unit**, on first use in prose and in every axis label
  and column header.
- **Currency.** State whether prices include VAT (Finland's standard rate is
  25.5% since 1 September 2024); state nominal vs inflation-adjusted for
  comparisons across years, and name the index and base year.
- **Normalise to the decision.** Per order, per 100 deliveries, per staff-hour,
  per € of ad spend; say which denominator.
- **Name the average.** Mean, median, or weighted mean; for skewed values
  (order value, lead time) prefer the median and say so.
- **Percent storage.** Decide whether rates are stored as fractions (0.24) or
  percent (24) and declare it in the unit; ieeVisualizer will not convert.

## Locale

Pick one locale per report and apply it everywhere, including chart ticks.

| | English report | Finnish report (fi-FI) |
|---|---|---|
| Thousands / decimal | 12,345.6 | 12 345,6 (no-break space) |
| Currency | €12,345.60 | 12 345,60 € |
| Percent | 12.3% | 12,3 % |
| Range | 20–28% | 20–28 % |
| Date | 4 October 2026; 4 Oct | 4.10.2026 |

- **Ranges** with an en dash and the unit once: "20–28%"; in prose "from 20%
  to 28%".
- **Negative numbers** with a true minus sign (−4), not a hyphen.
- **Large numbers**: "€1.2 million" (or "€1.2m" in labels), consistent.

## Time

- **Name the period exactly.** "ISO week 40 (28 Sep–4 Oct 2026)" or "the week
  to 4 October". Not "last week" in a document that will be read later.
- **State the timezone** for daily or weekly buckets (the business's own
  timezone, named, e.g. Europe/Berlin) and the data cut-off ("retrieved
  5 Oct 06:00 CEST").
- **Partial periods are labelled** ("October to date, 1–14 Oct").

## ieeVisualizer enforcement

- Units are stored as given and **never converted**: the `timeseries` template
  takes the y unit from the columns, reports `mixed_units` when drawn
  columns disagree and `unit_override_conflict` when `y_unit` contradicts
  a declared unit; `validate()` reports `axis_unit_conflict` when layers on
  one axis disagree. A missing unit is a `missing_unit` warning.
- Axis labels are rendered "Label (unit)".
- Datetime values are stored canonically and keep their UTC offset; the
  renderer labels them in `provenance.timezone` (or UTC with a
  `datetime_displayed_in_utc` warning).
- Not enforced: tick and label locale formatting, rounding in titles and
  captions, pp vs % wording. The skill is the guard.

## Good / bad

| Bad | Good |
|---|---|
| Conversion up 3% (21% → 24%) | Conversion up 3 percentage points, to 24% |
| Revenue €182,437.18 (in a headline) | Revenue €182,000 |
| Cancellations doubled to 20% (East region) | 2 of 10 East-region orders cancelled, up from 1 of 10 |
| Avg order value €870 | Revenue per order €691 (weighted; North and South regions) |
| CPA €45 | Ad spend per paid order €45 (28-day click attribution, ex VAT) |
| Accuracy 0.71 vs 71% in the same table | 71.0% throughout |

## Checklist

- [ ] Precision no finer than the uncertainty; 2–3 significant figures in prose.
- [ ] pp for rate differences, % for relative change; both levels given.
- [ ] Counts shown for small bases.
- [ ] Every number has a unit; VAT and nominal/real stated for money.
- [ ] Average named; denominator named.
- [ ] One locale applied to prose, tables and ticks.
- [ ] Periods exact, timezone stated, partial periods labelled.

Adapted in part from jamditis `data-journalism` (MIT) and UK Analysis Function
guidance (OGL v3.0); changed: rewritten, Finnish locale and examples added.
Sources and licences: `SOURCES.md`.
