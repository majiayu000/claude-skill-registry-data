---
name: darwin-cron-guard
description: Use when creating or editing cron jobs - prevents timeouts, silent failures, and delivery gaps.
---

# Darwin Cron Guard

## Trigger
Use whenever a scheduled job is created, edited, or diagnosed.

## Procedure
1. Terminal timeouts must be <= 120s inside cron runs.
2. Background processes need notify_on_complete=true.
3. Exit code 2 may be a SUCCESS-with-changes convention -
   check the tool's documented exit semantics before alerting.
4. Verify last_status after the first scheduled run.

## Pitfall
A job that exits 0 with empty output may have done nothing.

## Verification
After following the procedure: confirm the outcome
with real evidence (exit code, file, or API response).
```bash
python -c "import sys; print('darwin-species-ok')"
```
