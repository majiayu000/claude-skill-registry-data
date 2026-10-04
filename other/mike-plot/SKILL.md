---
name: mike-plot
version: 0.2.0
description: Produce publication-style figures from MIKE+ .res1d results via the mike-plus MCP server — a stacked rainfall-runoff hydrograph, a single time series, a network map, a baseline-vs-scenario overlay, or a longitudinal profile (bed / crown / ground / max water level along a pipe string), in the house style (Arial 12, ticks inward, SI units, no title). Use when an agent must render MIKE+ results as a PNG without opening the GUI. No license required.
---

# MIKE+ Plot

Renders MIKE+ results in the project house style. **No license / no MIKE+ install needed.**

## House style (do not change without being asked)
Arial 12 · ticks inward (`direction='in'`, both axes) · SI units · **no title** · inverted hyetograph · dpi 300. Rain `#4C78A8`, flow `#F58518`, baseline-in-a-comparison `#4D4D4D` (dashed). Style lives in `mikeplus_mcp/contracts/plot_style.py` and is shared with the SWMM figures layer.

## Tools
- **`mike_plot_rain_flow`** — `{res1d, element, quantity?='Discharge', rain_dfs0?, out_png}` → stacked two-panel figure: **rainfall inverted on top, flow on the bottom**, shared time axis. `rain_dfs0` is optional (a `.dfs0`); without it only the flow panel is drawn.
- **`mike_plot_timeseries`** — `{res1d, quantity, element, out_png}` → single-panel series.
- **`mike_plot_network`** — `{res1d, out_png}` → network layout map (reaches as lines, nodes as points, equal aspect). Use for an overview / location figure of the whole model.
- **`mike_plot_compare`** — `{res1d_a, res1d_b, quantity?, element, out_png, label_a?, label_b?, rain_dfs0?, skip_hours?}` → overlay of the same series from two runs (baseline dashed grey, scenario solid), optional hyetograph on top. Numbers come from `mike_results_compare` (see `mike-compare`).
- **`mike_plot_profile`** — `{res1d, reaches?[] | from_node + to_node, out_png, skip_hours?}` → longitudinal profile along a pipe string: bed/invert, pipe crown (invert + height), ground level (interpolated between nodes) and the **max water level envelope** vs cumulative chainage, node boundaries marked. Give the ordered reach ids, or two node ids and the shortest chain is found (flow direction first). Returns `reaches`, `length_m`, `max_water_level` (+ chainage, reach), `min_freeboard_m`, `connectivity_problems`.

## Conventions
- Discover valid `element` / `quantity` / node ids with `mike_results_list` first; don't guess ids.
- Do not claim a figure exists unless the tool returned `{ok:true, png:...}` and the file was written.
- Keep units SI and the style fixed; expose only data choices (which element/quantity, which rainfall file, which reach chain) to the user.
- Profiles: pass `skip_hours` so the envelope is the storm, not the initial condition; if `connectivity_problems` is non-empty the chain you gave is not contiguous, say so.
- Long chains (> 15 reaches) label only the end nodes; that is by design, not a missing feature.

## Unsupported / not-yet plot types (decision order)
Requests like a stage-discharge curve, a flooding map, a 2D (dfsu) inundation map, catchment runoff panels, or an animated profile are not covered. Do not force an existing tool to fit them:
1. Confirm the `.res1d` (or other file) exists and `mike_results_list` shows the quantity/element.
2. If an existing tool covers it, use it. If not, pull the numbers with `mike_results_read` / `mike_results_compare` and say the figure type is not available yet.
3. A new plot type is added by extending `contracts/plot_style.py` + `workers/plot_worker.py` + `tools/plot.py` (house style, tested on a real res1d) — do not paint ad-hoc matplotlib in a chat unless the user asks for a one-off.

## Orchestration
```
mike_results_list  -> pick element + quantity (or a reach chain / two nodes)
mike_plot_rain_flow | mike_plot_timeseries | mike_plot_network | mike_plot_compare | mike_plot_profile -> out_png
```
