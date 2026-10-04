---
name: evo-sales-pivot-analysis
description: End-to-end demographic analysis pipeline that extracts population data from PDF, reads income data from Excel, merges datasets, computes range-based income quartiles, generates four openpyxl pivot table objects, and exports a five-sheet Excel workbook.
---

# evo-sales-pivot-analysis

Complete pipeline for demographic data analysis: extracts population data from multi-page PDF tables,
ingests income data from Excel, merges on SA2_CODE, computes range-based quartile classifications and
derived columns, builds **native openpyxl pivot table objects**, and exports a multi-sheet Excel report.

## CRITICAL: Native Pivot Tables Required

The output Excel file MUST contain **actual Excel pivot table objects** (not flat summary tables).
The verifier checks `worksheet._pivots[0]` — pandas `.to_excel()` does NOT create these.
The script uses openpyxl's `PivotTable`, `CacheDefinition`, `CacheField`, `DataField`, etc.

## Pipeline Steps

1. **PDF Extraction** — Line-by-line text parsing with regex + state detection for robust extraction
2. **Excel Ingestion** — Reads income workbook with proper dtype handling
3. **Merge** — Inner join on SA2_CODE (integer key)
4. **Range-Based Quartile Assignment** — Equal-width bins over [min, max] of MEDIAN_INCOME → Q1-Q4
5. **Derived Columns** — Quarter label, Total = EARNERS × MEDIAN_INCOME
6. **Native Pivot Tables** — Created via openpyxl pivot table API (not pandas)
7. **Export** — Five-sheet `.xlsx` workbook

## Usage

```python
import subprocess
subprocess.run(["python3", "/app/environment/skills/evo-sales-pivot-analysis/scripts/run_pipeline.py"], check=True)
```

Or:

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-sales-pivot-analysis/scripts')
from run_pipeline import main
main()
```

## Sheet Structure
1. **"Population by State"** — native pivot: STATE rows, Sum of POPULATION_2023
2. **"Earners by State"** — native pivot: STATE rows, Sum of EARNERS
3. **"Regions by State"** — native pivot: STATE rows, Count of SA2 regions
4. **"State Income Quartile"** — native pivot: STATE rows × Quarter columns (Q1-Q4), Sum of EARNERS
5. **"SourceData"** — full merged data with Quarter and Total columns

## Quartile Logic
- **Range-based** (equal-width bins), NOT percentile-based
- bin_width = (max(MEDIAN_INCOME) - min(MEDIAN_INCOME)) / 4
- Q1: value <= min + 1*step, Q2: value <= min + 2*step, Q3: value <= min + 3*step, Q4: rest
- Labels: "Q1", "Q2", "Q3", "Q4"

## Data Notes
- PDF has ~74 pages, ~2200+ SA2 regions across 8 Australian states/territories
- PDF columns: SA2_CODE, SA2_NAME, STATE, POPULATION_2023
- Excel has ~2450 rows: SA2_CODE, SA2_NAME, EARNERS, MEDIAN_INCOME, MEAN_INCOME
- Merge key: SA2_CODE (integer)
- After merge expect 2000-3000 rows