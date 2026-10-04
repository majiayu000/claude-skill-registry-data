---
name: evo-civ6-adjacency-rules
description: Encodes all Civ6 Gathering Storm district adjacency bonus rules, placement validity, population limits, and civ-specific modifiers.
---

# evo-civ6-adjacency-rules

Computes adjacency bonuses for Civ6 districts.

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-civ6-adjacency-rules/scripts')
from utils import calculate_adjacency_bonus, is_valid_district_placement, max_specialty_districts, is_valid_city_center

bonus = calculate_adjacency_bonus(map_data, x, y, 'CAMPUS', placements, 'GENERIC')
valid = is_valid_district_placement(map_data, x, y, 'CAMPUS', city_center, placed_tiles)
max_d = max_specialty_districts(population)
```

## Key Functions

- `calculate_adjacency_bonus(map_data, x, y, district_type, placements, civ)` - Compute adjacency bonus
- `is_valid_district_placement(map_data, x, y, district_type, city_center, placed_tiles)` - Check placement validity
- `is_valid_city_center(map_data, x, y)` - Check city center validity
- `max_specialty_districts(population)` - Population to district cap
- `is_specialty_district(district_type)` - Check if specialty
- `get_available_district_types()` - List placeable district types
