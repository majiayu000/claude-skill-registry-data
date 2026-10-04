---
name: ameriflux-bif-ecosim-mgmt
description: "Extract AmeriFlux BASE-BADM/BIF crop management records into EcoSIM-editable plant-management and soil-management Excel workbooks that can be converted to EcoSIM NetCDF files. Use when asked to derive EcoSIM planting, harvest, fertilizer, or tillage management inputs from AMF *_BIF_*.xlsx or BIF CSV files, especially for crop sites where management details live in GRP_DM_* records and DM_COMMENT fields."
---

# AmeriFlux BIF To EcoSIM Management

## Overview

Use this skill to convert AmeriFlux BADM/BIF management metadata into two editable EcoSIM workbooks:

- `*_plant_mgmt.xlsx`, matching `$ecosim-natural-plant-mgmt`.
- `*_soil_mgmt.xlsx`, matching `$ecosim-soil-mgmt`.

The extractor also writes companion JSON files and a `*_management_extraction_review.xlsx` workbook. Always review assumptions before converting the generated Excel files to NetCDF, because many AmeriFlux management quantities are stored in free-text comments.

Read `references/mapping_rules.md` when you need the exact parsing and default mapping rules.

## Workflow

1. Inspect the BIF workbook if needed. Prefer the `AMF-BIF` sheet.
2. Run the bundled extractor with the repo Python environment so it can read both XLSX and the PFT parameter NetCDF:

```bash
.venv-cmip6/bin/python \
  .agents/skills/ameriflux-bif-ecosim-mgmt/scripts/extract_bif_mgmt_to_ecosim_excel.py \
  /path/to/AMF_SITE_BIF_YYYYMMDD.xlsx \
  --pftpar-nc /path/to/ecosim_pftpar_YYYYMMDD.nc \
  --koppen-code 41 \
  --out-dir result/SITE/ecosim_mgmt_from_bif
```

3. Open the review workbook and check:
   - crop-to-PFT mapping (`corn=maiz41`, `soybean=soyb41` by default);
   - parsed planting populations from seed rates;
   - fertilizer N rates and product split among `NH4Soil`, `NH3Soil`, `UreaSoil`, and `NO3Soil`;
   - tillage depth/type defaults;
   - harvest defaults and `FractionCut` assumptions.
4. Edit the generated plant/soil Excel workbooks if needed.
5. Convert reviewed workbooks to NetCDF using the existing bridge skills:

```bash
.venv-cmip6/bin/python .agents/skills/ecosim-natural-plant-mgmt/scripts/plant_mgmt_excel_bridge.py \
  xlsx-to-nc SITE_plant_mgmt.xlsx SITE_pft_mgmt.nc --json-output SITE_pft_mgmt.json

.venv-cmip6/bin/python .agents/skills/ecosim-soil-mgmt/scripts/soil_mgmt_excel_bridge.py \
  xlsx-to-nc SITE_soil_mgmt.xlsx SITE_soil_mgmt.nc --json-output SITE_soil_mgmt.json
```

## Useful Options

- `--start-year` and `--end-year`: limit the output years.
- `--pftpar-nc`: EcoSIM PFT parameter NetCDF used to validate `pft_type` against `pfts`.
- `--koppen-code`: two-digit EcoSIM climate number used to compose `<pfts_short><koppen>`.
- `--crop-pft-map crop=pftcode`: explicit crop mapping override, repeatable.
- `--planting-depth-m`: default planting depth used when BIF only provides seed rate.
- `--topo NH1,NV1,NH2,NV2`: set EcoSIM topo-unit bounds.
- `--default-fertilizer-n-g-m2`: placeholder N rate when a fertilizer event lacks a parseable rate.
- `--tillage-depth-m` and `--tillage-type`: placeholders for BIF tillage records.

## Output Contract

The plant workbook has the exact sheets required by `plant_mgmt_excel_bridge.py`: `control`, `topo_units`, `pft_years`, and `management`.

The soil workbook has the exact sheets required by `soil_mgmt_excel_bridge.py`: `control`, `topo_units`, `year_selectors`, `event_files`, `fertilizer`, `tillage`, and `irrigation`.

The review workbook is not consumed by EcoSIM. It exists to protect unit consistency and mass-flow assumptions before NetCDF conversion.
