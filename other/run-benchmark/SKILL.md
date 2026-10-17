---
name: run-benchmark
description: Measure Lodestone's renderer with its benchmark against the recorded baseline, or deliberately record a new baseline. Use after changes that could affect rendering performance or draw calls, when the "Benchmark draw calls stay within the baseline" test fails, and before finishing renderer work.
---

# Run the Renderer Benchmark

`LodestoneBenchmark` (`Tests/Benchmark`) renders a small city that turns on every renderer feature, along a fixed camera flight, and reports CPU and GPU frame times, per-pass GPU times, draw calls and triangles (see `docs/Testing.md#performance`). The baseline is `Tests/Benchmark/Baseline.json`: its draw calls are gated on every platform, and its timings are the reference GPU's.

## Measure
1. Build Release - Debug timings mean nothing: `cmake --build --preset release --target LodestoneBenchmark`
2. Run it on the GPU, at 1920x1080:
   ```sh
   build/release/Tests/LodestoneBenchmark --baseline Tests/Benchmark/Baseline.json --min-fps 60
   ```
   It prints the report as JSON (`--output <file>` also writes it), fails if draw calls rose above the baseline's or the frame rate is under `--min-fps`, and compares timings with the baseline's when the baseline was recorded on the same GPU at the same size - warning about slowdowns over 10%
3. Laptops: plug in power and close heavy programs; numbers vary by a few percent between runs. Run twice before believing a regression

## When draw calls rose
The test `Render.Benchmark draw calls stay within the baseline` runs the benchmark's probe frames on lavapipe. Draw calls don't depend on the GPU, so a rise is a real change: culling broken, extra passes, more pipelines per material. Find the cause first. Only if the rise is meant (a new pass, a richer benchmark scene), record a new baseline.

## Record a new baseline
Only on purpose, and on a real GPU:
```sh
build/release/Tests/LodestoneBenchmark --frames 300 --record Tests/Benchmark/Baseline.json
```
Commit it with a message saying why the baseline changed, the GPU it was recorded on, and the old and new draw calls and frame times. Changing the benchmark scene (`BenchmarkScene.cpp`) or its camera flight always needs a new baseline.
