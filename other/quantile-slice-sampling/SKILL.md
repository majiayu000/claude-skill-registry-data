---
name: cv-quantile-slice-sampling
description: >
  Samples a fixed number of slices from variable-length CT/MRI stacks using quantile indexing to produce consistent input depth.
---
# Quantile Slice Sampling

## Overview

3D medical imaging models require fixed-depth input, but CT/MRI scans vary widely in slice count (50-500+). Quantile slice sampling selects N evenly-spaced slices by computing quantile indices over the full stack. This preserves anatomical coverage from top to bottom regardless of scan length, unlike truncation (loses anatomy) or padding (wastes compute).

## Quick Start

```python
import numpy as np
from glob import glob

def sample_slices(scan_dir, n_slices=64):
    paths = sorted(glob(f"{scan_dir}/*"),
                   key=lambda x: int(x.split('/')[-1].split('.')[0]))
    n_scans = len(paths)
    if n_scans <= n_slices:
        indices = list(range(n_scans))
    else:
        indices = np.quantile(
            list(range(n_scans)),
            np.linspace(0., 1., n_slices)
        ).round().astype(int)
    return [paths[i] for i in indices]

# Sample 64 slices from a scan with 300+ slices
selected = sample_slices("/data/train_images/patient_001", n_slices=64)
```

## Workflow

1. List and sort all slice files in the scan directory
2. Compute N quantile positions uniformly from 0 to 1
3. Map quantile positions to integer indices in the slice array
4. Load only the selected slices and stack into a 3D volume

## Key Decisions

- **n_slices**: Match model architecture input depth (32, 64, 128 typical)
- **Sort order**: Sort by DICOM InstanceNumber or filename to preserve anatomical order
- **vs stride sampling**: Quantile handles edge cases better (always includes first and last)
- **Short scans**: If scan has fewer slices than target, use all slices and pad

## References

- [RSNA 2022 1st Place Solution - Train Stage1](https://www.kaggle.com/code/haqishen/rsna-2022-1st-place-solution-train-stage1)
