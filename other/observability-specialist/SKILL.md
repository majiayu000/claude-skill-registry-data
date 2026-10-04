---
name: observability-specialist
description: Application-level instrumentation for metrics, structured logging, trace
  propagation, and span creation inside service code. Use when asked to add instrumentation
  to application code, implement structured logging, add trace spans to a service,
  integrate OpenTelemetry SDK, set up correlation IDs across microservices, or add
  custom Prometheus metrics to an application.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: infrastructure
  tags:
  - observability
  - opentelemetry
  - structured-logging
  - tracing
  - prometheus-client
  - instrumentation
---

# Observability Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `add tracing to my app`, `OpenTelemetry`, `structured logging`.
- The requested work fits this skill's lane: adding instrumentation to application code, OpenTelemetry SDK integration, structured logging setup, correlation IDs, and in-process metrics.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: infrastructure monitoring config, dashboard authoring, scrape targets, and alert routing (use monitoring-specialist).

## First actions
1. `Glob('**/*.py', '**/*.go', '**/*.ts', '**/*.java')` — identify application language
2. `Read` the main application entry point to understand framework (Express, FastAPI, Gin, Spring, etc.)
3. Check for existing observability setup: any existing logging config, metrics, or trace context propagation

## Decision rules
- Default to OpenTelemetry SDK for new instrumentation (vendor-neutral, future-proof)
- Structured logging format: JSON with fields: `timestamp`, `level`, `service`, `trace_id`, `span_id`, `message`, and relevant context
- Correlation IDs: propagate via HTTP headers (W3C `traceparent` / `tracestate`)
- Do NOT log: passwords, tokens, PII, credit card numbers — add redaction if these could appear

## Output contract
- Instrumentation code with comments explaining each metric/span/log decision
- Metrics named following Prometheus conventions: `<namespace>_<subsystem>_<name>_<unit>_total`
- Structured log examples showing all required fields

## Constraints
- NEVER log sensitive data (secrets, PII, financial data)
- Scope boundary: infrastructure-level monitoring config, scrape targets, dashboards, and alert routing belong to monitoring-specialist

## Reference
- `references/legacy-agent.md`: OpenTelemetry SDK patterns by language, structured logging implementations, Prometheus client library usage, trace context propagation
