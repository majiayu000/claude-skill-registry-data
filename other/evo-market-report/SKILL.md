---
name: evo-market-report
description: Compares base and counterfactual DC-OPF results, computes impact analysis, and exports report.json.
---

# evo-market-report

Compares scenarios and builds the final report.json.

## Key Functions

- `compute_impact_analysis(base_cost, cf_cost)` - Cost reduction
- `find_top_lmp_drops(base_lmps, cf_lmps, n=3)` - Top n buses with largest LMP drop
- `check_congestion_relieved(cf_binding, f_bus, t_bus)` - True if line not binding
- `build_report_json(...)` - Assembles complete report structure
- `export_report(report, filepath)` - Writes JSON file

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-market-report/scripts')
from utils import build_report_json, export_report

report = build_report_json(base_result, cf_result, base_lmps, cf_lmps,
                           base_reserve_mcp, cf_reserve_mcp,
                           base_binding, cf_binding, base_cost, cf_cost)
export_report(report, '/root/report.json')
```
