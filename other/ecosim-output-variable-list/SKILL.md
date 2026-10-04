---
name: ecosim-output-variable-list
description: Extract and update the EcoSIM output-variable catalog from Fortran history-field registration calls such as hist_addfld1d and hist_addfld2d. Use only when explicitly asked to update, regenerate, refresh, or rebuild the list of EcoSIM output variables from HistDataType.F90 or related F90 source; do not invoke for ordinary EcoSIM output analysis unless the variable list itself must be updated.
---

# EcoSIM Output Variable List

## Purpose

Use this skill to rebuild the catalog of EcoSIM model output variables registered in Fortran history files. The source of truth is `call hist_addfld...(...)` registration calls, especially in `HistDataType.F90`.

The catalog is meant to guide downstream EcoSIM output processing: variable selection, dimension handling, aggregation interpretation, unit checks, and NetCDF metadata review.

## Workflow

1. Locate the selected `.F90` source. If the user gives a path, use it. If no path is given, search `data/` first, then the repository, for `HistDataType.F90` or files containing `hist_addfld`.
2. Create an output folder under `result/`, for example:

```bash
mkdir -p result/ecosim_output_variables
```

3. Run the bundled extractor. Prefer JSON for automated processing and CSV for quick review:

```bash
python3 .agents/skills/ecosim-output-variable-list/scripts/extract_hist_output_vars.py /absolute/path/to/HistDataType.F90 --format json --output result/ecosim_output_variables/ecosim_output_variables.json
python3 .agents/skills/ecosim-output-variable-list/scripts/extract_hist_output_vars.py /absolute/path/to/HistDataType.F90 --format csv --output result/ecosim_output_variables/ecosim_output_variables.csv
```

4. Inspect the summary. Report total fields, counts by `hist_addfld*` routine, counts by rank, the number of dynamic `fname` expressions, and any duplicate literal variable names.
5. Preserve dynamic names as templates instead of inventing expansions. For example, names built from `trim(micpar%cplxname(jj))` or `trim(fieldname)` should remain marked with `is_dynamic_fname=true` unless the loop values are explicitly available from source or runtime configuration.
6. Use the catalog to guide processing code. Preserve the registered `units`, `avgflag`, `type2d`, `pointer_kind`, `pointer_target`, `long_name`, `condition_context`, and `loop_context` fields.

## Output Contract

Each extracted variable record includes:

- `source_file`, `source_line`, `end_line`: where the history registration call appears.
- `addfld_subroutine`: the registration routine, such as `hist_addfld1d` or `hist_addfld2d`.
- `rank`: derived from the routine name when possible (`1d`, `2d`, etc.).
- `fname`: literal variable name when available; otherwise a readable template.
- `fname_expr`: raw Fortran expression for `fname`.
- `is_dynamic_fname`: true when `fname` is assembled from expressions.
- `units`, `avgflag`, `type2d`, `default`, `long_name`: named arguments from the registration call.
- `pointer_arg`, `pointer_kind`, `pointer_expr`, `pointer_target`: pointer metadata used to infer whether the output is column-, patch-, or other domain-oriented.
- `condition_context`, `loop_context`, `enclosing_subroutine`: lightweight source context for conditional and loop-registered variables.

## Interpretation Rules

- Do not include commented-out `hist_addfld` calls in the active variable list.
- Treat `avgflag` as EcoSIM history metadata and preserve it verbatim. Do not change temporal units solely from `avgflag`; check whether units already encode rates (`/hr`, `/s`) or interval totals (`gC/m2`, `mm H2O/m2`).
- Treat `type2d` as the vertical or secondary dimension key for 2-D history variables, such as `levsoi`, `levcan`, `node`, `rootaxs`, `elements`, or `pmorphunits`.
- Flag unit inconsistencies for review, especially carbon, nitrogen, phosphorus, gas, water, and heat variables where `g`, `mol`, `umol`, `m2`, `m3`, `hr`, and `s` conversions can create mass-balance errors.
- Do not edit the Fortran source unless the user asks for code changes. This skill updates the output-variable catalog derived from the source.

## Reporting

When reporting the update, include the catalog paths, record counts, dynamic-name examples, duplicate-name warnings if any, and the selected F90 source path. Keep the output focused on how the catalog should guide EcoSIM model-output processing.
