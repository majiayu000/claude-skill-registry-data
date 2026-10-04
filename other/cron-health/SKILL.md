---
name: cron-health
description: Scheduled task monitoring skill. Use when checking cron job health, diagnosing missed jobs, or setting up monitoring.
---

Monitor scheduled tasks and ensure nothing runs silently broken.

## What to Track Per Job

| Field | Description |
|-------|-------------|
| Name | Job identifier |
| Schedule | Cron expression |
| Last run | Timestamp of most recent execution |
| Last status | Success or failure |
| Duration | How long it took |
| Output | Key metrics or error message |

## Health Check Pattern

For each scheduled job:
1. Has it run in the expected window? (compare schedule vs last_run)
2. Did it succeed? (check status)
3. Was the duration normal? (compare vs 7-day average)
4. Did it produce expected output? (records_processed > 0)

## Alert Conditions

- **Missed run** — job didn't execute within 2× its scheduled interval
- **Consecutive failures** — same job failed 3+ times in a row
- **Duration anomaly** — took 3× longer than average
- **Zero output** — ran successfully but processed 0 records (may indicate upstream data issue)

## Daily Summary Format

```
Cron jobs (24h): X ok, Y failed
  Failed:
  • job_name: error description
  Slow:
  • job_name: took Xms (avg: Yms)
```

## Safety: Before Restart

Before restarting any service, check:
1. Are any cron jobs currently running?
2. Are any scheduled to run in the next 5 minutes?
3. If yes → defer the restart until the window is clear
4. If no → safe to restart
