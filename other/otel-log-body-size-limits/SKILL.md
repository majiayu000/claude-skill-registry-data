---
name: otel-log-body-size-limits
description: "Validate opentelemetry log body size limits with task-specific acceptance criteria, boundary cases, and reproducible evidence."
---

# OpenTelemetry Log Body Size Limits

## Purpose

Establish a verifiable engineering contract for opentelemetry log body size limits. Identify a concrete failure mode, reproduce it safely, and produce evidence that distinguishes expected behavior from hidden state, lost signals, or unsafe recovery.

## Required inputs

OpenTelemetry Collector configuration, receiver/processor/connector/exporter graph, representative synthetic OTLP payloads, resource attributes, exporter status, and sanitized telemetry.

## Workflow

1. Locate the receiver, processor, connector, exporter, extension, and configuration responsible for opentelemetry log body size limits. Record signal types, owners, endpoints, and the exact configuration revision.
2. State the data-plane invariant for opentelemetry log body size limits: what is accepted, transformed, sampled, rejected, queued, or exported, and which identity or attributes must be preserved.
3. Build synthetic telemetry fixtures for normal traffic, malformed/high-cardinality input, and a slow or unavailable downstream destination.
4. Validate configuration syntax and component order, then run the test against the exact Collector distribution and version used by the target environment.
5. Measure accepted, refused, dropped, retried, queued, and exported items separately while observing memory, cardinality, throughput, and latency.
6. Inject one controlled failure and verify bounded backpressure, explicit diagnostics, and recovery without silent loss or unbounded buffering.
7. Record the config diff, signal accounting, resource budget, deployment gate, and rollback path; label any production-only assumptions as pending.

## Validation checklist

- [ ] The receiver-to-exporter path and processor ordering are explicit.
- [ ] Accepted, dropped, refused, retried, delayed, and exported signals are tracked separately.
- [ ] Resource identity, sensitive attributes, and cardinality policies are validated.
- [ ] Queue, retry, and memory bounds are tested under representative load.
- [ ] Stale or missing input is not mistaken for a healthy pipeline.
- [ ] The rollout and rollback instructions reference the same tested config revision.
- [ ] Any external exporter or auth dependency not exercised is marked pending.

## Required output

Produce an observability pipeline audit containing a pipeline map, config diff, signal-loss accounting, resource budget, and rollback-safe rollout plan. Include the target revision/configuration, acceptance criteria, pass/fail/blocked checks, exact command or artifact references, observed limitations, and the smallest justified next action.

## Boundaries and failure handling

Use synthetic or sanitized telemetry. Preserve signal semantics and resource identity across processors, and redact sensitive attributes before export. If a receiver, exporter, or metric source is unavailable, distinguish no input from dropped data and failed export; an empty output is not a success signal.

## Trigger examples

- **Positive:** A telemetry pipeline change needs proof of opentelemetry log body size limits under normal and degraded load.
- **Negative:** A request asks to drop high-volume telemetry silently or raise queue/memory/retry limits without measuring downstream effects.
