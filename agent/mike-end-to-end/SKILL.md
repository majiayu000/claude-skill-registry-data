---
name: mike-end-to-end
version: 0.1.0
description: Standard operating procedure for an auditable, headless MIKE+ workflow via the mike-plus MCP server — how to plan, copy, run, QA-gate, compare, plot, audit, and safely stop. Use FIRST whenever an agent is handed a MIKE+ model (.sqlite) or result (.res1d) plus a plain-language goal; it picks the operating mode and tells the agent which mike-* skill to open next and in what order.
---

# MIKE+ End-to-End (SOP)

The other `mike-*` skills describe one tool group each. This one says how they fit
together, what must be true before a number or figure is reported, and when to stop.

## 1. Pick an operating mode (state it in the first reply)

| Mode | When | Chain | License |
|---|---|---|---|
| **A. Read / plot only** | a `.res1d` already exists, or no MIKE+ install | `mike-results` -> `mike-plot` -> `mike-audit` | none |
| **B. Run an existing model** | a `.sqlite` and a goal ("run the 1-year storm") | copy -> `mike-model` -> (`mike_set_scenario`) -> `mike-runner` -> `mike-results` -> `mike-plot` -> `mike-audit` | yes |
| **C. What-if / compare** | "what if the pipe were 0.5 m", "before vs after" | baseline copy + variant copy -> `mike-params` (variant only) -> `mike-runner` x2 -> `mike-compare` -> `mike-audit` | yes |
| **D. Import from SWMM** | an EPA SWMM `.inp` (SWMMCanada, agentic-swmm) | `mike-import` -> then B or C | yes |
| **E. New rainfall** | a CSV storm / gauge record to drive the model | `mike-rain` -> point the model's rainfall boundary at the `.dfs0` (`mike-params`) -> B | rain: none, run: yes |

If the goal only needs Mode A, do not touch mikeplus at all: it is faster and needs no license.

## 2. Standard run directory (create it, use it everywhere)

```
runs/<case>/
  00_model/        COPY of the whole model folder (.sqlite, .mupp, .dfs0, hotstart .res1d ...)
  01_inputs/       rain CSV/.dfs0 you produced, notes
  02_results/      the engine writes next to the model: 00_model/<name>_m1d - Result Files/*.res1d
  03_plots/        every PNG
  manifest.json    mike_manifest_write, written last
```
For Mode C use `00_model_baseline/` and `00_model_<variant>/`: two independent copies.

## 3. Hard rules

1. **Copy first, always the whole folder.** mikeplus has no undo and the MIKE 1D engine writes result files (and a `.log`) next to the model; external files (rain `.dfs0`, hotstart, `.mupp`) are referenced relatively, so copying only the `.sqlite` breaks the run.
2. **Gate on `status`, not `ok`.** `mike_run` returns `ok:true` whenever the call returned. Usable = `status` in `{ok, completed_with_warnings}`; `completed_with_errors` / `incomplete` / `unknown` = do not use the results, surface `errors`, `warnings`, `log_file`.
3. **Discover ids before using them.** `mike_model_info` (setups, scenarios), `mike_results_list` (quantities, element ids), `mike_get_values` (current values). Never invent an element id, table or column.
4. **Warm-up.** Global peaks can sit at t≈0 (initial condition). Pass `skip_hours` to `mike_results_summary` / `mike_results_compare` / `mike_results_flooding` / `mike_plot_profile` and always report `peak_time`.
5. **Variants are copies, not scenarios.** `mike_set_scenario` only activates scenarios that already exist in the model (prepared in the GUI). Table edits made "inside" a scenario are not isolated (see `mike-compare`), so a what-if edit goes on a separate model copy.
6. **License boundary.** run / edit / scenario / import need MIKE+ + a checked-out license; results / plots / compare / rain / manifest do not. On a license failure ("license not available", demo mode, an edit that "did not persist", an import that "exceeds the demo limit") stop that branch and report it; do not retry in a loop, the seat is rate-limited and re-tries make it worse.
7. **Evidence only.** Report a number only from a tool return; report a figure only when the tool returned `ok:true` and `png`; say "not run" for anything skipped.

## 4. Stop rules (stop the branch, report, ask)

- `mike_run` status is `incomplete` / `completed_with_errors` / `unknown`.
- Any license or "did not persist" error.
- The requested element / quantity / table / column does not exist.
- `mike_results_compare` returns `aligned: interpolated` and the two runs were meant to share a time base (different setups were compared).
- The user's model would have to be edited in place (no copy possible).

## 5. QA gates before the final answer

| Claim | Evidence required |
|---|---|
| "the run completed" | `status` in `{ok, completed_with_warnings}` and `result_files` non-empty |
| "peak X at t" | from `mike_results_summary/read/compare`, with `skip_hours` stated |
| "N nodes flood" | `mike_results_flooding` (outlets excluded by default; say so) |
| "the change increased/decreased ..." | `mike_results_compare` deltas, signed, with units and `%` |
| "see figure" | the PNG path returned by a `mike_plot_*` tool |
| "reproducible" | `manifest.json` written, `missing_files: []` |

## 6. Report template (one screen)

1. Mode + what ran: model copy, simulation setup, scenario, elapsed.
2. QA: run status, warnings count, anything skipped and why (license, missing data).
3. Numbers: peaks with units + times, flooded nodes, deltas (for C).
4. Figures: paths.
5. Provenance: manifest path.
6. Not done / next step.

## 7. Skill map

| Skill | Tools | License |
|---|---|---|
| mike-model | mike_model_info, mike_set_scenario | yes |
| mike-params | mike_get_values, mike_set_values | yes |
| mike-runner | mike_run | yes |
| mike-import | mike_import_swmm | yes |
| mike-results | mike_results_list / summary / read / flooding | no |
| mike-compare | mike_results_compare, mike_plot_compare | no |
| mike-plot | mike_plot_rain_flow / timeseries / network / compare / profile | no |
| mike-rain | mike_rain_to_dfs0 | no |
| mike-audit | mike_manifest_write | no |
