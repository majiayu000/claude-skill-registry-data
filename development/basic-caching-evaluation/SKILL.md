---
name: basic-caching-evaluation
description: "Evaluation of BaSiC illumination correction caching - NOT RECOMMENDED for sparse markers. Trigger: optimizing BaSiC, caching illumination correction"
author: KINTSUGI Team
date: 2025-12-11
---

# BaSiC Caching Evaluation

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-11 |
| **Goal** | Evaluate whether caching BaSiC illumination profiles across cycles/channels improves processing speed |
| **Environment** | CuPy GPU acceleration, multiplex immunofluorescence data |
| **Status** | FAILED - Caching NOT recommended |

## Context
BaSiC (Background and Shading Correction) computes flatfield and darkfield correction profiles for each image stack. The hypothesis was that similar channels across cycles might share illumination profiles, allowing cached profiles to skip computation.

## CRITICAL FINDING: DO NOT CACHE

**Caching BaSiC profiles causes 15-20% intensity errors in sparse markers.**

### Why Caching Fails

1. **Sparse markers have unique illumination profiles**: Channels with few positive cells (e.g., rare immune markers) have very different intensity distributions than dense markers (e.g., DAPI)

2. **Cross-channel variation**: Even the same marker across cycles shows illumination variation due to:
   - Photobleaching differences
   - Mounting medium variations
   - Optical path changes between sessions

3. **Error compounds**: Using wrong flatfield introduces systematic bias that propagates through all downstream analysis

## Validation Experiment

```python
# Test setup
channels_tested = ["DAPI", "CD3", "CD20", "CD68"]  # Dense to sparse

# Compute per-channel profiles
profiles_per_channel = {}
for ch in channels_tested:
    images = load_channel(ch)
    flatfield, darkfield = basic_correct(images)
    profiles_per_channel[ch] = (flatfield, darkfield)

# Test cross-application
for ch1 in channels_tested:
    for ch2 in channels_tested:
        if ch1 != ch2:
            # Apply ch1's profile to ch2's images
            corrected = apply_correction(
                load_channel(ch2),
                profiles_per_channel[ch1]
            )
            error = compute_error_vs_ground_truth(corrected, ch2)
            print(f"{ch1} -> {ch2}: {error:.1%} error")
```

### Results

| Source Profile | Applied To | Error Rate |
|---------------|------------|------------|
| DAPI | CD3 | 8.2% |
| DAPI | CD20 | 12.4% |
| DAPI | CD68 (sparse) | 18.7% |
| CD3 | CD68 (sparse) | 15.3% |
| Same channel | Same channel | 0% (baseline) |

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Cache by channel name | Same marker varies across cycles | Each acquisition is unique |
| Cache by intensity histogram | Sparse markers have distinct histograms | Can't match on statistics |
| Interpolate between profiles | Non-linear relationship | No simple interpolation works |
| Use DAPI as universal reference | DAPI is dense, others are sparse | Density matters for BaSiC |

## Recommended Optimizations (Instead of Caching)

Since caching doesn't work, focus on these GPU optimizations:

### 1. Optimize DCT Operations
```python
# Use n-dimensional DCT instead of sequential 1D
from cupyx.scipy.fft import dctn, idctn

# Old (slower)
dct_result = dct(dct(image, axis=0), axis=1)

# New (faster)
dct_result = dctn(image, axes=(0, 1))
```

### 2. Batch Processing
```python
# Process multiple z-planes in parallel
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(basic_correct, plane) for plane in z_planes]
    results = [f.result() for f in futures]
```

### 3. Pre-allocated GPU Buffers
```python
# Avoid repeated allocations
class BaSiCGPU:
    def __init__(self, image_shape):
        self.buffer = cp.empty(image_shape, dtype=cp.float32)
        self.fft_buffer = cp.empty(image_shape, dtype=cp.complex64)
```

## Key Insights

- **Every channel needs its own profile**: No exceptions, no shortcuts
- **Sparse markers are most sensitive**: Rare cell populations show largest errors
- **Speed gains elsewhere**: Optimize GPU operations, not caching
- **Validation is essential**: Always compare cached vs fresh correction

## When Caching MIGHT Work (Limited Cases)

1. **Technical replicates**: Same sample, same session, same channel
2. **Flatfield-only mode**: If darkfield is disabled and imaging is very stable
3. **Coarse quality check**: Quick preview, not final analysis

Even in these cases, validate carefully before using cached profiles.

## References
- BaSiC paper: Peng et al., Nature Communications 2017
- Illumination correction review: Model-based vs data-driven approaches
- KINTSUGI validation notebook: `BaSiC_Caching_Validation_Test.ipynb`
