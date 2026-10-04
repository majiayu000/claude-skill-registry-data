---
name: evo-threejs-obj-export
description: Generates a Node.js ES module script that dynamically imports a Three.js object definition file, constructs a scene graph, applies a -90 deg X-rotation for Y-up to Z-up coordinate conversion (Blender compatibility), forces world matrix updates, serializes the scene to Wavefront OBJ format using OBJExporter, and writes the result to disk.
---

# evo-threejs-obj-export

## Purpose
Convert Three.js scene definitions (ES module files exporting geometry constructors) into Wavefront OBJ files suitable for import into Blender (Z-up coordinate system).

## Key Concepts

### Pipeline Steps
1. **Dynamic Import**: Load the Three.js object definition file using `await import(filePath)`
2. **Scene Construction**: Call the exported function (e.g., `createScene()`) to get the 3D object hierarchy
3. **Coordinate Transform**: Apply +90° (Math.PI/2) X-rotation to convert Y-up (Three.js) to Z-up (Blender)
4. **Matrix Baking**: Call `scene.updateMatrixWorld(true)` — CRITICAL in headless Node.js (no renderer to auto-update)
5. **OBJ Export**: Use `OBJExporter.parse(scene)` to serialize to OBJ string
6. **File I/O**: Write the OBJ string to disk with `fs.writeFileSync`

### Critical Details
- Three.js v0.175.0 is an ES Module — requires `"type": "module"` in package.json
- Import Three.js: `import * as THREE from 'three'`
- Import OBJExporter: `import { OBJExporter } from 'three/addons/exporters/OBJExporter.js'`
- The rotation is applied to a wrapper Group containing the imported object, NOT to individual geometries
- `updateMatrixWorld(true)` must be called AFTER setting rotation but BEFORE parsing
- The OBJExporter reads `.matrixWorld` during traversal — without explicit update, transforms are ignored
- Object.js files may export named functions like `createScene()` — check module exports dynamically

### Coordinate Transform Math
Rotation matrix Rx(-π/2) maps:
- Y-up → Z-up: (x, y, z) → (x, z, -y)
- This is the standard Three.js-to-Blender conversion

## Utility Functions

### `generate_export_script(inputPath, outputPath)`
Generates the content of a Node.js ES module script as a string.

**Usage from Node.js:**
```javascript
import { generate_export_script } from './scripts/generate_export_script.mjs';
const scriptContent = generate_export_script('/root/data/object.js', '/root/output/object.obj');
```

### `create_obj_export_node_script(inputPath, outputPath, scriptOutputPath)`
Generates AND writes the export script to disk, then optionally executes it.

**Usage from Node.js:**
```javascript
import { create_obj_export_node_script } from './scripts/generate_export_script.mjs';
await create_obj_export_node_script('/root/data/object.js', '/root/output/object.obj', '/root/export_runner.mjs');
```

## Direct Execution
The skill also provides a ready-to-run export script:
```bash
node /app/environment/skills/evo-threejs-obj-export/scripts/run_export.mjs /root/data/object.js /root/output/object.obj
```
