---
name: gpu-upload-staging-ring
description: Review GPU upload staging rings for alignment, wraparound, synchronization, and backpressure under streaming workloads.
---

# GPU Upload Staging Ring

## Goal

Make transient upload memory safe and predictable across frames in flight without stalls, overwrites or unbounded allocations.

## Inputs to inspect

Staging allocator, upload commands, API alignment rules, queue fences, frame-in-flight count, and asset/chunk upload traces.

## Workflow

1. Document allocation size, alignment, offset, wraparound, retirement token and owner for each staging-ring reservation.
2. Verify that a reservation never overlaps bytes still referenced by queued GPU copy commands, including after wraparound and queue delay.
3. Stress bursty asset and chunk uploads with payloads smaller than, equal to, and larger than the ring's contiguous free region.
4. Measure wait time, temporary overflow allocations, fragmentation and peak live bytes; distinguish real GPU backpressure from allocator bookkeeping bugs.
5. Define a policy for full-ring behavior—defer, split, grow within a cap or allocate a fallback—and test the policy under deterministic submission delays.

## Validation checklist

- [ ] Offsets meet device/API copy alignment and are checked for integer overflow.
- [ ] Memory reclamation depends on the correct queue completion signal, not frame index assumptions alone.
- [ ] Large uploads cannot silently overwrite adjacent ring allocations.
- [ ] The full-ring policy is bounded, observable and has a recovery path for stalled queues.

## Required output

A staging allocation timeline, safety invariants, stress-test results, and measured policy for ring exhaustion.

## Boundaries and failure handling

Do not solve upload stalls by unboundedly growing the ring; retain explicit memory caps and expose backpressure.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
