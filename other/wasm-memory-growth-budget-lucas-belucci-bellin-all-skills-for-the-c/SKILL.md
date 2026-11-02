---
name: wasm-memory-growth-budget
description: "Use when WebAssembly linear-memory growth causes pauses or approaches a runtime budget; not for general WASM/native speed comparison."
---

# Wasm Memory Growth Budget

## Purpose

Measure and constrain linear-memory behavior under representative and peak workloads.

## Required inputs

WASM module/runtime, initial/maximum memory, allocation pattern, workload fixtures, memory snapshots, latency.

## Workflow

1. Record initial/maximum pages, growth strategy, allocator, runtime limits, and host copies.
2. Measure warmup, steady-state, peak allocation, repeated load, and recovery from temporary spikes.
3. Test allocation near limit, failed growth, fragmentation-like patterns, and multiple competing instances.
4. Set a justified budget and observable failure path; avoid growth/shrink oscillation when unsupported.

## Verification checklist

- [ ] Page/byte measurements match the runtime model.
- [ ] Peak and repeated workloads are measured.
- [ ] Failed growth cannot corrupt state or leave invalid pointers in use.
- [ ] Budget accounts for instance count and host overhead.

## Required output

A memory profile, growth timeline, budget recommendation, and near-limit regression tests.

## Boundaries and failure handling

WASM linear memory is not total process memory; stress only in an isolated runtime with explicit limits.

When evidence, permissions, or environment details are missing, stop at the supported analysis, record the missing prerequisite, and do not report unexecuted validation as passing.

## Trigger examples

- **Positive:** A WASM plugin pauses when expanding linear memory.
- **Negative:** Comparing native and WASM execution speed with no memory concern.
