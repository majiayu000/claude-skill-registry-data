---
name: evo-civ6-map-parser
description: Parses .Civ6Map SQLite database files to extract map dimensions, terrain, features, resources, and river edge data. Provides hex coordinate utilities for odd-r pointy-top hex grid.
---

# evo-civ6-map-parser

Parses Civilization VI .Civ6Map files (SQLite databases) and provides hex grid utilities.

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-civ6-map-parser/scripts')
from utils import parse_civ6map, get_hex_neighbors, hex_distance, is_land_tile, is_mountain, is_tile_river_adjacent, get_land_tiles

map_data = parse_civ6map('/path/to/map.Civ6Map')
neighbors = get_hex_neighbors(5, 3)
dist = hex_distance(0, 0, 3, 3)
```

## Key Functions

- `parse_civ6map(db_path)` - Returns dict with width, height, tiles, rivers
- `offset_to_cube(col, row)` - Odd-R offset to cube coords
- `cube_to_offset(q, r, s)` - Cube to odd-R offset coords  
- `get_hex_neighbors(x, y)` - Get 6 neighboring tile coordinates
- `hex_distance(x1, y1, x2, y2)` - Hex distance between tiles
- `is_tile_river_adjacent(map_data, x, y)` - Check if tile touches a river
- `is_land_tile(map_data, x, y)` - Check if tile is land
- `is_mountain(map_data, x, y)` - Check if tile is a mountain
- `get_land_tiles(map_data)` - Get all land tile coordinates
