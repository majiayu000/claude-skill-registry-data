---
name: nldas-gesdisc-point-download
description: Download NASA GES DISC NLDAS_FORA0125_H version 2.0 primary hourly forcing data for a point location. Use when Codex needs to retrieve NLDAS File A meteorological forcing from the GES DISC API or HTTPS archive for a longitude/latitude pair, including Earthdata username/password authentication, hourly URL generation, nearest-grid-point extraction, CSV output, or EcoSIM climate-forcing preprocessing.
---

# NLDAS GES DISC Point Download

## Overview

Use this skill to retrieve `NLDAS_FORA0125_H` version `2.0` primary hourly forcing ("File A") from NASA GES DISC for a single point. The user-provided location is always longitude first, latitude second. Output must contain only the requested location or the nearest native NLDAS grid point, never a spatial grid.

Prefer the bundled script for repeatable downloads and point extraction. By default, it uses GES DISC OPeNDAP constraint expressions to request only scalar values for the nearest NLDAS grid cell; it does not download full gridded NetCDF granules unless `--access-method https-granule` is explicitly selected. In this repository, use `.venv-cmip6/bin/python` when extracting values because it includes the NetCDF stack needed by the fallback granule path:

```bash
.venv-cmip6/bin/python .agents/skills/nldas-gesdisc-point-download/scripts/download_nldas_fora_point.py \
  --lon -72.1715 \
  --lat 42.5378 \
  --auto-span complete-calendar-years \
  --allow-large-download \
  --output result/nldas/US-Ha1_nldas_fora_primary.csv
```

If credentials are not provided as command-line arguments, the script checks `USR_NLDAS` and `PASSWD_NLDAS`. A `.netrc` file is used only when explicitly passed with `--netrc-file`. Never write credentials to output files, manifests, logs, or shell snippets shown back to the user.

When `USR_NLDAS` and `PASSWD_NLDAS` are defined in `~/.bashrc` but are not visible in the current shell process, the script sources `~/.bashrc` and reads only those two variables into memory.

## Inputs

- `--lon`: longitude in decimal degrees, west negative. Must be in the NLDAS domain `[-125, -67]`.
- `--lat`: latitude in decimal degrees. Must be in the NLDAS domain `[25, 53]`.
- `--start`, `--end`: UTC timestamps. Accept `YYYY-MM-DD`, `YYYY-MM-DDTHH`, or `YYYY-MM-DDTHH:MM`. The script downloads all whole UTC hours from start through end, inclusive.
- `--auto-span complete-calendar-years`: infer the first complete UTC calendar year and last complete UTC calendar year from the GES DISC archive. Use this for EcoSIM annual forcing.
- `--auto-span available-years`: start at the first actual product hour and end at the last complete UTC calendar year. For `NLDAS_FORA0125_H`, this includes partial year 1979 starting at `1979-01-01T13:00Z`.
- `--variables`: optional native NLDAS variable list. Defaults to the EcoSIM climate-native set: `Tair`, `Wind_E`, `Wind_N`, `Rainf`, `Qair`, `SWdown`, `PSurf`.
- `--variable-set`: `ecosim-climate` by default; use `all-primary-file-a` only when the user explicitly asks for non-EcoSIM File A fields.
- `--username`, `--password`: optional Earthdata credentials that override `USR_NLDAS` and `PASSWD_NLDAS`.
- `--credential-profile`: bash profile to source for credentials, default `~/.bashrc`.
- `--access-method`: `opendap-point` by default for scalar point API access; use `https-granule` only when debugging or when the OPeNDAP service is unavailable.
- `--keep-raw`: keep full hourly NetCDF granules after point extraction. By default, newly downloaded raw granules are deleted after selected-location CSV extraction.
- `--allow-large-download`: required when a request exceeds the large-download threshold. Without it, the script writes a manifest with the inferred span and aborts before issuing many hourly API requests.
- `download_nldas_fora_point.py --allow-invalid` and `download_nldas_giovanni_ecosim.py --allow-invalid`: allow outputs even when validity checks flag out-of-range values. By default, validity failures make the command exit nonzero after writing the manifest or quality report.

## Data Source Facts

Load [references/nldas_gesdisc_api.md](references/nldas_gesdisc_api.md) when you need endpoint details, official links, file naming, authentication notes, or variable definitions.

Core facts:

- Collection: `NLDAS_FORA0125_H_2.0`.
- OPeNDAP point API base: `https://hydro1.gesdisc.eosdis.nasa.gov/opendap/NLDAS/NLDAS_FORA0125_H.2.0/`.
- HTTPS archive base: `https://hydro1.gesdisc.eosdis.nasa.gov/data/NLDAS/NLDAS_FORA0125_H.2.0/`.
- File pattern: `YYYY/DDD/NLDAS_FORA0125_H.AYYYYMMDD.HH00.020.nc`, where `DDD` is day of year.
- Spatial domain: west `-125`, east `-67`, south `25`, north `53`.
- Native temporal resolution: hourly UTC.
- Dataset summary: `https://disc.gsfc.nasa.gov/datasets/NLDAS_FORA0125_H_2.0/summary?keywords=NLDAS`.
- CMR reports the first product time as `1979-01-01T13:00:00Z`; the GES DISC archive currently has year folders through `2026`, so on `2026-06-26` the complete calendar-year span is `1980-01-01T00:00Z` through `2025-12-31T23:00Z`.

EcoSIM climate-native variables downloaded/extracted by default:

- `Tair`: maps to `TMPH` after K to degC conversion.
- `Wind_E`, `Wind_N`: map to `WINDH` as scalar wind speed.
- `Rainf`: maps to `RAINH`; native `kg m-2` hourly accumulation is numerically equivalent to mm water.
- `Qair`, `PSurf`: used to derive atmospheric vapor pressure for `DWPTH`.
- `SWdown`: maps to `SRADH`.
- `PSurf`: maps to `PATM` after Pa to kPa conversion.

EcoSIM annual auxiliary variables written by the Giovanni EcoSIM writer:

- `Z0G`, `IFLGW`, and `ZNOONG` are derived directly from site/grid assumptions and longitude.
- For US/NLDAS-domain grids, precipitation chemistry variables are added from the same NADP source used by US AmeriFlux workflows: `PHRG`, `CN4RIG`, `CNORIG`, `CSORG`, `CCARG`, and other supported template variables when source rasters exist.
- The Giovanni EcoSIM writer defaults to `--add-us-chemistry auto`, which adds NADP chemistry for coordinates in `[-125, -67]` longitude and `[25, 53]` latitude. Use `--add-us-chemistry never` to skip or `--add-us-chemistry always` to force.
- Use `--chemistry-input` to point to an alternate NADP raster directory and `--chemistry-output` to choose the intermediate extracted-chemistry JSON path.

Other primary File A variables, only when explicitly requested:

- `LWdown`: downward longwave radiation, `W m-2`.
- `PotEvap`: potential evaporation, `kg m-2`.
- `CAPE`: convective available potential energy, `J kg-1`.
- `CRainf_frac`: fraction of total precipitation that is convective.

## Workflow

1. Confirm the user supplied longitude then latitude. If a value looks swapped, stop and ask for clarification because the grid-cell choice affects water and energy forcing.
2. Confirm the requested period and variables. Interpret all times as UTC unless the user explicitly says otherwise.
3. When the user asks for "first to last available year" for EcoSIM, use `--auto-span complete-calendar-years`; this drops the partial first year (`1979`) and incomplete trailing year (`2026` as of June 26, 2026).
4. Ensure Earthdata credentials are available when GES DISC requires authentication. The standard repo workflow is to set `USR_NLDAS` and `PASSWD_NLDAS` in `~/.bashrc`; the script sources that file automatically when needed. The user may still pass `--username` and `--password` to override.
5. Run the script from the repository root.
6. Inspect the generated CSV and manifest:
   - Check requested lon/lat and selected grid lon/lat.
   - Check that every requested UTC hour is represented.
   - Check that the variable set is `ecosim-climate` unless the user explicitly requested another set.
   - Check units before converting to EcoSIM forcing names.
   - Check the quality report's `validity_checks.all_passed` field before using the NetCDF in an EcoSIM run.
   - For EcoSIM NetCDF outputs, check `annual_forcing.auxiliary_climate_variables` to confirm whether NADP chemistry was added, skipped, or default-filled.

## Output Rules

- Put outputs under `result/` unless the user provides another path.
- The default OPeNDAP access path writes only scalar point values for the selected nearest native NLDAS grid cell. The HTTPS archive fallback serves full hourly NetCDF granules; when that fallback is used, the script extracts the point and removes newly downloaded raw granules unless `--keep-raw` is supplied.
- Long automatic spans are request-heavy. For `1980-2025`, expect `403,248` hourly point API requests. The script refuses such runs unless `--allow-large-download` is explicitly supplied.
- Write a JSON manifest next to the CSV. Include source URLs, selected grid cell, variables, units, and download timestamps, but never include username or password.
- Preserve native units. Do not convert precipitation, pressure, or temperature for EcoSIM until a downstream conversion step is explicitly requested.

## EcoSIM Unit Cautions

- `Tair` is Kelvin; EcoSIM climate tools often expect degC for `TMPH`.
- `PSurf` is Pa; EcoSIM climate tools often use kPa for `PATM`.
- `Rainf` is hourly accumulated water mass per area (`kg m-2`), numerically equivalent to mm water depth for liquid water density. Do not treat it as a `kg m-2 s-1` rate unless the file metadata for a future product says so.
- `Wind_E` and `Wind_N` are vector components. Compute wind speed as `sqrt(Wind_E**2 + Wind_N**2)` only when the downstream workflow needs scalar speed.

## Validity Checks

The bundled point downloader and Giovanni EcoSIM downloader write explicit `validity_checks` to the manifest or quality report and fail by default when a variable is outside its accepted range.

Native NLDAS checks:

- `Tair`: `183.15` to `333.15 K` (`-90` to `60 degC`).
- `Wind_E`, `Wind_N`: `-75` to `75 m s^-1`.
- `Rainf`: `0` to `500 kg m^-2 h^-1`.
- `Qair`: `0` to `0.05 kg kg^-1`.
- `SWdown`: `0` to `1400 W m^-2`.
- `PSurf`: `50000` to `110000 Pa`.
- `LWdown`: `0` to `800 W m^-2`.
- `PotEvap`: `0` to `500 kg m^-2 h^-1`.
- `CAPE`: `0` to `10000 J kg^-1`.
- `CRainf_frac`: `0` to `1`.

EcoSIM checks:

- `TMPH`: `-90` to `60 degC`.
- `WINDH`: `0` to `75 m s^-1`.
- `RAINH`: `0` to `500 mm h^-1`.
- `DWPTH`: `0` to `15 kPa`.
- `SRADH`: `0` to `1400 W m^-2`.
- `PATM`: `50` to `110 kPa`.

Annual auxiliary checks:

- `Z0G`: positive measurement height, `0.01` to `100 m`.
- `IFLGW`: allowed flags `0` or `1`.
- `ZNOONG`: `0` to `24 hour`.
- `PHRG`: `0` to `14 pH`.
- Precipitation chemistry concentrations: non-negative.

NADP chemistry values must be finite and non-negative, with `PHRG` constrained to pH `0-14`. Annual gaps are filled by linear interpolation with nearest-edge filling. If no valid NADP pH is available, use neutral `PHRG=7` and record the fallback in the quality report. Do not silently apply NADP chemistry outside the US/NLDAS auxiliary domain.

## Validation

For any delivered extraction, report:

- Product short name and version.
- Requested longitude/latitude and selected grid-cell longitude/latitude.
- UTC start/end and number of hourly files.
- Variables extracted and their native units.
- Whether `validity_checks.all_passed` is true and which variables failed if false.
- Whether authentication was supplied via CLI arguments, `USR_NLDAS`/`PASSWD_NLDAS`, or not needed. Do not reveal credential values.
