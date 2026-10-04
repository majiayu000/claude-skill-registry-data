---
name: evo-mesh-geometry-analysis
description: Performs connected component analysis on triangle meshes using BFS with vertex adjacency and computes mesh volume via the signed tetrahedron method. Handles unit conversion and mass calculation.
---

# evo-mesh-geometry-analysis

Mesh topology and volume computation.

## Key Functions

- `get_largest_connected_component(triangles, rounding_decimals=4)` - Find largest connected component via vertex-based BFS adjacency with 4-decimal quantization
- `compute_mesh_volume(triangles)` - Volume via signed tetrahedron method: abs(sum(v1.(v2×v3)))/6.0
- `convert_volume_mm3_to_cm3(volume_mm3)` - Divide by 1000
- `calculate_mass(volume_cm3, density_g_cm3)` - Mass = Volume × Density

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-mesh-geometry-analysis/scripts')
from utils import get_largest_connected_component, compute_mesh_volume, convert_volume_mm3_to_cm3, calculate_mass

largest = get_largest_connected_component(triangles)
vol_mm3 = compute_mesh_volume(largest)
vol_cm3 = convert_volume_mm3_to_cm3(vol_mm3)
mass = calculate_mass(vol_cm3, density)
```

## Critical Details
- Vertex quantization: 4 decimal places
- Adjacency: vertex-based (share ANY vertex = connected)
- Volume formula: V = abs(Σ v1·(v2×v3)) / 6.0
- Unit conversion: mm³ / 1000 = cm³
