---
name: ssp-ghg-atmgas-generator
description: Build EcoSIM atmospheric greenhouse-gas forcing files by combining a historical monthly atmgas NetCDF with RCMIP/CMIP6 SSP concentration pathways. Use when Codex needs SSP245/SSP585 or other SSP atmospheric CO2, CH4, and N2O concentrations, key-year tables, or scenario NetCDF files spanning historical years through 2100 for EcoSIM or related biogeochemical forcing workflows.
---

# SSP GHG Atmgas Generator

## Overview

Create scenario-specific atmospheric concentration forcing for EcoSIM by splicing historical monthly CO2, CH4, and N2O data with RCMIP annual SSP concentration pathways. Prefer the bundled script for reproducibility and unit-safe NetCDF writing.

## Data Sources

- Historical input: an EcoSIM-style NetCDF with `time`, fractional `year`, and `CO2`, `CH4`, `N2O` variables.
- Future pathway input: RCMIP concentrations annual means CSV, usually `rcmip-concentrations-annual-means-v5-1-0.csv`.
- Default RCMIP URL:

```text
https://rcmip-protocols-au.s3-ap-southeast-2.amazonaws.com/v5.1.0/rcmip-concentrations-annual-means-v5-1-0.csv
```

Use the `World` region and variables:

- `Atmospheric Concentrations|CO2` in ppm; write EcoSIM units as `ppmv`.
- `Atmospheric Concentrations|CH4` in ppb; write EcoSIM units as `ppbv`.
- `Atmospheric Concentrations|N2O` in ppb; write EcoSIM units as `ppbv`.

RCMIP scenario model labels are scenario-specific. Preserve them in metadata instead of assuming a single IAM model across all SSPs.

## Quick Start

Run from the repository root:

```bash
.venv-cmip6/bin/python .agents/skills/ssp-ghg-atmgas-generator/scripts/build_ssp_atmgas.py \
  --historical-netcdf /path/to/fatm_hist_GHGs_1750-2025.nc \
  --rcmip-csv /path/to/rcmip-concentrations-annual-means-v5-1-0.csv \
  --output-dir result/ssp_gas_concentrations \
  --scenarios ssp245 ssp585 \
  --end-year 2100
```

If the RCMIP CSV is not local, either let the script download it with `--download-rcmip` or download it first with an approved network command and pass `--rcmip-csv`.

## Workflow

1. Inspect the historical NetCDF before writing outputs:
   - Confirm variables `CO2`, `CH4`, `N2O`, and `year` exist.
   - Confirm historical gas units are ppmv/ppbv-compatible.
   - Confirm the fractional-year convention. EcoSIM atmgas files usually encode month as `calendar_year + month / 12`, so December 2022 is `2023.0`.
2. Extract RCMIP annual means for requested scenarios and gases from `Region == "World"`.
3. Keep historical monthly values through the last complete historical calendar year unless the user asks for a different splice year.
4. Expand SSP annual values to monthly future values. The default script policy assigns each month of a calendar year that year's annual RCMIP mean; do not invent a future seasonal cycle unless explicitly requested.
5. Write one NetCDF per scenario with EcoSIM variable names and units:
   - `year(time)` as fractional AD year.
   - `CO2(time)` in `ppmv`.
   - `CH4(time)` and `N2O(time)` in `ppbv`.
6. Write compact CSV summaries with key years and annual scenario values for auditability.

## Output Rules

- Put outputs under `result/` unless the user provides another location.
- Name scenario files clearly, for example `fatm_GHGs_ssp245_1750-2100.nc`.
- Preserve enough metadata to reproduce the splice: historical source path, RCMIP source, scenario, scenario model label, splice calendar year, monthly expansion policy, and creation timestamp.
- Treat `ppm` as `ppmv` and `ppb` as `ppbv` for EcoSIM atmgas forcing, and note that this is a mixing-ratio naming convention.
- For a requested end calendar year of 2100, the final fractional `year` coordinate will be `2101.0` because it represents December 2100 in the existing EcoSIM convention.

## Validation Checklist

- Print or inspect each output file's dimensions, first/last `year`, variable units, and 2100 CO2/CH4/N2O values.
- Check continuity at the splice: the first future month should use the selected scenario annual value for that calendar year.
- Ensure `N2O` is present in both historical and scenario outputs; do not deliver CO2/CH4-only products when the request mentions greenhouse gases or atmgas.
- Report source and unit assumptions in the final response.

## Bundled Script

Use `scripts/build_ssp_atmgas.py` for the full workflow. It can read a local RCMIP CSV or download one, create NetCDF outputs, and write summary CSV files.
