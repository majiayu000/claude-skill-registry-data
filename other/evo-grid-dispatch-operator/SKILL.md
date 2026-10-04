---
name: evo-grid-dispatch-operator
description: "End-to-end DC Optimal Power Flow with spinning reserve co-optimization. Parses MATPOWER JSON network data, builds DC power flow model with bus voltage angles, formulates and solves the DCOPF+reserve QP/LP via cvxpy (CLARABEL solver), computes line loading and operating margins, and produces a structured report.json."
---

# evo-grid-dispatch-operator

Solves DC Optimal Power Flow with spinning reserve co-optimization from MATPOWER JSON data and produces a structured dispatch report.

## Quick Start — Full Pipeline

```python
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "cvxpy", "clarabel", "-q"])

import sys as _sys
_sys.path.insert(0, '/app/environment/skills/evo-grid-dispatch-operator/scripts')
from solve import main
main("/root/network.json", "/root/report.json")
```

This single call handles everything: parse → optimize → report.

## Formulation Details

### DC Power Flow Model
- Bus voltage angle variables `theta` (radians), slack bus angle fixed to 0
- Branch power flow: `flow_MW = (1/X) * (theta_f - theta_t) * baseMVA`
- Transformer tap ratios handled (tap=0 treated as 1.0)
- Nodal power balance: `sum(Pg at bus) - Pd = B_row @ theta` (per-unit)

### Generator Cost
- Quadratic polynomial: `cost = c2 * Pg_MW^2 + c1 * Pg_MW + c0`
- Coefficients from gencost array columns [4,5,6] for ncost=3

### Constraints
- Generator limits: `Pmin <= Pg <= Pmax` (per-unit internally)
- Line flow limits: `|flow_MW| <= RATE_A` (skip if RATE_A=0)
- Reserve non-negativity: `Rg >= 0`
- Reserve capacity: `Rg <= reserve_capacity[g]`
- Capacity coupling: `Pg_MW + Rg <= Pmax_MW`
- System reserve: `sum(Rg) >= reserve_requirement`

### Solver
- **cvxpy with CLARABEL** (interior-point, handles QP and LP)

### Report Structure
```json
{
  "generator_dispatch": [
    {"id": 1, "bus": 1, "output_MW": 100.0, "reserve_MW": 30.0, "pmax_MW": 150.0}
  ],
  "totals": {
    "cost_dollars_per_hour": 8000.0,
    "load_MW": 259.0,
    "generation_MW": 259.0,
    "reserve_MW": 500.0
  },
  "most_loaded_lines": [{"from": 1, "to": 2, "loading_pct": 85.0}],
  "operating_margin_MW": 50.0
}
```

### Key Definitions
- `operating_margin_MW = sum(Pmax - output_MW - reserve_MW)` over all generators
- `most_loaded_lines`: top 3 lines sorted descending by `loading_pct`
- `loading_pct = |flow_MW| / RATE_A * 100` (only for lines with RATE_A > 0)

## Module Reference

### `data_loader.py`
- `load_network(filepath)` — Load MATPOWER JSON, return dict with numpy arrays
- `build_bus_index_map(bus_data)` — External-to-internal bus ID mapping
- `get_slack_bus_index(bus_data, ext2int)` — Find reference bus (type==3)

### `network_model.py`
- `build_b_matrix(branches, n_bus, ext2int)` — Build nodal susceptance matrix
- `get_gen_bus_indices(gens, ext2int)` — Map generators to internal bus indices
- `get_branch_flow_data(branches, ext2int)` — Branch susceptances and endpoint indices

### `optimizer.py`
- `solve_dcopf_with_reserves(...)` — Full cvxpy DCOPF+reserve formulation with CLARABEL

### `report_generator.py`
- `compute_line_loadings(theta, branch_flow_data, baseMVA)` — Line flows and loading %
- `build_report(...)` — Assemble report dict
- `save_report(report, filepath)` — Write JSON