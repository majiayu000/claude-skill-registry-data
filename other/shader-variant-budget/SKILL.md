---
name: shader-variant-budget
description: Control shader permutation growth by measuring variant dimensions, build cost, cache usage, and runtime selection requirements.
---

# Shader Variant Budget

## Goal

Keep shader permutations bounded and predictable without removing visually or functionally required rendering features.

## Inputs to inspect

Shader source and include graph, permutation defines, material features, build logs, pipeline cache metrics, and target hardware.

## Workflow

1. Enumerate all compile-time switches and their owners; separate true structural variants from values better represented as uniforms, specialization constants or data.
2. Estimate theoretical permutation count and compare it with variants actually requested by representative materials, scenes and platform configurations.
3. Measure shader compilation duration, binary/cache storage, startup warmup, and first-use stutter for clean and incremental builds.
4. Identify redundant or mutually exclusive combinations, then reduce the space through constraints, feature grouping or runtime parameters with a quality/performance comparison.
5. Add a CI report for variant-count deltas and compile-budget overruns; preserve a small representative material matrix for regression coverage.

## Validation checklist

- [ ] Every removed permutation has a verified replacement with equivalent required behavior.
- [ ] Worst-case build and runtime demand are measured separately from theoretical combinatorics.
- [ ] Cache keys include all semantics-affecting options and exclude irrelevant build noise.
- [ ] Variant budgets have explicit thresholds and report the source of growth.

## Required output

A permutation inventory, before/after build and cache metrics, retained variant matrix, and CI regression rule.

## Boundaries and failure handling

Do not collapse variants solely to reduce counts when it changes shader behavior, precision, target support or material correctness.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
