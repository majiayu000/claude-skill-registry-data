---
name: evo-fjsp-data-io
description: Parses FJSP instance, downtime, policy, baseline files and exports solutions to JSON/CSV.
---
# evo-fjsp-data-io

All file I/O for FJSP scheduling tasks.

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-fjsp-data-io/scripts')
from utils import (parse_fjsp_instance, parse_downtimes_csv,
    parse_policy_budgets, parse_baseline_schedule,
    export_solution_json, export_solution_csv)
```

## Functions
- `parse_fjsp_instance(filepath)` -> (jobs, num_machines)
- `parse_downtimes_csv(filepath)` -> {machine_id: [[start,end],...]}
- `parse_policy_budgets(filepath)` -> policy dict
- `parse_baseline_schedule(filepath)` -> (baseline_dict, makespan, schedule_list)
- `export_solution_json(schedule, makespan, status, filepath)`
- `export_solution_csv(schedule, filepath)`
