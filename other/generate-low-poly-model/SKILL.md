---
name: generate-low-poly-model
description: Generate procedural low-poly 3D models with Three.js and export them as glTF or GLB assets. Use when Codex needs to create browser-previewable low-poly props, terrain, rocks, trees, buildings, vehicles, collectibles, or simple game assets with flat shading, simple geometry, materials, export controls, and validation guidance.
---

# Skill: Generate Low-Poly 3D Models with Three.js and Export to glTF/GLB

## Purpose

Use this skill to procedurally create low-poly 3D models in JavaScript with Three.js, preview them in a browser, and export them as glTF 2.0 assets, preferably binary `.glb` files for portability.

This skill is best for:

- Low-poly props, terrain, rocks, trees, buildings, vehicles, icons, collectibles, and simple creatures.
- Procedural generation from dimensions, seed values, or high-level art direction.
- Browser-based previews and downloadable `.glb` exports.

This skill is not ideal for:

- Production character topology, rigging, skeletal animation, complex UV unwrapping, or photorealistic assets.
- Dense sculpted models that should be authored in Blender or a DCC tool.

## Core Tools

### Runtime and rendering

- `three`: main rendering and geometry library.
- `three/addons/exporters/GLTFExporter.js`: exports `THREE.Scene`, `THREE.Object3D`, or mesh collections to glTF 2.0.
- `three/addons/controls/OrbitControls.js`: browser preview camera control.
- Optional: `lil-gui` for procedural parameters.
- Optional: `seedrandom` or a custom deterministic RNG for repeatable model generation.

### Validation and inspection

- Khronos glTF Validator: validate exported `.gltf` or `.glb` files.
- Blender: inspect scale, normals, materials, hierarchy, and compatibility.
- Three.js `GLTFLoader`: re-load the exported file into a clean scene as a smoke test.

## Recommended Project Structure

```text
low-poly-generator/
  package.json
  index.html
  src/
    main.js
    modelFactory.js
    exportGLB.js
    materials.js
    geometryUtils.js
  exports/
```

## Bundled Procedural Scripts

Use `scripts/procedural-low-poly-models.js` when a request asks for animals, humans, vegetation, or reusable game props. Copy or import the script into the target Three.js project, then call the fixed factory that matches the requested species or object.

The script exports:

- `LOW_POLY_SPECIES`: category map for animal, human, and object families.
- `LOW_POLY_FACTORIES`: registry of named factories.
- `createLowPolyModel(THREE, kind, params)`: dispatch helper for dynamic model selection.
- Animal factories: `createLowPolyDog`, `createLowPolyCat`, `createLowPolyHorse`, `createLowPolyDeer`, `createLowPolyGoat`, `createLowPolyTiger`, `createLowPolyBear`, `createLowPolyPanda`, `createLowPolyMonkey`, `createLowPolyBird`, `createLowPolyChicken`, `createLowPolyFish`.
- Human factories: `createLowPolyHuman`, `createLowPolyChild`, `createLowPolyWorker`, `createLowPolyAdventurer`, `createLowPolyRobot`.
- Object factories: `createLowPolyOakTree`, `createLowPolyPineTree`, `createLowPolyPalmTree`, `createLowPolyFlower`, `createLowPolyGrassClump`, `createLowPolyBush`, `createLowPolyRock`, `createLowPolyCrate`, `createLowPolyBarrel`, `createLowPolyMushroom`.

Each factory accepts `(THREE, params = {})`, returns a named `THREE.Group`, stores the resolved parameters in `group.userData.procedural`, keeps the origin near bottom-center, and uses export-friendly low-poly primitives. Prefer these factories over ad hoc modeling when the requested asset matches one of the supported categories.

If the requested species or object is not bundled, use the closest bundled procedural as a body-plan reference and create a new local procedural file or factory for the target asset. Keep the same conventions: pass `THREE` explicitly, accept a `params` object, return a named `THREE.Group`, use low-segment primitives with flat `MeshStandardMaterial`, place the origin near bottom-center, name important child meshes, and store generation metadata in `group.userData.procedural`.

Example:

```js
import * as THREE from 'three';
import {
  createLowPolyDog,
  createLowPolyHuman,
  createLowPolyOakTree,
} from './procedural-low-poly-models.js';

scene.add(createLowPolyDog(THREE, {
  scale: 1.2,
  bodyColor: 0x9b6a3c,
  tail: 'upright',
}));

scene.add(createLowPolyHuman(THREE, {
  height: 1.7,
  build: 'slim',
  shirtColor: 0x3f6fb5,
  tool: 'sword',
}));

scene.add(createLowPolyOakTree(THREE, {
  height: 2.8,
  crownRadius: 0.9,
}));
```

## Installation

```bash
npm create vite@latest low-poly-generator -- --template vanilla
cd low-poly-generator
npm install three
npm run dev
```

## Low-Poly Modeling Principles

1. Prefer simple primitives and custom `BufferGeometry`.
2. Use flat shading, hard edges, and faceted normals.
3. Keep silhouettes readable from a distance.
4. Use a limited material palette.
5. Model with real scale in mind: use meters as the default unit.
6. Keep transforms clean before export: sensible pivots, object names, and hierarchy.
7. Avoid unnecessary textures. Vertex colors or simple materials often suit low-poly style better.
8. Use instancing for preview performance, but convert to exportable meshes if the target pipeline needs ordinary mesh nodes.

## Geometry Guidelines

### Use built-in geometry when possible

Good low-poly starting points:

```js
new THREE.BoxGeometry(width, height, depth);
new THREE.ConeGeometry(radius, height, radialSegments);
new THREE.CylinderGeometry(radiusTop, radiusBottom, height, radialSegments);
new THREE.IcosahedronGeometry(radius, detail);
new THREE.DodecahedronGeometry(radius, detail);
new THREE.PlaneGeometry(width, height, segmentsX, segmentsY);
```

Use low segment counts:

```js
const trunk = new THREE.CylinderGeometry(0.18, 0.24, 1.4, 6);
const rock = new THREE.IcosahedronGeometry(0.5, 0);
const treeTop = new THREE.ConeGeometry(0.9, 1.5, 7);
```

### Force faceted shading

```js
geometry.computeVertexNormals();
const material = new THREE.MeshStandardMaterial({
  color: 0x6fa35f,
  roughness: 0.85,
  metalness: 0.0,
  flatShading: true,
});
```

For generated geometries, call:

```js
geometry.computeVertexNormals();
geometry.computeBoundingBox();
geometry.computeBoundingSphere();
```

### Custom `BufferGeometry` pattern

```js
function createPyramidGeometry(width = 1, height = 1) {
  const hw = width / 2;

  const vertices = new Float32Array([
    // base
    -hw, 0, -hw,   hw, 0, -hw,   hw, 0, hw,
    -hw, 0, -hw,   hw, 0, hw,   -hw, 0, hw,

    // sides, duplicated per face for hard normals
    -hw, 0, -hw,   hw, 0, -hw,   0, height, 0,
     hw, 0, -hw,   hw, 0,  hw,   0, height, 0,
     hw, 0,  hw,  -hw, 0,  hw,   0, height, 0,
    -hw, 0,  hw,  -hw, 0, -hw,   0, height, 0,
  ]);

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
  geometry.computeVertexNormals();
  return geometry;
}
```

Duplicate vertices per face when you want crisp facets. Shared vertices produce smoother normals unless hard edges are otherwise encoded.

## Materials

Use `MeshStandardMaterial` for broad compatibility with glTF export.

```js
export const palette = {
  grass: new THREE.MeshStandardMaterial({ color: 0x5d9c59, roughness: 0.9, flatShading: true }),
  bark: new THREE.MeshStandardMaterial({ color: 0x7a4f2a, roughness: 0.95, flatShading: true }),
  stone: new THREE.MeshStandardMaterial({ color: 0x8a8f98, roughness: 0.9, flatShading: true }),
};
```

Avoid procedural shader materials when exporting to glTF, unless baking is part of the workflow. glTF export works most predictably with standard PBR materials.

## Scene Assembly Pattern

Create models as `THREE.Group` objects with named child meshes.

```js
function createLowPolyTree() {
  const group = new THREE.Group();
  group.name = 'LowPolyTree';

  const trunk = new THREE.Mesh(
    new THREE.CylinderGeometry(0.16, 0.22, 1.2, 6),
    palette.bark
  );
  trunk.name = 'Trunk';
  trunk.position.y = 0.6;

  const crown = new THREE.Mesh(
    new THREE.ConeGeometry(0.8, 1.4, 7),
    palette.grass
  );
  crown.name = 'Crown';
  crown.position.y = 1.65;

  group.add(trunk, crown);
  return group;
}
```

## Export to GLB

Use `GLTFExporter` with `binary: true` to create a `.glb` file.

```js
import { GLTFExporter } from 'three/addons/exporters/GLTFExporter.js';

export function exportGLB(object3D, filename = 'model.glb') {
  const exporter = new GLTFExporter();

  exporter.parse(
    object3D,
    (result) => {
      const blob = new Blob([result], { type: 'model/gltf-binary' });
      const url = URL.createObjectURL(blob);

      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      link.click();

      URL.revokeObjectURL(url);
    },
    (error) => {
      console.error('GLB export failed:', error);
    },
    {
      binary: true,
      trs: false,
      onlyVisible: true,
      truncateDrawRange: true,
      maxTextureSize: 4096,
    }
  );
}
```

For `.gltf` JSON export, set `binary: false`. Note that `.gltf` may reference separate `.bin` and texture files, while `.glb` packages the asset into one binary file.

## Export Checklist

Before exporting:

- Ensure all meshes are added under one root `Group` or `Scene`.
- Name the root object and important child objects.
- Remove debug helpers, axes, grids, lights, and cameras unless intentionally exporting a whole scene.
- Set `mesh.visible = true` for exportable parts.
- Freeze or normalize transforms when needed.
- Confirm the model origin/pivot is useful, often bottom-center for props and characters.
- Use compatible materials such as `MeshStandardMaterial` or `MeshBasicMaterial`.
- Avoid unsupported runtime-only effects, custom shaders, and post-processing.

After exporting:

- Re-import the `.glb` with `GLTFLoader` in a fresh Three.js scene.
- Validate with Khronos glTF Validator.
- Open in Blender and inspect scale, normals, materials, hierarchy, and origin.
- Check file size and mesh count.

## Re-Import Smoke Test

```js
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
loader.load('/exports/model.glb', (gltf) => {
  scene.add(gltf.scene);
  console.log('Loaded exported model:', gltf.scene);
});
```

## Common Problems and Fixes

### Exported model is smooth instead of faceted

Use `flatShading: true`, duplicate vertices per face for custom geometry, and recompute normals.

### Model exports but looks black

Add lights for preview, use standard materials, and inspect roughness/metalness. For unlit low-poly style, use `MeshBasicMaterial`.

### Custom shader does not export correctly

Replace shader materials with `MeshStandardMaterial` or bake the effect into textures or vertex colors.

### File is too large

Reduce mesh count, merge static meshes, remove unused nodes, simplify geometry, reduce texture size, and prefer shared materials.

### Pivot or scale is wrong in Blender

Use a root group at `(0, 0, 0)`, set model dimensions intentionally, and apply transforms before export when needed.

## Procedural Generation Tips

- Use a seedable RNG for repeatable assets.
- Randomize proportions within constrained ranges.
- Keep generated geometry symmetrical unless variation is intentional.
- Add controlled vertex jitter to rocks, terrain, and foliage.
- Use small rotations and scale variation for natural-looking low-poly clusters.
- Keep a metadata object with generation parameters so assets can be regenerated.

Example deterministic helper:

```js
function mulberry32(seed) {
  return function random() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
```

## Prompting Guidelines for AI Code Generation

When asking an AI coding tool to generate a model, specify:

- Target object and style: “low-poly pine tree”, “faceted sci-fi crate”, “toy-like island”.
- Approximate scale: height, width, or unit assumptions.
- Geometry constraints: max triangles, no textures, number of parts.
- Material palette: named colors, flat shading, roughness.
- Export target: `.glb` using `GLTFExporter`.
- Preview requirements: orbit controls, lights, grid optional.
- Validation expectations: re-import smoke test and no console errors.

Example prompt:

```text
Create a Vite + Three.js app that procedurally generates a low-poly camping tent model.
Use simple BufferGeometry or built-in geometries, flat MeshStandardMaterial colors, named child meshes,
a browser preview with OrbitControls, and an Export GLB button using GLTFExporter.
Keep the model under 1,000 triangles and put the pivot at bottom center.
```

## Minimal Complete Example

```js
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFExporter } from 'three/addons/exporters/GLTFExporter.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf2f5f7);

const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(3, 2.5, 4);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0.8, 0);
controls.update();

scene.add(new THREE.HemisphereLight(0xffffff, 0x777777, 2));

const green = new THREE.MeshStandardMaterial({ color: 0x4f9d5d, roughness: 0.9, flatShading: true });
const brown = new THREE.MeshStandardMaterial({ color: 0x7a4f2a, roughness: 0.95, flatShading: true });

const tree = new THREE.Group();
tree.name = 'LowPolyTree';

const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.22, 1.2, 6), brown);
trunk.name = 'Trunk';
trunk.position.y = 0.6;

const crown = new THREE.Mesh(new THREE.ConeGeometry(0.85, 1.4, 7), green);
crown.name = 'Crown';
crown.position.y = 1.6;

tree.add(trunk, crown);
scene.add(tree);

function exportGLB(object3D, filename = 'low-poly-tree.glb') {
  const exporter = new GLTFExporter();
  exporter.parse(
    object3D,
    (result) => {
      const blob = new Blob([result], { type: 'model/gltf-binary' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      link.click();
      URL.revokeObjectURL(url);
    },
    (error) => console.error(error),
    { binary: true, onlyVisible: true }
  );
}

const button = document.createElement('button');
button.textContent = 'Export GLB';
button.style.position = 'absolute';
button.style.top = '12px';
button.style.left = '12px';
button.onclick = () => exportGLB(tree);
document.body.appendChild(button);

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
animate();
```

## Quality Bar

A generated asset is acceptable when:

- It loads without errors in Three.js after export.
- It validates as glTF 2.0 or has only understood non-blocking warnings.
- It has correct scale, origin, orientation, and naming.
- It uses flat low-poly shading intentionally.
- It has no accidental helper objects, invisible junk meshes, or debug nodes.
- It has a reasonable triangle count for the intended use.

## References

- Three.js `BufferGeometry` represents mesh data through buffered vertex positions, indices, normals, colors, UVs, and custom attributes.
- Three.js `GLTFExporter` exports glTF 2.0 as `.gltf` JSON or binary `.glb`.
- glTF is designed as an efficient runtime transmission format for 3D scenes and models.
- Khronos glTF Validator validates assets against the glTF 2.0 specification and reports issues and asset statistics.
