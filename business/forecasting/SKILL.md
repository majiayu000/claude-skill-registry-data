---
name: forecasting
description: Forecast with discipline — baselines, seasonality, drivers, ranges, accuracy tracking, revision hygiene.
version: 1
triggers: forecasting, forecast, seasonality, demand forecast, forecast accuracy
category: Money & markets
blurb: Forecast with discipline — baselines, seasonality, drivers, ranges and accuracy tracking.
archetype: knowledge
example: Forecast next year's demand with honest ranges.
---

# Forecasting

Forecasts are planning instruments, not prophecies: compute the baseline, decompose the pattern, express ranges, and measure yourself honestly.

## When to use
- Business planning (revenue, cost, headcount, capacity, demand).
- Operating forecasts and re-forecast cycles.
- Personal financial planning over time.

## Method
1. **Purpose & horizon**: operational (weeks) vs strategic (years); forecast to the decision cadence — daily forecasts for daily decisions, not everything for everyone.
2. **Baseline methods always**: naive (last value), moving average, seasonal-naive — computed and shown; complexity must beat simplicity to earn its place.
3. **Decompose**: level/trend/seasonality; and prefer **driver-based** forecasts where drivers are known (units × price, loads × rates, headcount × costs) over blind extrapolation.
4. **Ranges, not points**: prediction intervals or low/base/high scenarios — a point forecast to leadership without a range is false precision.
5. **Scenario & sensitivity**: base/best/worst with trigger conditions (what signal tells you you're in the worst case) — feeds `budgeting`.
6. **Accuracy tracking**: measure per series (MAE/MAPE) **and bias** — consistently under-forecasting is a process bug, not bad luck; publish scorecards so trust is earned.
7. **Revision hygiene**: keep forecast-vs-actual history; document why revisions happened; never silently restate old forecasts ("we always said!" is a lie the spreadsheet tells).
8. **Cadence**: monthly rolling forecasts (12-month) typical; weekly for operations; annual for strategy — matched to the review rhythm.

## Quality gates
- [ ] Baseline computed and compared; decomposition/drivers shown.
- [ ] Ranges + scenarios delivered, not bare points.
- [ ] Accuracy (incl. bias) tracked per series with a scorecard.
- [ ] Revision reasons documented; history preserved.

## Red lines
- No hindsight edits; no forecasts without owners; no single numbers for uncertain futures without ranges.

## Related
`prediction` · `budgeting` · `revenue-management` (forecast inputs).
