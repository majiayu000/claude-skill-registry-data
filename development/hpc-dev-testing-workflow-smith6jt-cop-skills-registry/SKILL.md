---
name: hpc-dev-testing-workflow
description: "Efficient development testing workflow for HPC environments with VS Code tunneling. Trigger: testing code changes on HPC, development workflow with external data directories, VS Code Remote SSH development"
author: KINTSUGI Team
date: 2025-12-14
---

# HPC Development Testing Workflow

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2025-12-14 |
| **Goal** | Create efficient workflow for testing code changes when data is external to repo |
| **Environment** | HiperGator HPC, VS Code Remote SSH, Python scientific pipeline |
| **Status** | Success |

## Problem Statement

When developing scientific pipelines on HPC with VS Code tunneling:
- Repository code lives in one directory
- Project data (large image files) lives in external directory
- After each code change, user must:
  1. Re-initialize project folder to get updated code
  2. Open project folder in VS Code (ends Claude session)
  3. Copy errors back to repo session

This creates a fragmented workflow that kills productivity.

## Verified Solution

### 1. VS Code Multi-Root Workspace

Create a workspace file that opens all folders simultaneously:

```json
// kintsugi-dev.code-workspace
{
  "folders": [
    { "path": "/path/to/repo", "name": "Repo (code)" },
    { "path": "/path/to/repo/test_data/mini_project", "name": "Test Project" },
    { "path": "/path/to/full_project", "name": "Full Project" }
  ],
  "settings": {
    "python.defaultInterpreterPath": "/path/to/repo/.venv/bin/python",
    "search.exclude": {
      "**/data/raw": true,
      "**/data/processed": true,
      "**/*.zarr": true
    }
  }
}
```

Open with: `code /path/to/kintsugi-dev.code-workspace`

**Benefits:**
- Claude session stays alive across all folders
- Switch between repo and project without losing context
- Single kernel/terminal session spans all work

### 2. Minimal Test Dataset Inside Repo

Create a small test dataset inside the repository:

```
repo/
├── src/
├── notebooks/
└── test_data/
    └── mini_project/
        ├── data/raw/cyc001/  # Subset of tiles
        ├── meta/
        └── notebooks/
```

**Key decisions:**
- Extract **center tiles** (most representative of real processing)
- Include **all z-planes** (tests full stack processing)
- Include **all channels** (tests multi-channel workflows)
- Use **2-3 cycles** (tests multi-cycle registration)
- Keep size manageable (~3-5 GB vs 50+ GB full dataset)

### 3. Tile Renumbering Script

When extracting tiles, renumber them to form a valid grid:

```python
#!/usr/bin/env python3
"""Extract and renumber center tiles for test dataset."""

import shutil
from pathlib import Path

# For 13x9 grid, center 2x2 tiles (snake pattern)
TILE_MAPPING = {
    58: 1,  # Row 4, Col 5 → position (0,0)
    59: 2,  # Row 4, Col 6 → position (0,1)
    73: 3,  # Row 5, Col 5 → position (1,0) - snake reverses
    72: 4,  # Row 5, Col 6 → position (1,1) - snake reverses
}

def rename_tile(filename: str, old_tile: int, new_tile: int) -> str:
    old_str = f"1_{old_tile:05d}_"
    new_str = f"1_{new_tile:05d}_"
    return filename.replace(old_str, new_str)

def copy_cycle(source_dir: Path, dest_dir: Path):
    dest_dir.mkdir(parents=True, exist_ok=True)
    for old_tile, new_tile in TILE_MAPPING.items():
        pattern = f"1_{old_tile:05d}_*.tif"
        for src_file in source_dir.glob(pattern):
            new_name = rename_tile(src_file.name, old_tile, new_tile)
            shutil.copy2(src_file, dest_dir / new_name)
```

### 4. Updated Test Parameters

After creating test dataset, update notebook parameters:

```python
# Original parameters (full 13x9 grid)
n = 9   # rows
m = 13  # columns

# Test parameters (2x2 grid)
n = 2   # rows
m = 2   # columns
overlap_percentage = 30  # keep same
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Symlinks to notebooks | Changes don't reflect immediately with editable install | Copy notebooks, use `%autoreload 2` |
| Single folder workflow | Constantly switching folders kills Claude session | Multi-root workspace keeps session |
| Random tile subset | Tiles don't form valid grid for stitching | Must extract contiguous tiles and renumber |
| Too small test set (1 tile) | Can't test stitching, registration, or multi-tile algorithms | Need minimum 2x2 grid |
| Too large test set (full row) | Still too slow for rapid iteration | 2x2 is optimal balance |
| PYTHONPATH manipulation | Confusing, doesn't handle notebook imports | Editable install + autoreload is cleaner |

## Workflow Summary

```
┌─────────────────────────────────────────────────────────┐
│           VS Code Multi-Root Workspace                   │
├─────────────────┬─────────────────┬─────────────────────┤
│   Repo (code)   │  Test Project   │   Full Project      │
│                 │                 │                     │
│  Make changes   │  Quick test     │  Final validation   │
│  Claude session │  2x2 grid       │  Full 13x9 grid     │
│  ~0 GB data     │  ~3 GB data     │  ~50+ GB data       │
└─────────────────┴─────────────────┴─────────────────────┘
         │                │                  │
         └────────────────┴──────────────────┘
                    Single session
```

## Test Dataset Specifications

| Parameter | Test Dataset | Full Dataset |
|-----------|-------------|--------------|
| Grid size | 2×2 | 13×9 (117 tiles) |
| Tiles | 4 | 117 |
| Cycles | 3 | 9+ |
| Channels | 4 | 4 |
| Z-planes | 13 | 13 |
| Files/cycle | 208 | 6,084 |
| Total size | ~3 GB | ~50+ GB |
| Process time | ~2-5 min | ~30-60 min |

## Key Configuration Files

### Workspace File Location
```
/blue/maigan/smith6jt/kintsugi-dev.code-workspace
```

### Test Data Setup Script
```
repo/test_data/setup_test_data.py
```

### Regenerate Test Data
```bash
python test_data/setup_test_data.py
kintsugi init test_data/mini_project --name "Dev Test 2x2" --force
```

## Platform-Specific Notes

### HiperGator (SLURM)
- Use `/blue/` filesystem for large data (faster I/O)
- Workspace file can live in home directory
- VS Code Server runs on login node, compute via SLURM

### VS Code Remote SSH
- Install "Remote - SSH" extension
- Workspace file must use absolute paths
- Search exclude patterns prevent indexing large data dirs

## References
- VS Code Multi-Root Workspaces: https://code.visualstudio.com/docs/editor/multi-root-workspaces
- Python editable installs: https://pip.pypa.io/en/stable/topics/local-project-installs/
- IPython autoreload: https://ipython.readthedocs.io/en/stable/config/extensions/autoreload.html
