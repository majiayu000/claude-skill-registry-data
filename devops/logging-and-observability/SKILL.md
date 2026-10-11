---
name: logging-and-observability
description: Add or improve production-safe diagnostic visibility for applications. Use when Codex needs to support production debugging, deployment readiness, maintenance, client handover, backend workflows, payment/booking/order/staff workflows, external integrations, background jobs, file uploads, intermittent bugs, API error visibility, health checks, request IDs, structured logs, safe traces, monitoring readiness, operational alerts, error tracking, audit logging, performance timing logs, deployment logs, or support diagnostics while avoiding sensitive data exposure.
---

# Logging and Observability

Use this skill when developers need enough safe diagnostic information to understand normal operation, failures, incidents, or user-reported bugs.

## Core Rule

Logs must be useful, safe, structured where possible, and consistent with project conventions. Do not log passwords, tokens, secrets, full private request bodies, or sensitive personal data.

## Workflow

1. Identify the observability need:
   - issue/workflow, target layer, debugging or production-readiness goal, information needed during failure, and information that must not be logged
2. Inspect existing logging patterns:
   - logger utilities, middleware, error handlers, console logs, structured logging, log levels, request ID middleware, health checks, monitoring/error tracking, background job logs, deployment logs, Docker logs, cloud logs, and CI/CD logs
3. Use appropriate log levels:
   - debug for detailed diagnostics, info for normal important events, warn for recoverable issues, error for failed operations, critical/fatal for severe incidents
4. Prefer structured logs when supported:
   - event, request_id, user_id, role, endpoint, method, status_code, duration_ms, entity_type, entity_id, error_code, external_service, job_id, timestamp
5. Add or preserve request identifiers:
   - generate or accept trusted request IDs, attach them to logs, return them in safe error responses when useful, and use them across route/service/database/external calls
6. Add useful backend logs for important workflows:
   - request start/finish, auth failure, permission denial, important record creation, status changes, payment updates, upload failures, external service failures, job failures, unexpected exceptions, slow operations, retries, and health failures
7. Add safe frontend diagnostics when useful:
   - error boundary reporting, API failure context, user-safe error reference ID, route load failure, form submit failure, upload failure, auth refresh failure, and data fetch failure
8. Review or add health checks:
   - basic health, readiness, liveness, and dependency health without exposing secrets or internal config
9. Add performance timing logs when investigating slowness:
   - request duration, DB query duration, external API duration, file processing, job duration, queue wait time, and build/render timing where applicable
10. Add external service and background job observability:
   - service name, operation, safe reference IDs, status code, retry count, error code, job ID, records processed, duration, and correlation ID
11. Separate operational logs from audit logs:
   - audit role changes, invitations, payment status changes, refunds, admin overrides, exports, deactivations, order status changes, and system setting changes intentionally
12. Redact or sanitize sensitive fields:
   - passwords, tokens, authorization, cookies, API keys, secrets, client secrets, payment tokens, card data, and private payloads
13. Add observability for important business events where useful.
14. Review deployment log access:
   - stdout/stderr, Docker logs, VPS journal, cloud logs, log files, monitoring dashboards, error tracking, and CI/CD logs
15. Recommend monitoring or alerts proportionate to the project:
   - app down, DB unreachable, error rate spike, payment failures, job failures, disk/CPU/memory, queue backlog, external service outage, failed login spike
16. Add or update tests where practical.
17. Run relevant checks discovered from project scripts or docs.
18. Summarize scope, logs added, request ID behavior, health checks, error logging, audit logging, redaction, files, checks, debugging value, gaps, and follow-up recommendations.

Read `references/observability-checklist.md` for log levels, structured field guidance, redaction lists, health check patterns, audit logging, alert ideas, tests, and the final report format.

## Non-Negotiable Rules

- Do not log passwords, tokens, secrets, or API keys.
- Do not log full private request bodies unless sanitized.
- Do not expose sensitive data in frontend console logs.
- Do not add noisy logs that make production logs useless.
- Do not use logs as a replacement for proper error handling.
- Do not expose health check internals publicly.
- Do not confuse audit logs with debug logs.
- Do not log private customer data unless there is a clear, safe, and approved reason.
- Do not add monitoring complexity the project cannot maintain.
- Keep logs useful, safe, structured, and consistent.

## Output Contract

When using this skill, provide:

1. Observability scope and existing gaps.
2. Logs added or improved with level, fields, and sensitive data protection.
3. Request ID or correlation behavior.
4. Health checks added or reviewed.
5. Error logging and external service logging behavior.
6. Audit logs added or recommended.
7. Redacted fields and data intentionally not logged.
8. Files changed.
9. Tests/checks or manual verification.
10. How this helps future debugging.
11. Remaining observability gaps and follow-up recommendations.
