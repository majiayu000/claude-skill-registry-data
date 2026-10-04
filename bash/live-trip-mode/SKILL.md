---
name: live-trip-mode
description: Start or stop the paid Flink stream job around a live trip with just live-up / live-down (stays, live stats, savepoints, ~$5.30/day while running).
---
# Live-trip mode

The Managed Service for Apache Flink ("Managed Flink") application `wos-stream-intelligence`
computes stays (detected dwell periods) and per-minute live stats from
`wos.events.v1` onto `wos.derived.v1`. Managed Flink bills while RUNNING (~$5.30/day,
2-KPU minimum) so the app is stopped by default and bracketed around each trip.

## Read first
- flink/README.md — "How it deploys and runs in production", "Configuration", and Known issues (Confluent credential state of the deployed app).
- tools/README.md — "live-up and live-down" section.

## Commands
```bash
just live-up      # start, restoring from the latest snapshot; waits for RUNNING
just live-down    # graceful stop WITH savepoint → back to $0/day
```
AWS credentials for account 458443189947; region defaults to us-east-1 (`AWS_REGION` honored); app name from `WOS_MSF_APP` (default `wos-stream-intelligence`). Both scripts are idempotent — they exit early if already in the target state.

## Gotchas
- **Credential preflight (added July 2026, PR #44):** `live-up` refuses to start while Confluent credentials are placeholders. Two failure modes, two fixes: placeholder `set-after-confluent-signup` SASL properties on the deployed app mean the PR #44 fix isn't deployed yet — dispatch `backend-deploy` (property map gains `secret.arn`) and `flink-deploy` (JAR that reads it); a bus secret still holding `pending-confluent-api-key` means `just bootstrap-secrets` hasn't run with real credentials. As surveyed July 6, 2026 the deployed app still had the placeholder properties, and keeps them until those deploys are dispatched.
- If the preflight cannot read the secret (missing `secretsmanager:GetSecretValue`), it warns and continues — the job itself then fails fast at startup if the secret is a placeholder.
- `live-down` takes a savepoint first, so the next `live-up` resumes state (distance totals, half-open stay clusters) instead of reprocessing the topic.
- A new JAR (uploaded by a manual `flink-deploy` workflow dispatch — merging alone ships nothing) takes effect only at the next start.
- No Flink alarms exist — a failing job is silent. Check the `MsfLogs` CloudWatch group.
