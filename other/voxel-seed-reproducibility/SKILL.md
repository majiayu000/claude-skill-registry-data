---
name: voxel-seed-reproducibility
description: Make procedural voxel generation reproducible across chunk order, thread scheduling, reloads, and supported engine versions.
---

# Voxel Seed Reproducibility

## Goal

Ensure world generation results are stable for a documented seed and generator configuration, independent of incidental execution order.

## Inputs to inspect

World seed handling, chunk coordinates, RNG usage, worldgen stages, concurrency model, and saved generator-version metadata.

## Workflow

1. Trace seed derivation from world seed through dimension, chunk coordinates, generation stage, and feature identity. Flag shared mutable RNG streams whose output depends on request order.
2. Define a versioned deterministic seed-mixing function and independent streams per chunk/stage/feature. Specify signed-coordinate handling and integer widths.
3. Audit nondeterministic inputs including unordered-map iteration, floating-point reductions, wall-clock values, platform-specific math, and race-dependent writes.
4. Create golden fixtures for negative and positive coordinates, chunk edges, extreme coordinates, and known world seeds. Compare generated block data or stable hashes.
5. Run chunks in forward, reverse, shuffled, parallel, and reloaded orders. If cross-platform bitwise reproducibility is not promised, document the exact supported boundary.

## Validation checklist

- [ ] The same seed and generator version create the same chunk output under different request schedules.
- [ ] Adjacent chunks agree on borders and feature ownership without duplicate or missing structures.
- [ ] World saves record enough generator/version metadata to preserve compatibility or trigger a deliberate migration.
- [ ] Hash changes are attributable to intentional generator-version changes, not test instability.
- [ ] The seed policy handles negative coordinates without accidental unsigned conversion or overflow.

## Required output

Document the seed contract, stage-specific derivation, golden fixture set, test results, and rules for versioning intentional generation changes.

## Boundaries and failure handling

Do not rely on default RNG behavior remaining stable forever; do not promise cross-platform bitwise determinism unless it is actually tested.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
