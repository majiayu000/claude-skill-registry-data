---
name: mike-compare
version: 0.1.0
description: Compare two MIKE+ runs via the mike-plus MCP server — baseline vs scenario, before vs after a parameter edit — to say WHERE a change mattered and BY HOW MUCH (delta peak, delta volume, timing shift, RMSE/NSE) and to draw the overlay hydrograph. Use whenever two .res1d files of the same model exist or a re-run just finished. Comparing needs no license; producing the second run does.
---

# MIKE+ Compare

Closes the loop `identify -> change -> re-run -> compare`. Works on any two `.res1d`
files with the same element ids (same model, different parameters / scenario / rain).

## Making the two runs (do this on COPIES, not MIKE+ scenarios)

```
runs/<case>/00_model_baseline/   <- copy of the model folder, untouched
runs/<case>/00_model_<variant>/  <- second copy; mike_set_values here only
mike_run on each  -> A.res1d (baseline), B.res1d (variant)
```
Why not `mike_set_scenario` + create a scenario? Verified on MIKE+ 2026: a scenario
created through mikeplus shares its parent's alternatives, so an edit "in the
scenario" changes Base too; and if the scenario is given its own alternatives,
`mikeplus` cannot write into them (`mike_set_values` reports "did not persist").
`mike_set_scenario` is therefore only for running scenarios that were prepared in
the GUI. Copies are unambiguous and audit-friendly.

## Tools

- **`mike_results_compare`** — `{res1d_a, res1d_b, quantity, element?, skip_hours?, top_n?, label_a?, label_b?}`
  - **ranked mode** (no `element`): peak change for every element of `quantity`, sorted by |delta| — `by_element.top[]`, `n_increased / n_decreased / n_unchanged`, `n_only_a/b` (ids missing on one side). Ask this first: "where did my edit matter?"
  - **single mode** (`element` given): `comparison{peak_a, peak_b, delta_peak, delta_peak_pct, peak_time_a/b, peak_time_shift_min, mean_a/b, max_abs_diff(+time), rmse, nse_b_vs_a}`; for flow quantities (unit `m3/s`) also `volume_a/b, delta_volume(_pct)` in `m3`. `aligned` = `exact` (same time base) or `interpolated` (B was interpolated onto A's steps; say so).
- **`mike_plot_compare`** — `{res1d_a, res1d_b, quantity?, element, out_png, label_a?, label_b?, rain_dfs0?, skip_hours?}` → overlay (baseline dashed grey, variant solid orange), optional inverted hyetograph on top. House style; no title.

## Conventions

- Same simulation setup and time window on both sides; pass the same `skip_hours` (warm-up) to both.
- Report deltas **signed, with units and %**, plus the peak times: "peak +0.041 m3/s (+5.2 %), 6 min earlier".
- Volume only for flows; for levels use `mean` / `max_abs_diff`.
- `nse_b_vs_a` measures how different B is from A (1 = identical), not model skill.
- If `n_only_a/n_only_b > 0`, the two runs are not the same network: say so before comparing further.
- Do not claim a figure exists unless the tool returned `{ok:true, png}`.

## Orchestration

```
mike_results_compare (ranked, quantity=Discharge|WaterLevel)  -> top elements
mike_results_compare (element=<top id>)                       -> deltas for the story
mike_plot_compare    (same element, rain_dfs0 if any)         -> 03_plots/compare_<id>.png
mike_manifest_write  (both res1d as results, the edit as edits)
```
