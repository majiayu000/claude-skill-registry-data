---
name: ecosim-natural-plant-mgmt
description: "Prepare, validate, and edit EcoSIM plant management inputs using pft_mgmt_in NetCDF, editable Excel workbooks, and optional PlantMgmtWriter.py JSON files. Use when creating or checking natural PFT management data, converting pft-mngt NetCDF to an Excel sheet for editing, converting edited Excel back to JSON or NetCDF, validating pft_type/pft_pltinfo/pft_mgmt entries, or preparing PlantMgmtWriter.py inputs for EcoSIM."
---

# EcoSIM Natural Plant Management

## Overview

Use this skill to build, validate, or edit EcoSIM `pft_mgmt_in` inputs for natural ecosystems. Natural PFTs normally need planting information; tree PFTs also receive an annual 1% thinning rate spread uniformly over 12 monthly events. Existing NetCDF files can be exported to an Excel workbook for editing, then converted back to JSON or NetCDF.

Read `references/plant_mgmt_contract.md` when you need exact NetCDF dimensions, Excel sheet columns, variable names, string formats, thinning event fields, or JSON examples.

## Workflow

1. Identify active PFTs for each topo unit and validate EcoSIM vegetation codes with `$ecosim-vegetation-code` against the active PFT parameter CDL.
2. Choose the editing path:
   - For an existing `.nc`, export to Excel, edit the workbook, then convert the edited workbook back to JSON or NetCDF.
   - For a new file, create either JSON directly or an Excel workbook matching the contract schema.
3. Set `pft_dflag = 0` for constant natural vegetation unless year-specific PFT composition or management is needed. With `pft_dflag = 0`, EcoSIM uses record 1. With `pft_dflag = 1`, the selected `PlantInfoMod.F90` matches the forcing year (`yeari`) to the NetCDF `year` record.
4. Set each topo unit `NZ` to the active PFT count. Do not exceed `maxpfts = 5`; only the first `NZ` PFT entries matter.
5. For each PFT, set `pft_type` to the validated six-character EcoSIM code. EcoSIM will use the first four characters plus the grid Koppen code when `KoppenClimZone_col > 0`, but keep the full validated code for clarity.
6. For planting, use `DDMMYYYY = "01019999"` unless the user provides a site-specific date. Derive `Planting_population` as plants, shoots, tillers, or stems per square meter and `Planting_depth` in meters.
7. For non-tree natural PFTs, set `mgmt` empty. For tree PFTs, add 12 monthly thinning events using `FractionCut = 0.01 / 12 = 0.0008333333`.

## Conversion Commands

Use the bundled bridge for NetCDF, Excel, and JSON conversions:

```bash
.venv-cmip6/bin/python .agents/skills/ecosim-natural-plant-mgmt/scripts/plant_mgmt_excel_bridge.py nc-to-xlsx pft-mngt.nc pft-mngt.xlsx
.venv-cmip6/bin/python .agents/skills/ecosim-natural-plant-mgmt/scripts/plant_mgmt_excel_bridge.py xlsx-to-json pft-mngt.xlsx pft-mngt.json
.venv-cmip6/bin/python .agents/skills/ecosim-natural-plant-mgmt/scripts/plant_mgmt_excel_bridge.py xlsx-to-nc pft-mngt.xlsx pft-mngt-edited.nc --json-output pft-mngt-edited.json
```

JSON remains supported. To create NetCDF directly from JSON, use either the bridge or `PlantMgmtWriter.py`:

```bash
.venv-cmip6/bin/python .agents/skills/ecosim-natural-plant-mgmt/scripts/plant_mgmt_excel_bridge.py json-to-nc input.json output.nc
.venv-cmip6/bin/python applications/notebooks/scripts/PlantMgmtWriter.py input.json output.nc
```

## Evidence Rules

- Search the web or literature for typical density and planting depth when values are not provided. Cite sources in the response or derivation note.
- Prefer species-specific stand density, seedling density, stem density, tiller density, or plant density. Convert all density units to plants m-2.
- Avoid substituting percent cover, LAI, biomass, or seeding rate for plant density unless no better source exists; if used, label it as an assumption.
- Convert depths to meters. If evidence is weak, use conservative defaults only with an explicit note: herbaceous PFTs often need shallow depths, tree seedlings need a larger initial depth.

## Tree Thinning Convention

Apply monthly thinning only to tree PFTs such as `ndlf`, `ndld`, `bdlf`, `bdln`, `bdlw`, `bspr`, `dfir`, `jpin`, `lpin`, `tasp`, and `woak`. Treat `bush`, `busn`, and `shru` as non-tree woody PFTs unless the user asks to include woody shrub thinning.

Use these monthly event dates with year `0000`:

```text
31010000 28020000 31030000 30040000 31050000 30060000
31070000 31080000 30090000 31100000 30110000 31120000
```

Each thinning event should use:

```json
{
  "iHarvType": 0,
  "jHarvType": 0,
  "CutHeight": 1000.0,
  "FractionCut": 0.0008333333,
  "FineFractionLeafHarvested_pft": 1,
  "FineFractionNonleafHarvested_pft": 1,
  "StalkFractionHarvested_pft": 1,
  "StandeadFractionHarvested_pft": 0,
  "FineFractionLeafHarvested_col": 0,
  "FineFractionNonleafHarvested_col": 0,
  "StalkFractionHarvested_col": 0,
  "StandeadFractionHarvested_col": 0
}
```

This represents natural mortality/thinning without ecosystem biomass export. Flag the mass-flow assumption if changing ecosystem-level export fractions.

For harvested biomass, the ecosystem-level harvest fraction applies to the harvested component, not to the original component pool. Litter return is:

```text
component_pool * pft_harvest_fraction * (1 - ecosystem_harvest_fraction)
```

For transient yearly schedules, prefer actual calendar years in `DDMMYYYY` if exact day-of-year alignment matters. The selected `PlantInfoMod.F90` treats year `0000` as a leap year when converting dates to ordinal day.

## Validation

Run the bridge round trip on a scratch path and inspect the decoded JSON:

```bash
.venv-cmip6/bin/python .agents/skills/ecosim-natural-plant-mgmt/scripts/plant_mgmt_excel_bridge.py nc-to-json input.nc /tmp/pft-mgmt.json
.venv-cmip6/bin/python .agents/skills/ecosim-natural-plant-mgmt/scripts/plant_mgmt_excel_bridge.py nc-to-xlsx input.nc /tmp/pft-mgmt.xlsx
.venv-cmip6/bin/python .agents/skills/ecosim-natural-plant-mgmt/scripts/plant_mgmt_excel_bridge.py xlsx-to-nc /tmp/pft-mgmt.xlsx /tmp/pft-mgmt-roundtrip.nc --json-output /tmp/pft-mgmt-roundtrip.json
```

Verify that `pft_dflag`, `year`, `NH1/NV1/NH2/NV2/NZ`, `pft_type`, `pft_pltinfo`, `nmgnts`, and `pft_mgmt` exist; `NZ` equals active PFT count; `nmgnts` equals populated management rows; non-tree PFTs have zero management events unless explicitly managed; tree PFTs have 12 thinning events when using the natural-tree convention.
