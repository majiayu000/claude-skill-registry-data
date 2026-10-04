---
name: global-aux-climate-chemistry
description: Download, screen, and map non-North-America auxiliary EcoSIM climate variables from global or regional atmospheric-chemistry data sources. Use when a non-US/non-NLDAS site needs annual EcoSIM precipitation chemistry variables such as PHRG, CN4RIG, CNORIG, CSORG, CCARG, CMGRG, CNARG, CKARG, or CCLRG; when deciding whether to use CAMS, EBAS, EANET, or MERRA-2; or when deriving site-specific auxiliary variables after ERA5 climate forcing has been prepared.
---

# Global Auxiliary Climate Chemistry

## Scope

Use this skill for grids outside the US/NADP/NLDAS workflow when EcoSIM climate forcing needs annual auxiliary variables beyond ERA5/NLDAS meteorology.

This skill covers:

- Annual precipitation chemistry variables: `PHRG`, `CN4RIG`, `CNORIG`, `CSORG`, `CCARG`, `CMGRG`, `CNARG`, `CKARG`, `CCLRG`, and supported template defaults.
- Annual non-chemistry variables: `Z0G`, `IFLGW`, and `ZNOONG`.
- Source selection among CAMS, EBAS, EANET, and MERRA-2.

Do not use NADP or tDEP outside their valid US/North-America domain unless the user explicitly supplies already-processed compatible rasters and asks to force them.

## Source Priority

1. **CAMS global atmospheric composition forecasts**: first automated gridded choice for non-North-America wet-deposition chemistry. Use it for a small test subset before downloading target years.
2. **Regional station networks**: use as preferred pH/base-cation observations or as validation/override near the site.
   - Use EANET in East and Southeast Asia.
   - Use EBAS where European or other public precipitation-chemistry stations are available.
3. **MERRA-2**: fallback aerosol/deposition context only. Do not treat it as a complete precipitation-chemistry replacement without an explicit unit and species-mapping review.
4. **Defaults**: when no defensible source exists, use EcoSIM defaults with provenance. Use neutral `PHRG=7` only when pH cannot be derived.

## Workflow

1. Confirm site coordinates, simulation years, and existing climate forcing NetCDF.
2. Compute simple variables without downloading chemistry data:
   - `ZNOONG`: compute from longitude.
   - `Z0G`: use the forcing wind reference height. ERA5/CAMS 10 m winds imply `Z0G=10 m`; if a forcing source uses another measurement height, use that value and record it.
   - `IFLGW`: use site/tower/vegetation metadata if available; otherwise use `0` with a note.
3. For chemistry, run a **small CAMS smoke test** first:
   - Request one month or one year around the site.
   - Include precipitation and candidate wet-deposition variables.
   - Inspect returned metadata for units, accumulation period, species basis, and missing values.
   - Do not build a full converter until this smoke test passes.
4. Download only the target years needed after the smoke test succeeds.
5. Check for nearby station data:
   - Use EBAS/EANET observations to validate CAMS annual concentrations where possible.
   - Prefer station pH and base cations over model-derived estimates when the station is representative and close enough for the study purpose.
6. Convert annual wet-deposition fluxes to precipitation concentrations only after confirming source units.
7. Write a derivation JSON under `result/<site_id>/` and update the EcoSIM NetCDF only after all validity checks pass.

## Unit Policy

EcoSIM precipitation chemistry variables are concentrations in precipitation, not deposition fluxes.

For gridded wet-deposition sources:

```text
concentration_g_m3 = annual_wet_deposition_kg_m2 * 1000 / annual_precipitation_m
```

Apply elemental mass fractions only when the source deposition is stored as compound/ion mass rather than elemental mass:

- `NH4` to `CN4RIG`: multiply by `14.0067 / 18.0385 = 0.7765`.
- `NO3` to `CNORIG`: multiply by `14.0067 / 62.0049 = 0.2259`.
- `SO4` to `CSORG`: multiply by `32.065 / 96.06 = 0.3338`.
- If the source already reports N or S mass, do not apply the ion-to-element factor.

For station concentrations, preserve the native concentration basis and convert explicitly:

- `1 mg/L = 1 g/m3`.
- `1 ug/L = 0.001 g/m3`.
- `ueq/L` requires ion charge and molar mass; do not convert by a scalar shortcut.

## Validity Checks

Reject or flag:

- Non-finite values, source fill values, negative concentrations, or negative precipitation.
- `PHRG` outside `0-14`.
- Annual precipitation totals too small to safely divide wet deposition into concentration.
- CAMS or MERRA-2 variables whose metadata does not clarify whether the mass basis is compound/ion/elemental.
- Full-year EcoSIM outputs that contain partial-year chemistry without a documented interpolation or climatology policy.

Gap policy:

- Interpolate short annual gaps with linear interpolation and nearest-edge fill only when neighboring years are from the same data source and variable.
- Use neutral `PHRG=7` only when no valid pH source exists.
- Do not synthesize base cations from dust or sea-salt fields without labeling the result low confidence.

## Source-Specific Details

For download snippets, source access notes, and suggested source-to-variable mappings, read `references/source_downloads.md` only when needed.

## Reporting

Always report:

- Site lon/lat, years, and bounding box or station-distance criteria.
- Dataset names and access method.
- Exact source variables used and units read from metadata.
- Conversion factors, elemental-basis assumptions, and precipitation divisor.
- Whether values came from CAMS, EBAS, EANET, MERRA-2, station override, interpolation, or defaults.
- Quality flags and any variables left absent/defaulted.
