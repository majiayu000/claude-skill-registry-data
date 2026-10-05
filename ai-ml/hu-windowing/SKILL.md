---
name: cv-hu-windowing
description: Apply radiological windowing to HU images — clamp to center/width range for tissue-specific visualization (lung, bone, soft tissue)
domain: cv
---

# HU Windowing

## Overview

Different tissues are best visualized at different Hounsfield Unit ranges. Windowing clamps pixel values to a center±width/2 range, then rescales to display range. Use multiple windows as separate input channels to give models tissue-specific contrast without losing information.

## Quick Start

```python
import numpy as np

def apply_window(hu_image, center, width):
    """Apply radiological window to HU image.
    
    Args:
        hu_image: array in Hounsfield Units
        center: window center (e.g., -600 for lung)
        width: window width (e.g., 1500 for lung)
    Returns:
        windowed image clamped to [min_val, max_val]
    """
    min_val = center - width / 2
    max_val = center + width / 2
    windowed = np.clip(hu_image, min_val, max_val)
    return windowed

# Common presets
WINDOWS = {
    'lung':        (-600, 1500),   # air-filled structures
    'soft_tissue': (40, 400),      # organs, muscles
    'bone':        (400, 1800),    # skeletal structures
    'brain':       (40, 80),       # intracranial
    'mediastinum': (50, 350),      # chest soft tissue
}

# Multi-window 3-channel input for CNN
lung = apply_window(hu_slice, *WINDOWS['lung'])
soft = apply_window(hu_slice, *WINDOWS['soft_tissue'])
bone = apply_window(hu_slice, *WINDOWS['bone'])
rgb_input = np.stack([lung, soft, bone], axis=-1)
```

## Key Decisions

- **Multi-window channels**: stack 3 windows as RGB — each channel highlights different anatomy
- **Preset selection**: lung window for COVID/pneumonia; soft tissue for tumors; bone for fractures
- **Normalize after windowing**: scale to [0, 1] before model input for stable training
- **DICOM metadata**: WindowCenter/WindowWidth fields provide scanner-recommended defaults

## References

- Source: [pulmonary-dicom-preprocessing](https://www.kaggle.com/code/allunia/pulmonary-dicom-preprocessing)
- Competition: SIIM-FISABIO-RSNA COVID-19 Detection
