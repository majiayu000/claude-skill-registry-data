---
name: evo-threejs-scene-parser
description: Parse a Three.js createScene() file in headless Node.js, identify part-level structure (Groups and standalone Meshes), and export OBJ files for both individual sub-meshes per part and merged part assemblies (links). Use when extracting decomposed 3D object structure from Three.js scene definitions.
---

# evo-threejs-scene-parser

Parses a Three.js scene file (one that exports a `createScene()` function) using a headless Node.js runtime, then exports each part as Wavefront OBJ files in two views:

- `part_meshes/<part_name>/<mesh_name>.obj` — one OBJ per direct child Mesh of each Group
- `links/<part_name>.obj` — merged OBJ of all direct child meshes of the Group (NOT nested sub-group descendants)

## Output Layout
```
output/
├── part_meshes/
│   ├── <part_name>/<mesh_name>.obj  # one per direct child Mesh
│   └── ...
└── links/
    ├── <part_name>.obj  # merged direct child meshes only
    └── ...
```

## Part Identification Rules
1. A "part" is ANY `THREE.Group` found anywhere in the scene tree (excluding the root). Use `root.traverse()` and collect `node.isGroup`.
2. Standalone Meshes that are direct children of the root (not inside any Group) are also exported as their own part.
3. For each Group:
   - Direct child Meshes go to `part_meshes/<group.name>/<mesh.name>.obj`
   - Direct child Meshes are merged (with world transforms baked) → `links/<group.name>.obj`
   - Nested sub-groups are treated as SEPARATE parts (not included in parent's link)
4. `root.updateMatrixWorld(true)` MUST be called before export so world matrices are baked.
5. Use `node.name` for naming; fallback `UnnamedGroup_<i>` / `UnnamedMesh_<i>`.
6. For merging: clone geometries, apply matrixWorld, convert indexed→non-indexed, strip non-essential attributes (keep only position+normal), then use mergeGeometries().

## Usage (Python)
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-threejs-scene-parser/scripts')
from run import run_threejs_parser
result = run_threejs_parser('/root/data/object.js', '/root/output')
print(result)
```

## Usage (CLI)
```bash
cd /root && node /app/environment/skills/evo-threejs-scene-parser/scripts/parser.mjs /root/data/object.js /root/output
```

## Key Implementation Notes
- Polyfill `global.self`, `global.window`, `global.document` for headless Three.js addons.
- Import paths: `three`, `three/examples/jsm/exporters/OBJExporter.js`, `three/examples/jsm/utils/BufferGeometryUtils.js`.
- Three.js v0.170.0: use `mergeGeometries` (not `mergeBufferGeometries`), `BufferGeometry` only.
- Sanitize file names with `[^A-Za-z0-9_.-]+` → `_`.
- For links: merge only DIRECT child meshes of each group, not descendants from nested sub-groups.
