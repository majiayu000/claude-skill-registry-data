---
name: 3d-renderer-development
description: "Use when designing, implementing, or debugging a software 3D renderer, whether the target is a CPU rasterizer, ray tracer, or a bounded graphics pipeline to define coordinate conventions and a minimal image-producing slice, then verify projection, clipping, depth, and shading with deterministic scenes. Trigger for renderer projects or changes to geometry-to-image behavior."
---

# 3D Renderer Development

## Overview

This skill applies when designing, implementing, or debugging a software 3D renderer, whether the target is a CPU rasterizer, ray tracer, or a bounded graphics pipeline. Its intended outcome is to define coordinate conventions and a minimal image-producing slice, then verify projection, clipping, depth, and shading with deterministic scenes.

## When to Use

### Preserved source section: When to Use

Use when the project transforms 3D geometry into a 2D image or implements a rendering pipeline. Select one explicit rendering approach and target rather than mixing rasterization, ray tracing, and GPU execution prematurely.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Safety and Verification

Bound image dimensions, mesh sizes, recursion or ray depth, and allocation. Validate external mesh and scene data before use. Do not claim visual correctness from a successful build alone; retain reproducible scenes, expected properties, and representative image comparisons.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Target language, runtime, output format, and whether execution is CPU-only or graphics-API based.
- Required primitives, camera model, color space, and image dimensions.
- Performance and memory constraints plus any reference images or expected scenes.

## Instructions

### Preserved source section: Procedure

1. **Define conventions.** Specify handedness, axis directions, vector/matrix layout, units, clip-space range, and color representation. Add small tests for the conventions.
2. **Build one visible slice.** Start with a camera and a single triangle or analytic primitive that produces a saved image. Keep scene parsing and presentation separate from geometry calculations.
3. **Implement the pipeline in order.** For rasterization, transform vertices, clip against the view volume, divide by perspective, map to pixels, rasterize coverage, interpolate attributes correctly, and resolve depth. For ray tracing, test ray generation, intersections, nearest-hit selection, and a simple shading rule.
4. **Make edge behavior explicit.** Handle degenerate triangles, near-plane crossings, invalid coordinates, empty scenes, and depth ties without unbounded loops or invalid memory access.
5. **Add deterministic fixtures.** Use tiny scenes that isolate camera projection, back/front ordering, clipping, winding, and color. Compare exact values for math and bounded pixel differences for images.
6. **Profile only after correctness.** Measure the actual bottleneck, preserve a simple reference implementation, and optimize one stage at a time.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Output and Acceptance

Report the implemented rendering subset, coordinate conventions, supported inputs, tests or reference images, performance limits, and unsupported features. Accept the slice only when deterministic tests cover its geometry and the rendered output matches stated expectations within declared tolerances.

## Output Format

### Preserved source section: Output and Acceptance

Report the implemented rendering subset, coordinate conventions, supported inputs, tests or reference images, performance limits, and unsupported features. Accept the slice only when deterministic tests cover its geometry and the rendered output matches stated expectations within declared tolerances.

## Validation Checklist

### Preserved source section: Safety and Verification

Bound image dimensions, mesh sizes, recursion or ray depth, and allocation. Validate external mesh and scene data before use. Do not claim visual correctness from a successful build alone; retain reproducible scenes, expected properties, and representative image comparisons.

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

4. **Make edge behavior explicit.** Handle degenerate triangles, near-plane crossings, invalid coordinates, empty scenes, and depth ties without unbounded loops or invalid memory access.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Report the implemented rendering subset, coordinate conventions, supported inputs, tests or reference images, performance limits, and unsupported features. Accept the slice only when deterministic tests cover its geometry and the rendered output matches stated expectations within declared tolerances.
