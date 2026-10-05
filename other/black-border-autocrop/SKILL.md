---
name: cv-black-border-autocrop
description: >
  Crops uninformative black or dark borders from images by deriving a binary mask from the grayscale channel and trimming rows/columns.
---
# Black Border Autocrop

## Overview

Medical images (retinal scans, X-rays), scanned documents, and padded photos often have large black or dark borders that waste resolution and confuse models. This technique converts to grayscale, thresholds to find informative pixels, then crops to the bounding box of non-dark content. Works on both grayscale and multi-channel images, applying the same mask consistently across all channels.

## Quick Start

```python
import numpy as np
import cv2

def autocrop_black_border(img, tol=7):
    """Crop dark borders from an image.

    Args:
        img: (H, W) or (H, W, C) numpy array
        tol: pixel intensity threshold (0-255); below this is "dark"
    Returns:
        cropped image
    """
    if img.ndim == 2:
        mask = img > tol
        return img[np.ix_(mask.any(1), mask.any(0))]

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    mask = gray > tol
    rows = mask.any(1)
    cols = mask.any(0)
    if not rows.any():
        return img  # entirely dark — return original
    return img[np.ix_(rows, cols)]

# Usage
img = cv2.imread("scan.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
cropped = autocrop_black_border(img, tol=7)
cropped = cv2.resize(cropped, (512, 512))
```

## Workflow

1. Convert color image to grayscale
2. Create binary mask: pixels > threshold are "content"
3. Find rows/columns that contain any content pixels
4. Crop to the bounding box of content rows/columns
5. Resize cropped image to target dimensions

## Key Decisions

- **tol**: 7 for near-black borders; increase (20-30) for dark-gray borders
- **Safety check**: Return original if mask is empty (image too dark)
- **Before resize**: Always crop before resize to maximize effective resolution
- **Multi-channel**: Apply grayscale mask to all channels uniformly via `np.ix_`

## References

- [APTOS Eye Preprocessing in Diabetic Retinopathy](https://www.kaggle.com/code/ratthachat/aptos-eye-preprocessing-in-diabetic-retinopathy)
