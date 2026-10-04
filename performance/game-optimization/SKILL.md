---
name: game-optimization
description:
  "For GameGen projects, diagnose and improve game frame time, memory, loading and responsiveness using measured Godot
  workloads and saved platform budgets for 2D, 2.5D or 3D."
---

# Optimize a measured game workload

Read [shared context](../../references/shared-context.md), ready preferences and existing performance evidence. Identify
the actual symptom and reproduce it before changing quality. Slow movement may come from speed tuning, input response,
collision or animation cadence rather than rendering performance.

## Measure a baseline

Use a real graphical run in the selected renderer with a representative camera, actor count, effects and UI. Record
device, engine/version, resolution, render scale, vsync or frame cap, warmup and sampling duration. Measure frame-time
distribution and spikes as well as average fps. Separate CPU, GPU, memory, loading and input latency where the tools
allow it.

Check movement distance over elapsed time and compare it with animation cadence. Headless or fixed-fps tests are useful
for simulation invariants but not rendering throughput. Avoid concurrent rendering/encoding jobs during a benchmark.
Short desktop samples are diagnostic; sustained thermal and memory checks require the target device and an appropriate
run length.

## Change the actual bottleneck

- 3D: inspect draw calls/material splits, visible triangle count, skinning, lights/shadows, transparency, textures and
  post-processing. Preserve silhouette and deformation while simplifying. Reuse or instance compatible geometry and
  materials.
- 2D: inspect atlas batching, excessive texture switches, transparent overdraw, shader passes, animation updates and
  oversized textures. Fix native-size filtering and pixel scaling without degrading art unintentionally.
- Tile worlds: profile visible/chunk updates, collision/navigation rebuilds and off-screen work. Test seams and
  traversal after chunking changes.
- Hybrid scenes: inspect transparent sorting, billboard updates, sprite shadows and mixed-resolution assets.
- Gameplay: profile expensive update loops and unnecessary per-frame work. Retain deterministic timing and input
  responsiveness.

Set asset budgets from measurements and target requirements, not from a universal polygon number. Reuse source assets
and rebuild only affected exports. Record quality tradeoffs, and compare the same scene/camera before and after each
meaningful change.

Verify the symptom is improved without introducing visual, movement or collision regressions. Report the measurement
conditions and boundary of the conclusion. Stop broadening the optimization when the requested problem and agreed budget
are satisfied.
