---
name: cv-tile-grid-mosaic-assembly
description: >
  Assembles N extracted tiles into a sqrt(N) x sqrt(N) mosaic image for single-forward-pass CNN inference on whole slide images.
---
# Tile Grid Mosaic Assembly

## Overview

After extracting the top-N informative tiles from a WSI, they need to be fed into a standard CNN. Rather than processing tiles independently, this technique arranges them into a sqrt(N) x sqrt(N) grid image (e.g., 36 tiles of 256px → one 1536x1536 image). This preserves some spatial context between adjacent tiles and allows a single forward pass through a standard image classifier. Per-tile augmentation can be applied before assembly, and whole-grid augmentation after.

## Quick Start

```python
import numpy as np

def assemble_mosaic(tiles, tile_size=256, n_tiles=36, transform=None):
    """Arrange N tiles into a square grid image."""
    n_row = int(np.sqrt(n_tiles))
    mosaic = np.ones((tile_size * n_row, tile_size * n_row, 3),
                     dtype=np.uint8) * 255  # white background

    for i in range(min(len(tiles), n_tiles)):
        h, w = i // n_row, i % n_row
        tile = tiles[i]
        if transform:
            tile = transform(image=tile)['image']
        mosaic[h*tile_size:(h+1)*tile_size,
               w*tile_size:(w+1)*tile_size] = tile

    return mosaic

# Usage
mosaic = assemble_mosaic(top_tiles, tile_size=256, n_tiles=36)
# Feed mosaic to standard image classifier
```

## Workflow

1. Extract top-N tiles from WSI (see tissue-content-tile-selection)
2. Optionally apply per-tile augmentations
3. Place tiles into a sqrt(N) x sqrt(N) grid
4. Optionally apply whole-mosaic augmentations
5. Feed single mosaic image to CNN

## Key Decisions

- **Grid size**: 4x4 (16 tiles), 6x6 (36 tiles); must be a perfect square
- **Padding**: Fill missing tile slots with white (255) for background
- **Augmentation order**: Per-tile first (color jitter), then whole-grid (rotation, flip)
- **vs independent tiles**: Mosaic is simpler but loses tile independence; concat-tile-feature-pooling is more flexible

## References

- [Train EfficientNet-B0 w/ 36 tiles](https://www.kaggle.com/code/haqishen/train-efficientnet-b0-w-36-tiles-256-lb0-87)
