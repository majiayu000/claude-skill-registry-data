---
name: debug-and-logging
description: "Use when diagnosing Apex behavior with debug logs, choosing log levels, or replacing `System.debug` habits with structured production logging and async job monitoring. Triggers: 'debug log', 'System.debug', 'logging framework', 'AsyncApexJob monitoring', 'production logs'. NOT for exception taxonomy design alone or for non-Apex observability platforms by themselves."
category: apex
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Reliability
tags:
  - debug-logs
  - system-debug
  - logging-framework
  - asyncapexjob
  - observability
triggers:
  - "how should I debug Apex in production-safe ways"
  - "too many System.debug statements in code"
  - "custom logging framework for Apex"
  - "AsyncApexJob monitoring and failure logs"
  - "which debug log levels should I use"
inputs:
  - "execution context such as synchronous request, trigger, Queueable, Batch, or REST"
  - "whether the issue is development-time debugging or production-time observability"
  - "current logging destination such as debug logs, custom object, or platform event"
outputs:
  - "logging strategy recommendation"
  - "review findings for observability gaps or noisy debug usage"
  - "Apex logging pattern with retention and escalation guidance"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-03-13
---

Use this skill when the question is not merely “where do I put a debug line?” but “how do I make Apex diagnosable in the environments that matter?” Debug logs are useful in development and targeted troubleshooting. Structured logs, async job monitoring, and durable records are what keep production support workable.

## Before Starting

- Is the need short-lived debugging in a lower environment or persistent production observability?
- Which contexts fail today: synchronous requests, triggers, Queueables, Batch jobs, or event subscribers?
- What can safely be logged without leaking secrets, tokens, or sensitive business data?

## Core Concepts

### `System.debug` Is A Development Tool First

`System.debug` is valuable for temporary investigation and lower-environment diagnosis, especially when paired with the right debug categories and levels. It is not a durable production logging strategy. Teams that rely on `System.debug` alone usually discover too late that the information they need was never retained or queryable.

### Structured Logging Needs A Durable Sink

For production support, use a real destination such as a custom log object, platform event, or external observability system. The important properties are durability, correlation, and queryability. A useful log record usually includes operation name, record IDs or correlation ID, severity, outcome, and normalized error details.

### Log Levels Should Reflect Actionability

Debug levels are not decorative. Excessive low-value logging creates noise and storage pressure. Use lower-detail debug traces during focused diagnosis, but keep persistent production logging targeted toward warnings, errors, and key workflow checkpoints that support can actually act on.

### Async Monitoring Is Part Of Logging

If Queueable or Batch work matters to the business, `AsyncApexJob` status and job metrics are part of observability. Logging should connect the initiating action to job IDs, job outcomes, and error counts instead of leaving async failures orphaned.

## Common Patterns

### Temporary Debug Logging With Removal Discipline

**When to use:** A developer is tracing a bug in a sandbox or lower environment.

**How it works:** Add targeted `System.debug` statements with clear labels and remove them after diagnosis.

**Why not the alternative:** Leaving broad debug noise in production code makes future diagnosis harder.

### Structured Logger Wrapper

**When to use:** A service, integration, or async worker needs durable support diagnostics.

**How it works:** Centralize logging through one utility or service that writes severity, context, and identifiers to a durable sink.

### Async Job Correlation

**When to use:** Batch or Queueable work drives business-critical outcomes.

**How it works:** Log the initiating business context alongside the enqueued job ID, then monitor `AsyncApexJob` for failures and throughput.

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Sandbox-only debugging session | Targeted `System.debug` with clear labels | Fastest way to inspect runtime state temporarily |
| Production support needs durable diagnostics | Structured log object or event | Queryable and retained beyond transient debug logs |
| Async worker must be monitored | Correlate to `AsyncApexJob` and log job outcomes | Required for real operational visibility |
| Sensitive integration flow | Minimal structured logs with secret-safe fields | Avoids leaking tokens or payload secrets |


## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner activating this skill:

1. Gather context — confirm the org edition, relevant objects, and current configuration state
2. Review official sources — check the references in this skill's well-architected.md before making changes
3. Implement or advise — apply the patterns from Core Concepts and Common Patterns sections above
4. Validate — run the skill's checker script and verify against the Review Checklist below
5. Document — record any deviations from standard patterns and update the template if needed

---

## Review Checklist

- [ ] `System.debug` usage is targeted and justified, not left as permanent noise.
- [ ] Durable logging exists for production-critical failures.
- [ ] Logged fields exclude secrets, tokens, and unnecessary sensitive payload data.
- [ ] Async processes can be traced through job IDs or equivalent correlation.
- [ ] Log severity and volume are aligned to support actionability.
- [ ] Teams know where logs are retained and how they are purged.

## Salesforce-Specific Gotchas

1. **Debug logs are temporary and operationally fragile** — they are not a replacement for durable production logs.
2. **Overlogging can hide the signal you actually need** — a flood of low-value debug lines makes incidents slower to diagnose.
3. **Async failures often need both logs and `AsyncApexJob` inspection** — one without the other leaves blind spots.
4. **Logging secrets is still a security defect even if the log helps debugging** — sanitize outbound request data and auth fields.

## Output Artifacts

| Artifact | Description |
|---|---|
| Logging review | Findings on debug noise, missing durable logs, and async visibility gaps |
| Logging strategy | Recommendation for debug usage, structured logging, and retention |
| Correlation pattern | Guidance for linking business actions, exceptions, and async job IDs |

## Related Skills

- `apex/exception-handling` — use when the main gap is how exceptions are classified, rethrown, or mapped.
- `apex/batch-apex-patterns` — use when observability issues center on Batch lifecycle and job monitoring.
- `apex/callouts-and-http-integrations` — use when logs need to support outbound API troubleshooting safely.
