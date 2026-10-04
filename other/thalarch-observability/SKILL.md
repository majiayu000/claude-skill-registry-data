---
name: thalarch-observability
description: >
  Production observability and instrumentation skill for services, background jobs, queues,
  external integrations, retries, distributed systems, and production incident follow-up. Use when
  adding or reviewing logs, metrics, traces, correlation, alerting, telemetry privacy, or when a
  feature needs evidence that production behavior can be diagnosed after release.
---

# Thalarch Observability

Observability should answer operational questions, not maximize telemetry volume.

Use the repository's existing telemetry stack and conventions unless the task explicitly introduces
or migrates observability infrastructure.

## 1. Start from operational questions

Before adding signals, write the small set of questions an operator would need answered if this
feature fails or degrades, for example:

- Did the operation succeed, fail, retry, or fall back?
- Which dependency or stage consumed the time?
- How often is the failure happening?
- Can one affected request/job be reconstructed end-to-end?

Every new signal should answer a real question. Telemetry without a question becomes noise and cost.

## 2. Choose the right signal

Use the smallest appropriate evidence channel:

- structured logs for specific events and failure context;
- metrics for aggregate rate/error/duration/resource trends;
- traces for cross-boundary causal/latency paths;
- events/audit records when durable business/security history is the actual requirement.

Do not duplicate the same high-cardinality payload across logs, metric labels, and traces.

## 3. Structured logging

Prefer stable event names plus machine-queryable fields over prose-only interpolation.

Preserve or introduce correlation/request/job identifiers at system boundaries when the architecture
supports them, and propagate them across downstream calls/queues where useful.

Never log:

- credentials/tokens/secrets;
- full sensitive request/response bodies by default;
- unnecessary personal data;
- unbounded arbitrary objects merely because serialization is easy.

Follow project retention/redaction/privacy rules.

## 4. Metrics

For request-driven operations, consider rate, errors, and latency/distribution. For finite resources,
consider utilization, saturation, and errors.

Use bounded-cardinality dimensions. User IDs, raw URLs, request IDs, free-form error messages, and
other unbounded values are generally unsuitable metric labels.

Prefer distributions/histograms for latency where the telemetry system supports them; a single
average can hide tail behavior.

Do not invent universal latency/error thresholds. Use product SLOs, historical baselines, or an
explicit task requirement.

## 5. Tracing

Use the project's existing tracing standard when present. Add spans around meaningful boundaries,
not every helper function.

Preserve context across asynchronous/process/service boundaries when needed to reconstruct the
operation. Sampling strategy, exporter choice, and backend-specific configuration must be grounded
in the actual deployment stack rather than assumed.

## 6. Retries, queues, and external calls

These surfaces deserve extra scrutiny because failures are often hidden by recovery behavior.

When relevant expose enough evidence to distinguish:

- first-attempt success from recovered retry;
- retry exhaustion from immediate permanent failure;
- queue wait from processing time;
- local timeout from dependency timeout;
- fallback use from primary-path success;
- duplicate/idempotent processing from unique work.

Do not log or meter every retry with unbounded dimensions if aggregate/structured signals can answer
the operational question more safely.

## 7. Alerting

Prefer user-visible symptoms and service objectives over low-level causes when deciding what should
page a human.

Every alert should have:

- a measurable condition;
- a justified threshold/window;
- an expected human action;
- enough context/runbook guidance to start diagnosis.

If an alert routinely fires without action, it is training operators to ignore telemetry.

## 8. Telemetry security

Treat observability pipelines as data exfiltration surfaces.

Review:

- redaction and field allowlisting;
- auth/access to dashboards and traces;
- tenant boundaries;
- secret/PII leakage;
- retention/export destinations;
- injection or log-forging risks where untrusted text is included.

Route security-sensitive telemetry decisions through `thalarch-security` when needed.

## 9. Verify the instrumentation

Telemetry implementation is not proven by compilation.

When the environment permits, exercise the actual path and confirm:

- expected structured fields appear;
- correlation survives the intended boundaries;
- metric series/dimensions are sane and bounded;
- trace continuity is not broken;
- an induced or known failure can be found using the emitted evidence;
- alert delivery/routing works when alert configuration is part of scope.

If the real telemetry backend/staging environment cannot be accessed, keep backend behavior
`UNVERIFIED` and report what was proven locally.

## 10. Shortcut defenses

Reject these shortcuts:

- "More logs means more observability" — noisy unstructured output can make incidents slower.
- "We'll instrument after launch" — missing telemetry is most expensive during the first failure.
- "A user ID metric label is convenient" — convenience can create cardinality explosions and data
  exposure.
- "CPU is high, page someone" — alerts should normally correspond to actionable service/user impact.
- "The SDK initialization compiles, so tracing works" — verify emitted telemetry when possible.

## Completion

Report:

- operational questions covered;
- signals added/changed;
- privacy/cardinality considerations;
- actual telemetry verification performed;
- environment/backend behavior that remains `UNVERIFIED`.