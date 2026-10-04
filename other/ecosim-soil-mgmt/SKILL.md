---
name: ecosim-soil-mgmt
description: "Prepare, validate, inspect, and edit EcoSIM soil management inputs using soil_mgmt_in NetCDF, editable Excel workbooks, and optional JSON files. Use when checking fertilizer, tillage, or irrigation management data; converting soil-mngt NetCDF to Excel for editing; converting edited Excel back to JSON or NetCDF; decoding fertf/tillf/irrigf selector variables; or validating EcoSIM ReadManagementMod.F90 soil-management inputs."
---

# EcoSIM Soil Management

## Overview

Use this skill to build, inspect, validate, or edit EcoSIM `soil_mgmt_in` files. Soil management files use yearly selectors (`fertf`, `tillf`, `irrigf`) that point to event-table variables inside the same NetCDF file. Existing NetCDF files can be exported to Excel for editing, then converted back to JSON or NetCDF.

Read `references/soil_mgmt_contract.md` when you need exact NetCDF dimensions, Excel sheet columns, field order, units, or Fortran reader behavior.

## Workflow

1. Identify the EcoSIM branch/reader when possible. The canonical reader contract for this skill is `f90src/IOutils/ReadManagementMod.F90`.
2. For an existing `.nc`, inspect it first:

```bash
.venv-cmip6/bin/python .agents/skills/ecosim-soil-mgmt/scripts/soil_mgmt_excel_bridge.py inspect soil-mngt.nc
```

3. Choose the editing path:
   - Existing NetCDF: export to Excel, edit the workbook, then convert the edited workbook back to JSON or NetCDF.
   - New file: create JSON directly or an Excel workbook matching the contract schema.
4. In Excel, keep event-table names in the `event_files` sheet so empty but intentional variables are preserved during round trips.
5. Keep selector strings short: `fertf`, `tillf`, and `irrigf` entries are fixed 10-character names. Use `NO` for inactive management.
6. Fertilizer quantities are read as `g m-2`. Convert annual or field-rate values before writing: `1 g m-2 = 10 kg ha-1`.
7. Use actual calendar years in `DDMMYYYY` for year-specific schedules. The Fortran reader uses the year embedded in the event string for leap-year day-of-year conversion.
8. After conversion, inspect the new file and check date-year mismatches, missing selector targets, nonzero nutrient totals, and whether expected tillage/irrigation events are present.

## Conversion Commands

Use the bundled bridge for NetCDF, Excel, and JSON conversions:

```bash
.venv-cmip6/bin/python .agents/skills/ecosim-soil-mgmt/scripts/soil_mgmt_excel_bridge.py nc-to-xlsx soil-mngt.nc soil-mngt.xlsx
.venv-cmip6/bin/python .agents/skills/ecosim-soil-mgmt/scripts/soil_mgmt_excel_bridge.py xlsx-to-json soil-mngt.xlsx soil-mngt.json
.venv-cmip6/bin/python .agents/skills/ecosim-soil-mgmt/scripts/soil_mgmt_excel_bridge.py xlsx-to-nc soil-mngt.xlsx soil-mngt-edited.nc --json-output soil-mngt-edited.json
```

JSON remains supported:

```bash
.venv-cmip6/bin/python .agents/skills/ecosim-soil-mgmt/scripts/soil_mgmt_excel_bridge.py nc-to-json soil-mngt.nc soil-mngt.json
.venv-cmip6/bin/python .agents/skills/ecosim-soil-mgmt/scripts/soil_mgmt_excel_bridge.py json-to-nc soil-mngt.json soil-mngt.nc
```

## Validation

For fertilizer-only files, verify that:

- `fertf` selectors point to existing fertilizer variables for every active year.
- `tillf` and `irrigf` are `NO` if there are no tillage or irrigation events.
- Each fertilizer row has 27 fields.
- Fertilizer dates are valid `DDMMYYYY` and match the selector year unless deliberately yearless.
- Annual N and P totals are plausible for the site and management intensity.

For tillage and irrigation files, also verify row counts do not exceed reader limits: fertilizer `<=12`, scheduled irrigation `<=24`, and tillage `<=367`.
