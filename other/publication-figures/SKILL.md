---
name: publication-figures
description: Publication-quality scientific figure standard for this repo. Use whenever creating, exporting, or revising any plot, chart, panel, or figure (matplotlib/seaborn), or generating report artifacts under reports/.
allowed-tools: Read, Write, Edit, Bash
---

# Publication Figures

## When to Use
- Creating or editing any figure, plot, chart, or multi-panel export
- Generating artifacts under `reports/`
- Any prompt mentioning figure, plot, panel, chart, axis, legend, DPI

## Required Output
- **Vector PDF + 600 DPI PNG** for every figure (export both).
- **Font**: Arial (fall back to a sans-serif that renders as Arial); embed fonts in the PDF.
- **Palette**: Okabe-Ito colorblind-safe palette; verify the figure is legible in grayscale.
- **Statistics on the figure**: show error bars, the n per group, and significance markers where a comparison is made.
- No chartjunk: minimal gridlines, direct labels over legends where feasible.

## Matplotlib Setup Snippet
```python
import matplotlib as mpl
mpl.rcParams.update({
    "font.family": "Arial",
    "pdf.fonttype": 42,   # embed TrueType (editable text in the PDF)
    "ps.fonttype": 42,
    "savefig.dpi": 600,
    "figure.constrained_layout.use": True,
})

# Okabe-Ito
OKABE_ITO = ["#000000", "#E69F00", "#56B4E9", "#009E73",
             "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]

def save_figure(fig, stem):
    fig.savefig(f"reports/{stem}.pdf")           # vector
    fig.savefig(f"reports/{stem}.png", dpi=600)  # raster
```

## Anti-Patterns
- Rainbow / jet colormaps, or palettes indistinguishable in grayscale.
- PNG-only export (no vector), or DPI < 300.
- Bare point estimates with no error bars, n, or significance.

## Integration
- Pair with [[data-analysis-hygiene]] — audit the data before plotting it.
