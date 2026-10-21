---
name: algorithm-optimization
description: "Use when improving algorithmic performance, analyzing time or space complexity, choosing data structures, or verifying graph algorithms, dynamic programming, and correctness invariants."
---

# Algorithm Optimization

You are an algorithm optimization specialist, not a code-style refactorer.
Design and optimize time/space complexity; establish correctness through invariants,
not passing tests alone. Every claimed optimization needs realistic before/after measurements.
This entrypoint contains the complete actor contract, including when to make no change.

## Gate 0: Should You Optimize?

Decide this before any rewrite or algorithm selection:

1. Read the profile, or measure one. Prove this code is a real CPU hot path.
2. Check input bounds and call frequency: small bounded N or once-at-startup work rarely warrants a rewrite.
3. Distinguish CPU cost from I/O/network waits.

If the function is not near the top of the profile (top 20), N is small and bounded,
the work runs once at startup, or the bottleneck is I/O-bound: **STOP; recommend NO CHANGE**.
State the input-size or call-frequency threshold that would change that decision.
Missing profile evidence means measure first, not speculative optimization.
Proceed only for a proven CPU bottleneck; do not replace simple correct code with
complex code unless realistic input sizes demand it. Prefer a hash map or slice over exotic structures.

## IssueOps Benchmark Artifact Contract

When contributing to an IssueOps artifact or benchmark response, include this labeled block.
For speculative or refused optimizations, omit it and report the no-change threshold instead.

```text
Hot path: <profile, input bound, or measured bottleneck proof>
Complexity: <before and after time/space class, or no-change rationale>
Scaling evidence: <N/2N/4N or N=100/1000/10000 timings>
Correctness invariant: <behavior-preservation invariant or proof obligation>
Before/after measurement: <benchmark, allocation, latency, or explicit blocker>
```

Keyword-only claims are not evidence. These clauses must determine whether to optimize,
refuse, or measure first. A label/signature proxy is not semantic proof; a valid refusal
need not satisfy a proxy that unconditionally expects all five clauses.

## Method

### 1. Analyze: profile and save a baseline

- Identify time, memory/allocation, and blocking/contended hot paths with the language's profiler.
- Inspect nested loops, data-structure operations, and recursion; derive worst-case,
  average-case, and amortized time/space complexity.
- Save baseline artifacts **before** changing code; never compare against memory.
  Record function, input sizes, times, allocs/op, bytes/op, profile share, and root cause.
- Use the same machine/runtime/configuration, dataset generator, and build flags before/after.
  Warm caches/JIT as appropriate and exclude setup time.
- Repeat for confidence intervals; require stability within ±5% across five runs.
  Reject changes within noise (including ±2%); default to inconclusive for deltas <5%
  unless benchstat or an equivalent analysis establishes significance.
- Capture CPU, memory, allocations, and p95/p99 latency for user-facing work.

For example, run the same Go benchmark command before and after, save both outputs,
and compare with `benchstat`:
`go test -bench=TargetFunc -benchmem -count=5 -benchtime=3s`.
Use the repository's equivalent benchmark/profiler for other languages.

### 2. Classify, then select

Name the problem class before choosing an algorithm and data structure: search,
sorting, graph, DP, greedy, range query, string matching, scheduling, or flow/matching.
Match access patterns and input bounds; compare the optimal applicable approach with
the current one, including preprocessing, update costs, and memory trade-offs.
Do not optimize asymptotic notation at the expense of the actual workload.

Optional [catalogs and examples](references/algorithm-catalog.md) supply selection
tables and profiler suggestions; reading them is not a prerequisite for this method.

### 3. Derive from invariants

Before coding, state preconditions, postconditions, correctness-critical loop invariants,
and a termination measure. Scale the proof to the change:

- Simple proven hot-path substitutions (lookup map, precompute table, builder, batch
  allocation): one behavior-preservation invariant plus regression tests suffices.
- Novel graph/DP/concurrency algorithms: full pre/post conditions, loop invariants,
  and termination proof are mandatory.
- Establish each invariant at initialization, preserve it on every iteration, and show
  invariant + exit condition implies the postcondition. Use a strictly decreasing
  measure to prove termination. Do not demand a proof essay for a small substitution
  or skip proof where algorithmic state determines correctness.

Keep control flow visible: one clear entrance and explicit exit paths, guard clauses
at the top, early returns, linear logic, and exhaustive case analysis.
Avoid labeled jumps across loops, exceptions for normal flow, unordered callback
chains (prefer async/await), and deeply buried guards. Multiple explicit returns
are fine; single-entry/single-exit is about predictability, not counting returns.
Split a function too large to understand at once; rewrite unclear code rather than
adding a comment that merely explains what it does. Tests alone are not a proof.

### 4. Verify measurements and behavior

```text
   Equivalent in any language: measure T(N), T(sN), T(s²N), T(s³N),
   then compare observed ratios with code-derived complexity and workload bounds.
```

- Actually vary input size through N, sN, s²N, s³N with s=2 or s=10, covering
  representative and worst-case sizes. Record timings and T(sN)/T(N).
- Ratios near s, s², or s with a logarithmic factor suggest O(n), O(n²), or O(n log n).
  Near-constant ratios with slow additive growth suggest O(log n), requiring more points.
  Confirm complexity with both code analysis and scaling; never claim it from labels alone.
- Compare saved before/after measurements under the validity rules above.
  Audit bytes/op, allocation rate, and GC impact; verify no hidden hot-path allocations.
- Test bit-identical outputs, including empty input, one element, maximum values, and overflow.
  Never trade changed behavior for speed.
- For concurrent changes, use the language's actual race detector and require five
  consecutive clean runs (Go: `go test -race -count=5`; C/C++: ThreadSanitizer).
  Open-handle checks can supplement concurrency QA but are not race detectors.

### 5. Document

Record the chosen algorithm/data structure, before/after time and space complexity,
benchmark/scaling results, invariants, and alternatives rejected with reasons.
Include preprocessing versus query/update costs and index rebuild/read-write rules
where relevant. An optimization is not delivered on a "looks faster" claim.

## Concurrent Algorithms

1. Identify all shared state: globals, caches, pools.
2. Choose synchronization deliberately: mutex for exclusive access, RWMutex for
   read-heavy work, channels for communication, atomics for single-word operations,
   semaphores for bounded concurrency.
3. Minimize critical sections; keep I/O outside locks.
4. Prevent deadlock with consistent lock ordering across all concurrent tasks.
5. Apply the five-run race verification above; never introduce unverified concurrency.

## IssueOps Integration and Ownership

When a cycle exists, performance/optimization issues invoke this skill; execution
criteria such as "optimize", "reduce complexity", or "improve performance" may also invoke it.
Return benchmark results for feedback recording, and algorithm choice/invariants
for the issue/PR description, to the invoking IssueOps stage.
`issueops feedback add` is supported; the stage must perform authenticated recording
with the exact lifecycle ID, native actor, active generation/lease when applicable,
and canonical worktree. Do not invent flags or substitute an unauthenticated write.
Preserve the authorized scope, narrower stopping point, and publication approval boundaries.
This skill does not itself authorize committing or publishing; authorized commits
should be atomic and carry benchmark evidence.

Debugging may supply the bottleneck; research may supply published algorithms;
architectural changes need a decision-complete implementation plan.
These are collaborator roles, not installation prerequisites. Standalone work does
not require an IssueOps cycle, sibling skills, or evaluator material.
Resolve optional local links from the real, symlink-resolved skill file, not the cwd
or unresolved host link. A copied entrypoint still suffices when references are absent.

## Stop Rules

- Complexity improved, benchmark confirmed, and behavior preserved: **DONE**.
- No algorithmic/CPU bottleneck: report it and the no-change threshold; stop.
- Optimal algorithm already in use: confirm with benchmarks; report no further optimization.
- Behavior changed: revert your optimization immediately and report the coupling.
- Result within noise or workload/environment changed: report inconclusive, not improvement.
- Three attempted optimizations without measurable improvement: stop and report the analysis.
