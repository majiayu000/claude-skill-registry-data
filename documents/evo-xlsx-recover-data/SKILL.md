---
name: evo-xlsx-recover-data
description: "Recover missing values (marked as \"???\") in a multi-sheet NASA budget Excel workbook. Handles 4 interdependent sheets with cross-sheet constraint propagation, floating-point precision management, and robust Excel I/O via openpyxl."
---

# evo-xlsx-recover-data

## Purpose
Recover missing values (marked as "???") in a multi-sheet NASA budget Excel workbook.
The workbook has 4 interdependent sheets:
1. **Budget by Directorate** - Raw dollar values ($M) per category per year (FY2015-FY2024)
2. **YoY Changes (%)** - Year-over-year percentage changes
3. **Directorate Shares (%)** - Each category as % of yearly total
4. **Growth Analysis** - Summary statistics (CAGR, averages, deltas) for FY2019-2024

## Key Formulas
- **Row Sum**: Total = sum of all category columns
- **YoY%**: ((current - previous) / previous) * 100, rounded to 2dp
- **Share%**: (category / total) * 100, rounded to 2dp
- **CAGR%**: ((end/start)^(1/n) - 1) * 100, rounded to 2dp, n=5 for FY2019-FY2024
- **Average Budget**: mean of FY2019-FY2023 (5 years), rounded to 1dp
- **5-Year Change**: FY2024 - FY2019, integer

## Rounding Rules
- Budget amounts: integer (no decimals)
- YoY/Share/CAGR percentages: 2 decimal places
- Average budgets: 1 decimal place
- Dollar change/delta: integer

## Sheet Layout Details
- Budget: rows 4-13 (FY2015-2024), cols B(2)-K(11), K=Total
- YoY: rows 4-12 (2016-2024), cols B-K. YoY row N maps to budget rows N and N+1
- Shares: rows 4-13 (2015-2024), cols B-J (no Total column)
- Growth: row 4=CAGR, row 5=FY2019, row 6=FY2024, row 7=Change, row 8=Avg. Cols B-J

## Dependency Resolution Strategy
The `recover_all()` function uses iterative constraint propagation:
1. Solve Budget sheet row sums (Total column vs category columns)
2. Use YoY percentages to recover Budget values and vice versa
3. Use Share percentages to recover Budget values and vice versa
4. Cross-sheet sync: Growth Analysis ↔ Budget sheet (FY2019=row8, FY2024=row13)
5. Compute CAGR, 5-Year Change, and Average Budget in Growth Analysis
6. Repeat until no more progress (handles cascading dependencies)
7. Final pass: recompute all Growth Analysis averages for consistency

## Robustness Features
- Handles merged cells safely (skips MergedCell objects)
- Floating-point tolerance checks using math.isclose()
- Type inference: preserves int vs float based on context
- Multiple missing values in same row/column: only solves when exactly 1 unknown
- Iterates up to 50 passes to handle deep dependency chains
- Graceful handling of edge cases (division by zero, negative CAGR inputs)

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-xlsx-recover-data/scripts')
from utils import load_workbook, recover_all, save_workbook

wb = load_workbook('/root/nasa_budget_incomplete.xlsx')
recovered = recover_all(wb)
for sheet, cell, val in recovered:
    print(f"{sheet} {cell} = {val}")
save_workbook(wb, '/root/nasa_budget_recovered.xlsx')
```