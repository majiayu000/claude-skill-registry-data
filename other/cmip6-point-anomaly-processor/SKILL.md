---
name: cmip6-point-anomaly-processor
description: Extract point-scale CMIP6 historical and SSP future climate data from the Pangeo Google Cloud catalog and convert them into bias-corrected additive or multiplicative anomalies for LSM or EcoSIM climate forcing. Use when a task needs site latitude/longitude, scenario-specific CMIP6 variables, vapor pressure derived from huss and ps, calendar-aware day-of-year climatologies, or projected change summaries for the 2050s and 2090s.
---

# CMIP6 Point-Scale Anomaly Processor

## Use When

- You need point-specific CMIP6 climate anomalies for a land-surface model or EcoSIM forcing workflow.
- Inputs include latitude, longitude, temporal resolution, SSP scenario, and variables such as `tas`, `pr`, `ps`, `sfcWind`, `rsds`, `rlds`, or `huss`.
- The output should be a timestamped CSV or CF-style NetCDF anomaly file plus summary deltas relative to a historical baseline.

## Required Inputs

- Latitude and longitude in standard GPS coordinates.
- Temporal resolution: usually `daily` or `3-hourly`.
- Scenario: map user labels to CMIP6 experiment IDs:
  - `SSP1-2.6` -> `ssp126`
  - `SSP2-4.5` -> `ssp245`
  - `SSP3-7.0` -> `ssp370`
  - `SSP5-8.5` -> `ssp585`
- Target variables: default to `tas`, `pr`, `ps`, `sfcWind`, `rsds`, `rlds`, and `huss` unless the user requests a subset.
- Optional but recommended: site elevation in meters, desired output units, model/source selection, ensemble member, baseline period, and output format.

## Data Source

Use the Pangeo CMIP6 Google Cloud intake-esm catalog:

```python
cat_url = "https://storage.googleapis.com/cmip6/pangeo-cmip6.json"
```

Query the catalog; do not assume that every variable, table, model, member, or SSP is available. Prefer `table_id="day"` for daily data and `table_id="3hr"` for 3-hourly data. If a requested variable is unavailable at the requested temporal resolution, report the missing facet combination instead of silently substituting another table.

## Ensemble Integrity Rules

1. Search historical and future datasets together for the requested `experiment_id`, `table_id`, and `variable_id` values.
2. Build candidate ensembles from the intersection of `source_id`, `member_id`, and preferably `grid_label`.
3. Select only candidates that include every requested variable for both historical and future experiments.
4. When multiple versions exist for the same facet tuple, prefer the latest catalog `version` and record it in metadata.
5. Do not mix historical and SSP data across different models or ensemble members unless the user explicitly accepts the scientific compromise.

## Core Workflow

1. Normalize coordinates:
   - Keep the user longitude for reporting.
   - Convert to CMIP6 0-360 convention with `lon_cmip = lon % 360`.
2. Load datasets lazily with xarray/dask from the selected Zarr stores.
3. Extract the nearest grid cell for each variable:
   - For 1D `lat`/`lon`, use `.sel(lat=lat, lon=lon_cmip, method="nearest")` or matching coordinate names.
   - For 2D `latitude`/`longitude`, compute the wrapped longitudinal distance and select the minimum distance grid index.
4. Slice the baseline and future periods:
   - Default historical baseline: `1995-01-01` through `2014-12-31`.
   - Default future period: `2015-01-01` through `2100-12-31`.
5. Standardize calendars before computing day-of-year statistics:
   - Use cftime-aware xarray operations.
   - Drop leap day or convert to `noleap` unless the user requests a 366-day product.
   - For `360_day` calendars, keep a 360-day climatology and record the calendar in metadata.
6. Compute the historical day-of-year climatology over the baseline period.
7. Align each future timestamp to its historical day-of-year climatology.
8. Calculate anomalies:
   - Additive variables: `tas`, `ps`, `sfcWind`, `rsds`, `rlds`, and derived vapor pressure `e`.
   - Multiplicative variables: `pr` and `huss`.
   - Additive anomaly: `future_abs - historical_doy_mean`.
   - Multiplicative anomaly: `future_abs / historical_doy_mean`.
9. Protect physical units and mass/energy consistency:
   - Use small positive floors before ratio calculations for `pr` and `huss`.
   - Preserve dry-day meaning for precipitation; avoid creating spurious precipitation from divide-by-zero handling.
   - Record any clipping, flooring, or missing-data policy in output metadata.

## Bias-Correction Terminology

The anomaly output is a delta or change-factor product relative to the model's own historical climatology. Do not describe it as fully bias-corrected absolute climate unless those deltas or ratios are applied to an observed, AmeriFlux, ERA5, or other reference baseline. When applying the anomaly to a baseline forcing series:

- Additive correction: `corrected_future = observed_baseline_climatology + delta`.
- Multiplicative correction: `corrected_future = observed_baseline_climatology * ratio`.
- Recheck physical bounds after correction, especially for precipitation, humidity, radiation, and vapor pressure.

## Unit Policy

Always inspect source units and convert to the requested standard before anomaly calculation unless the user asks for native-unit anomalies.

Recommended defaults for EcoSIM/LSM forcing:

| Variable | Common CMIP6 unit | Recommended standard |
| --- | --- | --- |
| `tas` | `K` | `degC` |
| `pr` | `kg m-2 s-1` | `mm d-1` for daily or `mm timestep-1` for subdaily forcing |
| `ps` | `Pa` | `kPa` |
| `sfcWind` | `m s-1` | `m s-1` |
| `rsds` | `W m-2` | `W m-2` |
| `rlds` | `W m-2` | `W m-2` |
| `huss` | `1` or `kg kg-1` | `kg kg-1` |
| `e` | derived | `kPa` |

For precipitation, remember that `kg m-2` water equals `mm` water. Convert rates by multiplying by the time interval in seconds.

## Vapor Pressure

Derive actual vapor pressure from specific humidity and surface pressure:

```python
epsilon = 0.622
e = huss * ps / (epsilon + (1.0 - epsilon) * huss)
```

Use pressure-consistent units; if `ps` is Pa, `e` is Pa. Convert to kPa for EcoSIM-style outputs. If using a Magnus-Tetens pathway, document the additional assumptions because Magnus-Tetens normally requires temperature and relative humidity or dew point, not just `huss` and `ps`.

## Elevation and Lapse-Rate QC

If site elevation is available, compare it with the GCM grid-cell surface elevation when `orog` or equivalent metadata can be retrieved for the same `source_id` and grid. Warn when the absolute difference is large enough to bias near-surface temperature, using 250 m as a default threshold. Estimate the potential temperature bias with a standard environmental lapse rate:

```text
temperature_bias_degC ~= -0.0065 * (site_elevation_m - gcm_elevation_m)
```

Do not automatically lapse-rate-correct unless the user requests it; emit a warning and record the estimated bias.

## Output Requirements

Write outputs under `result/` unless the user provides another path.

For CSV:
- Include `time`, `source_id`, `member_id`, `scenario`, original `lat`, original `lon`, selected grid coordinates, and one anomaly column per variable.
- Name ratio anomalies clearly, for example `pr_ratio` and `huss_ratio`.
- Name additive anomalies clearly, for example `tas_delta_degC` and `rsds_delta_W_m-2`.

For NetCDF:
- Follow CF conventions where possible.
- Include global attributes for catalog URL, scenario, baseline period, future period, selected model/member/grid, calendar policy, unit conversions, and nearest-grid-cell metadata.
- Add each variable's `units`, `long_name`, and anomaly method (`additive_delta` or `multiplicative_ratio`).

## Summary Table

Always provide a compact summary of projected changes relative to the 1995-2014 baseline unless the user opts out.

Default windows:
- 2050s: `2041-01-01` through `2070-12-31`
- 2090s: `2071-01-01` through `2100-12-31`

For additive variables, summarize mean delta. For multiplicative variables, summarize mean ratio and percent change:

```text
percent_change = (ratio_mean - 1.0) * 100
```

Report units, model/member, scenario, and whether the values are single-model or multi-model ensemble statistics.

## Validation Checklist

- Coordinates were converted from -180/180 to 0/360 for CMIP6 lookup.
- Historical and future datasets share `source_id`, `member_id`, and preferably `grid_label`.
- Requested temporal resolution and variable availability were verified in the catalog.
- Source units were converted before anomalies were computed.
- Calendar handling is explicit and reproducible.
- Multiplicative anomalies avoid negative or undefined physical values.
- Vapor pressure units are pressure-consistent.
- Elevation mismatch warnings are included when site elevation and GCM `orog` are available.
- Output files include enough metadata to reproduce the extraction and anomaly calculation.
