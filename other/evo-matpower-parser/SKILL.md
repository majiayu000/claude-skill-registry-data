---
name: evo-matpower-parser
description: Parses MATPOWER JSON files into structured Python data with bus mapping, network matrix construction (A, Bbranch, Bbus, PTDF), branch modification, and generator cost parsing.
---

# evo-matpower-parser

Parses MATPOWER JSON network files and builds all data structures needed for DC-OPF.

## Key Functions

- `load_matpower_json(filepath)` - Load JSON file, returns dict
- `create_bus_mappings(bus_data)` - Returns (ext2int, int2ext) dicts
- `find_slack_bus(bus_data)` - Returns external bus ID of slack (type 3)
- `parse_generators(gen_data, ext2int)` - Returns dict with ng, gen_bus_int, pmax, pmin, status
- `parse_branches(branch_data, ext2int)` - Returns dict with nl, f/t_bus_int/ext, x, rate_a, status
- `parse_gencost(gencost_data)` - Returns dict with c2, c1, c0 arrays
- `compute_network_matrices(bus_data, branches, ext2int, slack_ext)` - Returns dict with PTDF, Bbus, etc.
- `modify_branch_rate(data, f_bus, t_bus, multiplier)` - Deep copies data, scales RATE_A
- `get_load_vector(bus_data, nb)` - Returns load array
- `get_gen_bus_matrix(gen_info, nb)` - Returns Cg matrix (nb x ng)

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-matpower-parser/scripts')
from utils import (load_matpower_json, create_bus_mappings, find_slack_bus,
                   parse_generators, parse_branches, parse_gencost,
                   compute_network_matrices, modify_branch_rate,
                   get_load_vector, get_gen_bus_matrix)

data = load_matpower_json('network.json')
ext2int, int2ext = create_bus_mappings(data['bus'])
slack = find_slack_bus(data['bus'])
gens = parse_generators(data['gen'], ext2int)
branches = parse_branches(data['branch'], ext2int)
costs = parse_gencost(data['gencost'])
matrices = compute_network_matrices(data['bus'], branches, ext2int, slack)
load_p = get_load_vector(data['bus'], len(data['bus']))
```
