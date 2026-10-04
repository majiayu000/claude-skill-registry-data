---
name: frequency
description: Frequency-domain and signal-processing skill; use when working on Fourier, spectral, or resonance analysis.
---

# Skill: Frequency

Domain: `trinity` | Depth: `axiom`

## Capabilities
- Fourier analysis: FFT, IFFT, spectral decomposition (numpy, scipy)
- Wavelet transforms (scipy)
- Solfeggio frequencies and harmonic series computation
- Resonance and standing wave modeling
- Brainwave frequency bands: delta, theta, alpha, beta, gamma
- Cymatics: frequency-to-geometry mapping
- Signal synthesis: sine, square, sawtooth, harmonic stacking
- Schumann resonance (7.83 Hz) and Earth frequency modeling

## Frequency Reference
| Name       | Hz range     | Domain |
|------------|-------------|--------|
| Delta      | 0.5–4 Hz    | Deep sleep, healing |
| Theta      | 4–8 Hz      | Meditation, creativity |
| Alpha      | 8–14 Hz     | Relaxed focus |
| Beta       | 14–30 Hz    | Active thinking |
| Gamma      | 30–100 Hz   | Higher cognition |
| Schumann   | 7.83 Hz     | Earth resonance |
| Solfeggio  | 174–963 Hz  | Sacred tones |

## Libraries
| Library | Purpose |
|---------|---------|
| numpy   | FFT and signal arrays |
| scipy   | Wavelet, signal processing |
| matplotlib | Spectrum visualization |

## Module
`agents/skills/frequency.py`

## Key Functions
- `fft_spectrum(signal, sample_rate)` — frequency spectrum
- `synthesize(frequencies, amplitudes, duration, sr)` — build waveform
- `solfeggio()` — dict of all solfeggio frequencies
- `brainwave_bands()` — frequency band definitions
- `schumann_resonances()` — first 7 Schumann harmonics
- `wavelet_transform(signal)` — continuous wavelet transform
