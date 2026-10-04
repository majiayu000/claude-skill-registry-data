---
name: evo-lake-data-pipeline
description: Loads, merges, and preprocesses lake water temperature and environmental driver CSV datasets. Provides category mapping for Heat/Flow/Wind/Human factor groups.
---

# evo-lake-data-pipeline

Loads and merges four CSV datasets (water_temperature, climate, land_cover, hydrology) into analysis-ready DataFrames.

## Category Mapping

| Category | Variables |
|----------|----------|
| Heat | AirTempLake, Shortwave, Longwave |
| Flow | Precip, Outflow, Inflow |
| Wind | WindSpeedLake |
| Human | DevelopedArea, AgricultureArea |

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-lake-data-pipeline/scripts')
from utils import load_all_datasets, merge_datasets, get_feature_columns, get_feature_columns_by_category, get_category_map

water_temp, climate, land_cover, hydrology = load_all_datasets('/root/data/')
merged = merge_datasets(water_temp, climate, land_cover, hydrology)
features = get_feature_columns()
cat_map = get_category_map()
```

## Key Functions

- `load_all_datasets(data_dir)` — loads all 4 CSVs, returns tuple of DataFrames
- `merge_datasets(wt, clim, lc, hydro)` — inner-joins on Year column
- `get_feature_columns()` — returns list of 9 predictor column names
- `get_feature_columns_by_category()` — returns dict of category -> [features]
- `get_category_map()` — returns dict of feature_name -> category_name

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
