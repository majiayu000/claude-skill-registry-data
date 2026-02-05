---
name: tile-snake-pattern-stitching
description: "SNAKE vs RASTER tile acquisition patterns for image stitching in KINTSUGI"
author: KINTSUGI Team
date: 2024-12-15
---

# Tile SNAKE Pattern Stitching - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-15 |
| **Goal** | Correctly stitch multiplex microscopy tiles acquired in SNAKE pattern |
| **Environment** | KINTSUGI pipeline, Python 3.10+, CuPy GPU |
| **Status** | Success |

## Context
CODEX and similar multiplex imaging systems acquire tiles in a SNAKE pattern (also called serpentine or boustrophedon). This pattern alternates direction on each row to minimize stage movement. Incorrect tile ordering causes stitching failures with misaligned or scrambled images.

## SNAKE vs RASTER Pattern

### SNAKE Pattern (Default for CODEX)
Even rows scan left-to-right, odd rows scan right-to-left:
```
Row 0:  →  →  →  (tiles 1, 2, 3)
Row 1:  ←  ←  ←  (tiles 6, 5, 4)
Row 2:  →  →  →  (tiles 7, 8, 9)
```

### RASTER Pattern
All rows scan left-to-right:
```
Row 0:  →  →  →  (tiles 1, 2, 3)
Row 1:  →  →  →  (tiles 4, 5, 6)
Row 2:  →  →  →  (tiles 7, 8, 9)
```

## Verified Workflow

### Building Tile Coordinates for SNAKE Pattern
```python
from itertools import chain, repeat

n_rows = 2  # Grid rows
n_cols = 2  # Grid columns

# Row indices (same for both patterns)
rows = list(chain.from_iterable(repeat(row, n_cols) for row in range(n_rows)))

# Column indices - SNAKE PATTERN
# Even rows: 0,1,2... (L→R)
# Odd rows: ...2,1,0 (R→L)
cols = list(chain.from_iterable(
    range(n_cols) if row % 2 == 0 else range(n_cols - 1, -1, -1)
    for row in range(n_rows)
))

# For 2x2 grid:
# rows = [0, 0, 1, 1]
# cols = [0, 1, 1, 0]  <- SNAKE: second row reversed
```

### Test Data Tile Reordering
When test data tiles are renamed by POSITION (1,2,3,4 for grid positions) but were acquired in SNAKE order, reorder before stitching:

```python
# Files load as position order: [tile1, tile2, tile3, tile4]
# Grid positions:
#   [1] [2]    row 0 (L→R)
#   [3] [4]    row 1 (should be R→L for snake)
#
# For snake acquisition, row 1 was acquired as [4, 3] not [3, 4]
# So actual acquisition order was: 1, 2, 4, 3
#
# Reorder to match acquisition order:
if n_rows == 2 and n_cols == 2:
    corrected = corrected[[0, 1, 3, 2]]  # [1,2,3,4] → [1,2,4,3]
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Using RASTER pattern `cols = [0,1,0,1]` | Tiles misaligned at row boundaries | CODEX uses SNAKE pattern - odd rows are reversed |
| Not reordering position-named test tiles | Stitching scrambled because tile order didn't match stitch model | Test data tiles named by position need reordering to match snake acquisition |
| Assuming tile filenames reflect acquisition order | Test data was renamed by grid position, not acquisition order | Always verify whether tile names are position-based or acquisition-order-based |

## Final Parameters

### SNAKE Pattern Coordinates (2x2 grid)
```python
rows = [0, 0, 1, 1]
cols = [0, 1, 1, 0]  # NOT [0, 1, 0, 1] (that's RASTER)
```

### SNAKE Pattern Coordinates (3x3 grid)
```python
rows = [0, 0, 0, 1, 1, 1, 2, 2, 2]
cols = [0, 1, 2, 2, 1, 0, 0, 1, 2]  # Row 1 reversed
```

### General Formula
```python
cols = list(chain.from_iterable(
    range(n_cols) if row % 2 == 0 else range(n_cols - 1, -1, -1)
    for row in range(n_rows)
))
```

## Key Insights
- SNAKE pattern is standard for CODEX and similar multiplex imaging systems
- The pattern minimizes stage travel time between tiles
- Even rows: left-to-right (columns 0,1,2...)
- Odd rows: right-to-left (columns ...2,1,0)
- When test data tiles are renamed by position, they must be reordered to match acquisition order before stitching
- The stitch model is computed from tile positions, so tile array order must match the coordinate lists

## References
- CODEX multiplex imaging documentation
- KINTSUGI Notebook 1 (Single Channel Eval) and Notebook 2 (Cycle Processing)
