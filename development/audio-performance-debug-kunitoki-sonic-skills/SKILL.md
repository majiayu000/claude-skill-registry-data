---
name: audio-performance-debug
description: >
  Profiling strategy for audio CPU issues — xruns, spikes, and buffer underruns. Use when
  the user reports CPU overload, audio glitches under load, or performance regressions.
  Trigger on phrases like "I'm getting xruns", "my plugin causes CPU spikes", "dropouts
  under high voice count", "audio thread is too slow", "how do I profile my DSP".
  References audio-numerics-review for denormal slowdown and audio-dsp-review for
  lock contention.
---

# Audio Performance Debug

Audio performance requires good worst-case complexity, not average-case — the audio thread fires on a hard deadline every buffer, regardless of what else is happening.

## Step 1 — Identify the symptom

Measure before guessing. Different symptoms point to different root causes.

| Symptom | Measurement approach |
|---------|---------------------|
| Consistent high CPU average | CPU meter in DAW; `perf stat` / Instruments Time Profiler |
| Sporadic xruns / dropouts | Host xrun log; correlate with system events (GC, network, page fault) |
| CPU spikes on note-on | Profile with many simultaneous note-on events; watch for allocation spikes |
| Latency reporting wrong | Log `getLatencySamples()` before and after `prepareToPlay` at varying buffer sizes |
| Gets worse with more voices | Profile with 1 vs 8 vs 32 voices; O(N²) shows quadratic growth |
| Memory bandwidth pressure | `perf mem` / VTune memory bandwidth counter; cache miss rate |

## Step 2 — Locate the hotspot

- [ ] Build a release (optimized) binary before profiling — debug builds are not representative.
- [ ] Use a reproducible test case: fixed buffer size, fixed voice count, looped audio.
- [ ] Attach a profiler to the audio thread specifically, not the whole process.
- [ ] Identify the top-3 hottest functions by exclusive CPU time, not inclusive.
- [ ] Check whether the spike is periodic (every N buffers → container rehash or GC) or random (OS jitter, page fault).

| Platform | Profiler | Notes |
|----------|----------|-------|
| macOS | Instruments — Time Profiler | Filter to audio I/O thread; use "hide system libraries" to focus on your code |
| macOS | Instruments — Allocations | Catch allocations on the audio thread during a session |
| Linux | `perf record -g` + `perf report` | `--call-graph dwarf` for C++ templates; `perf stat` for cache miss ratio |
| Windows | VTune Profiler — Hotspots | Use "Platform Profiler" preset; filter to realtime thread |
| Cross-platform | Tracy | Frame-level instrumentation; zero-cost when disabled; shows per-buffer timing |
| JUCE | `juce::PerformanceCounter` | Inline timer around suspect blocks; logs to console |

## Step 3 — Fix patterns

| Anti-pattern | Why it hurts | Optimization |
|--------------|-------------|--------------|
| O(N²) voice loop | Quadratic growth — 32 voices = 1024 iterations per sample | Restructure to O(N): batch per-voice work, use SIMD across voices |
| Wrong FFT size | Power-of-two FFT on non-power-of-two frames → zero-padding waste | Size FFT to next power-of-two; or use prime-factor FFT (FFTW `FFTW_MEASURE`) |
| Unnecessary buffer copy | `memcpy` of full buffer each callback | Process in-place; pass pointer + length; avoid intermediate staging buffers |
| `std::map` / `unordered_map` lookup on audio thread | O(log N) / amortized O(1) but with cache misses; `unordered_map` rehash = alloc | Replace with `std::array` + index, or a sorted `std::array` with `lower_bound` |
| `unordered_map` insert | Triggers rehash → heap allocation on audio thread | Pre-populate at `prepareToPlay`; never insert during playback |
| Heap allocation on audio thread | `new`/`delete` acquires global allocator lock | Pre-allocate in `prepareToPlay`; use pool or ring buffer; see `audio-dsp-review` |
| First-touch page fault | OS maps physical pages on first write → stall | `prepareToPlay`: allocate AND write to every byte of every buffer |
| Scalar loop over samples | Compiler may not auto-vectorize complex loops | Use JUCE `FloatVectorOperations`, `xsimd`, or explicit SIMD intrinsics |
| Denormal-induced slowdown | Subnormal FP values cause 100× slowdown on x86 | Set FTZ+DAZ in `prepareToPlay`; see `audio-numerics-review` |
| Lock contention | Mutex held by UI thread blocks audio thread | Replace with atomics or SPSC queue; see `audio-dsp-review` |

For anti-pattern code examples and platform profiler workflows see
`references/performance-patterns.md`.
