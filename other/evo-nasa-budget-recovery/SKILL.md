---
name: evo-nasa-budget-recovery
description: Analyzes NASA budget workbook mathematical structure to recover missing ??? values via constraint propagation across sheets (row sums, YoY percentages, directorate shares, growth analysis).
---

# evo-nasa-budget-recovery

Recovers missing ??? values in multi-sheet NASA budget Excel files.

## Relationships Detected
1. **Row sums**: Budget sheet Total col = sum of directorate cols
2. **YoY %**: (current - previous) / previous * 100, rounded to 2 decimals
3. **Shares %**: directorate_val / total * 100, rounded to 2 decimals
4. **Growth Analysis**: CAGR, 5-year change, average annual budget
5. **Cross-sheet**: Budget values recoverable from YoY + previous year

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-nasa-budget-recovery/scripts')
from utils import run_recovery_pipeline

wb = run_recovery_pipeline('input.xlsx', 'output.xlsx')
```

## Key Functions
- `run_recovery_pipeline(input_path, output_path)` - Full pipeline
- `solve_row_with_one_unknown(ws, row, data_cols, total_col)` - Row sum solver
- `recover_yoy_value(budget_ws, yoy_ws, row, col)` - YoY % calculator
- `recover_share_value(budget_ws, shares_ws, row, col)` - Share % calculator
- `recover_growth_analysis(wb)` - Growth sheet recovery
- `recover_budget_from_yoy(budget_ws, yoy_ws, row, col)` - Cross-sheet recovery
