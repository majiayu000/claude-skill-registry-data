---
name: post-deployment-readonly-verification
description: Generic read-only post-deployment verification workflow for confirming service health, artifact activation, routing, logs, and rollback signals after a deployment action.
---

# Post-Deployment Read-Only Verification

## Purpose
Verify whether a deployment is actually healthy after a change. The workflow distinguishes "command executed" from "service currently healthy" by checking runtime state, artifact activation, routes, logs, and user-visible behavior without making further changes.

## When to use
- After a deployment, restart, rollback, config change, package replacement, or migration.
- When a service reports active but user-facing checks still fail.
- Before telling a user a deployment succeeded.
- When a previous deployment action was performed by another person or agent and needs independent verification.

## Safety rules
- Default workflow is read-only.
- Do not restart, reload, edit, redeploy, roll back, clear caches, run migrations, or execute write-path tests without explicit approval.
- Do not print raw production logs, customer data, order data, tokens, cookies, JWTs, database URLs, internal IPs, or real domains.
- Replace identifiers with `<PROJECT_NAME>`, `<SERVICE_NAME>`, `<APP_DOMAIN>`, `<PROJECT_ROOT>`, `<SERVER_IP>`, and `<ARTIFACT_NAME>`.
- Health checks should be safe GET/read-only probes unless the user approves write-path validation.

## Read-only workflow
1. Confirm what changed: artifact, config, service, migration, rollback, or unknown. Record who/what performed the action if known.
2. Check current service state, not only the state immediately after deployment: active state, substate, main PID, restart count, exit status, and uptime.
3. Verify artifact activation: running command line, file timestamp, version endpoint if safe, static asset timestamp, container image digest, or application startup banner.
4. Check local ports and process bindings against expected ports.
5. Check logs since deployment time: summarize startup success, warnings, errors, crash loops, migration messages, and repeated exceptions without raw sensitive content.
6. Perform safe local probes: health endpoint, root page, read-only API, static asset, or internal readiness endpoint.
7. Perform safe external-route probes if allowed: reverse proxy domain, TLS status, CDN/tunnel route, gateway prefix, and status code class. Avoid exposing real domains in public reports.
8. Validate dependency signals: database pool ready, queue/worker connected, external API readiness, proxy state, and scheduled task handoff if relevant.
9. Compare observed behavior to rollback criteria. Identify whether rollback should be considered, but do not execute it.
10. Produce a pass/warn/fail verdict with evidence and next steps.

## Evidence to collect
- Deployment time or change window.
- Current service active/substate, PID, restart count, uptime.
- Artifact/version activation evidence.
- Port and process binding summary.
- Safe log summary since deployment.
- Local read-only probe results.
- External read-only probe results if in scope.
- Dependency readiness summary.
- Rollback trigger indicators.

## Stop conditions
- Verification requires write-path tests without approval.
- Logs contain sensitive data that cannot be summarized safely.
- The deployment time or changed component is unknown and cannot be inferred.
- Current checks indicate active data corruption, migration failure, or customer-impacting outage requiring human decision.
- A rollback or restart appears necessary but has not been approved.

## Optional user-approved actions
Only after explicit user approval:
- Restart/reload service or proxy.
- Execute rollback.
- Run write-path smoke tests.
- Run data migration verification queries requiring elevated access.
- Patch configuration or redeploy an artifact.
- Increase logging or add temporary diagnostics.

## Final report format
```text
Summary: <pass/warn/fail verdict>
Change verified: <artifact/config/service/unknown>
Current runtime: <service/PID/restarts/uptime>
Artifact activation: <evidence>
Read-only probes: <local/external status summary>
Logs since change: <safe summary>
Dependencies: <summary>
Rollback signals: <none/present/unknown>
Recommended next step: <observe / approval-required fix / rollback decision>
Needs approval: <specific action if any>
```
