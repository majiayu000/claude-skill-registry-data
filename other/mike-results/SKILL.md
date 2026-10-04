---
name: mike-results
version: 0.2.0
description: Read MIKE+ .res1d results via the mike-plus MCP server — list contents, summarize peaks, extract a single time series, or check which nodes flood (peak water level vs ground level). Use when an agent needs to inspect or pull numbers from MIKE+ network results (node water levels, link/reach discharge, velocities, flooding). No MIKE+ license or installation required.
---

# MIKE+ Results

Reads MIKE+ `.res1d` result files (via mikeio1d). **No license / no MIKE+ install needed** — fully portable.

## When to use
To find out what is in a result file, get peak values, extract a series for analysis/plotting, or answer "which manholes flood?". Use after `mike_run`, or on any existing `.res1d`. (Two result files side by side: `mike-compare`.)

## Tools
- **`mike_results_list`** — `{res1d}` → quantities, element counts + sample ids (nodes/reaches/structures/catchments), time range. Start here to discover valid `quantity`/`element` values.
- **`mike_results_summary`** — `{res1d, quantities?, skip_hours?}` → per-quantity peak (value, element, chainage, time), in the canonical schema.
- **`mike_results_read`** — `{res1d, quantity, element, max_points?}` → a single downsampled time series (`times`, `values`, `unit`, `peak_value`, `peak_time`).
- **`mike_results_flooding`** — `{res1d, skip_hours?, top_n?, include_outlets?}` → per node: peak water level vs `ground_level` (and `critical_level`) → `n_flooded`, `flooded[]` ranked by exceedance (`freeboard_m` < 0, with `peak_time`, node `type`), `n_above_critical`, `closest_to_flooding[]`. Outlets are skipped by default (their level is the boundary, not flooding).

## Conventions
- Column identity is `Quantity:ElementId[:chainage]` (e.g. `Discharge:Link_29:33.5333`). `element` matches the id prefix.
- Output follows the canonical, engine-agnostic schema (`{engine, quantity, element_id, chainage, unit, ...}`) so the same downstream skills work for SWMM/LSTM later. (`mike_results_summary` reports the peak's element as `peak_element` — same idea, named for the peak.)
- **Global-max caveat:** `mike_results_summary` returns the max over the WHOLE run, which can land in the warm-up / initial-condition period (e.g. a base-flow value near t=0), not the storm peak. Always check `peak_time`; when you want the event peak, pass `skip_hours` (e.g. `skip_hours: 6`) to drop the initial window. The same applies to `mike_results_flooding`.
- Flooding is judged against the ground level stored in the result file. Nodes with an obviously artificial `critical_level` (e.g. 100 m) or river/basin nodes may carry a nominal ground level: report the `type` and level, and let the user judge; do not filter them silently (only outlets are excluded by default, and that is stated in the output).
- Report only what the file contains; if a `quantity`/`element` has no series, say so (the tool errors with a clear message) rather than guessing.

## Orchestration
```
mike_results_list      -> learn quantities + element ids
mike_results_summary   -> peaks for a quick read (skip_hours)
mike_results_flooding  -> flooded nodes ranked (skip_hours)
mike_results_read      -> a series for a specific element  -> mike-plot
```
