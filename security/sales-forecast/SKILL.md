---
name: sales-forecast
version: 1.0.0
description: Build a defensible weighted forecast — worst/likely/best scenarios, commit vs. upside, weighted total, and the gap-to-target with what must convert.
author: matrixx0070
tags: [sales, forecast, pipeline, revenue, quota]
capabilities: []
---

# Sales Forecast

## When to use
Use this at forecast time when you have a set of open deals and need a defensible number for the period — with reasoning a manager can challenge and the gaps you must close to hit quota.

**Not for:** deal-by-deal coaching and hygiene (use sales-pipeline-review); daily action ranking (use sales-daily-briefing). Forecast answers "what number will land," not "what to work today."

## Method
1. **Set the frame.** Confirm the period, the quota/target, and any already-closed-won bookings.
2. **Normalize each deal.** Capture amount, stage, close date, and a probability — using stage defaults adjusted for real signals (engagement, next step set, champion strength). **Decision point:** close date outside the period → exclude from this forecast, note in pipeline.
3. **Categorize.** Sort into Commit (high confidence, will close), Best Case/Upside (possible, not banked), and Pipeline (early, this-period unlikely).
4. **Compute scenarios.** Worst = closed-won + rock-solid commits. Likely = commit + probability-weighted best case. Best = commit + full best case.
5. **Weight the total.** Sum amount × probability for the weighted forecast.
6. **Gap analysis.** Compare each scenario to target; state the shortfall and what must convert to close it. **Decision point:** likely < target → identify the smallest set of upside deals that closes the gap and name their blockers.
7. **Flag risk.** Call out slipping dates, no next step, or single-threaded contacts that inflate the number.

## Example
Target $500K, closed-won $180K. Commit deals total $200K; best case $220K at ~40% avg. Worst = $380K. Likely = $180K + $200K + ($220K×0.4) = $468K. Best = $600K. Weighted forecast $468K. Gap to target = $32K under on likely → the $80K "Globex" upside deal (blocker: security review) closes the gap if it converts. At-risk: "Initech" $90K commit has no next step and one contact — downgrade to best case.

## Pitfalls
- **Stage-default probabilities as gospel.** A Stage-4 deal with no champion is not 80%; adjust for real signals.
- **Sandbagging or happy ears.** Both destroy trust; the number must be defensible either way.
- **Single-thread inflation.** One-contact deals routinely slip; weight them down.
- **Ignoring close-date slip.** A deal that keeps moving right is not a commit.

## Output format
```
Period & target: <one line, incl. closed-won>
Scenario summary: worst $<> | likely $<> | best $<>
Commit vs. upside:
  Commit $<>: <deals>
  Upside $<>: <deals>
Weighted forecast: $<> (sum amount × probability)
Gap to target: $<> — must close: <deals/actions>
At-risk deals:
  - <deal> — <risk> — forecast impact: $<>
Assumptions: <probabilities & stage defaults used>
```
