---
name: kdense-data-viz-selected
description: "精选 K-Dense Scientific Agent Skills 的数据分析与科学可视化工具包。用于 EDA、统计分析、Matplotlib、Seaborn、scientific visualization、NetworkX、Polars、Dask 等分析和图表任务，并按 Auto-sci-research 的论文图件、文献计量图、政策矩阵、空间暴露和可视化审稿风险进行封装。"
---

# K-Dense Data/Viz Selected

This wrapper packages selected Data Analysis & Visualization skills from `K-Dense-AI/scientific-agent-skills` for Auto-sci-research.

Use it when a task needs:

- exploratory data analysis;
- statistical test selection and reporting;
- assumption diagnostics, effect sizes, uncertainty, or power analysis;
- Matplotlib, Seaborn, NetworkX, Polars, or Dask technical guidance;
- publication-grade scientific figures.

## Included Upstream Subskills

Located in `subskills/k-dense/`:

- `exploratory-data-analysis`
- `statistical-analysis`
- `matplotlib`
- `seaborn`
- `scientific-visualization`
- `networkx`
- `polars`
- `dask`

## Local Adaptation

Use these upstream skills with Auto-sci-research rules:

1. Start every figure from the claim it must support.
2. Audit units, missingness, outliers, groups, and spatial/temporal coverage before statistical analysis.
3. Use effect sizes and uncertainty, not only p-values.
4. For bibliometric visuals, connect clusters and networks to field evolution, evidence gaps, and policy relevance.
5. Export figures at journal-ready dimensions with colorblind-safe palettes and readable captions.

For domain-specific guidance, also read:

- `../agent-auto-sci-data-viz/references/k_dense_data_viz_mapping.md`
- `../agent-auto-sci-data-viz/references/review_bibliometric_figure_system.md`

## Must Not Do

- Do not make a figure that does not answer a manuscript claim.
- Do not let visual attractiveness replace evidence.
- Do not hide small sample size, missingness, or uncertainty.
- Do not imply causality from descriptive charts.
