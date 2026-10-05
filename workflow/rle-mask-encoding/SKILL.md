---
name: cv-rle-mask-encoding
description: >
  Encodes binary segmentation masks into compressed RLE format for efficient storage and submission.
---
# RLE Mask Encoding

## Overview

Run-Length Encoding (RLE) compresses binary segmentation masks by storing consecutive runs of 0s and 1s as (start, length) pairs. Combined with zlib compression and base64 encoding, this produces compact ASCII strings suitable for competition submissions and efficient storage.

## Quick Start

```python
import numpy as np
from pycocotools import _mask as mask_util
import zlib
import base64

def mask_to_rle(binary_mask):
    """Convert binary mask to COCO-format RLE."""
    fortran_mask = np.asfortranarray(binary_mask.astype(np.uint8))
    rle = mask_util.encode(fortran_mask)
    return rle

def rle_to_compressed_string(rle):
    """Compress RLE to base64 string for submission."""
    compressed = zlib.compress(rle["counts"])
    return base64.b64encode(compressed).decode("ascii")

def rle_to_mask(rle, shape):
    """Decode RLE back to binary mask."""
    return mask_util.decode(rle).astype(bool)
```

## Workflow

1. Generate binary mask from segmentation model output
2. Convert to Fortran-order array (column-major, required by COCO tools)
3. Encode via `pycocotools._mask.encode`
4. Optionally compress with zlib + base64 for submission strings
5. Decode back with `mask_util.decode` when needed

## Key Decisions

- **Fortran order**: COCO RLE requires column-major order; `np.asfortranarray` is essential
- **pycocotools vs custom**: pycocotools is the standard; custom RLE risks encoding mismatches
- **Compression**: zlib + base64 reduces string size 5-10x for sparse masks
- **Batch encoding**: Process masks in bulk with `mask_util.encode` for speed

## References

- HPA Single Cell Classification competition (Kaggle)
- Source: [hpa-cellwise-classification-inference](https://www.kaggle.com/code/dschettler8845/hpa-cellwise-classification-inference)
