---
name: evo-lake-trend-analysis
description: Performs Mann-Kendall trend detection on lake water temperature time series using pymannkendall. Outputs slope (Sen's slope) and p-value to trend_result.csv.
---

# evo-lake-trend-analysis

Performs non-parametric Mann-Kendall trend detection on water temperature time series.

## Key Concepts

- Uses `pymannkendall` library for Mann-Kendall tests
- Sen's slope attribute: `result.slope`
- P-value attribute: `result.p`
- NaN values MUST be dropped before passing to pymannkendall
- For annual data (low autocorrelation risk), `original_test` is appropriate
- For data with autocorrelation, use `hamed_rao` or `yue_wang` methods

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-lake-trend-analysis/scripts')
from utils import run_mann_kendall_trend, save_trend_result

# Run trend test on water temperature series
trend = run_mann_kendall_trend(merged_df['WaterTemperature'], method='original')

# Save to CSV (columns: slope, p-value)
result_df = save_trend_result(trend, '/root/output/trend_result.csv')
```

## Key Functions

- `run_mann_kendall_trend(series, method, alpha)` — runs MK test, returns dict with slope, p_value, trend
- `save_trend_result(trend_dict, output_path)` — saves slope and p-value to CSV

## Output Format

trend_result.csv:
```
slope,p-value
0.0245,0.034
```

## Import Pattern (avoiding naming conflicts)

When using multiple skills that each have `utils.py`, use importlib to avoid conflicts:

```python
import importlib.util

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

data_utils = load_module('data_utils', '/app/environment/skills/evo-lake-data-pipeline/scripts/utils.py')
trend_utils = load_module('trend_utils', '/app/environment/skills/evo-lake-trend-analysis/scripts/utils.py')
factor_utils = load_module('factor_utils', '/app/environment/skills/evo-lake-factor-attribution/scripts/utils.py')
```
