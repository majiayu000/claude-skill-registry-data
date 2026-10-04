---
name: mike-rain
version: 0.1.0
description: Turn a timestamped rainfall CSV (design storm, gauge record, climate-scenario series) into a MIKE+ rainfall .dfs0 via the mike-plus MCP server, verified by read-back, ready to drive a model's rainfall boundary or to sit on top of a hydrograph figure. Use when the user brings rain as CSV or asks to run a model with a different storm. No license required (writing the file); wiring it into the model needs one.
---

# MIKE+ Rain

MIKE+ rainfall boundaries read a `.dfs0` of **Rainfall Intensity, mm/h,
mean-step-backward**: exactly the shape of DHI's own example rain files
(`Sirius_IDF_1year_rainfall.dfs0`). This skill produces that file from a CSV.

## Tool

- **`mike_rain_to_dfs0`** — `{csv, out_dfs0, time_col?, value_col?, unit?, item_name?}`
  - `unit`: `'mm/h'` (intensity, default) or `'mm'` (depth per step, converted with each step's own duration; the conversion is reported).
  - Returns `{dfs0, item, n_steps, start, end, timestep_s, uniform_step, total_depth_mm, peak_intensity_mm_h, peak_time, conversion}` after reading the file back.

## Conventions

- Time column first, value column second by default; name them if the CSV differs.
- Rejects negative values, non-numeric cells, unsorted duplicates, fewer than two steps: fix the CSV, do not silently clean it.
- Report `total_depth_mm` and `peak_intensity_mm_h`; if `uniform_step` is false say so (MIKE 1D accepts irregular steps, but the user should know).
- The tool never touches the model. To make a MIKE 1D model use the new rain, edit its rainfall boundary with `mike-params` on a COPY. The boundary lives in table **`msm_BBoundary`** (the rainfall row has `TypeNo = 1`; in Sirius_RTC its MUID is `Rainfall`) with columns
  - `TSConnection` = dfs0 path **relative to the model folder** (DHI's example: `Sirius_IDF_1year_rainfall.dfs0`), so write the new file into the model copy folder,
  - `TimeseriesName` = the dfs0 **item name** (must match: pass `item_name` to `mike_rain_to_dfs0`, or set this column to `Rainfall`),
  - `DataTypeName` = `Rainfall Intensity`.
  `mike_get_values {table: msm_BBoundary, columns: [TypeNo, TSConnection, TimeseriesName, DataTypeName]}` first, then `mike_set_values` on that MUID, then run and check `mike_results_summary`.
- The same `.dfs0` is what `mike_plot_rain_flow` / `mike_plot_compare` take as `rain_dfs0`, so use it for the figure of the run it drove.

## Orchestration

```
mike_rain_to_dfs0 {csv, out_dfs0: runs/<case>/00_model/storm.dfs0, item_name: <existing TimeseriesName or 'Rainfall'>}
mike_get_values  {sqlite: <copy>, table: msm_BBoundary, columns: [TypeNo, TSConnection, TimeseriesName]}
mike_set_values  {sqlite: <copy>, table: msm_BBoundary, muids: [<rain row>], values: {TSConnection: storm.dfs0, TimeseriesName: ...}}
mike_run -> mike_results_summary (skip_hours) -> mike_plot_rain_flow {rain_dfs0: storm.dfs0}
mike_manifest_write {inputs: [csv, storm.dfs0], ...}
```
