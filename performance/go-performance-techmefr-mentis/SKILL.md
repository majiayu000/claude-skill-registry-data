---
name: go-performance
description: "Use when optimising or reviewing the performance of Go code: choosing what to measure (pprof, execution traces, escape analysis, benchmarks with testing.B.Loop), reducing allocations (preallocated slices and maps, strings.Builder, retained backing arrays, sync.Pool), and judging garbage collector settings."
---

# go-performance

Step 6 of the pipeline (`WORKFLOW.md`), for the Go changes made because something is slow or large. The
premise: **an optimisation without a measurement is a guess, and the Go toolchain ships the measuring
tools**. Memory and CPU limits in containers are `go-container-runtime` §2; correctness rules are
`go-conventions`; generic anti-patterns for tests are `testing-anti-patterns`.

## When
- A change is justified by speed, latency or memory.
- A benchmark is written or reviewed.
- Allocation-heavy code (loops building slices, maps or strings) is written.
- A garbage collector setting is changed, or a toolchain upgrade changes timings.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Measure first: profiles, traces, escape analysis, benchmarks | before any change made for performance, or a benchmark is written | [`01-measure.md`](./references/01-measure.md) |
| 2 | Allocation: preallocation, string building, retained arrays, pools | allocation-heavy code is written or a profile shows allocation | [`02-allocation.md`](./references/02-allocation.md) |
| 3 | Garbage collector: GOGC, toolchain changes, re-measuring | a collector setting is touched or a toolchain is upgraded | [`03-gc.md`](./references/03-gc.md) |

## Output / checkpoint
A before and after number from the same benchmark or profile accompanies the change, taken with the same
toolchain and settings, and the change is kept only if the number moved. A "faster" claim with no number is
not verified.

## Guardrails
- Never optimise from reading alone (§1.1).
- Never introduce a pool, a hand-rolled buffer or unsafe code without a profile pointing at it (§2.4).
- Versions: each rule names its Go version. Nothing was run while writing this block.

## Origin
Rewritten from the Go diagnostics guide, garbage collector guide, release notes, `testing`, `strings` and
`sync` package documentation, the slices article and the language specification (CC-BY-4.0 text, BSD-3
code), read 2026-10-08. Overlaps with `skills/go-conventions` (2026-10-19); cross-referenced, not merged. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
