---
name: cv-3d-center-crop-zero-pad
description: Select center slices from a 3D volume and zero-pad along depth when the scan has fewer slices than the target count
---

# 3D Center Crop with Zero Padding

## Overview

Medical imaging volumes vary in slice count across patients and scanners. To feed them into a fixed-depth 3D CNN, select slices centered around the midpoint and zero-pad the depth dimension if the scan has fewer slices than required. This preserves the most informative region while maintaining a consistent input shape.

## Quick Start

```python
import numpy as np

def load_volume_fixed_depth(files, num_slices=64, img_size=256, load_fn=None):
    """Load center slices from a sorted file list, zero-pad if too few."""
    middle = len(files) // 2
    half = num_slices // 2
    p1 = max(0, middle - half)
    p2 = min(len(files), middle + half)

    slices = [load_fn(f, img_size) for f in files[p1:p2]]
    vol = np.stack(slices).T  # (H, W, D)

    if vol.shape[-1] < num_slices:
        pad = np.zeros((img_size, img_size, num_slices - vol.shape[-1]))
        vol = np.concatenate([vol, pad], axis=-1)

    return np.expand_dims(vol, 0)  # (1, H, W, D)

volume = load_volume_fixed_depth(sorted_dcm_files, num_slices=64, load_fn=read_dcm)
```

## Workflow

1. Sort slice files by position (filename or DICOM metadata)
2. Compute center index and symmetric range around it
3. Load only the center slices
4. If fewer slices than target, append zero arrays along depth
5. Add channel dimension for 3D CNN input

## Key Decisions

- **Zero-pad vs repeat-pad**: zeros are standard; repeating edge slices can reduce boundary artifacts
- **Pad location**: appending at the end is simplest; symmetric padding centers content better
- **num_slices**: match the model's expected depth (typically 32, 64, or 128)
- **vs resize**: interpolating along depth changes inter-slice spacing; zero-pad preserves it

## References

- [Efficientnet3D with one MRI type](https://www.kaggle.com/code/rluethy/efficientnet3d-with-one-mri-type)
- [Brain Tumor 3D [Training]](https://www.kaggle.com/code/ammarnassanalhajali/brain-tumor-3d-training)
