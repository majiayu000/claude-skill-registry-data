---
name: ecosim-evaluation-output-check
description: Verify EcoSIM evaluation-output coverage with an isolated one-year run. Use before model-data comparison or a full site run when observations need matching history variables, units, temporal/depth support and plant pools; also diagnose missing evaluation outputs. This checks output readiness, not model skill or a replacement for the two-year plant-trait smoke test.
---

# One-year evaluation output check

Use a one-year cold-start run to establish what the selected executable actually
writes. A successful process exit or a variable name in source code is insufficient.

## Select targets from observations

1. Inventory actual nonmissing observations for the requested site, including
   QC, dates, units, depths, organs and uncertainty. Use the BIF timeseries skill
   for irregular field records and inspect tower values, not just CSV headers.
   Distinguish observations, partition-derived GPP/respiration, forcing inputs,
   calibration data and unavailable series. Do not invent grain yield from a
   `Total` or `Foliage` production record.
2. Choose one calendar year with required climate and management coverage,
   preferably overlapping useful observations. Record why it was selected. This
   cold-start year tests output plumbing; it is not an equilibrated prediction.
3. Write a manifest using [references/manifest.md](references/manifest.md) and
   the mappings in [references/target_mapping.md](references/target_mapping.md).
   Include **every relevant observation target**, marking unresolved mappings
   `blocked` with the reason instead of dropping them. Trace units, sign,
   cumulative/instantaneous semantics, depth support and tissue pools through
   the active history registration and update code. Do not assume that defaults
   include requested fields or that relative saturation equals volumetric water.

## Prepare, run and verify

Run from the `ecosim-agent` root (Python, NumPy and netCDF4 required):

```bash
python .agents/skills/ecosim-evaluation-output-check/scripts/check_outputs.py prepare \
  --namelist result/SITE/run_dir/SITE.namelist --manifest /path/to/manifest.json \
  --scratch result/SITE/output_check/unique-run
python .agents/skills/ecosim-evaluation-output-check/scripts/check_outputs.py run \
  --scratch result/SITE/output_check/unique-run --exe /path/to/ecosim.f90.x
```

`prepare` copies selected inputs into a new scratch case, requests the union of
existing history selections and required manifest fields, fixes daily h0 output,
and sets one selected forcing/model year, fresh initialization and annual stop.
The source case and existing runs/restarts stay untouched. It checks registry
names and year axes; the full climate-readiness checker runs before execution.
Required fields registered with `default='inactive'` are explicitly enabled via
`hist_fincl1`; do not change their Fortran registration defaults. Required fields
are removed from conflicting `hist_fexcl1` entries in the scratch namelist,
while unrelated selections/exclusions remain. `plan.json` and `report.json`
record these changes. The subsequent NetCDF check must confirm the fields were
actually emitted; adding a name alone does not establish successful output.
Unsupported namelist syntax, coupled/daily-only forcing or restart initialization
must be resolved explicitly rather than silently approximated.

Before launch, `run` enforces the shared
[case preflight](../ameriflux-namelist-generator/references/case_preflight.md)
on both the source production request and the one-year scratch case. A missing
later production year blocks even if the selected short year is complete. Source
namelist changes require a new prepared case. Unsupported model namelist keys
are errors even when another model version or a template supports them.

Select/build the intended executable using repository `AGENTS.md` toolchain
instructions. `run` rejects an executable older than selected Fortran sources;
`--allow-stale-executable` is an explicit diagnostic exception, retained in the
report, not evidence that the source and executable agree. The default wall-time
limit is two hours; adjust `--timeout-seconds` for the selected case. A failure
or timeout is reported without automatic parameter changes or continuation.
Use a new scratch path for each retry; preserve previous reports/logs.

To recheck already generated scratch output without rerunning EcoSIM:

```bash
python .agents/skills/ecosim-evaluation-output-check/scripts/check_outputs.py check \
  --scratch result/SITE/output_check/unique-run
```

Review `report.json` and `report.md`. The checker requires the expected number
of hourly steps, full-year daily history bounds, each required field in **every**
h0 file, compatible metadata, valid dimensions, and finite non-fill data in
all records on at least one consistent cell/PFT/layer. It scans all written
numeric history fields for unmasked NaN/Inf. Explicit manifest checks can require
nonzero values or variation when physically appropriate. Inactive/fill-only
PFT slots are not themselves errors; all-fill target output is an error.

The current history uses day-offset `time_bounds` without units. The checker
accepts exactly contiguous `[0,1] ... [days-1,days]` only for its controlled daily
scratch namelist, reporting that inferred convention. Other bounds must be
handled explicitly; the filename alone does not prove year coverage.

## Resolve gaps and preserve the outcome

- A requested field absent from the registry needs a history mapping or model
  instrumentation, not a guessed alias. Follow model-repository instructions for
  any authorized registration/allocation/update work, build and rerun the check.
- Missing output, units, finite data or depth/pool support prevents an overall
  pass. Target-specific `blocked` issues yield an incomplete result even if the
  other history fields pass. Preserve observation-unit/depth uncertainty in the
  manifest; the script cannot establish scientific equivalence from strings.
- Refresh inherited manifests against current registry/output and observation
  metadata before reuse. A previously blocked net-radiation mapping or unknown
  sensor depth may already have been resolved in a later site evaluation.
  Record the evidence for each revision; do not repeat stale missing-data
  claims or mark a conditional conversion as exact. Report process/history
  success, mapped-target passes and unresolved scientific mappings separately:
  an overall `incomplete` report is not necessarily an execution failure.
- `VSPore_vr * rWatFLP_vr` made from separately averaged daily fields is not
  necessarily mean volumetric water content. Prefer a directly accumulated
  volumetric-water field or demonstrate the needed instantaneous/time-weighted
  conversion and pore basis. Do not hide this gap by requesting two names only.
- Once coverage is verified, carry the reviewed history selections into the
  production namelist within the requested preparation scope, preserving its
  dates, forcing cycles, restart choices and other settings. Save the exact
  diff and input/executable identities; a scratch pass alone does not update
  production output controls. Rerun the relevant check if the mapping changes.
  Include all required inactive-by-default fields in production `hist_fincl1`
  as well, and reconcile their `hist_fexcl1` entries. Preserve reviewed `:A`/`:I`
  averaging qualifiers; a conflicting existing qualifier must be resolved using
  the manifest's temporal semantics, rather than appending a duplicate name.
- Record this as an evaluation-output check in the existing site tracker/guide;
  do not mark the two-year plant-trait smoke test, full simulation or scientific
  evaluation complete. Explain unsupported targets and what remains to enable.

## Validation

```bash
python -m unittest discover -s .agents/skills/ecosim-evaluation-output-check/tests -v
```
