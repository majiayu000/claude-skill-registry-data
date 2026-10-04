---
name: ameriflux-surgo-grid-extract
description: Extract dominant-component soil profile variables for EcoSIM grid or template inputs from gSSURGO, with FAO HWSD v2.0 fallback when gSSURGO data are unavailable or incomplete. Use when deriving soil depth, bulk density, field capacity, wilting point, hydraulic conductivity, texture, rock fraction, pH, CEC, or soil organic carbon; or when converting EcoSIM grid NetCDF files to editable Excel workbooks and back.
---

# AmeriFlux gSSURGO/FAO Grid Extractor

## Use When

- You need soil profile values for an AmeriFlux or EcoSIM site from a local gSSURGO geodatabase.
- You need FAO HWSD v2.0 fallback values when gSSURGO is outside coverage, unavailable, or has missing layer values.
- You need EcoSIM template variables such as `CDPTH`, `BKDSI`, `FC`, `WP`, `SCNV`, `SCNH`, `CSAND`, `CSILT`, `ROCK`, `PH`, `CEC`, or `CORGC`.
- You need depth-weighted interpolation from source horizons or HWSD2 layers to EcoSIM soil layers.
- You need to inspect or edit an existing EcoSIM grid NetCDF as an Excel
  workbook, then rebuild the NetCDF after edits.

## Constraints

- NEVER use it extract climate data.
- Do not require atmospheric gas scalar variables in EcoSIM grid files. Treat
  `OXYEG` (or typo `OXYGE`), `Z2GEG`, `CO2EIG`, `CH4EG`, `Z2OEG`, and
  `ZNH3EG` as optional legacy/template variables, not derivation gaps.

## Workflow

1. Locate `gSSURGO_CONUS.gdb` under `data/` first, then elsewhere in the repo if needed.
2. Identify the map unit (`MUKEY`) by spatial query on `MUPOLYGON`.
3. Select the dominant component by `comppct_r`.
4. Retrieve horizons and rock fragments from `chorizon` and `chfrags`.
5. Convert units and interpolate vertically to the target template layers.
6. If gSSURGO fails, generate the profile from FAO HWSD2 under `data/FAO_HWSD2`.
7. If gSSURGO succeeds but some layer values are invalid/fill values, replace only those missing values from FAO HWSD2.
8. Write the derived soil profile JSON under `result/<SITE_ID>/`.

## Overview

This document summarizes which variables in the provided template can be
extracted from the CONUS gSSURGO database (directory `gSSURGO_CONUS.gdb`) and
from FAO HWSD v2.0, along with methods for extraction and vertical
interpolation.

## Extractable Variables from gSSURGO

The following template variables can be derived from standard gSSURGO tables:

  ---------------------------------------------------------------------------
  Template Variable               gSSURGO Source               Notes
  ------------------------------- ---------------------------- --------------
  CDPTH                           chorizon.hzdepb_r / 100      Depth to
                                                               bottom of
                                                               horizon (m)

  BKDSI                           chorizon.dbovendry_r         Bulk density
                                                               (g/cm3)

  FC                              (wthirdbar_r / 100) *        Field capacity
                                  dbthirdbar_r                 (volumetric)

  WP                              (wfifteenbar_r / 100) *      Wilting point
                                  dbfifteenbar_r

  SCNV, SCNH                      ksat_r * 3.6                 Convert um/s
                                                               to mm/h

  CSAND                           sandtotal_r * 10             kg/Mg

  CSILT                           silttotal_r * 10             kg/Mg

  ROCK                            sum(chfrags.fragvol_r) / 100 Volume
                                                               fraction

  PH                              ph1to1h2o_r                  Soil pH

  CEC                             cec7_r                       Cation
                                                               exchange
                                                               capacity

  CORGC                           om_r * 0.58 * 10             Soil organic
                                                               carbon
  ---------------------------------------------------------------------------

## Fallback Variables from FAO HWSD v2.0

The fallback reads `HWSD2_RASTER/HWSD2.bil` to identify `HWSD2_SMU_ID`, then
uses the `HWSD2_LAYERS` attribute table from `HWSD2.mdb` or an exported
`HWSD2_LAYERS.csv`/SQLite table. Use the dominant soil sequence (`SEQUENCE=1`)
unless a different sequence is explicitly requested.

  ---------------------------------------------------------------------------
  Template Variable               FAO HWSD2 Source             Notes
  ------------------------------- ---------------------------- --------------
  CDPTH                           template CDPTH               Target EcoSIM
                                                               depths remain
                                                               template-driven

  BKDSI                           BULK, fallback REF_BULK      g/cm3 equals
                                                               Mg m-3

  FC, WP                          SAND/SILT/CLAY + AWC         Texture-class
                                                               defaults, adjusted
                                                               by plausible AWC
                                                               when available

  SCNV, SCNH                      SAND/SILT/CLAY               Texture-class
                                                               Ksat estimate

  CSAND                           SAND * 10                    kg/Mg

  CSILT                           SILT * 10                    kg/Mg

  ROCK                            COARSE / 100                 Volume fraction

  PH                              PH_WATER                     Soil pH

  CEC                             CEC_SOIL                     cmolc/kg

  CORGC                           ORG_CARBON                   g/kg equals
                                                               kg C/Mg soil
  ---------------------------------------------------------------------------

FAO HWSD2 negative miscellaneous/no-data codes (-1 through -9) must be treated
as invalid. The fallback should be recorded in the output JSON under
`sources_by_variable` and `fallbacks`.

## Non-Extractable Variables

The following variables are not directly available from gSSURGO and require
external datasets or modeling assumptions:

- Climate variables (e.g., ATCAG)
- Topography (e.g., ASPX, slope)
- Hydrologic boundary conditions
- Nutrient pools (NH4, NO3, PO4)
- Organic nitrogen/phosphorus pools
- Exchange coefficients (GKC*) are not measured by gSSURGO. If paired
  exchange-solution chemistry is unavailable, invoke the
  `gapon-coefficient-estimator` ecosystem-template fallback, match the closest
  ecosystem before climate and management refinements, and remap the selected
  values to the grid's layer-bottom depths.
- Water table dynamics

For template-based `GKC*` values, keep the selector's provenance JSON with the
EcoSIM grid and include this reminder in the report or input metadata:
"Gapon coefficients are initialized from the closest ecosystem template, not
derived from site-specific paired exchange and solution chemistry. They are
starting values and are subject to calibration or tuning when needed."

The atmospheric gas scalar variables `OXYEG`/`OXYGE`, `Z2GEG`, `CO2EIG`,
`CH4EG`, `Z2OEG`, and `ZNH3EG` are not part of this soil-grid derivation
contract. If they are absent from a generated grid NetCDF, do not flag the file
as incomplete for this skill.

## Vertical Interpolation

- Use overlap-weighted averaging for most variables.
- For soil organic matter (`CORGC`), apply logarithmic interpolation.
- Optionally extend deepest horizon or FAO layer downward with `--extend-last`.

## Script

A Python script (`extract_gssurgo_profile.py`) automates spatial lookup, horizon
extraction, variable conversion, vertical interpolation, and FAO HWSD2 fallback.

The companion bridge script
(`scripts/grid_netcdf_excel_bridge.py`) converts an EcoSIM grid NetCDF to an
editable `.xlsx` workbook and back. Use it for file-wide parameter inspection
or manual edits to grid parameters.

## Example Usage

```bash
python .agents/skills/ameriflux-surgo-grid-extract/extract_gssurgo_profile.py \
  --gdb /path/to/gSSURGO_CONUS.gdb \
  --lon -121.85 \
  --lat 39.0 \
  --template template.nc \
  --out result/<SITE_ID>/profile_<SITE_ID>.json \
  --extend-last
```

The FAO fallback is enabled by default and looks under `data/FAO_HWSD2`. Use
`--fao-hwsd2-dir /path/to/FAO_HWSD2` to override the location, or
`--no-fao-fallback` for a strict gSSURGO-only run.

## Grid NetCDF Excel Bridge

Use the bundled bridge for grid NetCDF, Excel, and NetCDF round trips:

```bash
.venv-cmip6/bin/python .agents/skills/ameriflux-surgo-grid-extract/scripts/grid_netcdf_excel_bridge.py \
  nc-to-xlsx input_grid.nc editable_grid.xlsx

.venv-cmip6/bin/python .agents/skills/ameriflux-surgo-grid-extract/scripts/grid_netcdf_excel_bridge.py \
  xlsx-to-nc editable_grid.xlsx edited_grid.nc --format NETCDF3_CLASSIC
```

Workbook sheets:

- `dimensions`: NetCDF dimension names, lengths, and unlimited flags.
- `global_attrs`: global NetCDF attributes.
- `variables`: variable names, dtypes, dimensions, and fill values.
- `variable_attrs`: per-variable metadata such as `long_name`, `units`, and
  `flags`.
- `values`: flattened variable values with zero-based index tuples.

After editing, run a scratch round trip and compare dimensions, variables,
attributes, and data values before using the rebuilt grid file in EcoSIM. Pay
special attention to units and mass-balance-sensitive pools; the bridge edits
values mechanically and does not make non-derivable parameters scientifically
valid.

## Notes

- Bulk density and water retention conversions assume standard pedotransfer interpretations.
- Ensure gSSURGO geodatabase includes required tables: `MUPOLYGON`, `component`, `chorizon`, `chfrags`.
- FAO HWSD2 provides seven layers (`D1`-`D7`, 0-200 cm). When `--extend-last` is used, the deepest FAO layer is extended downward to fill deeper EcoSIM template layers; this should be treated as a gap-fill assumption, not direct observation.
- Reading `HWSD2.mdb` requires GDAL/pyogrio with MDB support. If that driver is unavailable, export the Access table as `HWSD2_LAYERS.csv` in the same `FAO_HWSD2` directory.
