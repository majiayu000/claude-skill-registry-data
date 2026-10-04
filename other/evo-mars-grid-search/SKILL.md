---
name: evo-mars-grid-search
description: Parallel grid search over DBSCAN hyperparameters for Mars cloud clustering. Aggregates per-image F1 and delta scores with proper averaging semantics.
---

# evo-mars-grid-search

Parallel grid search over DBSCAN hyperparameters.

## Key Functions

- `load_data(citsci_path, expert_path)` - Load CSVs, return grouped dicts
- `evaluate_hyperparameter_combo(ms, eps, sw, images, citsci_dict, expert_dict)` - Eval one combo
- `run_grid_search(unique_images, citsci_dict, expert_dict, n_jobs)` - Full parallel grid search
- `filter_results(results_df, min_f1=0.5)` - Filter to F1 > 0.5

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-mars-grid-search/scripts')
from utils import load_data, run_grid_search, filter_results

_, _, images, citsci_dict, expert_dict = load_data('citsci.csv', 'expert.csv')
results = run_grid_search(images, citsci_dict, expert_dict)
filtered = filter_results(results)
```

## Averaging Rules

- Loop over ALL unique images from expert dataset
- Images with no citsci points: F1=0.0, delta=NaN
- F1 average includes all zeros
- Delta average excludes NaN values
- Filter: only keep F1 > 0.5
