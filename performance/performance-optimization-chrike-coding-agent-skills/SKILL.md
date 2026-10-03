---
name: performance-optimization
description: Runs a narrow, framework-neutral performance experiment. Use only when the request states a concrete performance goal or metric, provides a measured baseline or regression, identifies a bottleneck, or explicitly requests a performance audit or experiment. Do not use for vague speed requests, unknown slow paths or regressions, test design, architecture trade-offs, live browser evidence, generic review, existing tools alone, or automatic profiling and tool setup.
---

# Performance Optimization

## Overview

Own the performance question, not a universal optimization checklist. Establish what is being claimed, measure the relevant behavior, isolate one bottleneck, and compare one hypothesis at a time. The result is an evidence-backed keep, revert, or inconclusive recommendation; it is not silent code, configuration, monitoring, or branch work.

## When to Use

Activate only when at least one of these is explicit in the request:

- a performance goal or metric, such as latency, rendering/loading, query/data access, memory, throughput, or resource use;
- a measured baseline, regression, or other measurement artifact;
- an identified bottleneck or operation to investigate; or
- a request for a scoped performance audit or experiment.

A vague request to “make it faster” is not enough. An unknown slow path or unexplained regression belongs to `debug-systematically` first. Test harness, benchmark seam, fixture, assertion, or acceptance-signal design belongs to `test-strategy`; an unresolved architecture trade-off belongs to `design-codebase`; live browser runtime evidence belongs to `browser-testing-with-devtools`; generic review or readiness belongs to `review-and-finish`.

## Define the Experiment Before Measuring

Write a compact experiment packet before interpreting a result:

- **Claim:** the precise performance assertion to evaluate.
- **Metric:** the unit, statistic, direction of improvement, and relevant percentile or aggregate when the claim needs one.
- **Scope:** the component, endpoint, query, workload, resource, environment, and data state included and excluded.
- **Workload:** representative input, traffic shape, dataset, interaction, or request sequence.
- **Comparison:** the baseline revision, existing behavior, alternative implementation, or other named target.
- **Correctness invariant:** behavior, output, freshness, ordering, precision, error handling, resource safety, or other contract that must remain unchanged.

Select only the applicable lens or lenses. Latency, rendering/loading, query/data access, memory, throughput, and resource use are options, not a universal checklist. Do not impose Core Web Vitals, Lighthouse, RUM/CrUX, fixed budgets, fixed sample counts, fixed time or size limits, or a framework/library recipe when the claim does not require them.

## Web Audit Mode

For a scoped web or browser performance question:

- Identify the framework, rendering model, and project asset/runtime conventions before making stack-specific suggestions.
- When no measurement artifact exists, use source mode: report structural observations as `potential impact` and state that metrics are `not measured`; do not infer LCP, INP, CLS, or another runtime value from source shape.
- When an authorized artifact exists, name its source and keep field, lab, trace, and benchmark evidence distinct; unavailable values remain `UNVERIFIED`.
- Choose only the relevant loading, rendering/input, network/data, or resource lens. Consider resource dimensions or priority, long main-thread work, layout stability, code splitting or third-party loading, caching, or parallel I/O only when tied to the claim and correctness invariant.

## Conditional Checklist

For a web or service performance scope, inspect only the applicable prompts:

- **Loading and resources:** critical resource priority, reserved dimensions, deferred non-critical work, asset format, caching, and third-party cost.
- **Rendering and input:** long tasks, event-handler work, layout thrash or instability, list size, scheduling, and interaction responsiveness.
- **Data and backend:** bounded queries, indexes, pagination, batching, connection or worker saturation, and compression or caching where the claim concerns them.
- **Correctness and evidence:** keep the output, freshness, ordering, error, and resource invariants explicit; tie each observation to its source and label unmeasured items rather than filling a scorecard.

This is a conditional prompt set, not a universal Web Vitals target, bundle budget, sample count, command list, or release gate.

## Measurement Discipline

1. Establish a baseline before evaluating a change. Use the same meaningful method for baseline and comparison, with the same workload, data state, and environment where practical. State any unavoidable difference.
2. Attach every numeric observation to its evidence source and artifact. Distinguish:
   - **Field:** observations from real usage or production-like telemetry;
   - **Lab:** controlled synthetic execution;
   - **Trace:** a profiler, timeline, or other recorded execution trace;
   - **Benchmark:** a repeatable harness run over a named workload; and
   - **Other:** such as a query log, resource sample, or supplied measurement report.
3. Treat field, lab, trace, benchmark, and other evidence as different kinds of evidence. Do not transfer a value or target from one source to another without saying so.
4. If no measurement artifact is available, report a potential bottleneck or potential impact and `not measured`; do not invent a number. Static source patterns, a target fixture, a benchmark definition, an expected result, a source claim, or a proposed command is not live measurement.
5. When the environment permits, repeat comparable runs and record run-to-run variance, noise, caching, warm-up, contention, throttling, and other material conditions. Choose sample counts and decision thresholds for this project and claim; there is no universal gate.

## One Bottleneck, One Hypothesis

Identify one bottleneck supported by the available evidence. If the slow path or regression is still unknown, hand it to `debug-systematically` rather than guessing.

Evaluate one change or hypothesis at a time. Keep the expected mechanism and affected invariant explicit. Do not bundle speculative optimizations, change the workload to favor a result, or treat a structural anti-pattern as a measured bottleneck without evidence.

Correctness is ahead of the metric. A faster result that drops required work, changes semantics, serves stale data, hides errors, or violates the stated invariant is a regression. Implementation and remediation remain with the current implementation owner or the base flow; this owner does not silently edit code or configuration.

## Decision and Recommendation

Recommend exactly one outcome when evidence supports a decision:

- **Keep:** the correctness invariant holds and the measured improvement is supported beyond the observed noise using a project- and claim-specific comparison rule.
- **Revert:** the change regresses performance or correctness, or adds material complexity with no supported benefit under the project’s stated policy. Recommend the revert; do not perform it silently.
- **Inconclusive:** the evidence, artifact, repeatability, environment, or variance cannot distinguish the change from the baseline. Do not present an inconclusive result as a win.

A neutral result inside observed noise is not a keep. Whether it merits a revert or remains inconclusive depends on the project and claim; do not substitute a universal percentage or budget.

## Authorization and Side Effects

Read supplied artifacts as evidence, with sensitive values redacted. Before running a benchmark or project command, resolve its exact target and effects. Obtain action-specific authorization before running anything whose effects are not known, installing or updating tools or dependencies, using `npx`, Lighthouse, CrUX, network or external services, applying production load, setting up monitoring or RUM, writing a persistent report, changing configuration or code, or taking deployment, publication, or branch actions. An explicit performance question does not authorize all of those actions, and this skill does not run them automatically.

## Handoffs

- Unknown slow paths or unexplained regressions → `debug-systematically`.
- Test harness, benchmark seam, fixture, mock, assertion, or acceptance design → `test-strategy`.
- Architecture, ownership, interface, or dependency trade-offs → `design-codebase`.
- Live browser or DevTools evidence → `browser-testing-with-devtools`.
- Generic review or readiness → `review-and-finish`.
- Implementation or remediation → the current implementation owner or base flow.
- Commit, push, merge, discard, deletion, or other Git branch action → `finish-branch`.
- Deployment or publication → an explicitly named owner or host method; do not infer one.

## Report Format

Separate evidence from interpretation and unknowns:

## Observed measurements

List only measurements actually present in an authorized artifact or executed, authorized observation. Include the claim, metric, scope, workload, comparison, evidence source, conditions, sample information, and variance that the artifact supports. If there is no artifact, say `not measured`.

## Inference

Identify the single supported bottleneck and explain how it relates to the claim. Label potential impact and hypotheses as inference; do not turn static analysis, expected output, or a target fixture into runtime evidence.

## Gaps / UNVERIFIED

List missing baseline or comparison artifacts, unknown workload or environment, insufficient repetition, untested correctness invariants, unavailable tools, authorization gaps, and claims that the available evidence cannot settle.

## Recommendation

State `keep`, `revert`, or `inconclusive`, the evidence that supports it, and the owner for any next implementation, measurement, runtime-evidence, readiness, deployment, or branch action. Do not claim performance measurement or improvement when the report contains only potential impact.

## Verification

Before stopping, check that:

- the trigger had an explicit performance goal, evidence, bottleneck, or audit/experiment request;
- the claim packet defines the metric, scope, workload, comparison, and correctness invariant;
- baseline and comparison methods are meaningfully comparable and evidence sources are labeled;
- only one bottleneck and one change or hypothesis are being attributed;
- repeated measurements and variance are reported when the environment permits;
- correctness gates the recommendation and gaps are marked `UNVERIFIED`; and
- no command, tool installation, external service, production load, monitoring setup, persistent write, code/config edit, remediation, or branch action occurred without its own authorization.
