---
name: game-perf-profiling
description: "Profiles game builds against frame-time, memory, GPU draw-call, and GC-spike budgets using Unity Profiler + Profile Analyzer + Performance Testing package and Unreal Insights + stat commands. Establishes pass/fail thresholds (16.6 ms at 60 fps, 33.3 ms at 30 fps), writes automated performance regression tests that run in CI, and emits a structured budget report per SKU. Use when a title must hit a declared frame-time or memory budget before a milestone gate or platform-cert submission, or when a recent change needs a performance regression check."
metadata:
  keywords: "game-performance, frame-time, profiling, unity-profiler, profile-analyzer, performance-testing, unreal-insights, gc-spike, draw-calls, overdraw, ci-regression"
  version: "1.4.17"
---

# game-perf-profiling

## Overview

Game performance QA verifies that a build meets its declared budgets across
every target SKU before milestone sign-off or platform-cert submission.
The performance category (category 4 in the
platform-cert-overview-reference test-category taxonomy)
covers frame-time, memory, GPU, thermal, and battery axes. This skill covers
the two dominant engine stacks: Unity and Unreal Engine.

**Frame-time budget anchors** (from
platform-cert-overview-reference):

| Target frame rate | Frame-time budget |
|---|---|
| 60 fps | 16.67 ms per frame |
| 30 fps | 33.33 ms per frame |

Measuring averages is an anti-pattern: spikes hide in averages and cause
cert failures. Measure p99 (99th-percentile frame time) and sustained-window
maximums.

## Step 1: Unity - Capture with the Profiler

Open the Profiler via **Window > Analysis > Profiler** (`Ctrl+7`) and enable
the CPU Usage, GPU Usage, and Memory modules for a frame-time pass. Save the
capture as a `.data` file (Profiler toolbar > Save) and retain it alongside
any Profile Analyzer `.pdata` export - the `.pdata` file does not embed the
original profile frames. Module-by-module capture detail, GPU-module platform
constraints, and Profile Analyzer setup are in
[references/unity-profiler.md](references/unity-profiler.md).

## Step 2: Unity - Analyze with Profile Analyzer

Profile Analyzer compares two captures side by side, which the standard
Profiler cannot. Open it via **Window > Analysis > Profile Analyzer**, then run
the regression check:

1. Load the **baseline** `.data` file as the left dataset.
2. Load the **candidate** `.data` file as the right dataset.
3. Compare median and p99 frame times per marker against the budget.
4. Flag any marker whose p99 exceeds the per-frame budget allocation.

## Step 3: Unity - Automated regression with Performance Testing package

Add `"com.unity.test-framework.performance": "3.0.3"` to `Packages/manifest.json`
and reference `Unity.PerformanceTesting` in your assembly definition
([docs.unity3d.com/Packages/com.unity.test-framework.performance@3.0/manual/index.html](https://docs.unity3d.com/Packages/com.unity.test-framework.performance@3.0/manual/index.html)).

### Measure.Method (Edit Mode or Play Mode)

```csharp
[Test, Performance]
public void PathfindingCost_UnderBudget()
{
    Measure.Method(() => pathfinder.FindPath(start, goal))
        .WarmupCount(5)
        .MeasurementCount(20)
        .IterationsPerMeasurement(10)
        .Run();
}
```

- `WarmupCount(n)`: executes the method n times before recording to remove
  initialization overhead.
- `MeasurementCount(n)`: number of samples recorded; default is 7; 20+
  improves stability.
- `IterationsPerMeasurement(n)`: repeats the code within each measurement to
  extend execution time above the 1 ms sensitivity floor.

### Measure.Frames (Play Mode)

```csharp
[UnityTest, Performance]
public IEnumerator CombatScene_FrameTime_UnderBudget()
{
    yield return Measure.Frames()
        .WarmupCount(5)
        .MeasurementCount(60)
        .Run();
}
```

Target standard deviation below 5%; avoid measurements under 1 ms due to
environmental sensitivity.

Decorate tests `[Test, Performance]` for Edit Mode or `[UnityTest, Performance]`
for Play Mode coroutines. View results via **Window > Analysis > Performance
Test Report**.

### GC-spike detection

Enable the `ProfilerMarkers` method on `Measure.Method` to target
`GC.Alloc` markers specifically:

```csharp
Measure.Method(() => SpawnWave())
    .ProfilerMarkers("GC.Alloc")
    .MeasurementCount(20)
    .Run();
```

A passing frame should produce 0 bytes of GC allocation in hot gameplay
paths. Any non-zero sample is a regression candidate.

Disable VSync in Project Settings and remove cameras not needed for the
measurement to keep results consistent between runs.

## Step 4: Unreal - Stat commands for first-pass triage

Unreal Engine stat commands are entered into the PIE console while the
game runs
([dev.epicgames.com/documentation/en-us/unreal-engine/stat-commands-in-unreal-engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/stat-commands-in-unreal-engine)):

| Command | Shows |
|---|---|
| `stat fps` | Frames per second counter |
| `stat unit` | Frame, Game thread, Draw (render thread), GPU, RHIT, and DynRes times; recommended starting point |
| `stat gpu` | GPU statistics for the frame |
| `stat scenerendering` | General rendering statistics; entry point for rendering bottleneck triage |
| `stat game` | How long the various gameplay ticks are taking |
| `stat memory` | Memory usage by subsystem |

`stat unit` is the first command to run on any new build: it identifies
whether the bottleneck is game-thread, render-thread, or GPU, and measures
how long the video card takes to render the scene. Run in a non-debug build
for accurate results.

## Step 5: Unreal - Deep analysis with Unreal Insights

When `stat` triage is not enough, capture a full trace with Unreal Insights.
Launch it from the Editor's **Trace/Insights Status Bar Widget** or the
prebuilt `Engine\Binaries\[Platform]\UnrealInsights.exe` binary, then work the
CPU/GPU/Memory/Networking trace channels in the **Timing Insights** and
**Memory Insights** views. The trace channels, the live Session Browser, and
the two primary views are detailed in
[references/unreal-insights.md](references/unreal-insights.md).

## Step 6: GPU draw-call and overdraw budgets

### Unity

The GPU Usage module's Hierarchy view shows DrawCalls count and GPU ms per
rendering pass (see [references/unity-profiler.md](references/unity-profiler.md)).
Typical mobile budget: under 100 draw calls per frame; PC/console budget
is title-specific but PostProcess and Transparent passes are common
over-budget culprits.

Overdraw (multiple pixels written per screen pixel per frame) is visible
when Transparent pass GPU ms is disproportionate to scene complexity.
Reduce by: lowering particle counts, using depth pre-pass, culling
off-screen transparency.

### Unreal

Run `stat scenerendering` to surface general rendering statistics as the
entry point for rendering bottleneck identification. Follow with `stat gpu`
to get per-pass GPU time, then use the GPU Visualizer
(`ProfileGPU` console command) for a hierarchical breakdown of GPU passes
to isolate overdraw-heavy translucent passes
([dev.epicgames.com/documentation/en-us/unreal-engine/gpu-profiling-in-unreal-engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/gpu-profiling-in-unreal-engine)).

## Step 7: CI regression gate

### Unity

Run Performance Testing package tests in a headless Unity batch session:

```bash
unity -batchmode -runTests -testPlatform StandaloneWindows64 \
  -testResults results.xml -projectPath .
```

Parse `results.xml`; fail the build if any `PerformanceMeasurement` sample
set has a median or p99 exceeding the declared threshold. A zero-tolerance
`GC.Alloc` assertion on hot paths is a recommended gate: one stray allocation
per frame compounds to hundreds of KB/s under sustained play.

For stable CI numbers: disable VSync, remove unused cameras, set a fixed
Quality level, and disable hardware reporting in Player Settings.

### Unreal

Unreal Automation System (see
unreal-automation-system) exposes a
`PerformanceCapture` test type. Combine with a CI step that launches Insights
in server mode, runs the target map for N frames, exports the trace, and
compares the exported GPU/CPU frame time histogram against stored baselines.

## Budget report template

Emit one row per profiled scenario per SKU:

| Scenario | SKU | Metric | Budget | Measured (p50) | Measured (p99) | Status |
|---|---|---|---|---|---|---|
| Combat encounter | PC High | Frame time | 16.67 ms | 11.2 ms | 18.4 ms | FAIL p99 |
| Combat encounter | PC High | GC alloc/frame | 0 B | 0 B | 128 B | FAIL p99 |
| Open-world traversal | PC High | Frame time | 16.67 ms | 13.1 ms | 15.9 ms | PASS |

A FAIL on p99 triggers a regression investigation before milestone sign-off.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Averaging frame time across a level | Spikes hide in averages and cause cert failures | Use p99 and sustained-window maximums |
| Profiling with Graphics Jobs enabled in Unity | GPU module is disabled; no GPU data collected | Disable Graphics Jobs before capture |
| GC alloc tolerance in hot paths | Compounds to MB/s under sustained play | Assert 0 B per frame in CI on hot paths |
| Running perf tests in debug builds (Unreal) | Inaccurate results; use non-debug builds | Profile in Development or Shipping builds |
| Single-device perf sign-off | Low-end SKU (Series S, Switch handheld) is the binding constraint | Run budget checks on every SKU in the compatibility matrix |

## Limitations

- Unity GPU profiling: Vulkan (Android, Linux, Windows), Metal (iOS/macOS),
  and WebGL are not supported; only DirectX 11/12 (Windows) and OpenGL
  (Linux) work
  ([docs.unity3d.com/Manual/ProfilerGPU.html](https://docs.unity3d.com/Manual/ProfilerGPU.html)).
- Unity Memory module detailed object statistics are unavailable in release
  builds
  ([docs.unity3d.com/Manual/ProfilerMemory.html](https://docs.unity3d.com/Manual/ProfilerMemory.html)).
- Profile Analyzer `.pdata` files do not embed original Profiler frames;
  retain `.data` files alongside them
  ([docs.unity3d.com/Packages/com.unity.performance.profile-analyzer@1.2/manual/index.html](https://docs.unity3d.com/Packages/com.unity.performance.profile-analyzer@1.2/manual/index.html)).
- Sony TRC and Nintendo Lotcheck thermal/battery performance gates are
  NDA-gated; consult the developer portal for current requirement numbers.
  Cited by stable ID "Sony TRC" and "Nintendo Lotcheck" per
  `docs/PLUGIN_AUTHORING.md` Step 4 fallback.
- Godot engine performance tooling is out of scope; see
  godot-gut-tests for that engine's test
  framework.
