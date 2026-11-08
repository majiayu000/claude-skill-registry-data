---
name: telemetry
description: Design, implement, or review application telemetry instrumentation.
---

# Telemetry

Make application behavior observable with signals whose meaning, privacy, and delivery can be established. This skill covers instrumentation, not analytics queries or recurring operational reviews.

Use the repository's telemetry APIs and collection policies. Adding instrumentation within that contract does not require a new approval at each call site. Introducing a provider or expanding collection beyond approved data and populations requires separate authorization.

## Choose the signal

Name the operational or product question before adding a signal. Reuse existing observations when they answer it.

| Question | Signal |
| --- | --- |
| What action or outcome occurred in a product flow? | Product event |
| How often, how slow, how stale, or how saturated? | Aggregate metric |
| What failed, and what context explains it? | Structured log or error report |
| Where did time or failure accumulate across operations? | Trace with propagated context |

Complementary signals can serve different consumers; avoid duplicates that answer the same question.

For metrics, use counters for occurrences, gauges for current levels, and histograms or distributions for sample spreads. Follow the pipeline's aggregation semantics. Define latency endpoints explicitly: a completed request does not establish that the result was visible or interactive. Use a monotonic clock for elapsed time within a process.

## Define ownership and meaning

- Give each signal a stable meaning, emission point, and counting unit: user action, operation, attempt, session, or process. Follow existing names and field types. Make units and missing-value behavior explicit; unknown is not success or zero.
- Emit where the fact becomes authoritative. The UI owns interactions and presentation; the layer committing a mutation owns its outcome. A request to perform an action is not its completion.
- Reuse shared builders and authoritative domain events. Avoid a parallel telemetry state machine that reconstructs facts across callbacks. Add missing facts to the source event when appropriate; otherwise omit unsupported fields. Keep necessary timing or deduplication state scoped to the operation.
- Carry existing request, operation, trace, and session context across boundaries. Do not invent placeholder identities or assume one container has only one session. Correlation identifiers belong in supported event or trace fields, not metric dimensions.
- Preserve counting semantics across relevant retries, cancellation, timeout, resume, reconnect, and recovery paths. Separate internal attempts from user actions. Reject stale callbacks and duplicate terminal emissions without suppressing legitimate new operations. Do not rely on a UI component remaining mounted to finish a backend lifecycle.

## Protect data and application behavior

- Classify values by who can supply them. Names, paths, URLs, exception messages, and identifiers can contain or reveal sensitive information. Prefer bounded enums and aggregates; do not collect secrets or raw content merely because a restricted field exists.
- Preserve consent, opt-out, retention, and access controls. Use sensitive fields only through an approved route for an eligible population. Hashing is not automatic anonymization or permission to collect; reversible encoding does not change classification.
- Keep metric dimensions bounded, including their combinations. Do not use user IDs, raw error text, timestamps, or paths as tags. Bound payload size and aggregate or sample hot paths. Sampling must preserve the intended measurement or make its limits explicit.
- Ordinary telemetry failures must not change the application result or block critical work. Preserve bounded buffering, retries, and shutdown flushing. Report exporter failures through rate-limited diagnostics that do not recursively use the failing exporter. Required audit records may have a different failure contract.
- Disabled collection should avoid telemetry-only expensive work. Local debugging must respect the same sensitive-data boundaries; it is not permission to enable remote collection.

## Establish the contract

For changed paths, assert the emitted payload and expected counts, including relevant terminal outcomes and retry or recovery cases. Check context propagation, units, and field absence as well as presence. Exercise disabled collection and transport failure when the change affects those paths.

For encoded fields, serializers, exporters, schemas, routing, or collector changes, read [Payloads and delivery](references/payloads-and-delivery.md). That reference covers final-wire privacy checks, compatibility ordering, and destination evidence.

Completion means the intended question is answerable within the supported population, focused evidence establishes the changed contract, and instrumentation preserves application behavior. Distinguish local emission evidence from downstream arrival. If destination verification is unavailable or outside scope, report that limit without claiming delivery or expanding access.
