---
name: era5-cds-point-download
description: Download Copernicus CDS ERA5 single-level point time-series climate forcing for non-US or non-NLDAS EcoSIM sites from longitude/latitude coordinates. Use when a paper-derived site is outside the NLDAS domain, lacks AmeriFlux/FLUXNET curated forcing, or needs global ERA5 variables such as 2m temperature, dewpoint temperature, surface pressure, solar radiation, precipitation, and 10m wind components for EcoSIM preprocessing.
---

# ERA5 CDS Point Download

## Overview

Use this skill to retrieve ERA5 single-level point time-series data from the Copernicus Climate Data Store (CDS) for literature sites outside the US/NLDAS workflow. The coordinate convention is longitude first, latitude second, with longitude in `[-180, 180]` and latitude in `[-90, 90]`.

For US sites inside the NLDAS domain (`-125 <= lon <= -67`, `25 <= lat <= 53`), prefer `nldas-gesdisc-point-download` unless the user explicitly asks for ERA5 or the paper requires an ERA5-consistent forcing source.

## Required Setup

Use the CDS API instructions at `https://cds.climate.copernicus.eu/how-to-api` when credentials or local configuration are missing. The user must register or log in to locate their API key and configure `cdsapi` appropriately, usually through `~/.cdsapirc`.

Prefer `$HOME/.cdsapirc` when it exists with `url` and `key` entries. This repository also supports fallback credentials from environment variables after sourcing `~/.bashrc`: `ERA5_USR` and `ERA5_PSSWD`. Accept `ERA5_PASSWD` as a spelling fallback. If shell sourcing does not expose the values, the bundled script may directly parse simple `export KEY=value` assignments in `~/.bashrc`; this handles unquoted API keys containing shell metacharacters such as `&`. Current CDS API setup expects the personal-access token without a deprecated `<UID>:` prefix, so pass `ERA5_PSSWD` or `ERA5_PASSWD` as the `cdsapi.Client` key only when using `--credential-source env`, and keep `ERA5_USR` only for compatibility/presence checks. Never print, persist, or echo API keys in result files or responses.

Install `cdsapi` only when needed. If network or package installation is required, request approval according to the active sandbox policy.

## Default Variables

Download these variables for EcoSIM climate forcing preparation:

- `2m_dewpoint_temperature`
- `surface_pressure`
- `surface_solar_radiation_downwards`
- `2m_temperature`
- `total_precipitation`
- `10m_u_component_of_wind`
- `10m_v_component_of_wind`

Default dataset: `reanalysis-era5-single-levels`. This is the current CDS catalogue entry for ERA5 hourly single-level data. The older point-timeseries short name `reanalysis-era5-single-levels-timeseries` may be tested with `--dataset reanalysis-era5-single-levels-timeseries --request-style timeseries`, but if CDS returns endpoint or authorization errors, use the default gridded dataset with a small lon/lat bounding box and extract the nearest grid cell downstream.

Default date range, when the user does not specify a period: `1940-01-01/2025-10-01`.

## Bundled Script

Prefer the bundled script for repeatable requests and manifest writing:

```bash
python .agents/skills/era5-cds-point-download/scripts/download_era5_point_cds.py \
  --site-id Forbonnet-peatland \
  --lon 6.1722 \
  --lat 46.8264 \
  --date 1940-01-01/2025-10-01 \
  --output result/era5/Forbonnet-peatland_era5_single_levels_timeseries
```

For a current CDS single-levels smoke test, request one day from a small bounding box around the point:

```bash
python .agents/skills/era5-cds-point-download/scripts/download_era5_point_cds.py \
  --site-id Forbonnet-peatland \
  --lon 6.1722 \
  --lat 46.8264 \
  --date 2020-01-01/2020-01-01 \
  --output result/era5/Forbonnet-peatland_era5_20200101_test.grib
```

If the CDS credentials are stored in `~/.bashrc`, source it in the shell that launches the script:

```bash
source ~/.bashrc >/dev/null 2>&1
python .agents/skills/era5-cds-point-download/scripts/download_era5_point_cds.py \
  --site-id Forbonnet-peatland \
  --lon 6.1722 \
  --lat 46.8264 \
  --date 2020-01-01/2020-01-02 \
  --output result/era5/Forbonnet-peatland_era5_test.grib
```

To force a source, use `--credential-source cdsapirc` or `--credential-source env`. By default, `--credential-source auto` prefers `$HOME/.cdsapirc` and falls back to the ERA5 environment variables or simple `~/.bashrc` assignments.

Use `--dry-run` first when checking a paper extraction or CDS setup:

```bash
python .agents/skills/era5-cds-point-download/scripts/download_era5_point_cds.py \
  --site-id Forbonnet-peatland \
  --lon 6.1722 \
  --lat 46.8264 \
  --dry-run
```

The script writes a JSON manifest next to the downloaded file. The manifest records the dataset, variables, location, requested date range, output path, and timestamp, but never records credentials.

## Convert to EcoSIM

After downloading the CDS point time-series ZIP, convert it to EcoSIM hourly climate forcing with:

```bash
.venv-cmip6/bin/python .agents/skills/era5-cds-point-download/scripts/convert_cds_era5_to_ecosim.py \
  --input result/era5/Forbonnet-peatland_era5_timeseries_19400101_20251001.zip \
  --output result/era5/Forbonnet-peatland_ecosim_climate_1940_2024.nc \
  --site-id Forbonnet-peatland \
  --lon 6.1722 \
  --lat 46.8264 \
  --quality-report result/era5/Forbonnet-peatland_ecosim_climate_1940_2024_quality.json \
  --forcing-yaml result/Forbonnet-peatland/Forbonnet-peatland_forcing.yaml
```

The converter accepts either the CDS ZIP or the extracted NetCDF. By default, it writes only complete UTC calendar years and drops partial first or last years, because EcoSIM climate arrays are annual `year/day/hour` blocks and partial years leave fill values inside a simulation year. Use `--include-incomplete-years` only when a partial-year diagnostic file is explicitly needed, and document the missing hours in the quality report.

The converter maps:

- `t2m` K to `TMPH` degC.
- `sqrt(u10^2 + v10^2)` to `WINDH` m s^-1.
- `tp` m to `RAINH` mm h^-1.
- `d2m` K to vapor pressure `DWPTH` kPa.
- `ssrd` J m^-2 hourly accumulation to `SRADH` W m^-2 by dividing by `3600`.
- `sp` Pa to `PATM` kPa.

For US grids in the same auxiliary-data domain used by the US/AmeriFlux workflow (`-125 <= lon <= -67`, `25 <= lat <= 53`), the converter defaults to `--add-us-chemistry auto` and adds annual EcoSIM precipitation chemistry variables from NADP rasters under `data/nadp_data_grids`:

- `PHRG`: pH in precipitation.
- `CN4RIG`: NH4-N concentration in precipitation.
- `CNORIG`: NO3-N concentration in precipitation.
- `CSORG`: SO4-S concentration in precipitation.
- `CCARG`: Ca concentration in precipitation.
- Other template chemistry variables supported by `Tools/create_ecosim_climate_forcing.py`, including `CMGRG`, `CNARG`, `CKARG`, and `CCLRG` when NADP source rasters exist.

NADP values are validated the same way as US/AmeriFlux climate forcing: reject NoData, non-finite, negative concentrations, and pH outside `0-14`; fill annual gaps by linear interpolation with nearest-edge filling; if no valid `PHRG` exists, use neutral `PHRG=7` and record the fallback. Use `--add-us-chemistry never` to skip this for a US grid, or `--add-us-chemistry always` to force it. Use `--chemistry-input` to point to another NADP raster directory and `--chemistry-output` to set the intermediate JSON path.

For non-US grids, do not silently add NADP-derived chemistry. Leave the annual chemistry variables absent unless the user supplies an appropriate regional precipitation-chemistry source or asks for a site-specific mapping. When a non-US site needs annual EcoSIM precipitation chemistry, use `global-aux-climate-chemistry` to stage CAMS first, then EBAS/EANET station overrides or MERRA-2 fallback context as appropriate.

Use `.venv-cmip6/bin/python` for conversion because it includes `xarray` and `netCDF4`.

## Minimal CDS API Pattern

When writing a one-off Python snippet, use this request shape:

```python
import cdsapi

def download_era5_climate(lon=123.75, lat=44.75):
    dataset = "reanalysis-era5-single-levels-timeseries"
    request = {
        "variable": [
            "2m_dewpoint_temperature",
            "surface_pressure",
            "surface_solar_radiation_downwards",
            "2m_temperature",
            "total_precipitation",
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
        ],
        "location": {"longitude": lon, "latitude": lat},
        "date": ["1940-01-01/2025-10-01"],
    }

    client = cdsapi.Client()
    client.retrieve(dataset, request).download()
```

## EcoSIM Unit Cautions

Before converting ERA5 output to EcoSIM NetCDF, inspect the returned file metadata because CDS response format and accumulation conventions can differ by service version.

Core conversions commonly needed:

- `2m_temperature`: K to degC for `TMPH`.
- `10m_u_component_of_wind` and `10m_v_component_of_wind`: scalar wind speed `sqrt(u^2 + v^2)` for `WINDH`.
- `2m_dewpoint_temperature`: derive vapor pressure in kPa for `DWPTH`.
- `surface_pressure`: Pa to kPa for `PATM`.
- `surface_solar_radiation_downwards`: if accumulated energy in `J m^-2`, divide by the accumulation interval in seconds for `SRADH` in `W m^-2`.
- `total_precipitation`: convert accumulated water depth to hourly `RAINH`; check whether source units are meters of water equivalent or another accumulation convention.

Run physical range checks before writing EcoSIM forcing:

- `TMPH`: `-90` to `60 degC`.
- `WINDH`: `0` to `75 m s^-1`.
- `RAINH`: non-negative.
- `DWPTH`: `0` to `15 kPa`.
- `SRADH`: `0` to `1400 W m^-2`.
- `PATM`: `50` to `110 kPa`.

## Reporting

For any delivered ERA5 extraction, report:

- Dataset name and requested date range.
- Requested longitude/latitude.
- Variables requested.
- Output path and manifest path.
- Whether `cdsapi` credentials were configured through `$HOME/.cdsapirc`, `ERA5_USR`/`ERA5_PSSWD`, or `ERA5_USR`/`ERA5_PASSWD`, without revealing credential values.
- Any unresolved unit or format assumptions that must be checked before EcoSIM conversion.
