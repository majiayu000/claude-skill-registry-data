---
name: ameriflux-bif-timeseries-sorter
description: Sort AmeriFlux BASE-BADM BIF variables from Excel or CSV files into observation, management-event, static metadata, and plotting-ready target time-series tables. Use when Codex is asked to sort AmeriFlux BIF variables into time series; organize BADM/BIF variables by date; pivot AMF *_BIF_*.xlsx files by GROUP_ID; output total LAI, leaf mass per area, above-ground biomass, canopy height, fruit yield, or total yield time series; write MATLAB readers for BIF time-series plotting; or prepare dated AmeriFlux site observations and management records for EcoSIM workflows.
---

# AmeriFlux BIF Time-Series Sorter

## Overview

Use this skill to convert AmeriFlux BADM BIF long tables into time-series tables. BIF files commonly store one variable per row with columns such as `SITE_ID`, `GROUP_ID`, `VARIABLE_GROUP`, `VARIABLE`, and `DATAVALUE`. A single dated observation or management event is reconstructed by grouping rows with the same `SITE_ID`, `VARIABLE_GROUP`, and `GROUP_ID`.

## When To Use

Use this skill for requests such as:

- sort variables into time series
- sort AmeriFlux BIF variables into time series
- organize BADM variables by date
- convert `AMF_<SITE>_BIF_*.xlsx` into dated observation and management tables
- prepare BIF site observations or management events for EcoSIM comparison/input workflows

Do not treat BIF files as continuous half-hourly BASE flux files. BIF/BADM records are metadata, biological observations, soil observations, and management/event records, often irregular in time.

## Workflow

1. Inspect the input workbook or CSV.
   - Prefer the `AMF-BIF` sheet for AmeriFlux BIF Excel files.
   - Confirm required columns: `SITE_ID`, `GROUP_ID`, `VARIABLE_GROUP`, `VARIABLE`, `DATAVALUE`.
   - Record the site ID and the source file path.

2. Reconstruct records.
   - Group rows by `SITE_ID`, `VARIABLE_GROUP`, and `GROUP_ID`.
   - Pivot `VARIABLE` names into columns and keep raw `DATAVALUE` strings.
   - Preserve comments, units, depth/profile fields, species/organ/phenology qualifiers, and date uncertainty fields.

3. Identify date-bearing records.
   - Treat variables ending in `_DATE` as observation dates.
   - Treat variables ending in `_DATE_START` and `_DATE_END` as event intervals.
   - Preserve `_DATE_UNC` as a qualifier, not as the timestamp.
   - Normalize dates like `YYYYMMDD` to `YYYY-MM-DD` for sorting, while keeping raw values in the original variable columns.

4. Classify record groups.
   - Observation series: dated biological or soil observations, for example `GRP_AG_BIOMASS_CROP`, `GRP_LAI`, `GRP_HEIGHTC`, `GRP_LMA`, `GRP_BIOMASS_CHEM`, `GRP_SOIL_CHEM`, and `GRP_SPP_O`.
   - Management/event series: dated site operations, usually `GRP_DM_*`, such as planting, fertilization, tillage, pesticide, agriculture, or external-weather events.
   - Static metadata: records without a usable date, such as location, climate averages, soil texture, IGBP, DOI, team members, and references.

5. Write outputs under `result/<SITE_ID>/bif_timeseries/` unless the user asks for another path.
   - `all_records_wide.csv`: one row per reconstructed BIF record, sorted by series class, variable group, timestamp, and group ID.
   - `time_series_long.csv`: one row per main data variable from date-bearing records, with `timestamp`, `date_start`, `date_end`, `unit`, `raw_value`, and `qualifiers_json`.
   - `by_group/<VARIABLE_GROUP>.csv`: one wide dated table per variable group.
   - `target_timeseries/total_lai.csv`: plotting-ready rows from `GRP_LAI` variable `LAI_TOT`.
   - `target_timeseries/leaf_mass_per_area.csv`: plotting-ready rows from `GRP_LMA` variable `LMA`.
   - `target_timeseries/aboveground_biomass.csv`: plotting-ready rows from `GRP_AG_BIOMASS_CROP` variable `AG_BIOMASS_CROP`, preserving organ, phenology, unit, and comments.
   - `target_timeseries/canopy_height.csv`: plotting-ready rows from `GRP_HEIGHTC` variable `HEIGHTC`, preserving statistic qualifiers.
   - `target_timeseries/fruit_yield.csv`: plotting-ready rows from `GRP_AG_PROD_CROP` variable `AG_PROD_CROP` where `AG_PROD_CROP_ORGAN` is `Fruits`.
   - `target_timeseries/total_yield.csv`: plotting-ready rows from `GRP_AG_PROD_CROP` variable `AG_PROD_CROP` where `AG_PROD_CROP_ORGAN` is `Total`.
   - `static_metadata.csv`: wide records without usable dates.
   - `summary.json`: counts, groups, date fields, and output paths.

6. Report the result.
   - List observation time series, management/event series, and static metadata groups.
   - Mention records that lacked dates and were not sorted as time series.
   - For EcoSIM use, flag which groups can inform comparison targets versus management inputs.

## Bundled Script

Use `scripts/sort_bif_timeseries.py` for deterministic conversion:

```bash
python3 .agents/skills/ameriflux-bif-timeseries-sorter/scripts/sort_bif_timeseries.py \
  /path/to/AMF_US-Ne3_BIF_20250522.xlsx \
  --out-dir result/US-Ne3/bif_timeseries
```

The script accepts `.xlsx`, `.xlsm`, and CSV files. It uses `openpyxl` for Excel input and writes only CSV/JSON outputs.

Use `scripts/read_bif_target_timeseries.m` in MATLAB to read the plotting-ready target files:

```matlab
data = read_bif_target_timeseries("result/US-Ne3/bif_timeseries", true);
```

The returned struct contains `data.total_lai`, `data.leaf_mass_per_area`, `data.aboveground_biomass`, `data.canopy_height`, `data.fruit_yield`, and `data.total_yield` tables. Each table includes `Time` as `datetime` and `Value` as numeric when the source values can be parsed.

## EcoSIM Notes

- Use observation groups such as LAI, crop biomass, yield/crop production, height, biomass chemistry, and soil chemistry for model-data comparison after checking units and aggregation windows.
- Use `GRP_DM_*` groups as candidate management inputs, but check event semantics before converting to EcoSIM planting, harvest, fertilization, irrigation, tillage, or pesticide records.
- Do not silently convert units. Preserve raw units and report missing units where comparisons or EcoSIM inputs require conversion.
