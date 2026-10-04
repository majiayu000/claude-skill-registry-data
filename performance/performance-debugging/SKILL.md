---
name: performance-debugging
description: >
  Diagnose a known application's CPU, heap, allocation, lock, and latency regressions with profiles, reproducible baselines, and measured verification.
license: MIT
compatibility: "Optional, runtime-dependent profiler: perf, go tool pprof, py-spy, async-profiler, dotnet-trace, or heaptrack"
metadata:
  source: iuliandita/skills
  date_added: "2026-09-20"
  effort: high
  argument_hint: "[application-or-symptom]"
---

# Performance Debugging

Find and verify the cause of an observed performance regression in a known application or service.
This skill uses hypotheses, representative workloads, runtime profiles, and before/after measurements;
it does not turn a benchmark into a production load test or treat a flame graph as proof without a
reproduced symptom.

## When to use

- Investigating known application CPU, heap growth, allocation, lock contention, GC, throughput, or latency regressions
- Profiling a service, worker, CLI, or library after a reproducible slow path is identified
- Comparing a change against a stable baseline and checking for performance regressions
- Turning a production observation into a safe local or staging reproduction

## When NOT to use

- The broken or slow component is unknown; use **debug-triage** to localize the layer first
- Adding standing metrics, traces, logs, alerts, or dashboards; use **observability**
- Designing benchmark, load-test, soak-test, or capacity-test infrastructure; use **testing**
- Diagnosing database query plans or database engine health; use **databases**
- Changing Kubernetes limits, autoscaling, nodes, or infrastructure topology; use **kubernetes**
- Consumer lag, queue backlog, or redelivery symptoms; use **message-queues**

## Workflow

Copy and track; each step depends on the previous one:
- [ ] 1. Symptom and reproducible baseline captured
- [ ] 2. Hypotheses ranked; discriminating profile chosen
- [ ] 3. Profile captured safely during the symptom
- [ ] 4. One causal factor changed
- [ ] 5. Result measured on the same workload (if it does not improve or a user-facing metric regresses, return to Step 2)

### 1. Define the symptom and baseline

State the operation, input shape, environment, concurrency, warm-up, measurement window, and success
metric. Capture at least throughput plus latency percentiles, error rate, and resource use. Keep the
baseline workload and environment reproducible; compare like with like, including cache state and
data volume. A single elapsed-time run is a hypothesis, not a regression result.

### 2. Form and rank hypotheses

Use the baseline to separate CPU saturation, allocation/GC pressure, heap retention, lock wait,
I/O wait, queueing, and downstream latency. Choose the smallest discriminating profile or trace:
CPU profile for hot compute, allocation profile for allocation rate, heap snapshot for retained
objects, mutex/lock profile for contention, and a trace or dependency timing for waits outside the
process. Capture a profile during the symptom, not only when idle. Read `references/profilers.md`
for the standard tool and representative command per runtime and profile type.

### 3. Capture safely

Use bounded duration, production-safe sampling, and scrub or avoid sensitive request payloads. Keep
the raw profile, workload revision, runtime/build version, and command/configuration needed to repeat
it. Avoid enabling high-overhead instrumentation across a fleet during an incident; sample one
representative instance or reproduce outside production first.

### 4. Change one causal factor

Explain why the profile supports the proposed change, then alter one factor. Do not optimize a
function solely because it is visible in a flame graph: inclusive CPU includes time in callees,
and allocation hotness may be harmless unless it drives GC or memory pressure. Preserve correctness
and track any tradeoff such as memory for CPU or tail latency for throughput.

### 5. Measure the result and guard it

Repeat the same workload after warm-up. Report sample count, median and tail latency, throughput,
errors, CPU, allocation/heap, and the variance or confidence limits available from the runner.
Keep or add a small representative regression benchmark when the project has a benchmark convention;
otherwise record the reproducible command and baseline artifact. When a meaningful user-facing
metric regresses, even if a microbenchmark improves, roll back the change and return to Step 2.

## AI Self-Check

- [ ] The affected application/component and user-visible metric are known, not inferred from an unknown outage
- [ ] Baseline and candidate use the same input, concurrency, data/cache state, warm-up, and duration
- [ ] The profile was captured while the symptom occurred and supports the stated hypothesis
- [ ] CPU, allocation, heap-retention, contention, and external-wait explanations were distinguished
- [ ] The change has one causal purpose and correctness behavior was checked
- [ ] Results report p50 plus p95/p99, throughput, errors, and relevant CPU/memory measures
- [ ] Result variability, sample count, and meaningful regressions are disclosed
- [ ] Production capture or load changes have bounded scope and explicit authorization
- [ ] Cross-cutting agent hygiene applied - see `references/agent-hygiene.md`

## Output Contract

See `references/output-contract.md` for the full contract.

- **Skill name:** PERFORMANCE-DEBUGGING
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to write a performance investigation or review, emit the full
  contract and write it to `docs/local/audits/performance-debugging/<YYYY-MM-DD>-<slug>.md`.
  Interactive diagnosis and implementation remain conversational.
- **Severity scale:** `P0 | P1 | P2 | P3 | info`

## Sources

- [OpenTelemetry instrumentation](https://opentelemetry.io/docs/concepts/instrumentation/) - standing
  signals complement profiles but do not replace a reproduced diagnosis
- [gRPC deadlines](https://grpc.io/docs/guides/deadlines/) - validate realistic time bounds with load
  observations when profiling RPC paths

## Rules

1. **Optimize one variable at a time.** Multi-change patches destroy causal evidence.
2. **Protect the tail.** Always compare p95/p99 and error rate with throughput, not average latency alone.
3. **Do not run disruptive profiling or load against production without explicit authorization.**
