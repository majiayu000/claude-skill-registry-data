---
name: scientific-viz-executor
type: executor
description: "Execute scientific visualization implementations — plots, figures, statistical charts."
version: 0.1.0
---

# Scientific Visualization Executor Skill

## When to Use

**Primary triggers:**
- "plot this function", "3D surface plot", "network graph", "vector field"
- "generate a scientific visualization", "create a contour plot"
- "visualize this molecular structure", "plot the phase diagram"
- User has scientific/mathematical data and needs an interactive HTML visualization
- User has a dataviz-planner spec for a scientific chart type

---

## Do Not Use When

- You need a **standard chart** (bar, line, scatter, pie) — use `dataviz-executor`
- You need to **design** a visualization — use `dataviz-planner` first
- You need to **review** a visualization — use `dataviz-critic`
- You need a **dashboard** with multiple charts — use `dashboard-executor`
- You need **statistical analysis** — analyze first, then visualize
- You need **Python/R output** — this produces HTML only

---

## Resolution Paths

| Situation | Route |
|-----------|-------|
| Need 3D surface, network, or math plot | This skill |
| Need standard bar/line/scatter chart | Use `dataviz-executor` |
| Need to design the visualization first | Use `dataviz-planner`, then come back |
| Have a visualization, need review | Use `dataviz-critic` |
| Need multiple charts in a dashboard | Use `dashboard-executor` |

---

## Supported Visualization Types

| Type | Library | Use Case |
|------|---------|----------|
| 3D Surface | Plotly.js | Potential energy, topography, response surfaces |
| 3D Scatter | Plotly.js | Molecular structures, point clouds, PCA |
| 3D Mesh | Plotly.js | Isosurfaces, molecular surfaces |
| Network Graph | Cytoscape.js | Citations, protein interaction, dependencies |
| Force-Directed Graph | D3.js v7 | Small networks (<500 nodes) |
| Function Plot | Plotly.js + KaTeX | Math functions, parametric curves, polar plots |
| Phase Diagram | D3.js + SVG | State transitions, stability regions |
| Vector Field | D3.js + SVG | Flow fields, gradients, EM fields |
| Contour Plot | Plotly.js | Topographic maps, probability density |
| Scientific Heatmap | Plotly.js | Correlation matrices, gene expression |

---

## What You Get

- **Self-contained HTML file** with appropriate CDN libraries (Plotly.js, D3.js, Cytoscape.js, KaTeX)
- **Scientific color maps** (Viridis, Plasma, Inferno, Magma, Cividis — all colorblind-safe)
- **Unit-aware axis labels** (e.g., "Energy (eV)", "Distance (nm)")
- **Uncertainty and publication-readiness checks** (error bars/confidence bands when available, multi-panel consistency, export constraints, grayscale legibility)
- **LaTeX equations** rendered via KaTeX
- **Interactive controls** (3D orbit, network drag, tooltips)
- **Deviation log** and **critic handoff command**

---

## Companion Skills

- **dataviz-planner** (upstream): Designs the visualization plan
- **dataviz-critic** (downstream): Reviews the generated visualization

---

## meta-router Registry Note

Listed under the **Executors** table.
Trigger signals: `3D plot, surface plot, network graph, force graph, function plot, vector field, phase diagram, contour plot, scientific visualization, mathematical plot, LaTeX plot`
