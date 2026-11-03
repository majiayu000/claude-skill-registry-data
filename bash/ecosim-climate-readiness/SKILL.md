---
name: ecosim-climate-readiness
description: Validate the climate forcing selected by an EcoSIM run namelist before simulation or when diagnosing weather-input failures. Checks the remaining run's forcing years, days and hours, NetCDF reader schema, missing values, units and broad physical ranges, and writes read-only readiness reports. Use for existing hourly or mixed daily/hourly EcoSIM forcing, including NLDAS and ERA5-derived files; conversion and gap filling belong to their source-data workflows.
---

# EcoSIM Climate Readiness

Run a deterministic input check against the actual namelist and launch directory.
Do not infer complete coverage from filenames, year coordinates, or successful
NetCDF opening. This skill checks climate inputs; a pass is not whole-case
readiness or evidence of scientific correctness.

## Run the checker

Requires Python 3, NumPy, and netCDF4. From the `ecosim-agent` root:

```bash
python3 .agents/skills/ecosim-climate-readiness/scripts/check_climate_readiness.py \
  /path/to/run/name.namelist
```

- Relative input paths and `rpointer.esim` are resolved from the namelist's
  directory. If launch differs, pass `--run-cwd /actual/launch/directory`.
- Default scope is the remaining simulation: `start_date`, forcing triplets and
  cycle counts, stop settings, and the continuation checkpoint date determine
  what must be available. A branch's `finidat` date must match `start_date`.
- Use `--all-periods` for a full forcing-schedule audit, including completed
  spinup. It intentionally ignores restart/start-date truncation and `stop_n`.
- Reports default to a new timestamped directory under
  `result/climate_readiness/<case>_<UTC timestamp>/`. `--output-dir PATH` selects
  a new destination. Existing report directories are never overwritten.
- Exit **0** means the implemented checks passed (possibly with warnings),
  **1** means invalid inputs/configuration, and **2** means CLI/report-writing
  failure. A shell workflow can use the exit status to gate its authorized run.
  The checker itself never launches EcoSIM or edits inputs.

Read `report.md` and `report.json`. Summarize the checked window, selected files,
status, and failures with their variable, forcing date, one-based hour index,
and affected-value count. Preserve the distinction between **forcing year** and
**model year**, particularly during spinup. Report an invalid restart/stop window
as a configuration issue rather than silently examining a different period.

## What is checked

The helper follows the standalone reader contract documented in
[reader-contract.md](references/reader-contract.md). It covers ordinary
scalar/list Fortran namelists, repetition counts, reverse forcing periods, zero
cycles, Gregorian leap years, hourly stop boundaries, continuation pointers,
and the daily-to-hourly transition. It deduplicates repeated forcing records
and reads one annual variable slab at a time.

It checks the five required hourly meteorological fields, the corresponding six
daily fields when selected, required annual roughness/solar-noon/rain-chemistry
fields, and optional hourly pressure, longwave radiation, and dry deposition
when present. Missing values, NaN/Inf, sentinels and physically implausible
values are failures. A missing December 31 in a non-leap year is a failure;
unused day-366 padding is not. Missing/ambiguous unit metadata is reported;
explicitly incompatible units and unsupported packed data fail.

Also surface misspelled restart options and year-based stops capped by the
forcing schedule. These findings do not imply that weather data caused every
reported model failure.

## Limits and next steps

- Inspect the selected model's reader if it differs from the documented
  standalone contract. Do not treat unsupported ASCII, coupled/prescribed
  forcing modes, non-Gregorian calendars, or unsupported namelist syntax as
  verified. Unsupported inputs fail explicitly; investigate them separately.
- Year/day/hour arrays do not establish timezone, interval labeling, solar-noon
  alignment, or registration against observations. The report retains this
  uncertainty even when numeric checks pass. Other readiness workflows must
  assess provenance and the other case inputs (including GHG forcing and
  climate-adjustment factors).
- The numeric bounds are broad error screens in reader input units, not
  ecological suitability criteria or universal calibration ranges. Review any
  flagged extremes against the source before changing data or thresholds.
- Recommend source-backed repairs or a shorter supported run window. Do not
  silently interpolate, repeat a neighboring day, download replacements, or
  relax checks. After an authorized repair, rerun against the final file.

## Validation

```bash
python3 -m unittest discover -s .agents/skills/ecosim-climate-readiness/tests -v
```

The tests use generated NetCDF fixtures. They cover the SOAP missing-last-day
failure, leap padding, NaN/Inf/sentinels, units/ranges, optional fields, mixed
daily/hourly selection, forcing cycles, run/restart windows, relative paths,
CLI exit codes, and preservation of input files.
