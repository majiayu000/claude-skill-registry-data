---
name: evo-stl-binary-parser
description: Parses binary STL files using Python's struct module, extracting triangle vertices, normals, and the 2-byte attribute byte count (used as Material ID). Provides filtering by Material ID and density table parsing.
---

# evo-stl-binary-parser

Parses binary STL files and material density tables.

## Key Functions

- `parse_binary_stl(filepath)` - Parse binary STL, returns list of (v1, v2, v3, material_id) tuples
- `parse_material_density_table(filepath)` - Parse markdown density table, returns {id: density} dict
- `filter_facets_by_material_id(triangles, material_id)` - Filter triangles by material
- `detect_material_id(triangles)` - Find dominant material ID (excluding debris ID=1)
- `lookup_density(material_id, density_table=None)` - Look up density from table

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-stl-binary-parser/scripts')
from utils import parse_binary_stl, parse_material_density_table, lookup_density

triangles = parse_binary_stl('/root/scan_data.stl')
density_table = parse_material_density_table('/root/material_density_table.md')
```

## Binary STL Layout
- 80 bytes header, 4 bytes uint32 count, N x 50-byte facet records
- Each facet: 12 bytes normal + 36 bytes vertices + 2 bytes attribute (Material ID)
- Format string: '<12fH' (little-endian)
- data[3:6]=v1, data[6:9]=v2, data[9:12]=v3, data[12]=attribute
