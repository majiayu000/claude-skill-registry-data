---
name: ecosim-site-run-tracker
description: Track and report progress of a request to create and run an EcoSIM case for a site ("create an ecosim run for site US-UMB", "set up and run EcoSIM at <site>"). Records four stages — data preparation, namelist creation, model simulation, and output evaluation — in result/<SITE_ID>/progress.json and PROGRESS.md, derives step status from files and quality reports on disk, and records manual results such as the executable, test run, and evaluation verdicts. Use at the start of such a request, after each stage, and whenever the user asks where a site run stands.
---

# EcoSIM Site Run Tracker

## Use When

- The user asks to create, set up, or run an EcoSIM case for a site.
- The user asks for the status of a site run, or what remains to be done.
- A stage of a site run has just finished or failed.

## Stages and Steps

| Stage | Steps | Detected from |
| --- | --- | --- |
| Data preparation | `site_metadata`, `climate_forcing`, `atmospheric_chemistry`, `soil_grid`, `plant_management`, `soil_management` | `<SITE_ID>_ecosim_site.json` (location checks, run live if not recorded), `<SITE_ID>_ecosim_climate_<first>-<last>.nc` and ERA5 quality report (time registration, ZNOONG, tower warnings), climate derivation report (derived chemistry), grid NetCDF and layer validation (run live if not recorded), plant and soil management NetCDF |
| Namelist creation | `run_folder`, `namelist`, `chronology` | `result/<SITE_ID>/{input,run_dir}`, namelist paths resolving from `run_dir/`, `stop_n` equal to EcoSIM `get_sim_len` of `forc_periods` |
| Model simulation | `executable`, `smoke_test`, `plant_traits`, `full_run` | executable recorded by the smoke run; `smoke_run/smoke_summary.json` from `create_site_smoke_run.py` (2-year run: exit, steps, history scan); its `trait_check` and literature-backed correction rounds (`done` when corrections fixed every severe finding; `failed` when findings remain unresolved or rounds ran out; without corrections, strict errors fail and warnings or missing web evidence give `warning`); `*.ecosim.h0.*.nc` history files in `run_dir/` (reported `in_progress` until the run is confirmed) |
| Output evaluation | `target_extraction`, `benchmark_comparison`, `evaluation_report` | files in `result/<SITE_ID>/evaluation/` named `*targets*`, `*comparison*`/`*benchmark*`, `*report*` |

Statuses: `pending`, `in_progress`, `done`, `warning`, `failed`, `skipped`. A stage is `failed` if any step failed, `done`/`warning` when every non-skipped step is done, `pending` when none started, else `in_progress`.

## Workflow

Run from the python-tools repository root.

1. At the start of the request, initialize the tracker with the request text:

   ```bash
   python .agents/skills/ecosim-site-run-tracker/scripts/site_run_tracker.py init \
     --site-id US-UMB --request "create an ecosim run for site US-UMB"
   ```

2. After each stage (site inputs generated, run folder created, run finished, evaluation written), rescan and relay changed statuses to the user:

   ```bash
   python .agents/skills/ecosim-site-run-tracker/scripts/site_run_tracker.py scan --site-id US-UMB
   ```

3. Record what files cannot show. A manual status is kept across scans; `--auto` returns the step to detection.

   ```bash
   python .agents/skills/ecosim-site-run-tracker/scripts/site_run_tracker.py set --site-id US-UMB \
     --step soil_management --status skipped --note "Unmanaged forest"
   python .agents/skills/ecosim-site-run-tracker/scripts/site_run_tracker.py set --site-id US-UMB \
     --step executable --status done --note "build/<config>/.../ecosim.f90.x (gfortran 14)"
   python .agents/skills/ecosim-site-run-tracker/scripts/site_run_tracker.py set --site-id US-UMB \
     --step full_run --status done --note "exit 0; 113 years; h0 files to 2021"
   ```

4. Answer status questions from `show` (or `show --json`) after a fresh `scan`.

## Automatic Updates

These scripts rescan the tracker when they finish (creating it if needed), so data-preparation and namelist steps stay current without an explicit `scan`:

- `Tools/create_ecosim_climate_forcing.py`
- `Tools/create_ecosim_grid_forcing.py`
- `.agents/skills/unified-ameriflux-extractor/unified_ameriflux_extractor.py`
- `.agents/skills/ameriflux-namelist-generator/scripts/create_site_run_folder.py` (also after a failed assembly)

They call `Tools/run_progress.py`, which never fails the calling script; set `ECOSIM_PROGRESS_TRACKER=0` to disable. Simulation and evaluation steps still need `set`, because no tracked script runs EcoSIM or judges its output. Run `init --request` yourself so the request text is recorded.

## Rules

- Mark `full_run` done only after confirming the model exited normally and covered the namelist period; history files alone mean the run started, not that it finished.
- `smoke_test` and `plant_traits` are detected from `smoke_run/smoke_summary.json`; a passed smoke run shows the case runs, not that it is scientifically correct. Leave `plant_traits` failed or warning until the findings are reported to the user; set it manually only to record an explicit decision (e.g. "accepted for this run").
- Keep failed steps visible with the reason in `--note`; do not reset them to pending to tidy the report.
- `skipped` is for steps that do not apply (e.g. soil management at an unmanaged site), not for steps not yet done.
- Put evaluation products under `result/<SITE_ID>/evaluation/` so they are detected, e.g. `ecosim-h0-target-extractor` output as `evaluation/<SITE_ID>_h0_targets.json`.

## Files

```text
result/<SITE_ID>/
  progress.json   tracker state (stages, steps, status, source auto|manual, detail, note, evidence, timestamps)
  PROGRESS.md     rendered summary with open items
  input/          site inputs (ameriflux-namelist-generator run-folder layout)
  run_dir/        namelist and, after running, EcoSIM output
  smoke_run/      2-year smoke run, its plant_trait.desc, trait-check report, smoke_summary.json
  evaluation/     output-evaluation products
```

`create_site_run_folder.py` leaves `progress.json` and `PROGRESS.md` at the site root.
