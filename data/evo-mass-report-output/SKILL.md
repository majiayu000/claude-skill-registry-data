---
name: evo-mass-report-output
description: Orchestrates the full pipeline from STL parsing to JSON mass report output. Coordinates parsing, component analysis, volume computation, unit conversion, and mass calculation.
---

# evo-mass-report-output

End-to-end pipeline orchestrator for mass calculation from binary STL files.

## Pipeline
1. Parse binary STL -> triangles with material IDs
2. Find largest connected component (vertex-based adjacency, 4-decimal quantization)
3. Extract Material ID from first triangle of largest component
4. Look up density from material density table
5. Compute volume (mm³) using signed tetrahedron method
6. Convert mm³ to cm³ (divide by 1000)
7. Mass = volume_cm³ × density_g/cm³
8. Round to 2 decimal places
9. Write JSON: {"main_part_mass": X.XX, "material_id": N}

## Key Functions
- `run_mass_calculation_pipeline(stl_path, density_table_path, output_path)` - Full pipeline
- `write_mass_report_json(filepath, result)` - Write JSON output

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-stl-binary-parser/scripts')
import utils as stl_parser
sys.path.insert(0, '/app/environment/skills/evo-mesh-geometry-analysis/scripts')
import utils as mesh_analysis
import importlib
importlib.reload(mesh_analysis)

triangles = stl_parser.parse_binary_stl('/root/scan_data.stl')
largest = mesh_analysis.get_largest_connected_component(triangles)
material_id = largest[0][3]
density = stl_parser.lookup_density(material_id)
vol_mm3 = mesh_analysis.compute_mesh_volume(largest)
vol_cm3 = mesh_analysis.convert_volume_mm3_to_cm3(vol_mm3)
mass = round(mesh_analysis.calculate_mass(vol_cm3, density), 2)
```
