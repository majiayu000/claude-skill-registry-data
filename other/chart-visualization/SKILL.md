---
name: chart-visualization
description: "Generate charts: select type, extract data, render image."
allowed-tools:
  - bash
  - write_file
  - read_file
enabled: true
related-skills: [data-analysis, consulting-analysis]
license: MIT
author: Adapted from deer-flow (Bytedance, MIT)
---

# Chart Visualization

## Overview

Transform data into visual charts. Intelligently select the most suitable chart
type, extract parameters, and generate a chart image.

> **Poirot note:** The original deer-flow skill uses a bundled
> `scripts/generate.js` (Node.js + charting library). Poirot doesn't bundle
> that script. Use `bash` with Python (`matplotlib`/`plotly`) as the rendering
> engine instead. Install: `pip install matplotlib plotly`.

## Chart Selection Guide

| Data Pattern | Recommended Chart | When |
|---|---|---|
| **Time Series** | Line / Area | Trends over time |
| **Comparisons** | Bar / Column | Categorical comparison |
| **Distribution** | Histogram / Boxplot | Frequency distribution |
| **Part-to-Whole** | Pie / Treemap | Proportions |
| **Relationships** | Scatter | Correlation |
| **Flow** | Sankey | Flow between stages |
| **Multi-dimensional** | Radar | Compare across dimensions |
| **Process** | Funnel | Stage conversion |
| **Hierarchy** | Org chart / Mind map | Tree structure |
| **Geographic** | Map | Spatial data |

## Workflow

### 1. Select Chart Type

Analyze the user's data features:
- Time dimension? → Line/Area
- Categories? → Bar/Column
- Proportions? → Pie/Treemap
- Correlation? → Scatter
- Flow? → Sankey
- Multiple dimensions? → Radar

### 2. Prepare Data

Extract data from user input, format as Python data structure:

```python
data = {
    "labels": ["Jan", "Feb", "Mar", "Apr", "May"],
    "values": [120, 150, 180, 200, 220],
    "title": "Monthly Revenue",
    "xlabel": "Month",
    "ylabel": "Revenue ($K)"
}
```

### 3. Generate Chart

```bash
python3 -c "
import matplotlib
matplotlib.use('Agg')  # non-interactive backend
import matplotlib.pyplot as plt

labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
values = [120, 150, 180, 200, 220]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(labels, values, marker='o', linewidth=2, markersize=8)
ax.set_title('Monthly Revenue', fontsize=16, fontweight='bold')
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Revenue ($K)', fontsize=12)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('.poirot/outputs/chart.png', dpi=150, bbox_inches='tight')
print('Saved to .poirot/outputs/chart.png')
"
```

### Common Chart Types via matplotlib

```bash
# Bar chart
python3 -c "
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
cats = ['A', 'B', 'C', 'D']
vals = [23, 45, 12, 67]
plt.bar(cats, vals, color=['#4CAF50', '#2196F3', '#FF9800', '#F44336'])
plt.title('Category Comparison')
plt.savefig('.poirot/outputs/bar.png', dpi=150)
"

# Scatter plot
python3 -c "
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
x = np.random.randn(100)
y = x * 0.8 + np.random.randn(100) * 0.5
plt.scatter(x, y, alpha=0.6, c='steelblue')
plt.title('Correlation Scatter')
plt.savefig('.poirot/outputs/scatter.png', dpi=150)
"

# Pie chart
python3 -c "
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
labels = ['Product A', 'Product B', 'Product C']
sizes = [45, 35, 20]
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title('Market Share')
plt.savefig('.poirot/outputs/pie.png', dpi=150)
"
```

## Pitfalls

- **matplotlib backend**: always use `matplotlib.use('Agg')` for non-interactive
  (headless) rendering. Without it, matplotlib may try to open a GUI window.
- **Chinese characters**: matplotlib may not render CJK by default. Set font:
  `plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']`
- **DPI**: use `dpi=150` for crisp images. `dpi=300` for print quality.
- **File size**: PNG is standard. Use SVG for vector (`plt.savefig('chart.svg')`).
- **Color palettes**: use colorblind-friendly palettes. Avoid red/green only.
