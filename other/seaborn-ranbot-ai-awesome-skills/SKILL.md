---
name: seaborn
description: Statistical visualization with pandas integration. Use for quick exploration of distributions, relationships, and categorical comparisons with attractive defaults. Best for box plots, violin plots, pa
category: Creative & Media
source: antigravity
tags: [python, pdf, api, ai, design, presentation, rag, cro]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/seaborn
---


# Seaborn Statistical Visualization

## Overview

Seaborn is a Python visualization library for creating publication-quality statistical graphics. Use this skill for dataset-oriented plotting, multivariate analysis, automatic statistical estimation, and complex multi-panel figures with minimal code.

## Design Philosophy

Seaborn follows these core principles:

1. **Dataset-oriented**: Work directly with DataFrames and named variables rather than abstract coordinates
2. **Semantic mapping**: Automatically translate data values into visual properties (colors, sizes, styles)
3. **Statistical awareness**: Built-in aggregation, error estimation, and confidence intervals
4. **Aesthetic defaults**: Publication-ready themes and color palettes out of the box
5. **Matplotlib integration**: Full compatibility with matplotlib customization when needed

## Quick Start

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load example dataset
df = sns.load_dataset('tips')

# Create a simple visualization
sns.scatterplot(data=df, x='total_bill', y='tip', hue='day')
plt.show()
```

## Core Plotting Interfaces

### Function Interface (Traditional)

The function interface provides specialized plotting functions organized by visualization type. Each category has **axes-level** functions (plot to single axes) and **figure-level** functions (manage entire figure with faceting).

**When to use:**
- Quick exploratory analysis
- Single-purpose visualizations
- When you need a specific plot type

### Objects Interface (Modern)

The `seaborn.objects` interface provides a declarative, composable API similar to ggplot2. Build visualizations by chaining methods to specify data mappings, marks, transformations, and scales.

**When to use:**
- Complex layered visualizations
- When you need fine-grained control over transformations
- Building custom plot types
- Programmatic plot generation

```python
from seaborn import objects as so

# Declarative syntax
(
    so.Plot(data=df, x='total_bill', y='tip')
    .add(so.Dot(), color='day')
    .add(so.Line(), so.PolyFit())
)
```

## Plotting Functions by Category

### Relational Plots (Relationships Between Variables)

**Use for:** Exploring how two or more variables relate to each other

- `scatterplot()` - Display individual observations as points
- `lineplot()` - Show trends and changes (automatically aggregates and computes CI)
- `relplot()` - Figure-level interface with automatic faceting

**Key parameters:**
- `x`, `y` - Primary variables
- `hue` - Color encoding for additional categorical/continuous variable
- `size` - Point/line size encoding
- `style` - Marker/line style encoding
- `col`, `row` - Facet into multiple subplots (figure-level only)

```python
# Scatter with multiple semantic mappings
sns.scatterplot(data=df, x='total_bill', y='tip',
                hue='time', size='size', style='sex')

# Line plot with confidence intervals
sns.lineplot(data=timeseries, x='date', y='value', hue='category')

# Faceted relational plot
sns.relplot(data=df, x='total_bill', y='tip',
            col='time', row='sex', hue='smoker', kind='scatter')
```

### Distribution Plots (Single and Bivariate Distributions)

**Use for:** Understanding data spread, shape, and probability density

- `histplot()` - Bar-based frequency distributions with flexible binning
- `kdeplot()` - Smooth density estimates using Gaussian kernels
- `ecdfplot()` - Empirical cumulative distribution (no parameters to tune)
- `rugplot()` - Individual observation tick marks
- `displot()` - Figure-level interface for univariate and bivariate distributions
- `jointplot()` - Bivariate plot with marginal distributions
- `pairplot()` - Matrix of pairwise relationships across dataset

**Key parameters:**
- `x`, `y` - Variables (y optional for univariate)
- `hue` - Separate distributions by category
- `stat` - Normalization: "count", "frequency", "probability", "density"
- `bins` / `binwidth` - Histogram binning control
- `bw_adjust` - KDE bandwidth multiplier (higher = smoother)
- `fill` - Fill area under curve
- `multiple` - How to handle hue: "layer", "stack", "dodge", "fill"

```python
# Histogram with density normalization
sns.histplot(data=df, x='total_bill', hue='time',
             stat='density', multiple='stack')

# Bivariate KDE with contours
sns.kdeplot(data=df, x='total_bill', y='tip',
            fill=True, levels=5, thresh=0.1)

# Joint plot with marginals
sns.jointplot(data=df, x='total_bill', y='tip',
              kind='scatter', hue='time')

# Pairwise relationships
sns.pairplot(data=df, hue='species', corner=True)
```

### Categorical Plots (Comparisons Across Categories)

**Use for:** Comparing distributions or statistics across discrete categories

**Categorical scatterplots:**
- `stripplot()` - Points with jitter to show all observations
- `swarmplot()` - Non-overlapping points (beeswarm algorithm)

**Distribution comparisons:**
- `boxplot()` - Quartiles and outliers
- `violinp
