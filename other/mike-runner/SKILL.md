---
name: mike-runner
version: 0.2.0
description: Run MIKE+ simulations headless via the mike-plus MCP server and report result files + engine status. Use when an agent must execute a MIKE+ .sqlite model's active (or a named) simulation without opening the MIKE+ GUI, then hand the .res1d outputs to reading/plotting. Requires MIKE+ installed + a valid license. Always run on a copy.
---

# MIKE+ Runner

Executes a MIKE+ model headless through the `mike-plus` MCP server (engine: MIKE 1D).

## When to use
After a model is ready and you need to actually run it — the active simulation, or a named setup from `msm_Project`. Do **not** use this to read results (that's `mike-results`) or to plot (`mike-plot`). The whole-workflow rules (run directory, copy policy, stop rules, QA gates) are in `mike-end-to-end`; a baseline-vs-variant pair of runs is compared with `mike-compare`.

## Tool
- **`mike_run`** — args: `sqlite` (path), `simulation` (optional setup id), `timeout_s` (optional). Returns `{ok, active_simulation, result_files[], elapsed_s}`, a parsed QA gate `{completed, errors, warnings, issues, status, log_file}`, and `_log_tail` (engine console).

## Conventions (evidence boundaries)
- **License + install required.** `mike_run` loads the local MIKE 1D engine; it fails on a machine without MIKE+ + a valid license. (Reading/plotting do not.)
- **Always run on a COPY.** mikeplus has no undo — copy the model folder first and run the copy, never the user's original.
- **Gate on the QA fields, not just `ok`.** `ok` only means the call returned. Check `status`: `ok` / `completed_with_warnings` are usable; `completed_with_errors` or `incomplete` mean the run is untrustworthy — surface `errors`/`warnings` and point at `log_file` for detail, don't bury them. `status="unknown"` means no engine log was found.
- Do not fabricate metrics. Pass the returned `result_files` to `mike-results` / `mike-plot`, and the whole return value to `mike_manifest_write` (`mike-audit`).

## Orchestration
```
mike_model_info  -> confirm the active simulation / pick one (mike_set_scenario if a GUI scenario is wanted)
mike_run         -> result_files (.res1d) + status
        -> mike-results (summary / flooding / read)  -> mike-plot  -> mike-audit
```
