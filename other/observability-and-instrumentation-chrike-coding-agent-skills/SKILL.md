---
name: observability-and-instrumentation
description: Use when the user explicitly asks to design, add, or audit persistent operational telemetry such as logs, metrics, traces, or alerts, or when an active owner identifies a concrete observability gap needed to answer an on-call question. Do not use for every production feature, ordinary logging, unknown active failures, measured performance work, generic review, launch readiness, or existing monitoring/tool availability alone.
---

# Observability And Instrumentation

Own the operational signal needed to answer a concrete question. Start from the question, inspect the project's existing telemetry conventions, choose the smallest useful signal, and keep repository instrumentation separate from remote dashboards, live traffic, and launch judgment.

## When to Use

Activate only when the request explicitly asks to:

- design, add, or audit persistent logs, metrics, traces, alerts, or their schema and context propagation; or
- address a concrete observability gap identified by an active owner, such as an on-call question that current signals cannot answer.

A normal feature does not trigger this owner merely because it will run in production. An unknown active failure belongs to `debug-systematically`; measured performance belongs to `performance-optimization`; test seams belong to `test-strategy`; architecture or ownership belongs to `design-codebase`; generic review belongs to `review-and-finish`; release readiness belongs to `shipping-and-launch`.

## Define The Operational Question

Before choosing a signal, record two to four questions an operator must be able to answer about the scoped behavior. For each question, state:

- the component, event, dependency, or user-visible outcome in scope;
- the actor and environment that produce or consume the signal;
- the freshness, retention, and evidence strength needed for the decision;
- the privacy, cost, cardinality, and sampling constraints; and
- the smallest signal that can answer it.

Use only the applicable signal:

- **Structured log:** what happened in one case, with a stable event name and allowlisted fields.
- **Metric:** how often, how many, or how long in aggregate, with bounded labels and a meaningful distribution when percentiles matter.
- **Trace or context:** where time or failure crossed a component boundary, with propagation only across the relevant request or job path.
- **Alert:** a symptom or invariant that requires an identified response, threshold, duration, and runbook owner.

Do not require logs, metrics, traces, and alerts together. A signal without an operational question is noise, cost, or an unreviewed data path.

## Project Facts And Data Boundaries

Read the existing logger, meter, tracer, naming, sampling, redaction, configuration, retention, and dependency conventions before proposing a change. Do not assume OpenTelemetry, Prometheus, a vendor, a framework, a transport, or a new dependency. Keep event names and labels stable only when the current project contract supports them.

Allowlist the smallest fields needed to answer the question. Never read, print, or add secrets, credentials, tokens, passwords, full request bodies, storage contents, or unredacted personal data. Do not use user IDs, raw URLs, error text, or unbounded values as metric labels. Treat correlation IDs and trace context as sensitive operational data whose propagation and retention still need project justification.

## Conditional Signal Checklist

When the selected signal makes the prompt material, check:

- **Structured logs:** stable event names, allowlisted fields, justified correlation across outbound or asynchronous boundaries, actionable levels, and metadata-only dependency calls.
- **Metrics:** a distribution when percentile questions matter, bounded status or route classes, and queue depth, age, or processing duration only when the operational question needs them.
- **Traces:** propagation across the relevant request or job path, spans around meaningful units of work, and no secrets or unredacted personal data in attributes.
- **Alerts and dashboards:** a symptom or invariant, a named response or runbook, project-backed threshold and duration evidence, and views that answer the stated questions; remote configuration and test firing remain separate actions.

These are conditional prompts, not a universal RED/USE, full-trace, alert, dashboard, vendor, retention, or launch gate.

## Verification And Evidence

Separate these claims:

1. **Definition:** the repository contains the intended instrumentation schema or alert definition.
2. **Static evidence:** an authorized source or parser shows the code/configuration is structurally valid.
3. **Local behavior:** an authorized local check observes the emitted shape without external services.
4. **Runtime telemetry:** an identified environment receives, stores, correlates, and queries the signal.
5. **Operational response:** an alert reaches the named channel and its runbook supports an action.

Static source does not prove that a backend receives telemetry or that an alert pages the correct owner. If the environment, backend, channel, retention, or runtime observation is unavailable, report `UNVERIFIED`.

A repository-local implementation may be authorized by an explicit request with a clear scope, but instrumentation, dependency installation, test traffic, failure injection, dashboard or alert changes, and production access are separate actions. Do not silently run them.

## Handoffs

- Unknown active failure or missing root cause → `debug-systematically`.
- Benchmark, latency, resource, or measured performance claim → `performance-optimization`.
- Fixture, assertion, telemetry proof seam, or test timing → `test-strategy`.
- Ownership, interface, dependency, or context-propagation architecture → `design-codebase`.
- Security, privacy, secret, or trust-boundary analysis → `security-and-hardening`.
- Generic review or completion judgment → `review-and-finish`.
- Concrete production release readiness → `shipping-and-launch`.
- Commit, push, merge, PR, or branch action → `finish-branch`.
- Remote dashboard, alert channel, monitoring configuration, deployment, or publication → the explicitly named owner or host method; do not infer one.

## Report Format

- **Operational questions:** the questions and scope the signal is meant to answer.
- **Observed definition:** current files, conventions, and authorized checks.
- **Selected signal:** why this log, metric, trace, or alert is the minimum useful choice.
- **Inference:** expected answers, propagation, and material assumptions.
- **Gaps / UNVERIFIED:** missing runtime, backend, privacy, retention, sampling, channel, runbook, or authorization evidence.
- **Recommendation:** the smallest repository-local change or next evidence question and its owner.

Do not claim that telemetry is queryable, correlated, private, actionable, or production-ready without the corresponding evidence.

## Verification

Before stopping, check that:

- the trigger names an explicit operational telemetry question or concrete gap;
- the selected signal is minimal and follows current project conventions;
- fields and labels are bounded, allowlisted, and free of secrets and unredacted sensitive data;
- definition, static, local, runtime, and operational-response evidence remain distinct;
- no universal RED/USE, full-trace, alert, vendor, retention, or sampling gate was imposed; and
- no dependency install, network access, dashboard or alert publication, test traffic, failure injection, production access, deployment, or Git action occurred without its own authorization.
