---
name: visualize-se3-frames
description: Generate matplotlib code to visualize SE3 poses and coordinate frames in 3D. Use when the user needs to plot transformation matrices, coordinate frames, trajectories, kinematic chains, or debug robot poses visually.
argument-hint: [optional: variable name or file containing poses]
---

# Visualize SE3 Frames

Plot SE3 poses (4x4 homogeneous transformation matrices) as RGB coordinate frame axes in a 3D matplotlib figure.

## Convention

- **RGB = XYZ**: Red = X-axis, Green = Y-axis, Blue = Z-axis
- SE3 matrix layout: rotation in `T[:3, :3]`, translation in `T[:3, 3]`
- Each column of the rotation matrix is a frame axis direction

## Core Functions

```python
import numpy as np
import matplotlib.pyplot as plt


def plot_coordinate_frame(ax, T, scale=1.0, alpha=0.8, label=None):
    """Plot an SE3 pose as RGB axes. T is a 4x4 homogeneous matrix."""
    origin = T[:3, 3]
    for i, color in enumerate(["red", "green", "blue"]):
        axis = T[:3, i] * scale
        ax.quiver(
            origin[0], origin[1], origin[2],
            axis[0], axis[1], axis[2],
            color=color, alpha=alpha, arrow_length_ratio=0.1,
        )
    if label:
        ax.text(origin[0], origin[1], origin[2], f"  {label}", fontsize=8, alpha=0.7)


def arrow_scale_from_origins(origins):
    """Compute arrow length proportional to spatial extent of the scene."""
    extent = origins.max(axis=0) - origins.min(axis=0)
    return max(extent.max() / 12, 1e-3)
```

## Plotting a Trajectory of Poses

When plotting many poses (e.g. odometry), subsample and auto-scale:

```python
origins = np.array([T[:3, 3] for T in poses])
scale = arrow_scale_from_origins(origins)

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

# thin trajectory line connecting origins
ax.plot(origins[:, 0], origins[:, 1], origins[:, 2], "k-", alpha=0.3, linewidth=0.5)

for T in poses:
    plot_coordinate_frame(ax, T, scale=scale, alpha=0.6)
```

## Auto-fit Equal-Aspect Axis Limits

Force equal scaling on all three axes so frames don't appear distorted:

```python
origins = np.array([T[:3, 3] for T in poses])
lo, hi = origins.min(axis=0), origins.max(axis=0)
mid = (lo + hi) / 2
half = (hi - lo).max() / 2 + scale  # include arrow length in margin
ax.set_xlim(mid[0] - half, mid[0] + half)
ax.set_ylim(mid[1] - half, mid[1] + half)
ax.set_zlim(mid[2] - half, mid[2] + half)
```

## Common Conversions

Quaternion (x, y, z, w) to rotation matrix:

```python
def quaternion_to_rotation(x, y, z, w):
    return np.array([
        [1 - 2*(y*y + z*z),   2*(x*y - z*w),       2*(x*z + y*w)],
        [2*(x*y + z*w),       1 - 2*(x*x + z*z),   2*(y*z - x*w)],
        [2*(x*z - y*w),       2*(y*z + x*w),       1 - 2*(x*x + y*y)],
    ])
```

## Drawing Kinematic Chains

Connect parent-child frames with black lines:

```python
for parent_T, child_T in connections:
    ax.plot(
        [parent_T[0, 3], child_T[0, 3]],
        [parent_T[1, 3], child_T[1, 3]],
        [parent_T[2, 3], child_T[2, 3]],
        "k-", alpha=0.5, linewidth=1,
    )
```

## Chaining Transforms

Accumulate transformations along a kinematic chain:

```python
T_cumulative = np.eye(4)
for T_joint in joint_transforms:
    T_cumulative = T_cumulative @ T_joint
    plot_coordinate_frame(ax, T_cumulative, ...)
```

## When Applying This Skill

1. Determine whether poses are individual frames or a trajectory — use `arrow_scale_from_origins` either way
2. For trajectories: subsample (e.g. every Nth), draw a connecting line, use lower alpha
3. For individual frames: plot at full alpha with labels
4. Always auto-fit axis limits with equal aspect so orientations render correctly
5. Plot a world/root frame at `np.eye(4)` as reference when useful
