---
name: python-dataviz
description: >-
  This skill should be used when the user asks to "create a plot", "make a chart",
  "visualize data", "create a heatmap", "make a scatter plot", "plot time series",
  "create publication figures", "customize plot styling", "use matplotlib", "use seaborn",
  or needs guidance on Python data visualization, statistical graphics, or figure export.
version: 0.1.0
---

# Python Data Visualization

Python data visualization with matplotlib and seaborn for creating publication-quality figures, statistical graphics, and exploratory visualizations.

## When to use each library

**Matplotlib** is the foundational plotting library. Use it for:

- Fine-grained control over every plot element
- Custom layouts with GridSpec or subplot_mosaic
- 3D visualizations
- Animations
- Embedding plots in GUI applications
- When you need low-level customization

**Seaborn** builds on matplotlib for statistical visualization. Use it for:

- Statistical plots with automatic aggregation and confidence intervals
- Dataset-oriented plotting from DataFrames
- Faceted multi-panel figures (small multiples)
- Distribution visualization (KDE, histograms, violin plots)
- Correlation matrices and clustered heatmaps
- Publication-ready aesthetics with minimal code

**Combined approach**: Use seaborn for the main visualization, then customize with matplotlib.

## Core concepts

### Matplotlib hierarchy

1. **Figure** - Top-level container for all plot elements
2. **Axes** - Actual plotting area (one Figure can have multiple Axes)
3. **Artist** - Everything visible (lines, text, ticks, patches)
4. **Axis** - The x/y number lines with ticks and labels

### Two matplotlib interfaces

**Object-oriented interface (recommended)**:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, linewidth=2, label='data')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.legend()
plt.savefig('figure.png', dpi=300, bbox_inches='tight')
```

**pyplot interface** (quick exploration only):

```python
plt.plot(x, y)
plt.xlabel('X Label')
plt.show()
```

Always use the object-oriented interface for production code.

### Seaborn function levels

**Axes-level functions** plot to a single matplotlib Axes:

- Accept `ax=` parameter for placement
- Return Axes object
- Examples: `scatterplot`, `histplot`, `boxplot`, `heatmap`

**Figure-level functions** manage entire figures with faceting:

- Use `col`, `row` parameters for small multiples
- Return FacetGrid, JointGrid, or PairGrid objects
- Cannot be placed in existing figures
- Examples: `relplot`, `displot`, `catplot`, `lmplot`, `jointplot`, `pairplot`

```python
import seaborn as sns

# Axes-level: integrates with matplotlib
fig, axes = plt.subplots(1, 2)
sns.scatterplot(data=df, x='x', y='y', ax=axes[0])
sns.histplot(data=df, x='x', ax=axes[1])

# Figure-level: automatic faceting
sns.relplot(data=df, x='x', y='y', col='category', hue='group')
```

### Seaborn semantic mappings

Map data variables to visual properties automatically:

- `hue` - Color encoding
- `size` - Point/line size
- `style` - Marker/line style
- `col`, `row` - Facet into subplots

```python
sns.scatterplot(data=df, x='x', y='y',
                hue='category',      # Color by category
                size='importance',   # Size by value
                style='type')        # Different markers
```

## Quick start workflow

### 1. Import libraries

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
```

### 2. Set theme (optional)

```python
sns.set_theme(style='whitegrid', context='paper', font_scale=1.1)
```

### 3. Create the plot

```python
# Simple seaborn plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df, x='total_bill', y='tip', hue='day', ax=ax)

# Or figure-level with faceting
g = sns.relplot(data=df, x='x', y='y', col='category', kind='scatter')
```

### 4. Customize with matplotlib

```python
ax.set_xlabel('Total Bill ($)', fontsize=12)
ax.set_ylabel('Tip ($)', fontsize=12)
ax.set_title('Restaurant Tips', fontsize=14)
ax.legend(title='Day', bbox_to_anchor=(1.05, 1))
```

### 5. Save the figure

```python
plt.savefig('figure.png', dpi=300, bbox_inches='tight')
plt.savefig('figure.pdf')  # Vector format for publications
```

## Plot type selection

| Data Type | Recommended | Alternatives |
|-----------|-------------|--------------|
| Distribution (1 variable) | `histplot`, `kdeplot` | `boxplot`, `violinplot` |
| Relationship (2 continuous) | `scatterplot` | `regplot`, `hexbin` |
| Time series | `lineplot` | `plot` with dates |
| Categorical comparison | `barplot`, `boxplot` | `violinplot`, `stripplot` |
| Correlation matrix | `heatmap` | `clustermap` |
| Pairwise relationships | `pairplot` | `PairGrid` |
| Bivariate with marginals | `jointplot` | `JointGrid` |

For detailed plot type examples, see `references/plot-types.md`.

## Best practices

### Interface and layout

1. **Use object-oriented interface** - Explicit control, easier debugging
2. **Use `constrained_layout=True`** - Prevents overlapping elements
3. **Set figsize at creation** - `fig, ax = plt.subplots(figsize=(10, 6))`
4. **Close figures explicitly** - `plt.close(fig)` to prevent memory leaks

### Data preparation

1. **Use tidy/long-form data** - Each variable a column, each observation a row
2. **Use meaningful column names** - Seaborn uses them as axis labels
3. **Pass DataFrames** - Not raw arrays, to preserve semantic information

### Color and accessibility

1. **Use perceptually uniform colormaps** - `viridis`, `plasma`, `cividis`
2. **Avoid rainbow colormaps** - `jet` is not perceptually uniform
3. **Consider colorblind users** - Use `viridis`, `cividis`, or colorblind palette
4. **Use diverging colormaps for centered data** - `coolwarm`, `RdBu` for data with meaningful zero

### Export

1. **Use 300 DPI for publications** - `dpi=300`
2. **Use vector formats for print** - PDF, SVG
3. **Use `bbox_inches='tight'`** - Removes excess whitespace
4. **Set explicit figure size** - Control dimensions in inches

### Statistical plots

1. **Understand automatic aggregation** - Seaborn computes means and CIs by default
2. **Specify error representation** - `errorbar='sd'`, `errorbar=('ci', 95)`
3. **Show individual data points** - Combine `stripplot` with `boxplot`

## Common patterns

### Multi-panel figure

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10), constrained_layout=True)
sns.scatterplot(data=df, x='x', y='y', ax=axes[0, 0])
sns.histplot(data=df, x='x', ax=axes[0, 1])
sns.boxplot(data=df, x='cat', y='y', ax=axes[1, 0])
sns.heatmap(corr_matrix, ax=axes[1, 1], cmap='coolwarm', center=0)
```

### Publication figure

```python
sns.set_theme(style='ticks', context='paper', font_scale=1.1)
fig, ax = plt.subplots(figsize=(8, 6))

sns.boxplot(data=df, x='treatment', y='response', ax=ax)
sns.stripplot(data=df, x='treatment', y='response', color='black', alpha=0.3, ax=ax)

ax.set_xlabel('Treatment Condition')
ax.set_ylabel('Response (units)')
sns.despine()

plt.savefig('figure.pdf', dpi=300, bbox_inches='tight')
```

### Faceted exploration

```python
g = sns.relplot(
    data=df, x='x', y='y',
    hue='treatment', style='batch',
    col='timepoint', col_wrap=3,
    kind='line', height=3, aspect=1.5
)
g.set_axis_labels('X Variable', 'Y Variable')
g.set_titles('{col_name}')
```

## Scripts

This skill includes helper scripts:

- `scripts/plot_template.py` - Template demonstrating various plot types
- `scripts/style_configurator.py` - Interactive style configuration utility

## References

For detailed information, load specific references:

```bash
oaps skill context python-dataviz --references <name>
```

| Reference | Content |
|-----------|---------|
| `matplotlib-fundamentals` | Core matplotlib concepts, hierarchy, common operations |
| `seaborn-fundamentals` | Seaborn design, data structures, function categories |
| `plot-types` | Comprehensive plot type guide with examples |
| `styling` | Colormaps, palettes, themes, typography |
| `api-reference` | Quick reference for common functions and parameters |
| `troubleshooting` | Common issues and solutions |
| `seaborn-objects` | Modern seaborn.objects declarative interface |
