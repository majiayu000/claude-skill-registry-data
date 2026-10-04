---
name: evo-acopf-solver
description: Builds and solves AC Optimal Power Flow using Pyomo+IPOPT with polar coordinate formulation.
---
# evo-acopf-solver

Builds and solves full ACOPF problem using Pyomo and IPOPT.

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-acopf-solver/scripts')
from utils import build_and_solve_acopf, build_acopf_model, solve_acopf, install_solver

model, results = build_and_solve_acopf(baseMVA, buses, gens, branches, loads_by_bus, shunts_by_bus,
                                        gen_at_bus, branch_from, branch_to)
```

## Key Details
- Polar coordinate formulation with Pi-section branch model
- Squared thermal limits to avoid sqrt non-differentiability
- Reference bus angle fixed to 0
- Cost coefficients pre-scaled for per-unit variables
- IPOPT with ma27 linear solver via idaes
