---
name: analyze-performance-profile
description: "Use when parsing engine profiler traces (CPU frame time, GPU time, GC spikes) to pinpoint performance bottlenecks and recommend fixes."
---

## 1. Overview

Parse profiler traces (CPU/GPU/GC/draw calls) to identify hotspots and produce a prioritized optimization roadmap with estimated ms savings.

## 2. Core Pattern

1. **Budget Baseline**: Target budget by platform/FPS (e.g., 60 FPS = 16.7ms).
2. **Parse Frame Time**: CPU (Game Logic, Physics, AI, Rendering, GC), GPU (Draw Calls, Vertex, Pixel, Compute).
3. **Hotspot Ranking**: Find over-budget functions; rank by total time impact, not peak duration.
4. **Optimization Roadmap**: Propose fix + expected savings (ms) per hotspot.
5. **Export**: Write to `{TARGET_FOLDER}/docs/profiler_analysis.md`.

## 3. Interaction Protocol

* Frame time > budget → warn, proceed with analysis.
* Single hotspot > 40% frame time → flag as critical priority.
* After all P0 fixes, still over budget → notify: build fails performance targets.
* Incomplete/malformed data → request valid traces before proceeding.

## 4. Red Flags

Frame time > 2x budget · GC spikes > 10ms · Draw calls > 50% over budget · Single hotspot > 40% frame time

## 5. Output Contract

Target: `{TARGET_FOLDER}/docs/profiler_analysis.md`. Input: profiler data + platform budgets. Output: bottleneck rankings + optimization recommendations with projected savings.
