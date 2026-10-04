---
name: mike-audit
version: 0.1.0
description: Record provenance for an Agentic MIKE+ step via the mike-plus MCP server — a manifest.json tying the model copy, inputs, edits, run QA status, result files and figures together, each file with a sha256. Use at the end of every run/compare/plot task (successful or failed) so the work can be audited, re-compared or reproduced later. No license required.
---

# MIKE+ Audit

One JSON per case, written last. It is what makes "we ran X and got Y" checkable
a month later, and it is the record a platform layer (SWMM / MIKE+ / LSTM side by
side) can index.

## Tool

- **`mike_manifest_write`** — `{out_json, case?, model?, inputs?[], results?[], figures?[], run?, edits?[], tool_calls?[], notes?}` → writes the manifest and returns `{manifest, missing_files[], n_files, run_status}`.
  - `model`: the `.sqlite` COPY that was run.
  - `inputs`: rain `.dfs0` (incl. ones made by `mike_rain_to_dfs0`), CSVs, hotstart files.
  - `results`: the `result_files` returned by `mike_run` (or the two res1d of a compare).
  - `figures`: every PNG from `mike_plot_*`.
  - `run`: pass the whole `mike_run` return; the QA fields (`status, completed, errors, warnings, issues, log_file, elapsed_s, active_simulation, result_files`) are kept, the log tail is dropped.
  - `edits`: the `mike_set_values` returns (they carry table / muids / before / after).
  - `tool_calls`: ordered `{tool, args, ok}` records of what you called.
  - `notes`: the user's plain-language goal + anything not done and why.

## Manifest shape (`schema: agentic-mike/manifest/1`)

```
created_utc, engine=mikeplus, case,
model{path, exists, bytes, sha256}, inputs[], results[], figures[]  (same shape),
run{status, errors, warnings, ...}, edits[], tool_calls[], notes,
environment{python, platform, mikeplus_mcp}
```

## Conventions

- Write it even when the run failed: `run.status`, `errors` and `notes` are the evidence of *why*.
- `missing_files` must be `[]` before you say the case is complete; a listed path means you referenced something that is not on disk.
- Put it at `runs/<case>/manifest.json`; one case = one manifest (overwrite on re-run of the same case, or use a new case name).
- Never edit a manifest by hand; re-run the tool.

## Orchestration

```
... mike_run -> mike_results_* -> mike_plot_* ...
mike_manifest_write {out_json: runs/<case>/manifest.json, model, inputs, results, figures, run, edits, notes}
```
