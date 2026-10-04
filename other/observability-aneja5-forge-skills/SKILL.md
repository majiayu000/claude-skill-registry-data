---
name: observability
description: Use when adding logging, structured logs, metrics, traces, or alerts to a service, when designing dashboards, when defining SLOs, when investigating "how will I know if this breaks", or when production logs are too noisy to debug from.
---

# Observability

## Overview

Define how the system tells you it's broken — *before* it's broken. Output is `.forge/observability.md`: structured logging conventions, correlation ID flow, the metrics taxonomy (golden signals per service, USE for resources), trace sampling policy, SLO + alert thresholds (page-worthy vs ticket-worthy), dashboard layouts, log retention, and PII redaction rules. Pairs with `error-handling-and-resilience` (errors classified there get observed here) and `incident-response-and-postmortems` (alerts there route to runbooks).

## When to Use

- A service is going to production and there's no monitoring beyond `console.log`
- Logs exist but are unstructured (free-text) and unsearchable
- Alerts fire constantly (fatigue) or don't fire when they should (gaps)
- Distributed system has no correlation IDs and debugging requires log archaeology
- A new component has been added without dashboards or alerts
- The team can't answer "what's the p95 latency right now?" in under 30 seconds

## When NOT to Use

- Local-only scripts, prototypes, or one-off jobs
- Trivial CRUD additions to a service that already has observability
- Pure documentation or refactoring tasks with no runtime surface

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "Log everything, we'll filter later" | Noise drowns signal. INFO-everything logs are unsearchable in production at scale. |
| "We'll add monitoring later" | You can't debug what you can't see. Add the dashboard before the first user hits the endpoint. |
| "Console.log is fine for now" | Unstructured logs can't be queried, aggregated, or correlated across services. |
| "Alerts can wait" | The first outage you miss without an alert costs more than every alert you'll set up this quarter. |
| "We don't need traces, we have logs" | Logs tell you what happened; traces tell you why it took 4 seconds. They're different. |
| "Sample 100% of traces" | Tracing cost grows linearly with throughput. Sample, with head-based + tail-based sampling for errors. |

## Red Flags

- A service in production with no dashboard
- An alert without a linked runbook
- Logs that contain PII (emails, names, tokens) at INFO
- The same alert firing >10x/day without ack — fatigue
- An "ERROR" log line at INFO level (severity drift)
- A correlation ID that stops at a service boundary
- Traces sampled at 100% in a >10 RPS service
- A dashboard nobody has opened in 30 days

## Core Process

### Step 1: Define correlation ID flow

Every request entering the system gets a trace ID at the edge. Every downstream call (HTTP, queue, RPC) propagates it via the standard header (`traceparent` or `x-request-id`). Every log line carries it. Document the flow end-to-end in the architecture doc.

### Step 2: List golden signals per service

For each service, define the four REDs:
- **Rate** — requests per second
- **Errors** — 4xx / 5xx rate
- **Duration** — p50, p95, p99
- **Saturation** — queue depth, CPU, memory headroom

For data stores, define USE:
- **Utilization** — % busy
- **Saturation** — wait queue
- **Errors** — counts

### Step 3: Define SLOs and alert thresholds

For each user-facing endpoint:
- SLO (e.g., "99.9% of requests succeed within 500ms p95 over 30 days")
- Page-worthy threshold (burning the budget — alert the on-call)
- Ticket-worthy threshold (degraded — file a ticket, fix this week)
- Never-alert noise (background warnings, expected churn)

Every alert MUST link to a runbook (see `incident-response-and-postmortems`).

### Step 4: Establish log levels and structure

| Level | When |
|-------|------|
| ERROR | Failure requiring human attention |
| WARN | Anomaly that retried or recovered |
| INFO | State transitions: started, completed, deployed |
| DEBUG | High-volume internal detail; off in production by default |

Structured JSON only. Fixed top-level fields: `timestamp`, `level`, `service`, `trace_id`, `span_id`, `user_id` (hashed if PII-sensitive), `message`, `error.kind` (matching `error-handling-and-resilience` taxonomy).

### Step 5: Design dashboards

One dashboard per service, with a standard layout:
- Top row: SLO compliance + error rate + latency p95
- Middle: RED signals broken down by endpoint
- Bottom: dependency latencies and saturation

Plus one "user journey" dashboard per critical path from `.forge/testing-strategy.md`.

### Step 6: Configure trace sampling

- Head-based 1-10% baseline
- Tail-based 100% for errors, anomalous latency
- Always-sample for traces tagged `priority=high` (e.g., paying customer endpoints)

### Step 7: Log retention + PII redaction policy

- INFO/DEBUG retention: 7-14 days
- ERROR retention: 90 days
- Audit log retention: per compliance (1+ years)
- PII redaction rules: list every field that must be hashed, redacted, or excluded entirely (cross-reference `security-and-compliance` skill's PII inventory)

### Step 8: Header

Prepend a `forge:meta` header to `.forge/observability.md` (`generated_by: observability`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/architecture.md]` — paths only, never hashes, `generated_from: {.forge/architecture.md: <upstream content_hash AT generation time>}`, `content_hash: <sha256 first 8 of THIS file's body>`). See [forge-dependency-graph](../../references/forge-dependency-graph.md).

## Verification

- [ ] `.forge/observability.md` written
- [ ] Every request has a trace ID propagated through every service
- [ ] Every service has a dashboard with RED/USE signals
- [ ] Every endpoint has an SLO and at least one alert
- [ ] Every alert links to a runbook
- [ ] No PII (email, name, token, raw IP) in logs above DEBUG
- [ ] Trace sampling configured (not 100% in high-volume services)
- [ ] Log levels used consistently (no ERROR-at-INFO)
- [ ] Log retention + redaction policy documented
- [ ] Correlation IDs verified across every service boundary
