---
name: ecosim-h0-target-extractor
description: Extract typical annual GPP, annual evapotranspiration, mid-season LAI, mid-season root biomass, mid-season shoot biomass, median canopy height, maximum primary-root depth, Vcmax at 25oC, and Jmax at 25oC from EcoSIM h0 NetCDF output files. Use when asked to derive these EcoSIM output targets from a selected .ecosim.h0.*.nc file for model-output processing, trait checks, or benchmark summaries.
---

# EcoSIM h0 Target Extractor

## Purpose

Use this skill to summarize key ecosystem and plant physiological targets from EcoSIM `h0` NetCDF output:

- typical annual GPP
- typical annual ET
- mid-season LAI
- mid-season root biomass
- mid-season shoot biomass
- median canopy height
- maximum primary-root depth
- typical Vcmax at 25oC
- typical Jmax at 25oC

The default "typical" statistic is the median across complete calendar years. The script also reports year-by-year values, mean, standard deviation, minimum, and maximum.

## Workflow

1. Locate the selected EcoSIM h0 file. If no path is given, search `data/` first, then the repository, for `*.ecosim.h0.*.nc`.
2. Run the bundled extractor:

```bash
python3 .agents/skills/ecosim-h0-target-extractor/scripts/extract_h0_targets.py /absolute/path/to/FenStordIsland.ecosim.h0.2010-01-01-00000.nc --format json --output result/ecosim_h0_targets/FenStordIsland_h0_targets.json
```

3. For a human-readable table, also create Markdown:

```bash
python3 .agents/skills/ecosim-h0-target-extractor/scripts/extract_h0_targets.py /absolute/path/to/FenStordIsland.ecosim.h0.2010-01-01-00000.nc --format markdown --output result/ecosim_h0_targets/FenStordIsland_h0_targets.md
```

4. Review warnings, especially time-coordinate inference, cumulative-variable handling, and the Vcmax/Jmax weighting method.
5. Report each target value with its source NetCDF units and range when finite values are available. Do not summarize target values without units.

## Default Variable Mapping

The extractor uses these EcoSIM h0 variables by default:

- annual GPP: `ECO_GPP_col`
- annual ET: `ECO_ET_col`
- mid-season LAI: `ECO_LAI_col`
- mid-season root biomass: `Root_C_pft`
- mid-season shoot biomass: `SHOOT_C_pft`
- median canopy height: `CAN_HT_pft`
- maximum primary-root depth: `Root1stDepz_pft`
- Vcmax at 25oC: `VcMax25C_RUBISCO_pft`
- Jmax at 25oC: `JMax25C_photo_pft`

For Vcmax/Jmax PFT weighting, do not use `LAIstk_pft` by default because it includes stalk area. The default proxy is `SHOOT_C_pft * SLA_pft * 1e-4`, which estimates PFT leaf area index from live shoot C and specific leaf area. This is the closest PFT-resolved proxy available in many EcoSIM h0 files, but it is still a proxy because `SHOOT_C_pft` can include non-leaf shoot tissue. If this proxy is unavailable, use the active-PFT mean and report a warning.

Use command-line overrides such as `--gpp-var`, `--root-var`, `--vcmax-var`, or `--capacity-weight-method active_pft_mean` if a file uses different registry names or if proxy weighting is not appropriate.

## Calculation Rules

- Use complete calendar years only by default. A complete year must include January 1 and December 31 in the inferred or decoded date axis.
- If `ECO_GPP_col` or `ECO_ET_col` is marked as cumulative, annual totals are the year-end cumulative values, not sums of daily rows. This prevents inflated carbon and water budgets.
- If a cumulative variable declines after its within-year peak, report the year-end value as the net annual total and warn that the seasonal peak differs.
- Mid-season defaults to July 1 through August 31. Override with `--midseason-start MM-DD --midseason-end MM-DD` for sites with a different growing-season window.
- Root and shoot biomass are summed over active PFTs and reported as source units, usually `gC/m2`.
- Canopy height is reported as the mid-season median of the tallest active PFT canopy height, usually in `m`.
- Maximum primary-root depth is derived from `Root1stDepz_pft` by taking the maximum over primary-root axes, active PFTs, and complete-year time steps, usually in `m`.
- Vcmax and Jmax are weighted by the shoot-C/SLA leaf-area proxy when available. If unavailable, use the active-PFT mean and report that choice.
- Preserve source units and variable metadata in JSON output. Treat annual totals as source mass or water-depth units per year by temporal context, not by silently rewriting NetCDF units.
- JSON output must include the top-level `target_units` and `target_ranges` lookups as well as per-metric `units`, `min`, and `max` fields. Markdown output must include dedicated units and range tables. CSV output must include units and range columns.

## Date Handling

The script uses a real `time` coordinate when present. Some EcoSIM h0 files contain `time_bounds` but no time-coordinate units; in that case the script infers the first date from the filename pattern `YYYY-MM-DD`, such as `FenStordIsland.ecosim.h0.2010-01-01-00000.nc`. Use `--start-date YYYY-MM-DD` to override this inference.

## Reporting

Report the output file path, selected h0 file, complete years used, mid-season window, typical median values with units and ranges, and warnings. If the annual GPP or ET method is `year_end_cumulative`, explicitly mention that the script did not sum daily cumulative rows.
