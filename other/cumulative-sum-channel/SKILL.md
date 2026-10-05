---
name: cv-cumulative-sum-channel
description: Add a cumulative sum channel along the vertical axis to capture directional structural trends in grayscale images for segmentation
---

# Cumulative Sum Channel

## Overview

For images with directional structure (seismic sections, depth profiles, medical slices), a cumulative sum along the vertical axis encodes positional context that a CNN would otherwise need many layers to learn. Mean-subtract first to center around zero, then cumsum to create a gradient-like channel that captures trends. Normalize by standard deviation to keep values in a stable range.

## Quick Start

```python
import numpy as np

def add_cumsum_channel(img, border=5):
    center_mean = img[border:-border, border:-border].mean()
    csum = (img.astype(np.float32) - center_mean).cumsum(axis=0)
    csum -= csum[border:-border, border:-border].mean()
    csum /= max(1e-3, csum[border:-border, border:-border].std())
    return csum

# Stack as additional channel
images_2ch = np.zeros((N, H, W, 2), dtype=np.float32)
for i in range(N):
    images_2ch[i, ..., 0] = images[i].squeeze() / 255.0
    images_2ch[i, ..., 1] = add_cumsum_channel(images[i].squeeze())
```

## Workflow

1. Compute center-region mean of grayscale image (exclude border pixels)
2. Subtract mean and compute cumulative sum along vertical axis
3. Re-center and normalize by center-region standard deviation
4. Stack as additional input channel alongside the original image

## Key Decisions

- **Border exclusion**: ignores edge artifacts when computing statistics
- **Vertical axis**: captures top-to-bottom structure; use `axis=1` for horizontal
- **Normalization**: prevents cumsum values from dominating pixel values in the network
- **When useful**: seismic data, depth profiles, cross-section images — any domain with vertical gradients

## References

- [UNet with depth](https://www.kaggle.com/code/bguberfain/unet-with-depth)
