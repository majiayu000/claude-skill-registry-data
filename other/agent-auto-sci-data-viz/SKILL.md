---
name: agent-auto-sci-data-viz
description: "数据分析与科学可视化子 skill。用于 EDA、数据质量审计、统计检验选择、效应量、稳健性分析、表格设计、出版级图件、文献计量图表、政策矩阵、交互式 HTML 仪表盘和论文图注写作。触发于 exploratory data analysis、statistics、matplotlib、seaborn、scientific visualization、table design、figure plan、dashboard 等任务。"
---

# Agent Auto Sci Data Viz

Use this subskill whenever data, tables, or figures are central to the output.

## Fast Workflow

1. Inspect file types and schema.
2. Audit missingness, outliers, duplicates, ranges, and units.
3. Define each table or figure by the claim it should support.
4. Choose statistical tests and effect sizes before writing results.
5. Use publication-safe palettes and legible dimensions.
6. Export reproducible figures and record code paths.
7. Write captions that stand alone.

Read `references/data_analysis_visualization_workflows.md`.

For full paper projects, this skill owns EDA, statistical-test reporting, robustness visualization, table shells, publication figure planning, figure-title/caption checks, and final visual evidence audits. It should work with `agent-auto-sci-geospatial` for maps and with `agent-auto-sci-scicomm` for figure narrative.

For deeper K-Dense-style encapsulation:

- `references/k_dense_data_viz_mapping.md`: how EDA, statistics, scientific visualization, matplotlib, seaborn, and network analysis are adapted.
- `references/review_bibliometric_figure_system.md`: figure system for review, bibliometric, policy agenda, and sport geography empirical manuscripts.

## Related Helper Skills

- `exploratory-data-analysis`
- `statistical-analysis`
- `matplotlib`
- `seaborn`
- `scientific-visualization`
- `networkx`
- `xlsx`

## Must Not Do

- Do not make decorative charts that do not answer a research question.
- Do not choose tests after seeing desired significance.
- Do not use color palettes that fail grayscale or colorblind checks.
- Do not let map/figure aesthetics override evidence clarity.

