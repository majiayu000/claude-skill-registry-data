---
name: evo-threejs-to-obj
description: Convert Three.js scene graphs to Wavefront OBJ format suitable for Blender (Z-up coordinate system). Handles InstancedMesh, nested hierarchies, coordinate transforms, and headless Node.js execution.
---

# evo-threejs-to-obj

## Purpose
Convert Three.js scene graphs to Wavefront OBJ format suitable for Blender (Z-up coordinate system).

## Key Domain Knowledge

### Coordinate System Conversion
- Three.js: Y-up, -Z forward, right-handed
- Blender: Z-up, -Y forward, right-handed
- Apply -90° X rotation: X→X, Y→Z, Z→-Y
- Rotation matrix Rx(-90°): [[1,0,0],[0,0,1],[0,-1,0]]
- Applied AFTER world transform baking, BEFORE writing OBJ

### Pipeline (per geometry)
1. Clone source BufferGeometry
2. Apply node's world matrix (or composed world*instance matrix for InstancedMesh)
3. Apply -90° X rotation for Y-up to Z-up conversion
4. Collect transformed geometry

### InstancedMesh Handling
- Each instance has a per-instance 4x4 matrix
- Final transform: mesh.matrixWorld * instanceMatrix[i]
- Must export each instance as separate geometry
- Standard OBJExporter does NOT handle InstancedMesh - manual traversal required

### Non-Uniform/Negative Scales
- Apply full world matrix directly (don't decompose to pos/rot/scale)
- Negative scale flips winding order
- Decomposition loses shear from nested non-uniform scales

### Geometry Preparation for Merging
- Convert indexed geometries to non-indexed (toNonIndexed())
- Compute vertex normals if missing (computeVertexNormals())
- Remove extra attributes (UV, etc.) to ensure homogeneous attribute sets
- Keep only 'position' and 'normal' attributes
- Merge all into single BufferGeometry using mergeGeometries()

### OBJ Export Strategy
- Manual traversal with per-geometry transform baking (most reliable)
- Merge all geometries into single Mesh
- Pass single Mesh to OBJExporter (avoids exporter's limited traversal)

### World Matrix Update
- MUST call root.updateMatrixWorld(true) before reading any world matrices
- Without this, child nodes carry identity/stale matrices (DR ref: cite 17, 18, 20, 21)

### Scene Module Loading
- The input object.js may export via different patterns:
  - `export default function createScene()` or similar named export
  - `export function createScene()`
  - May return a Mesh, Group, Scene, or Object3D
- Must handle all common export patterns robustly

## Usage

IMPORTANT: The script must be run from a directory that has `three` in its
node_modules (e.g., /root/ if that's where package.json and node_modules are).
The script uses ES module imports so the project needs `"type": "module"` in package.json.

```bash
# Copy script to project root and run:
cp /app/environment/skills/evo-threejs-to-obj/scripts/convert.mjs /root/convert.mjs
cd /root && node convert.mjs /root/data/object.js /root/output/object.obj
```

## Files
- `scripts/convert.mjs` - Main conversion script. Takes input Three.js file path and output OBJ path as CLI arguments.

## Expected Output
For a typical scene:
- Collects all mesh geometries (including InstancedMesh instances)
- Merges into single geometry
- Applies Y-up to Z-up coordinate conversion
- Writes valid Wavefront OBJ file

## Troubleshooting
- If output appears rotated in Blender: verify the -90° X rotation is being applied
- If output is empty: check that the scene module exports a function that returns Object3D hierarchy
- If merge fails: likely attribute mismatch — the script strips all attributes except position/normal
- If "Cannot find module 'three'": run from directory with node_modules containing three