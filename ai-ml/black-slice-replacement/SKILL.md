---
name: cv-black-slice-replacement
description: Detect all-black DICOM/MRI slices (mean==0) and replace them by randomly sampling a non-black slice from the same series
---

# Black Slice Replacement

## Overview

Medical imaging volumes sometimes contain entirely black slices due to scanner artifacts, corrupt files, or padding. Feeding black slices into a model wastes capacity and can degrade training. Detecting slices with `mean == 0` and replacing them with a randomly sampled non-black slice from the same series maintains the expected input shape while providing meaningful pixel data.

## Quick Start

```python
import random
import numpy as np

def load_slice_with_fallback(path, all_paths, read_fn, max_retries=100):
    """Load a DICOM slice; if all-black, replace with random non-black slice."""
    image = read_fn(path)

    retries = 0
    while image.mean() == 0 and retries < max_retries:
        image = read_fn(random.choice(all_paths))
        retries += 1

    return image

def load_volume_safe(file_paths, read_fn):
    """Load volume with black-slice replacement."""
    slices = []
    for p in file_paths:
        slices.append(load_slice_with_fallback(p, file_paths, read_fn))
    return np.stack(slices)
```

## Workflow

1. Load each slice from the series
2. Check if `image.mean() == 0` (all-black)
3. If black, randomly sample another slice from the same series
4. Retry up to N times to avoid infinite loops on fully corrupt volumes
5. Stack non-black slices into the output volume

## Key Decisions

- **Detection threshold**: `mean == 0` catches fully black; use `mean < epsilon` for near-black
- **Replacement strategy**: random sampling is simple; nearest non-black slice preserves spatial context better
- **Max retries**: cap at 100 to handle volumes where most slices are black
- **vs zero-pad**: replacement provides real texture; zero-pad is cleaner but less informative

## References

- [[TF]: 3D & 2D Model for Brain Tumor Classification](https://www.kaggle.com/code/ipythonx/tf-3d-2d-model-for-brain-tumor-classification)
