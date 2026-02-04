---
name: debug_axes
description: プロットのスケール（対数軸など）、目盛、表示範囲の不具合を診断し、意図した見た目に修正する
---

# Debug Plot Axes Skill

This skill is for resolving issues where plot axis scales (especially log scales) or display ranges (ylim/xlim) in `gwexpy` do not appear as intended.

## Diagnostic Procedures

1.  **Verify Internal State**:
    *   Create a reproduction script and output `ax.get_yscale()` or `ax.get_ylim()` to confirm if the internal setting is actually 'log'.

2.  **Identity Visual Linearity Issues**:
    *   If the internal state is 'log' but it visually appears linear, it is often due to the data range being too narrow (e.g., 1.0 vs 2.23).
    *   Check if ticks are appropriately placed via `ax.get_yticks()`.

3.  **Confirm Judgment Logic**:
    *   Check if `determine_yscale` or `determine_xscale` in `gwexpy/plot/defaults.py` correctly recognizes the data, using debug prints if necessary.

## Correction Guidelines

1.  **Enforce Scale Application**:
    *   Explicitly call `ax.set_yscale()` after `super().__init__` within `Plot.__init__` in `gwexpy/plot/plot.py`.
    *   Always call `ax.autoscale_view()` after application to force a visual update.

2.  **Automatic Range Expansion (Log Scale specific)**:
    *   If the data range is less than 100x (2 orders of magnitude), log scales often show few ticks, appearing linear.
    *   Implement or fix `determine_ylim` logic to ensure a range of approximately 2 orders of magnitude centered around the median.

3.  **Robust Type Checking**:
    *   Since `isinstance` checks may fail due to environment differences (import sources), use duck-typing such as `type(obj).__name__` or `hasattr(obj, 'frequencies')` alongside it.

4.  **Prevent Duplicate Display in IPython/Jupyter**:
    *   Set `_repr_html_ = None` in the `Plot` class to prevent duplicate displays (repr and `plt.show`).
