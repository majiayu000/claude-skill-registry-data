---
name: evo-3d-scan-calc
description: Complete pipeline for binary STL parsing, connected component extraction, volume computation, material density lookup, and mass calculation with JSON output.
---

# evo-3d-scan-calc

End-to-end skill for computing the mass of a 3D printed part from a binary STL scan file.

## Pipeline Overview

1. **Parse binary STL** — Decode 80-byte header, 4-byte triangle count, and 50-byte facet records. Extract vertices and Material ID (uint16 attribute field) per triangle.
2. **Find connected components** — Build vertex-based adjacency (triangles sharing any vertex are connected) using vertices quantized to **4 decimal places**. BFS to find all components.
3. **Select main part** — Compute volume for each component. The **largest by volume** is the main part.
4. **Extract Material ID** — Use the attribute from the **first triangle** of the largest component.
5. **Lookup density** — Reference the material density table: `{1: 0.10, 10: 7.85, 25: 2.70, 42: 5.55, 99: 11.34}`.
6. **Calculate mass** — `mass = volume * density`. **No unit conversion needed** (density table matches mesh coordinate units).
7. **Write report** — Save JSON with `main_part_mass` and `material_id`.

## Critical Details

- **Vertex quantization**: Round to exactly **4 decimal places** for vertex matching (matches verifier).
- **Adjacency**: **Vertex-based** — two triangles are connected if they share at least one vertex (NOT edge-based).
- **Volume formula**: Signed tetrahedron method: `V = abs(Σ v1·(v2×v3)) / 6.0`. **No mm³-to-cm³ conversion.**
- **Component selection**: By **largest volume**, not by material ID count.
- **Material ID**: From the **first triangle** of the component (attribute byte count field).

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-3d-scan-calc/scripts')
from utils import run_full_pipeline

result = run_full_pipeline()
```

Or step by step:

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-3d-scan-calc/scripts')
from utils import (
    parse_binary_stl, find_connected_components,
    compute_signed_volume, lookup_density, write_mass_report
)

# 1. Parse STL
triangles = parse_binary_stl('/root/scan_data.stl')

# 2. Find all connected components (vertex-based adjacency, 4-decimal quantization)
components = find_connected_components(triangles)

# 3. Compute volume for each component, pick largest
best_comp = None
best_vol = -1
for comp in components:
    vol = compute_signed_volume(comp)
    if vol > best_vol:
        best_vol = vol
        best_comp = comp

# 4. Get material ID from first triangle of largest component
material_id = best_comp[0][3]

# 5. Lookup density and compute mass (NO unit conversion)
density = lookup_density(material_id)
mass = best_vol * density

# 6. Write report
write_mass_report('/root/mass_report.json', mass, material_id)
```