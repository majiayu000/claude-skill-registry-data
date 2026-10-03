---
name: audio-numerics-review
description: >
  Reviews audio DSP code for numerical correctness. Use when the user asks to review,
  audit, or check DSP code for correctness issues — filters, feedback loops, fixed-point
  arithmetic, accumulation loops, or any numeric computation in audio code. Trigger on
  "check this filter for NaN", "why does my reverb blow up?", "is this numerically
  stable?", "why do I hear DC in my output?". Pairs with audio-dsp-review (realtime
  safety); this skill covers numeric correctness. Flag issues proactively.
---

# Audio Numerics Review

Floating-point is not real math. IEEE 754 edge cases — denormals, NaN propagation,
catastrophic cancellation, precision loss — silently produce wrong audio output without
crashing. You won't find them with a debugger; you find them by knowing where to look.

## Step 1 — Find numeric-critical paths

Locate every function doing floating-point or integer DSP: filter state loops, feedback
delay lines, envelope followers, RMS/energy accumulators, pitch detectors, fixed-point
paths (CMSIS-DSP, SIMD int16/int32), any division whose denominator may be zero.

## Step 2 — Scan for violations

| Violation | Where to look | Symptom |
|-----------|--------------|---------|
| **Denormal floats** | IIR state vars, reverb tanks, delay feedback | Sudden 100× CPU spike when signal decays |
| **NaN / Inf** | Divisions, `sqrt`, `acos`/`asin`, peak normalizers | Silence or noise that can't be traced |
| **Catastrophic cancellation** | DC-blocking filters, near-Nyquist biquads, first-order diff | Noise floor jumps, loss of precision |
| **Fixed-point overflow** | Q15/Q31 multiply, CMSIS paths, SIMD int16 | Audible distortion / wrapping |
| **Precision loss** | RMS/energy sums, mixing buses, long loops | Accumulated DC offset, incorrect levels |
| **FTZ/DAZ absent** | `prepareToPlay`/stream-open — no mode setup | Denormals hit on some hosts but not others |

For code examples and platform-specific notes see `references/numerics-pitfalls.md`.

## Step 3 — Write the review

```
## Audio Numerics Review: `[file / function]`

### Verdict
[Safe | Has critical violations | Warnings only] — one sentence summary

### Critical Violations
**[Category]: [description]**
`file:line` — `offending code`
Why: one sentence on the numeric risk
Fix: concrete suggestion

### Warnings
[same format]

### What's Done Well
[guarded divisions, double accumulators, FTZ setup, etc.]

### Recommended Fixes (priority order)
1. ...
```

## Quick fix table

| Violation | Safe alternative |
|-----------|-----------------|
| Denormal in feedback | `ScopedNoDenormals`; FTZ+DAZ in `prepareToPlay`; DC-offset clamp |
| Division by zero | `(denom > 1e-6f) ? num/denom : fallback` |
| `sqrt`/`acos`/`asin` unclamped | `std::sqrt(std::max(0.f, x))`, `std::clamp` inputs |
| NaN propagating silently | `assert(!std::isnan(y))` in debug; validate at entry points |
| Cancellation in coefficients | Compute coefficients in `double`; use numerically stable forms |
| Fixed-point overflow | Promote to wider type before multiply; `__SSAT`, CMSIS saturating ops |
| Precision loss in long sum | `double` accumulator or Kahan compensated summation |
| FTZ/DAZ absent | Set explicitly in `prepareToPlay`; use `ScopedNoDenormals` per-block |
