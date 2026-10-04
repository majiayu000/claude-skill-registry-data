---
name: evo-mars-pareto-output
description: Computes Pareto frontier from grid search results (maximize F1, minimize delta) and writes formatted CSV output.
---

# evo-mars-pareto-output

Pareto frontier computation and formatted CSV output.

## Key Functions

- `compute_pareto_frontier(results_df)` - Find Pareto-optimal points (max F1, min delta)
- `format_and_save_pareto_csv(pareto_df, output_path)` - Format and save to CSV

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-mars-pareto-output/scripts')
from utils import compute_pareto_frontier, format_and_save_pareto_csv

pareto = compute_pareto_frontier(filtered_results)
format_and_save_pareto_csv(pareto, '/root/pareto_frontier.csv')
```

## Output Format

CSV columns: F1, delta, min_samples, epsilon, shape_weight
- F1 and delta: 5 decimal places
- shape_weight: 1 decimal place
- min_samples and epsilon: integers
- Uses paretoset with sense=['max', 'min']
