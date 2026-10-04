---
name: dsp-algorithm-guide
description: >
  Implementation guide for common DSP algorithms. Use when the user asks "implement a
  lowpass filter", "how do I write a compressor", "reverb algorithm", "FFT convolution",
  "pitch shifter", or "oscillator with no aliasing". Trigger on phrases like "biquad
  filter", "state variable filter", "feedback delay network", "phase vocoder",
  "overlap-add", "PolyBLEP", or any request to implement a specific DSP processing block.
---

# DSP Algorithm Guide

Three steps: pick the right algorithm family, address implementation concerns, then verify correctness.

## Step 1 — Identify the algorithm family

| User request | Algorithm family | Recommended starting point |
|---|---|---|
| Lowpass / highpass / bandpass / notch | Biquad (IIR) | Direct Form II transposed |
| High-quality parametric EQ, resonant filter | Biquad cascade or SVF | State Variable Filter (SVF) |
| Shelving / high-shelf / low-shelf | Biquad (Audio EQ Cookbook) | Peaking EQ or shelf coefficients |
| Reverb (algorithmic) | FDN or Schroeder/Moorer | Feedback Delay Network (FDN) |
| Reverb (convolution / IR) | OLA / OLS | Overlap-Add with FFT |
| Compressor / limiter / expander / gate | Level detector + gain computer | RMS or peak detector + knee curve |
| Pitch shift / time stretch | Phase vocoder or granular | Phase vocoder for tonal material |
| Anti-aliased oscillator | BLIT / PolyBLEP / wavetable | PolyBLEP for simple waveforms |
| Spectral processing / analysis | STFT pipeline | Overlap-Add / Overlap-Save |
| Waveshaper / saturation | Memoryless nonlinearity | Soft-clip with oversampling |

## Step 2 — Implementation concerns

Work through this checklist before writing any DSP code:

- [ ] **Stability** — confirm the algorithm's stability condition and check it after every coefficient update (e.g., biquad poles inside unit circle).
- [ ] **Coefficient precision** — use `double` for coefficient computation; cast to `float` for the inner loop only if profiling demands it.
- [ ] **Denormal protection** — use `ScopedNoDenormals`/FTZ where available, or add explicit state clamps/noise around feedback paths.
- [ ] **Latency reporting** — if the algorithm introduces latency (e.g., FFT block size), call `setLatencySamples()` so the host can compensate.
- [ ] **Initialisation** — clear all delay-line and state memory in `prepareToPlay`; never assume zero-init across transport loops.
- [ ] **Parameter smoothing** — ramp filter coefficients or gain values over a block; abrupt changes cause clicks and, for IIR filters, instability.
- [ ] **Oversampling** — nonlinear stages (waveshapers, saturators) need at least 2x oversampling to suppress alias products.

## Step 3 — Test the implementation

- [ ] Frequency response: compare magnitude/phase against the reference formula at multiple frequencies (e.g., plot with Python or MATLAB).
- [ ] Step response: feed a unit step; verify overshoot and decay match the algorithm's expected behaviour.
- [ ] Silence-in → silence-out: verify the output reaches and stays at zero after silent input (no denormal crawl).
- [ ] No NaN / Inf: run with extreme parameter values (fc = 1 Hz, fc = Nyquist − 1 Hz, gain = 0 dB, gain = +24 dB).
- [ ] Impulse response (convolution / reverb): verify IR matches the target via inverse FFT.
- [ ] CPU profiling: measure per-block worst case before shipping; compare against the buffer deadline on the target CPU instead of relying on fixed ns/sample budgets.

See `references/algorithm-cookbook.md` for difference equations, stability conditions, coefficient mappings, and numerical tips for each family.
