---
name: apple-runtime-performance-proof
description: Prove Apple app performance with runtime evidence. Use when diagnosing CPU, memory, launch, energy, responsiveness, or child-process behavior.
license: MIT
metadata:
  author: "coryparrry"
  version: "0.1.0"
  last-updated: "2026-08-30"
  last-reviewed: "2026-08-30"
  apple-docs-reviewed: "2026-08-30"
---

# Apple Runtime Performance Proof

Turn performance reports into reproducible, bounded claims. Code inspection creates hypotheses; it does not prove runtime behavior.

## Evidence contract

Bind every claim through this chain:

`source revision → built/installed artifact → executable UUID/hash → live PID and helpers → scenario → measurement window`

If a link is missing, stop at that boundary. A successful build does not prove which app was measured.

Record source; build/SDK/architecture/version; installed executable and symbols; process tree; device/OS/sandbox; representative data; tool, trace, and window.

Read [references/evidence-binding.md](references/evidence-binding.md) for the provenance record, child/provider attribution, and source, artifact, runtime, sandbox, provider, configuration, and harness boundaries.

## Workflow

1. Define a user-visible, falsifiable claim and correctness guardrail.
2. Bind the exact source, artifact, process tree, environment, and scenario.
3. Capture a baseline before editing; choose the instrument from the symptom.
4. Correlate semantic signposts with app and child/provider activity.
5. Make one evidence-supported change.
6. Repeat the same scenario on the bound new artifact and compare representative samples.
7. Report the causal interpretation and every remaining evidence boundary.

Temporal overlap does not prove causation. Measure app and provider work; distinguish fewer invocations, lower provider cost, and reduced waiting.

Use privacy-safe `OSSignposter` intervals for semantic operations. MetricKit metric reports are aggregated/version-dependent, while diagnostic reports are event-based; neither proves one local change by itself.

Read [references/measurement-playbook.md](references/measurement-playbook.md) for tool routing, signposts, comparable runs, XCTest metrics, MetricKit interpretation, and minimum proof by claim type.

## Completion

Deliver the exact claim, identity chain, comparable before/after evidence, child/provider correlation, correctness guardrails, reproduction artifacts, and uncertainty. Treat a source, sandbox, provider, configuration, or harness limit as a result rather than inventing runtime proof.

Consult [references/apple-documentation.md](references/apple-documentation.md) for reviewed Apple API anchors and refresh conditions.

## Review

- Last updated: 2026-08-30
- Last reviewed: 2026-08-30
- Apple documentation reviewed: 2026-08-30

Runtime performance measurement, signposting, XCTest metrics, MetricKit, and process-attribution guidance was reviewed against Apple evidence surfaced through Xcode MCP `DocumentationSearch`.

[Apple documentation evidence](references/apple-documentation.md)
