---
name: evo-excel-data-extraction
description: Utilities for exploring and extracting data from complex, multi-sheet Excel workbooks with irregular formatting. Provides functions to discover sheet structure, locate gold prices in IMF data, and extract country reserve data.
---

# evo-excel-data-extraction

Utilities for reading IMF commodity price data and template workbook structures.

## Key Functions

- `extract_gold_price_series(filepath)` - Extract gold price (US$/troy oz) time series from IMF file. Returns list of (date_str, price) tuples.
- `extract_country_reserve_data(filepath, sheet_name, year_row=18)` - Extract country gold reserves from Value/Volume sheets. Returns dict with country data.
- `extract_total_reserves_data(filepath, year_row=18)` - Extract total reserves for 2025.
- `explore_sheet_structure(filepath)` - Get sheet dimensions and info.
- `extract_country_names_from_desc(desc_str)` - Parse country name from column description.

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-excel-data-extraction/scripts')
from utils import extract_gold_price_series, extract_country_reserve_data, extract_total_reserves_data

gold_series = extract_gold_price_series('/root/data/imf-commodity-prices.xlsx')
value_countries = extract_country_reserve_data('/root/data/test-rar.xlsx', 'Value')
volume_countries = extract_country_reserve_data('/root/data/test-rar.xlsx', 'Volume')
total_reserves = extract_total_reserves_data('/root/data/test-rar.xlsx')
```

## Data Layout Notes

- IMF file: Single sheet, PGOLD column (BY/col 77), data rows 5-433, dates like "1990M1" to "2025M9"
- Template Gold price sheet: rows 2-430, dates in col A, prices go in col B
- Value sheet: row 18 = 2025 data, columns C-R have different countries
- Volume sheet: row 18 = 2025 data, volumes in various units (Mil.Troy Ounce, Thous.Troy Ounce)
- Total Reserves sheet: row 18 = 2025 data
- Answer sheet: Step 1 (rows 3-6), Step 2 (rows 11-13), Step 3 (rows 20-24)
