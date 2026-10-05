---
name: scientific-figures
description: Generate publication-quality scientific figures with consistent styling. Use when experiments need visualization, benchmarking results need plots, or papers need figures.
---

# Scientific Figures Skill

Generate publication-quality visualizations for experimental results.

## When to Use

- After running experiments that produce numerical results
- When synthesizing papers that need figures
- When benchmarking tools and need ROC/PR curves, bar plots, etc.
- When visualizing data distributions (violin plots, histograms)
- When creating graphical abstracts

## Output Requirements

**ALWAYS generate both formats:**
- PNG at 300 DPI (for web/preview)
- PDF vector (for publication)

**ALWAYS include:**
- Clear axis labels with units
- Legends when multiple series
- Panel labels (A, B, C, D) for multi-panel figures
- Figure titles
- Consistent color scheme

## Standard Figure Types

### 1. Performance Metrics (Benchmarking)
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set consistent style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Panel A: ROC curves
axes[0].set_title('A. ROC Curves', fontsize=12, fontweight='bold')
axes[0].set_xlabel('False Positive Rate')
axes[0].set_ylabel('True Positive Rate')
axes[0].plot([0, 1], [0, 1], 'k--', label='Random')

# Panel B: Bar comparison
axes[1].set_title('B. Performance Comparison', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('figure.png', dpi=300, bbox_inches='tight')
plt.savefig('figure.pdf', bbox_inches='tight')
```

### 2. Distribution Plots (QC, Score Distributions)
```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, (data, title) in zip(axes, [(d1, 'Metric A'), (d2, 'Metric B'), (d3, 'Metric C')]):
    sns.violinplot(data=data, ax=ax)
    ax.set_title(title)

plt.savefig('qc_metrics.png', dpi=300, bbox_inches='tight')
plt.savefig('qc_metrics.pdf', bbox_inches='tight')
```

### 3. Confusion Matrices
```python
from sklearn.metrics import confusion_matrix
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for ax, (cm, title) in zip(axes, [(cm1, 'A. Method 1'), (cm2, 'B. Method 2')]):
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=['Pred Neg', 'Pred Pos'],
                yticklabels=['True Neg', 'True Pos'])
    ax.set_title(title, fontsize=12, fontweight='bold')

plt.tight_layout()
```

### 4. UMAP/Scatter Plots
```python
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

scatter1 = axes[0].scatter(umap[:, 0], umap[:, 1], c=labels, cmap='tab20', s=5, alpha=0.7)
axes[0].set_title('A. Cell Types')
axes[0].legend(*scatter1.legend_elements(), loc='best', markerscale=2)

scatter2 = axes[1].scatter(umap[:, 0], umap[:, 1], c=scores, cmap='coolwarm', s=5, alpha=0.7)
axes[1].set_title('B. Doublet Scores')
plt.colorbar(scatter2, ax=axes[1])
```

### 5. Graphical Abstract
For synthesis papers, create a workflow diagram:
```python
# Use matplotlib patches and arrows for simple workflow diagrams
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis('off')

# Add boxes for each step
steps = [
    (1, 3, 'Input\nData'),
    (4, 3, 'Method A'),
    (7, 3, 'Method B'),
    (10, 3, 'Results'),
]

for x, y, text in steps:
    box = FancyBboxPatch((x-0.8, y-0.5), 1.6, 1,
                         boxstyle="round,pad=0.1", facecolor='lightblue',
                         edgecolor='black', linewidth=2)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='bold')
```

## Color Schemes

**Default categorical:** `sns.color_palette("husl", n_colors)`
**Sequential:** `"Blues"`, `"Greens"`, `"Oranges"`
**Diverging:** `"coolwarm"`, `"RdBu_r"`

## Figure Naming Convention

```
figures/
├── 01_qc_metrics.png
├── 01_qc_metrics.pdf
├── 02_method_comparison.png
├── 02_method_comparison.pdf
├── 03_roc_pr_curves.png
├── 03_roc_pr_curves.pdf
├── graphical_abstract.png
└── graphical_abstract.pdf
```

## Checklist Before Saving

- [ ] Both PNG and PDF generated
- [ ] All axes labeled
- [ ] Legend present if needed
- [ ] Panel labels (A, B, C) added
- [ ] Font sizes readable (min 10pt)
- [ ] Colors colorblind-friendly
- [ ] tight_layout() called
- [ ] DPI=300 for PNG

## Integration with Papers

When writing LaTeX papers, reference figures:
```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=\textwidth]{figures/01_qc_metrics.pdf}
\caption{\textbf{Quality Control Metrics.} (A) UMI counts per cell...}
\label{fig:qc}
\end{figure}
```

**K-Dense produced 8 beautiful figures. We must match or exceed that quality.**
