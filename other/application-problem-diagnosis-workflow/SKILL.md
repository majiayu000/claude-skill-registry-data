---
name: application-problem-diagnosis-workflow
description: Read-only first workflow for diagnosing application incidents by collecting service, log, network, configuration, and functional evidence before proposing any fix.
---

# Application Problem Diagnosis Workflow

## Purpose
Prevent blind fixes by enforcing a diagnose-before-treat workflow for application incidents. The skill gathers evidence from service state, logs, process state, configuration summaries, and functional probes before recommending any change.

## When to use
- A user reports an application is unavailable, degraded, or returning unexpected errors.
- A service appears running but requests fail.
- APIs return generic errors, 404/5xx responses, or inconsistent behavior.
- Before changing application, proxy, systemd, database, or runtime configuration.

## Safety rules
- Default workflow is read-only.
- Do not restart services, edit configs, deploy packages, change database schema, clear caches, or run migrations without explicit approval.
- Do not return raw production logs. Summarize error classes, counts, timestamps, and safe stack-frame hints only.
- Do not expose customer data, order data, tokens, cookies, JWTs, credentials, database URLs, private hostnames, IPs, or service account names.
- Replace production identifiers with `<PROJECT_NAME>`, `<SERVICE_NAME>`, `<APP_DOMAIN>`, `<SERVER_IP>`, and `<PROJECT_ROOT>`.

## Read-only workflow
1. Establish scope: affected service, user-visible symptom, time window, and expected behavior.
2. Check service state without changing it: active state, substate, main PID, recent exits, restart count, working directory, and command line.
3. Inspect recent logs safely: collect error categories, exception names, frequency, and first/last occurrence time without copying raw sensitive payloads.
4. Check process and port state: whether the expected process exists and whether expected local ports listen.
5. Verify application startup signals: framework started, web server bound to port, routes/mappings registered, database pool initialized, background workers ready.
6. Test functionality with safe read-only probes: health endpoints, root path, known read-only API, or direct local loopback request. Avoid mutating endpoints.
7. Review configuration summaries: which config file is loaded, active profile, expected port, upstream target, and required environment-variable presence. Do not print secret values.
8. Compare proxy/gateway layer against backend: determine whether failure is app-side, reverse-proxy-side, network-side, or wrong-path testing.
9. Form a hypothesis and list evidence for/against it.
10. Propose the smallest next action, keeping fixes behind user approval.

## Evidence to collect
- Symptom and time window.
- Service active/substate and restart count.
- Safe log summary: error classes, counts, timestamps, affected component.
- Process PID and command summary.
- Listening ports and expected port match/mismatch.
- Startup success or failure signals.
- Configuration presence and active profile without secret values.
- Read-only probe results and HTTP status classes.
- Reverse proxy/upstream status if applicable.
- Hypothesis ranking and confidence.

## Stop conditions
- Logs contain sensitive user/customer/order/auth data that cannot be safely summarized.
- The only next step is a write operation, restart, deployment, database change, or migration.
- You cannot identify the affected service or time window from available evidence.
- Probes would mutate state or trigger external side effects.

## Optional user-approved actions
Only after explicit user approval:
- Restart or reload a service.
- Edit configuration.
- Deploy or roll back an artifact.
- Run database migrations or schema checks requiring elevated access.
- Add temporary diagnostics or observability code.
- Execute write-path functional tests.

## Final report format
```text
Summary: <one-line incident diagnosis>
Scope: <PROJECT_NAME>/<SERVICE_NAME>/<time window>
Impact: <user-visible / internal / unknown>
Read-only evidence:
- Service: <state summary>
- Logs: <safe error summary>
- Ports/process: <summary>
- Config: <presence and active profile, no secrets>
- Probes: <status summary>
Likely cause: <ranked hypothesis>
Ruled out: <bullets>
Recommended next step: <read-only or approval-required>
Needs approval: <yes/no and specific action>
```
