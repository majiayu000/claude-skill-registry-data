---
name: asset-bundle-size-budget
description: Measure and govern per-bundle and total asset size using dependency attribution, compression metrics, duplication analysis, and platform budgets.
---

# Asset Bundle Size Budget

## Goal

Control download size, storage, patch cost and runtime memory without degrading required content or silently excluding dependencies.

## Inputs to inspect

Bundle manifests, uncompressed/compressed sizes, asset dependency graph, platform constraints, delivery groups and patch reports.

## Workflow

1. Define separate budgets for installed size, download size, peak extraction space, patch size and runtime-resident memory; identify their different accounting boundaries.
2. Attribute bundle bytes by asset, content type, dependency group and duplicate payload, including shared dependencies that appear in multiple bundles.
3. Measure compression ratio and build time on representative assets; check whether poor compression is due to already-compressed formats or packaging overhead.
4. Evaluate changes such as deduplication, optional downloads, texture/audio quality tiers or bundle partitioning against loading latency and gameplay requirements.
5. Add a CI size-delta report with explicit thresholds and require explanation for intentional budget changes; test that every required dependency remains available.

## Validation checklist

- [ ] Compressed and uncompressed sizes are not mixed in one budget without labeling.
- [ ] Shared assets are not falsely charged or omitted from totals without defining accounting rules.
- [ ] Budget reductions preserve runtime dependency closure and required platform variants.
- [ ] Reports identify the largest contributors and explain regressions rather than showing only a total number.

## Required output

A bundle budget table, top-contributor report, size-change thresholds and validation that package dependencies remain complete.

## Boundaries and failure handling

Do not shrink packages by removing assets blindly; validate load paths, optional-content semantics and visual/audio impact.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
