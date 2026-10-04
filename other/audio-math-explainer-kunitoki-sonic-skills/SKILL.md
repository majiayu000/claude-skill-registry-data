---
name: audio-math-explainer
description: >
  Explains DSP math concepts to developers who need the theory behind an algorithm. Use whenever the
  user asks how a signal-processing concept works, wants intuition behind a formula, or hits a
  math-shaped bug. Trigger on phrases like "how does a Fourier transform work", "explain
  z-transforms", "what is convolution", "why does my biquad ring", "what is windowing for",
  "what causes aliasing", or "how do I convert gain to dB". Also trigger when the user pastes DSP
  code and asks why it behaves a certain way.
---

# Audio Math Explainer

> **The rule:** DSP math is small and composable — each concept builds directly on the last.
> Start with what the user needs, then connect it to code they're writing.

## Step 1 — Identify the concept

| Topic | Core idea | Common "why" |
|-------|-----------|--------------|
| Fourier transform / DFT / FFT | Decompose signal into frequency components | "Why does my FFT output look wrong?" |
| Convolution | Weighted moving average; LTI system response | "How does an IR reverb work?" |
| Z-transform | Frequency-domain analysis of discrete systems | "How do filter poles/zeros work?" |
| Biquad / IIR filters | Recursive difference equation with feedback | "Why does my filter ring / go unstable?" |
| FIR filters | Non-recursive weighted sum | "How do I design a linear-phase filter?" |
| Windowing | Reduce spectral leakage in DFT | "Why are FFT edges smeared?" |
| Sample rate / Nyquist | Highest representable frequency = sr/2 | "What causes aliasing?" |
| Decibels | Log scale for amplitude/power ratios | "How do I convert gain to dB?" |

If the user's question maps to multiple rows, start with the most fundamental one and build up.

## Step 2 — Explain with three anchors

For each concept, give exactly these three things in order:

1. **Intuition** — one sentence a musician could understand
2. **Math** — the key formula (inline, no walls of derivation)
3. **Code** — one-line pseudocode or a real function call from common audio libraries

Keep each anchor to 1–3 lines. Cut anything that doesn't directly answer the question.

## Step 3 — Connect to the user's code

After the three anchors:
- Locate where the math appears in their implementation (coefficient calculation, loop structure, buffer size choice, etc.)
- Name the exact variable or line where theory becomes code
- If a value looks wrong, explain which part of the math it violates

## Quick connection table

| Math concept | Where it shows up in code |
|--------------|--------------------------|
| DFT basis frequencies | `bin_index * sr / N` — each FFT bin |
| Convolution sum | FIR tap loop: `y[n] = sum(h[k] * x[n-k])` |
| Z-plane pole radius | IIR feedback coefficients `a1`, `a2` |
| Nyquist limit | `if (freq > sampleRate / 2) clamp(...)` |
| Window function | Multiply `x[n] *= window[n]` before FFT |
| dB conversion | `gain_db = 20 * log10(amplitude)` |

## Output format

```
### [Concept name]

**Intuition:** [one sentence]

**Math:** `[formula]`

**Code:** `[one-liner]`

**In your code:** [where this appears and what it means for their specific question]
```

> See `references/dsp-math-reference.md` for full formula tables, gotchas, and property lists.
