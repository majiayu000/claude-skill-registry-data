---
name: observability-and-instrumentation
description: "Add or review logs, metrics, traces, and actionable alerts."
license: MIT
metadata:
  author: Addy Osmani and Skillz contributors
  source: addyosmani/agent-skills
  source-commit: 1401c8b8030e023baeebb31781a6653fe8e93026
  adaptation: curated-rewrite
  owner: software-factory
  risk: medium
  capabilities: addyosmani,observability-and-instrumentation
---

# Observability and instrumentation

Start with the operational question: what would an on-call engineer need to
distinguish success, failure, delay, and unknown outcomes? Add signals for those
questions using the existing telemetry stack. Do not install a new backend or
instrument every function by default.

## Choose signals deliberately

| Need | Signal |
| --- | --- |
| Explain one operation | Structured event with stable fields and bounded context. |
| Detect aggregate regressions | Counter or histogram with bounded label sets. |
| Locate delay across boundaries | Trace spans with propagated context. |
| Reconstruct a sensitive business action | Access-controlled audit record with the required retention. |

Operational logs are not a financial ledger or a substitute for durable audit
records. Sampling and dropped exports can make them incomplete.

## Instrument the boundaries

1. Give requests and background runs correlation identifiers. Validate and
   bound untrusted incoming identifiers or generate internal ones. Preserve
   context across asynchronous jobs and retries without treating caller-supplied
   context as authority or proof of identity.
2. Record the actual entry point, operation, outcome, duration, and classified
   error where useful. Distinguish scheduler, manual invocation, and replay.
   Name attempts separately from the overall business operation so retries do
   not inflate success totals or hide duplicate effects.
3. Allowlist fields. Redact credentials, cookies, tokens, payment details, and
   unnecessary personal data at emission and export. Do not log entire bodies,
   raw query strings, or exception objects without inspecting their content.
4. Use metrics for rate, errors, and duration; add utilization or backlog for
   constrained resources. Use histograms for latency distributions and inspect
   tail behavior. Counts and averages may supplement distributions.
5. Bound label cardinality: route templates, status classes, and known providers
   are suitable; request IDs, user IDs, raw URLs, and exception text are not.
   Check actual exporter series growth under representative inputs.
6. Trace the expensive or failure-prone boundaries. Use the installed SDK's
   current initialization and context-propagation requirements. Choose sampling
   and retention with cost and diagnostic coverage in mind; a sampled-out trace
   does not prove an operation never ran.

## Alert on actionable symptoms

Tie each alert to user impact or an explicit service objective, with an owner,
time window, minimum traffic where relevant, and a runbook. Include data
freshness or missing-telemetry signals so a broken exporter does not appear
healthy. Avoid inventing a universal failure percentage or observation window.

Draft alert rules locally when asked. Sending a test page, enabling monitoring,
changing retention, or creating recurring work requires the task's authority.

## Verify the telemetry

Exercise success, failure, retry, and timeout paths in an authorized test
environment. Read back emitted events, metric changes, and connected spans.
Check that redaction works and dimensions stay bounded. Simulate exporter loss
without letting diagnostics block the product indefinitely; durable audit
requirements may need a separate, fail-closed policy.

Show the operational questions and evidence that the signals answer them.
Report instrumentation that exists but has not been observed in its collector.
