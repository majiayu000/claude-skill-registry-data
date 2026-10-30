---
name: flame-graph-analyzer
description: "Use when a performance regression is traced to a commit but the hot path inside it is unclear. Reads flame graphs from py-spy, async-profiler, Go pprof or clinic.js, finds the hottest frames, tells CPU-bound from lock contention or allocation pressure and suggests the next step."
---

# flame-graph-analyzer

## Overview

Canonical flame-graph reference: [brendan-gregg-flame][bg]. The widest leaf
(bottom of the stack) is the hot path.

[bg]: https://www.brendangregg.com/flamegraphs.html

Each runtime produces flame graphs from its own profiler - py-spy (Python),
async-profiler (JVM), Go's built-in `pprof`, `clinic.js flame` (Node.js), and
`perf` / eBPF (native C/C++/Rust). This skill is **language-agnostic**: it
consumes the profiler output (SVG, JSON, or folded-stacks `.txt`) and surfaces
a hypothesis the engineer can act on. Per-runtime capture commands live in
[references/capturing-and-interpreting-flame-graphs.md](references/capturing-and-interpreting-flame-graphs.md).

## When to use

- A perf regression has been bisected but the introducing commit touches
  multiple functions; the team needs to know which function is the actual hot
  path.
- A load test under `k6-load-testing` or a sibling shows latency growth, but
  the API code hasn't visibly changed - the flame graph reveals the runtime
  cause.
- A production incident showed CPU saturation; the team has captured a profile
  and needs to triage before reducing fleet size.
- An `EXPLAIN ANALYZE` trace suggests CPU is the bottleneck rather than I/O -
  the flame graph confirms.

## How to use

1. Capture a profile under **realistic load** with the runtime's profiler and
   export folded stacks - per-runtime capture commands in [references/capturing-and-interpreting-flame-graphs.md](references/capturing-and-interpreting-flame-graphs.md).
2. Sort the folded stacks by sample count and read the **top 5 leaves** (the
   actual working code, not framework wrappers).
3. Classify each hot leaf's sample-time signature (CPU-bound vs allocator
   pressure vs lock contention vs I/O-misclassified) using the table below.
4. Propose the next step for the dominant leaf; the category-to-fix remediation
   catalog is in [references/capturing-and-interpreting-flame-graphs.md](references/capturing-and-interpreting-flame-graphs.md).
5. Re-profile after the change to confirm the delta, then hand off to
   `perf-budget-gate` to confirm the regression delta closes.

## Reading the hot path

Read the folded stacks (or extract them from the SVG / JSON), sort by sample
count, and identify the top leaves - the bottom-of-stack frames that are the
actual working code, not framework wrappers:

```bash
# top 5 leaves by sample count
sort -k2 -n -r folded.txt | head -5
```

Each hot leaf's sample-time signature points to one category:

| Category | Signature in the flame graph |
|---|---|
| **CPU-bound (hot algo)** | A wide leaf in user code (a regex, a JSON serializer, a hash function). |
| **Allocator pressure** | Wide GC frames (`gc::scavenge`, `Java GC`, `gc.collect`). |
| **Lock contention** | Wide synchronization frames (`pthread_mutex_lock`, `Object.wait`, `parking`). |
| **I/O wait misclassified** | On-CPU profilers don't show I/O blocks; switch to wall-clock profiling. |
| **Reflection / dynamic dispatch** | Wide `reflection.invoke`, `method_missing`, `getattr` chains. |
| **Logging overhead** | Wide `log.format`, `Logger.debug`, serialization for log lines. |

## Worked example

A Node.js endpoint regressed after a bisected commit. Capture under load, then
read the hot path end to end.

Capture (Node.js `clinic.js flame`; other runtimes in the reference):

```bash
npx clinic flame -- node app.js
# drive load against the process, then stop it; clinic writes flame.html + folded stacks
```

Sort the folded stacks and read the top leaves:

```bash
sort -k2 -n -r folded.txt | head -5
```

```
main;handleRequest;serializeJson;JSON.stringify   4521
main;handleRequest;dbQuery;Array.from              2103
main;handleRequest;dbQuery;parseRows               1832
main;authCheck;jwt.verify;crypto.createHash        904
main;handleRequest;serializeJson;Buffer.from       312
```

Emit the analysis:

```markdown
## Flame graph analysis - `flame.html`

**Runtime:** node
**Profile duration:** 30s under load

| Rank | Sample share | Stack (leaf)                          | Category |
|-----:|-------------:|---------------------------------------|----------|
| 1    | 38%          | `JSON.stringify` (in `serializeJson`) | CPU-bound hot algo |
| 2    | 17%          | `Array.from` (in `dbQuery`)           | Allocator pressure |
| 3    | 15%          | `parseRows` (in `dbQuery`)            | CPU-bound hot algo |
| 4    | 8%           | `jwt.verify` (in `authCheck`)         | CPU-bound hot algo (crypto) |
| 5    | 3%           | `Buffer.from` (in `serializeJson`)    | Allocator pressure |

### Hypothesis
The serialization path is load-bearing: rank 1 (`JSON.stringify`, 38%) plus
rank 5 (`Buffer.from`, 3%) account for ~41% of sampled time combined.

### Recommended next step
1. Switch to a streaming JSON serializer (`fast-json-stringify` in Node,
   `orjson` in Python, Jackson's `JsonGenerator` in the JVM) to eliminate the
   intermediate string allocation.
2. Re-profile; expect rank 1 to drop below 10%.
3. Hand off to `perf-budget-gate` to confirm the regression delta closes.
```

More interpreted cases (GC pressure, lock contention, reflection overhead) and
the category-to-fix remediation catalog are in
[references/capturing-and-interpreting-flame-graphs.md](references/capturing-and-interpreting-flame-graphs.md).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Reading the SVG visually only, no quantitative data | Easy to mis-judge widths; biases toward dramatic-looking deep stacks. | Always work from folded stacks; sort by sample count. |
| Profiling under load that is too low | One request per second can't expose contention or allocator pressure. | Profile under realistic load - pair with `k6-load-testing`. |
| Optimizing rank 5 first because rank 1 looks "structural" | Premature optimization; misses the dominant cost. | Always start with rank 1; only descend if rank 1 is genuinely framework-bound (e.g. `event_loop`). |
| On-CPU profiler for an I/O-bound workload | I/O wait doesn't appear; the flame graph shows what's running, not what's waiting. | Use wall-clock / off-CPU profiling for I/O-bound workloads. |
| Single 30-second capture under highly variable load | The sample is unrepresentative. | Capture multiple samples across the load-test duration; merge. |

## Limitations

- **Symbolication.** Without debug symbols, the flame graph shows hex
  addresses. Profile with debug info enabled in CI builds intended for
  analysis.
- **Inlining.** Aggressive inlining (especially in the JVM hot-path optimizer)
  can hide functions; the flame graph shows the post-inlining shape, which may
  not match the source.
- **Sampling vs. tracing.** Sample-based flame graphs give relative weights;
  for absolute timings of specific operations, use a tracer instead.

## References

- [Brendan Gregg's flame graphs page][bg] - canonical reference for the
  visualization technique.
- Per-runtime capture wiring, the remediation catalog, and extended
  interpretation cases: [references/capturing-and-interpreting-flame-graphs.md](references/capturing-and-interpreting-flame-graphs.md).
- py-spy - https://github.com/benfred/py-spy
- async-profiler - https://github.com/async-profiler/async-profiler
- Go pprof - https://pkg.go.dev/net/http/pprof
- Clinic.js - https://clinicjs.org/
- `k6-load-testing` - runner that produces the load under which the profile is
  captured.
