---
name: gpu-readback-stall-audit
description: Locate synchronization stalls caused by CPU readback of GPU resources and design bounded asynchronous alternatives.
---

# GPU Readback Stall Audit

## Goal

Avoid unnecessary CPU-GPU round trips while preserving correctness for picking, screenshots, diagnostics and gameplay queries.

## Inputs to inspect

Readback callsites, copy queues, fences, staging buffers, consumer timing, GPU captures and CPU wait traces.

## Workflow

1. Inventory each GPU-to-CPU readback and record its required freshness, data volume, call frequency and consumer deadline.
2. Trace the copy, queue synchronization and CPU mapping path to distinguish actual GPU latency from wait placement and buffer reuse issues.
3. Evaluate asynchronous readback, delayed results, reduced resolution, region-of-interest copies, GPU-side reduction or avoiding the readback entirely.
4. Test ring-buffer exhaustion, repeated requests, frame cancellation, resize and shutdown while reads remain in flight.
5. Measure wait duration, result age, bytes transferred and missed deadlines; keep the least complex approach that meets semantic requirements.

## Validation checklist

- [ ] The consumer's maximum acceptable result age is explicit.
- [ ] CPU code never maps/reads a staging region before the corresponding GPU completion signal.
- [ ] Repeated requests cannot overwrite a buffer that is still being filled or consumed.
- [ ] An asynchronous redesign preserves result ordering or labels stale/out-of-order results appropriately.

## Required output

A readback inventory, synchronized timing evidence, candidate comparison and chosen readback contract.

## Boundaries and failure handling

Do not silently return stale data to gameplay systems that require current state; distinguish asynchronous diagnostics from authoritative queries.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
