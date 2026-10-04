---
name: evo-macro-weo-data
description: Populates WEO_Data sheet with IMF WEO data for Georgia, extends GDP deflator and real GDP projections to 2043, and copies GeoStat SUT sheets into the workbook.
---

# evo-macro-weo-data

## Purpose
Handles IMF WEO data ingestion and projection extension for Georgia macro model.

## Key Knowledge
- WEO CSV has: Year, Real GDP (bn Lari), Real GDP Growth (%), GDP Deflator for 2020-2027
- Real GDP growth rate from 2027 is held constant through 2043
- GDP Deflator extended using average of last 4 years growth rates as fixed anchor
- GeoStat SUT 38x38 sheets copied with original names preserved

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-macro-weo-data/scripts')
from utils import populate_weo_data, extend_real_gdp_projection, extend_deflator_projection, copy_sut_sheets

import openpyxl
wb = openpyxl.load_workbook('test - demand.xlsx')
ws, last_csv_row = populate_weo_data(wb)
extend_real_gdp_projection(ws, last_csv_row)
extend_deflator_projection(ws, last_csv_row)
copy_sut_sheets(wb)
wb.save('test - demand.xlsx')
```

## Functions
- `populate_weo_data(wb, csv_path)` - Creates WEO_Data sheet, populates from CSV
- `extend_real_gdp_projection(ws, last_csv_row)` - Extends real GDP 2028-2043
- `extend_deflator_projection(ws, last_csv_row)` - Extends deflator 2028-2043
- `copy_sut_sheets(wb, sut_path)` - Copies SUPPLY and USE sheets
