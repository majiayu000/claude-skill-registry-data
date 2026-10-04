---
name: audio-artifacts-debug
description: >
  Systematic checklist for diagnosing audio artifacts. Use when the user describes a
  sound quality problem — clicks, pops, crackling, silence, DC offset, aliasing, phase
  issues, or latency problems. Trigger on phrases like "why do I hear clicks?", "my
  output has DC offset", "there's aliasing in my oscillator", "phase is wrong in mono",
  "dropout when CPU spikes". Pairs with audio-dsp-review (realtime safety) and
  audio-numerics-review (numeric correctness) — use those to fix once the cause is found.
---

# Audio Artifacts Debug

Audio artifacts have diagnostic signatures — match the symptom to the root cause before touching code.

## Step 1 — Characterize the artifact

Ask these questions before reading any code.

| Artifact type | Questions to ask |
|---------------|-----------------|
| **Clicks / pops** | Regular or random? On buffer boundaries? At note on/off? After channel strip toggle? |
| **Crackling / distortion** | Constant or load-dependent? Does it correlate with signal level? Worse on silent decay? |
| **Silence / dropout** | Immediate or gradual? Only under load? After a specific number of voices? Recovers? |
| **DC offset** | Constant or drift? Present from first sample? Appears only after long silence? |
| **Aliasing** | Audible as high-frequency mirror tones? Pitch-dependent? Present at all sample rates? |
| **Phase issues** | Stereo image collapse in mono? Comb filtering? Only on parallel paths or mid-side? |
| **Latency** | DAW reports wrong delay compensation? Wet/dry misaligned? Only at certain buffer sizes? |

## Step 2 — Narrow to root cause

| Symptom | Likely cause | Skill / check to apply |
|---------|-------------|----------------------|
| Click at fixed buffer-length intervals | Buffer boundary discontinuity — uninitialized tail, missing sample-accurate fade | `audio-dsp-review`: check process entry/exit |
| Click correlates with xrun log | CPU overload — audio thread missed deadline | `audio-dsp-review`: scan for allocations, locks, I/O |
| Crackling scales with signal amplitude | Clipping or fixed-point overflow | `audio-numerics-review`: overflow, Q-format multiply |
| Crackling on silent decay | Denormal floats — FTZ absent | `audio-numerics-review`: denormal section |
| Dropout / silence under load | xrun, NaN propagation, or buffer too small for latency | `audio-dsp-review` + `audio-numerics-review`: NaN guards |
| Silence after large value | NaN propagated from unclamped `sqrt` / division | `audio-numerics-review`: NaN / Inf section |
| DC offset from first sample | Uninitialized filter state or delay line | `audio-numerics-review`: precision loss / state init |
| DC offset after long silence | FTZ leaving near-zero state; missing high-pass | `audio-numerics-review`: denormal / FTZ section |
| Aliasing pitch-tracks with note | Oscillator not bandlimited; no anti-alias before downsampling | `audio-numerics-review`: check sample-rate handling |
| Stereo collapses to mono | Unmatched processing on L/R; phase inversion | `audio-dsp-review`: check parallel path symmetry |
| Comb filtering on mono | Latency mismatch on parallel paths | Plugin reports incorrect `getLatencySamples()` |
| Latency wrong at buffer-size change | Plugin caches latency at init only; not updated on reconfigure | `audio-dsp-review`: check `prepareToPlay` reset |

## Step 3 — Structured diagnosis report

```
## Audio Artifact Diagnosis: `[file / symptom]`

### Artifact characterization
Type: [clicks | crackling | silence | DC | aliasing | phase | latency]
Observed: [when / under what conditions]
Reproducible: [always | intermittent | load-dependent]

### Root cause hypothesis
Likely cause: [one sentence]
Evidence: [what in the code supports this]
Skill to apply: [audio-dsp-review | audio-numerics-review | both]

### Specific checks to run
1. [file:line] — [what to inspect]
2. ...

### Recommended fix
[Concrete action — no placeholder text]
```

For artifact-specific diagnostic questions and check-by-check references see
`references/artifact-patterns.md`.
