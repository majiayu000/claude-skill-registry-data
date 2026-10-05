---
name: cv-center-z-slice-selection
description: Select a fixed number of Z-slices centered around the volume midpoint for memory-efficient 2.5D input from 3D CT/MRI stacks
---

# Center Z-Slice Selection

## Overview

3D medical/scientific volumes often have 30-65+ slices, but loading all of them as input channels is memory-prohibitive. Selecting a fixed number of slices centered around the volume midpoint captures the most informative region (where the surface of interest typically lies) while reducing input channels from 65 to e.g. 6-12. This enables using standard 2D pretrained backbones with multi-channel input.

## Quick Start

```python
import cv2
import numpy as np

def load_center_slices(slice_dir, total_slices=65, n_channels=6):
    mid = total_slices // 2
    start = mid - n_channels // 2
    end = mid + n_channels // 2

    images = []
    for i in range(start, end):
        img = cv2.imread(f"{slice_dir}/{i:02d}.tif", cv2.IMREAD_GRAYSCALE)
        images.append(img)

    return np.stack(images, axis=-1)  # (H, W, n_channels)

volume = load_center_slices("fragment_01/surface_volume", n_channels=8)
# Feed to 2D model with in_channels=8
```

## Workflow

1. Determine total number of Z-slices in the volume
2. Compute center index: `mid = total // 2`
3. Select symmetric range: `[mid - n//2, mid + n//2)`
4. Load only those slices as grayscale images
5. Stack along channel dimension for 2D model input

## Key Decisions

- **n_channels**: 6-12 is typical; match to model's `in_channels` parameter
- **Center assumption**: works when the signal is near the volume center; adjust offset if not
- **Normalization**: 16-bit TIFFs → divide by 65535.0 for float32 [0, 1] range
- **vs all slices**: reduces memory 5-10x with minimal information loss for centered signals

## References

- [2.5d segmentaion baseline [inference]](https://www.kaggle.com/code/tanakar/2-5d-segmentaion-baseline-inference)
- [2.5d segmentaion baseline [training]](https://www.kaggle.com/code/tanakar/2-5d-segmentaion-baseline-training)
