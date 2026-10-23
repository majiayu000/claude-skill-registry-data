---
name: daily-report
description: Render the daily and weekly desk reports from the ledger on schedule, and deliver only the fields the evaluation reads.
bots:
  - bot-09-journal
gates:
  - G-2
required_tools:
  - journal.render_report
required_data: []
permissions:
  max_side_effect: paper-write
  network: true
  filesystem: var
fixtures:
  - tests/fixtures/replay/smoke
---

# Daily Report

## L1 - Summary

JOURNAL renders the desk's report card on schedule: daily at 00:05Z, weekly on Monday at 00:15Z. The report reads fills, P&L, halts, and review grades from the ledger through `journal.render_report` and delivers exactly the fields the evaluation reads. No commentary, no forecasts, no invented fills.

```
schedule fires -> ledger read -> render -> deliver to the allowlisted sinks -> receipt attached
```

## L2 - Method

1. S1 - Run on schedule: daily 00:05Z and weekly Monday 00:15Z from the cron seat. A missed run is reported as missed, never backfilled with invented rows.
2. S2 - Render from the ledger: call `journal.render_report` with the period and as-of day. Every number traces to a ledger row; grades come from `desk-post-trade-review` rows, not memory.
3. S3 - Deliver the fixed fields: period, fills with realised P&L, open positions with marks, halts and kills with reasons, review grades, and open action items. Fields outside this set do not ship.
4. S4 - Deliver to sinks only: stdout, file, and the configured allowlist. No new destinations per report; adding a sink is a reviewed config change.
5. S5 - Receipt the delivery: attach the render receipt per `verification-receipts` so the evaluation reads a proven report, not a claimed one.

## Failure modes

| Symptom | Cause | Action |
|---|---|---|
| Missed schedule | Cron or gateway outage | Report the miss with its cause; render the next period on time |
| Number without a row | Manual edit or rendering bug | Fail the report; every field traces to the ledger |
| Extra commentary added | Helpful narrative instinct | Strip it; the report carries fields, not forecasts |
| New sink used | Ad-hoc delivery | Refuse; sinks change only by reviewed config |

## References

- Tool: `journal.render_report` (period report rendering)
- Gate G-2: reports are receipted claims
- Companion skills: `portfolio-ledger` (ledger reads), `desk-post-trade-review` (grade rows)
