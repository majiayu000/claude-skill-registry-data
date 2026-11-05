---
name: production-health-report
description: Audit production health across Nick's Tire/StateNour infrastructure including live sites, Railway services and deploys, Neon/Postgres, GitHub main/PR/CI state, schedulers/cron/workers/queues, logs, errors, observability, and feature wiring. Use when the user asks for a production health report, system status, reliability audit, "what is actually working", periodic infrastructure review, or wants LIVE vs BUILT-UNWIRED vs BROKEN vs DUPLICATE vs MISSING classification.
triggers: production health, what's actually live, railway, neon, github main, ci state, cron, workers, queues, logs, errors, built but unwired, system reality report, deploys
---

# Production Health Report

Establish ground truth from live behavior and current system evidence before trusting code, docs, or previous session claims.

## Evidence order

Prefer evidence roughly in this order:
1. live production behavior and receipts
2. current production configuration and deployment state
3. current origin/main
4. active PRs/branches/worktrees
5. CI/tests
6. databases, logs, telemetry, queues, schedulers, and observability
7. current documentation
8. historical plans and prior AI claims

## Workflow

1. Define scope and exact inspection time.
2. Inspect authorized live endpoints and relevant connectors such as Railway, Neon, GitHub, and logs when available.
3. Reconcile production commit/deploy against current origin/main. Note skew explicitly.
4. Classify important capabilities:
   - LIVE + VERIFIED
   - LIVE BUT UNVERIFIED
   - BUILT + WIRED
   - BUILT-UNWIRED
   - BROKEN/DEGRADED
   - DUPLICATE/CONFLICTING
   - MISSING
5. Inspect reliability signals:
   - deploy failures/restarts
   - HTTP/app errors
   - database saturation or query failures
   - worker/queue/scheduler/cron failures
   - stuck or repeated jobs
   - auth/integration failures
   - CI drift and failing checks
   - observability gaps
6. For every severe issue, trace from symptom to likely component and evidence. Do not turn correlation into root cause without proof.
7. Distinguish "code exists" from "feature is reachable and used". Search for importers/callers/routes/jobs/flags and verify production receipt when possible.
8. Protect parallel work. Do not recommend deleting or overwriting active branches/worktrees without checking ownership/current activity.
9. Read `references/report-contract.md` and follow its output structure.

## Rules

- Never report completion because a PR merged; verify deployment and behavior when material.
- Never trust stale docs over current live/config/code evidence.
- Do not expose secrets from environment variables or logs.
- After a merge to main, read `list-deployments` for EACH touched service and confirm a deployment exists for the merge commit.
  A merge can produce NO deployment for the touched service while untouched services get SKIPPED records (2026-10-20 19:05-19:23Z,
  three pushes), and the project has no deploy webhook to page on it. Report it as "merged, not deployed".
- Use exact commit/deploy IDs and timestamps when available.
- If a connector/source is unavailable, mark that boundary rather than guessing.

## Useful triggers

Examples: "run production health", "what's actually live?", "audit Railway/Neon/GitHub", "find built but unwired features", "give me the monthly system reality report".
