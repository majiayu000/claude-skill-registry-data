---
name: cv-brovey-pansharpening
description: Fuse low-resolution multispectral bands with a high-resolution panchromatic band using the Brovey transform to produce sharp multi-band imagery
---

# Brovey Pansharpening

## Overview

Satellite sensors capture high-resolution panchromatic (single-band) and lower-resolution multispectral images. Pansharpening fuses both to get high-resolution color imagery. The Brovey transform normalizes each band by a weighted sum, then multiplies by the panchromatic intensity. This preserves spectral ratios while injecting spatial detail.

## Quick Start

```python
import numpy as np
from skimage.transform import rescale

def brovey_pansharpen(ms_bands, pan, nir_weight=0.1):
    R, G, B, NIR = ms_bands
    dnf = (pan - nir_weight * NIR) / (
        nir_weight * R + nir_weight * G + nir_weight * B + 1e-10)
    sharp = np.stack([R * dnf, G * dnf, B * dnf, NIR * dnf], axis=-1)
    return np.clip(sharp, 0, None)

ms_upscaled = np.stack([
    rescale(ms[i], 4, order=3) for i in range(4)], axis=-1)
ms_upscaled = ms_upscaled[:pan.shape[0], :pan.shape[1]]
result = brovey_pansharpen(
    [ms_upscaled[..., i] for i in range(4)], pan)
```

## Workflow

1. Upscale multispectral bands to match panchromatic resolution (typically 4x bicubic)
2. Crop to align dimensions if sizes differ by a pixel
3. Compute per-pixel normalization factor from pan and weighted band sum
4. Multiply each band by the normalization factor
5. Clip negatives to zero

## Key Decisions

- **NIR weight (W)**: 0.1 is typical; higher values reduce NIR influence on the ratio
- **vs HSV pansharpening**: Brovey preserves spectral ratios better; HSV preserves hue but can shift brightness
- **Upscale method**: bicubic (order=3) balances sharpness and artifacts
- **Band alignment**: always crop after rescale — off-by-one pixels cause misregistration

## References

- [Panchromatic sharpening](https://www.kaggle.com/code/resolut/panchromatic-sharpening)
