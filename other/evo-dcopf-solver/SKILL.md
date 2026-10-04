---
name: evo-dcopf-solver
description: Solves DC-OPF with spinning reserve co-optimization using PuLP/CBC. Extracts LMPs from dual variables, reserve MCP, binding lines.
---

# evo-dcopf-solver

Solves DC-OPF with reserve co-optimization using PTDF formulation and PuLP.

## Key Functions

- `solve_dcopf_with_reserves(nb, ng, nl, gen_info, branches, costs, load_p, matrices, reserve_capacity, reserve_requirement, Cg)` - Main solver
- `extract_lmps(result, int2ext)` - Returns list of {bus, lmp_dollars_per_MWh}
- `extract_reserve_mcp(result)` - Returns reserve MCP float
- `identify_binding_lines(result, branches, int2ext, threshold=0.99)` - Returns binding line dicts
- `compute_total_cost(result)` - Returns total cost float

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-dcopf-solver/scripts')
from utils import (solve_dcopf_with_reserves, extract_lmps, extract_reserve_mcp,
                   identify_binding_lines, compute_total_cost)

result = solve_dcopf_with_reserves(nb, ng, nl, gen_info, branches, costs,
                                    load_p, matrices, reserve_capacity,
                                    reserve_requirement, Cg)
lmps = extract_lmps(result, int2ext)
reserve_mcp = extract_reserve_mcp(result)
binding = identify_binding_lines(result, branches, int2ext)
total_cost = compute_total_cost(result)
```
