---
name: matplotlib
description: Use when creating static, animated, or interactive visualizations with Matplotlib; Use when plotting data, customizing figures, or building publication-quality charts in Python
risk: low
source: custom
date_added: '2026-06-11'
---
You are an expert in **Matplotlib**, Python's foundational plotting library for creating static, animated, and interactive visualizations.

## Use this skill when

- Creating line, bar, scatter, histogram, heatmap, pie, or 3D plots
- Customizing figure aesthetics (colors, fonts, styles, annotations)
- Building multi-panel / subplot layouts
- Generating publication-quality or export-ready figures
- Animating plots with `FuncAnimation`
- Integrating Matplotlib with numpy, pandas, or Polars data

## Do not use this skill when

- The user needs interactive browser-based charts (use Plotly or Bokeh instead)
- The task is purely data wrangling with no visualization

## Instructions

1. Always use the **object-oriented API** (`fig, ax = plt.subplots()`), not the state-machine `plt.*` API.
2. Label axes, add titles, and use legends for clarity.
3. Use `plt.tight_layout()` or `constrained_layout=True` to avoid clipping.
4. Save with `fig.savefig()` at an appropriate DPI before `plt.show()`.

## Core API

### Figure & Axes Setup
```python
import matplotlib.pyplot as plt
import numpy as np

# Single plot
fig, ax = plt.subplots(figsize=(8, 5))

# Multiple subplots
fig, axes = plt.subplots(2, 3, figsize=(12, 7))

# Constrained layout (better than tight_layout)
fig, ax = plt.subplots(figsize=(8, 5), layout="constrained")

# Unequal subplot sizes with gridspec
from matplotlib.gridspec import GridSpec
gs = GridSpec(2, 2, figure=fig)
ax1 = fig.add_subplot(gs[0, :])   # span full row
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[1, 1])
```

### Common Plot Types
```python
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

# Line plot
ax.plot(x, y, color="steelblue", linewidth=2, linestyle="--", label="sin(x)")

# Scatter plot
ax.scatter(x, y, s=20, c="tomato", alpha=0.7, label="points")

# Bar chart
categories = ["A", "B", "C"]
values = [3, 7, 5]
ax.bar(categories, values, color="teal", edgecolor="black")

# Horizontal bar
ax.barh(categories, values, color="teal")

# Histogram
data = np.random.randn(1000)
ax.hist(data, bins=30, color="slateblue", edgecolor="white", alpha=0.8)

# Box plot
ax.boxplot([np.random.randn(100), np.random.randn(100)], labels=["A", "B"])

# Heatmap / imshow
matrix = np.random.rand(10, 10)
im = ax.imshow(matrix, cmap="viridis", aspect="auto")
fig.colorbar(im, ax=ax, label="Value")

# Pie chart
ax.pie(values, labels=categories, autopct="%1.1f%%", startangle=90)

# Stem plot
ax.stem(x[:20], y[:20])

# Step plot
ax.step(x, y, where="mid")

# Fill between
ax.fill_between(x, y - 0.2, y + 0.2, alpha=0.3, color="steelblue")

# Error bars
ax.errorbar(x[::10], y[::10], yerr=0.1, fmt="o", capsize=4)
```

### Axes Customization
```python
ax.set_title("My Chart", fontsize=14, fontweight="bold", pad=12)
ax.set_xlabel("X Axis", fontsize=12)
ax.set_ylabel("Y Axis", fontsize=12)

ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)

ax.set_xticks([0, np.pi, 2 * np.pi])
ax.set_xticklabels(["0", "π", "2π"])

ax.tick_params(axis="both", labelsize=10)
ax.xaxis.set_tick_params(rotation=45)

ax.legend(loc="upper right", fontsize=10, framealpha=0.8)
ax.grid(True, linestyle="--", alpha=0.5)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
```

### Annotations & Text
```python
ax.annotate(
    "Peak",
    xy=(np.pi / 2, 1),           # point to annotate
    xytext=(np.pi / 2 + 0.5, 0.7),  # label position
    arrowprops=dict(arrowstyle="->", color="black"),
    fontsize=10,
)

ax.text(1, 0.5, "Note", transform=ax.transAxes, ha="right")  # axes-relative
ax.axhline(y=0, color="gray", linestyle=":")
ax.axvline(x=np.pi, color="red", linestyle="--", linewidth=1)
ax.axhspan(0, 0.5, alpha=0.1, color="green")
```

### Colors, Styles & Themes
```python
# Set a built-in style
plt.style.use("seaborn-v0_8-whitegrid")   # or "ggplot", "fivethirtyeight", etc.

# Colormaps for continuous data
cmap = plt.cm.viridis          # sequential
cmap = plt.cm.RdBu             # diverging
cmap = plt.cm.tab10            # categorical

# Color cycles for multiple lines
from matplotlib.cm import get_cmap
colors = get_cmap("tab10").colors

# Custom rcParams
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 12,
    "axes.titlesize": 14,
    "figure.dpi": 150,
})
```

### Colorbars
```python
sc = ax.scatter(x, y, c=y, cmap="plasma", s=50)
cbar = fig.colorbar(sc, ax=ax)
cbar.set_label("Magnitude")
```

### Twin Axes (dual y-axis)
```python
ax2 = ax.twinx()
ax2.plot(x, np.cos(x), color="darkorange", label="cos(x)")
ax2.set_ylabel("cos(x)", color="darkorange")
ax2.tick_params(axis="y", labelcolor="darkorange")
```

### 3D Plots
```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

X, Y = np.meshgrid(np.linspace(-3, 3, 50), np.linspace(-3, 3, 50))
Z = np.sin(np.sqrt(X**2 + Y**2))
ax.plot_surface(X, Y, Z, cmap="coolwarm", alpha=0.9)
ax.scatter(x_pts, y_pts, z_pts, c="red", s=20)
```

### Animations
```python
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1, 1)

def update(frame):
    x_data = np.linspace(0, 2 * np.pi, 100)
    y_data = np.sin(x_data + frame * 0.1)
    line.set_data(x_data, y_data)
    return line,

anim = FuncAnimation(fig, update, frames=100, interval=50, blit=True)
anim.save("animation.gif", writer="pillow", fps=20)
```

### Saving Figures
```python
fig.savefig("chart.png", dpi=150, bbox_inches="tight")
fig.savefig("chart.svg")           # vector format
fig.savefig("chart.pdf")           # publication-ready
plt.close(fig)                     # free memory — always close after saving
```

## Integration with Data Libraries

### With NumPy
```python
x = np.arange(10)
y = np.random.randn(10).cumsum()
ax.plot(x, y)
```

### With Pandas
```python
import pandas as pd
df = pd.DataFrame({"x": range(10), "y": np.random.randn(10)})
df.plot(x="x", y="y", ax=ax)       # pandas .plot() uses Matplotlib under the hood
```

### With Polars
```python
import polars as pl
df = pl.DataFrame({"x": range(10), "y": np.random.randn(10)})
ax.plot(df["x"].to_numpy(), df["y"].to_numpy())
```

## Best Practices

- **Always use the OO API** (`fig, ax = plt.subplots()`) — avoid `plt.plot()` directly.
- **Close figures** after saving: `plt.close(fig)` prevents memory leaks in loops.
- **Use `constrained_layout=True`** instead of `tight_layout()` — more robust.
- **Export vector formats** (SVG, PDF) for publications; PNG at ≥150 DPI for web.
- **Avoid excessive grid lines and chartjunk** — remove top/right spines for clean look.
- **Set figure DPI globally** via `rcParams["figure.dpi"]` for consistent rendering.
- **Use semantic color names** or hex codes rather than single-letter shortcuts.
- **Label everything**: title, x-axis, y-axis, legend entries, and colorbar.

## Common Plot Patterns

### Side-by-side comparison
```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), layout="constrained")
ax1.plot(x, np.sin(x)); ax1.set_title("sin(x)")
ax2.plot(x, np.cos(x)); ax2.set_title("cos(x)")
```

### Shared axes
```python
fig, axes = plt.subplots(3, 1, figsize=(8, 9), sharex=True, layout="constrained")
```

### Figure-level legend
```python
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.05))
```
