---
name: view-pcd
description: View a binary PCD pointcloud file with per-vertex RGB colors in a 3D matplotlib plot. Use when the user has a .pcd file and wants to visualize it interactively. Standalone — no project dependencies beyond numpy and matplotlib.
argument-hint: <path-to-pcd-file> [--subsample N] [--point-size S]
---

# View PCD Pointcloud

Standalone viewer for binary PCD files with packed RGB float color (PCL convention).

## Usage

```bash
python3 view_pcd.py cloud.pcd
python3 view_pcd.py cloud.pcd --subsample 4 --point-size 0.1
```

## Script

```python
"""View a binary PCD pointcloud file. Standalone — no project dependencies."""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


PCD_DTYPE = np.dtype([
    ("x", "<f4"), ("y", "<f4"), ("z", "<f4"),
    ("rgb", "<f4"),
])


def load_pcd(path):
    with open(path, "rb") as f:
        n_points = None
        while True:
            line = f.readline().decode("ascii").strip()
            if line.startswith("POINTS"):
                n_points = int(line.split()[-1])
            if line == "DATA binary":
                break
        if n_points is None:
            raise ValueError("No POINTS field in PCD header")
        return np.frombuffer(f.read(n_points * PCD_DTYPE.itemsize), dtype=PCD_DTYPE)


def unpack_rgb(rgb_float):
    packed = rgb_float.view(np.uint32)
    r = (packed >> 16) & 0xFF
    g = (packed >> 8) & 0xFF
    b = packed & 0xFF
    return r.astype(np.uint8), g.astype(np.uint8), b.astype(np.uint8)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--point-size", type=float, default=0.05)
    parser.add_argument("--subsample", type=int, default=None,
                        help="plot every Nth point (speeds up rendering)")
    args = parser.parse_args()

    pts = load_pcd(args.path)
    if args.subsample:
        pts = pts[::args.subsample]
    print(f"{len(pts)} points")

    r, g, b = unpack_rgb(pts["rgb"])
    rgb = np.column_stack([r, g, b]) / 255.0

    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(projection="3d")

    ax.scatter(
        pts["x"], pts["y"], pts["z"],
        c=rgb, s=args.point_size, rasterized=True,
    )

    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_zlabel("z (m)")
    ax.set_title(f"{args.path.name} ({len(pts)} points)")
    plt.show()


if __name__ == "__main__":
    main()
```

## Workflow: Remote Accumulate → Local View

On the remote machine, generate the PCD:

```bash
python3 -m pointclean.plot_accumulated path/to/data.mcap --pcd cloud.pcd -n 10
```

rsync locally:

```bash
rsync remote:path/to/cloud.pcd .
```

View locally:

```bash
python3 view_pcd.py cloud.pcd
```

## Notes

- PCD files use binary little-endian format with FIELDS x y z rgb (16 bytes/point)
- RGB is packed into a single float per the PCL convention (R << 16 | G << 8 | B, viewed as float32)
- Colors are baked in at save time from the intensity colormap — the viewer just unpacks RGB
- Use `--subsample 4` or higher if matplotlib is sluggish with large clouds
- PCD files are natively supported by PCL tools, Open3D, and CloudCompare
