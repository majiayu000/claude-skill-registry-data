---
name: mav-bp-operability
description: 'Operability standards — logging, alerting, and observability as one discipline. Maverick''s opinionated rules: error-only log levels (no info), structured JSON logs, alert-at-the-boundary, correlation across logs/metrics/traces. Applied when writing or reviewing code that logs, alerts, or instruments.'
user-invocable: false
disable-model-invocation: true
---

# Operability Standards

Logging, alerting, and observability as one discipline: record what
happened, demand attention when it matters, and make internal state
diagnosable from outside. Logs record; alerts interrupt; metrics and
traces correlate.

## Maverick's Rules

**Logging**
- **No `info` level.** If it matters in production it is `warn` or
  `error`; if it only helps during development it is `debug`. Info-level
  logging is a noise dumping ground — this is Maverick's most-fought
  deviation from default LLM behaviour; hold the line.
- Structured JSON only, to an aggregation service (stdout is fine when
  the platform ships it — container log drivers, CloudWatch agents).
  Required fields: `timestamp`, `level`, `message`, `service`, `context`
  (put `correlationId` and error details inside `context`).
- Log errors **once, at the boundary** — never log-and-rethrow at every
  layer. Never log PII, tokens, or secrets.
- One logger module per service; `console.log` never ships.

**Alerting**
- Alert only on unrecoverable failures and threshold breaches, from the
  **outermost error boundary** (global handlers, health checks) — never
  inside low-level functions, loops, or retries.
- Severities are `critical` (wake someone) / `high` (within the hour) /
  `warning` (next business day). **Alert severities are not log
  levels** — do not map one onto the other.
- Every alert carries: severity, service, environment, impact-stating
  message ("checkout is down", not "error occurred"), scope, and a log
  pointer. Always log first, then alert.
- Deduplicate: first alert wins, cooldown window suppresses repeats.
- Frontend code never calls alerting services directly — report to an
  error-reporting service or a backend endpoint.

**Observability**
- Three pillars share identifiers: the trace/correlation id in a metric
  spike must find the requests and their logs.
- Request-driven services expose RED metrics (rate, errors, duration);
  no high-cardinality metric labels (user ids belong in traces/logs).
- Liveness checks the process only; readiness checks dependencies —
  conflating them causes cascading restarts.
- Use a standard instrumentation library (OpenTelemetry or equivalent),
  never hand-rolled collection.

## Project Implementation Lookup

Check `docs/maverick/skills/logging/SKILL.md`,
`docs/maverick/skills/alerting/SKILL.md`, and
`docs/maverick/skills/observability/SKILL.md` for project-specific
implementations (library, transport, service names). If present, they
win on specifics. If missing, proceed with these standards and note the
gap in your summary — do not trigger skill generation mid-task.

## Detecting Operability Issues in Code Review

| Pattern                                            | Issue                         | Fix                                          |
| -------------------------------------------------- | ----------------------------- | -------------------------------------------- |
| `console.log(...)`                                 | Unstructured, not centralised | Replace with `logger.debug(...)` or remove   |
| `logger.info(...)`                                 | Creates noise                 | Evaluate: is it `warn`, `error`, or `debug`? |
| `logger.error('Error')`                            | No context                    | Add contextual metadata                      |
| `catch (err) { logger.error(err) }` then re-throws | Duplicate logging             | Log at the boundary only                     |
| Logging PII/secrets                                | Security risk                 | Mask or remove                               |
| Different loggers/alerters in different files      | Inconsistency                 | Use single logger/alerter module             |
| `try/catch` that silently swallows                 | Lost errors                   | Log or re-throw                              |
| Fatal error with no alert                          | Silent failure                | Add alert at the error boundary              |
| Alert inside a loop or retry                       | Alert flood                   | Move alert outside loop, add dedup           |
| Alert with no context                              | Unactionable                  | Add service, error, scope, log pointer       |
| Alert on expected conditions                       | Alert fatigue                 | Remove — only alert on unexpected failures   |
| Alert but no log                                   | Missing investigation trail   | Always log before alerting                   |
| Frontend calling alerting service directly         | Security risk                 | Route through backend API                    |
| No trace context propagation on outbound calls     | Broken traces                 | Add middleware for automatic propagation     |
| Liveness probe checking all dependencies           | Cascading restarts            | Liveness: process only; readiness: deps      |
| High-cardinality metric labels (user/request ids)  | Metric explosion, cost        | Ids belong in traces and logs, not labels    |
| No correlation ID in log entries                   | Cannot link logs to traces    | Include trace ID in structured log context   |
| SLO defined but not measured                       | False confidence              | Instrument the SLI and track the target      |

<!-- maverick-plugin-version: 4.0.2-dev -->
