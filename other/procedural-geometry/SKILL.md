---
name: procedural-geometry
description: Create realistic procedural Three.js geometry for large engineered environments. Use for trains, tracks, stations, buildings, bridges, pipes, infrastructure, vehicles, structures, and other 3D geometry generated from code.
---

# Procedural Geometry for Engineered Environments

Target: Three.js 0.187.0, WebGPU renderer (`three/webgpu`) and TSL node materials (`three/tsl`); WebGPU only, no WebGL fallback, no GLSL strings.

## Purpose

Create realistic, high-quality 3D geometry for engineered environments (vehicles, tracks, stations, buildings, bridges, pipes and infrastructure) using Three.js procedural geometry.

All geometry must be generated procedurally from JavaScript and Three.js geometry. Do not use GLB, GLTF, FBX, OBJ, CAD imports, downloaded meshes, or other pre-made 3D assets unless explicitly requested.

The objective is **believable manufactured geometry**, not generic "sci-fi" decoration and not low-poly abstraction.

The environment should feel like a functioning, enormous engineered place designed for humans.

---

# Core Modelling Vocabulary

Build everything from a small set of named operations: sweep, loft, revolve, extrude, fillet, bevel, inset, shell, panel gaps, curvature continuity, hard-surface topology, radial profiles, edge and support loops, normal continuity, silhouette fidelity and manufacturing logic. `references/modelling-vocabulary.md` defines each one, when to use it and what it must produce. Read it before constructing any new geometry.

---

# Large Engineered Environments

A station, an industrial district, a city or a ship is one engineered system, not a collection of unrelated futuristic buildings.

Everything should appear to exist within a coherent infrastructure. It should have:

* transportation infrastructure
* structural infrastructure
* utilities
* maintenance access
* drainage
* ventilation
* power distribution
* water distribution
* communications
* emergency systems
* pedestrian infrastructure
* service infrastructure
* residential, commercial and industrial areas

Whenever appropriate, incorporate:

* utility corridors
* service ducts
* cable trays
* maintenance walkways
* inspection panels
* structural rings or frames
* expansion joints
* access hatches

Infrastructure should reinforce the scale of the place. It should feel as though thousands or millions of people could actually live or work there.

---

# Scale

Use real-world dimensions.

Prefer metres.

Maintain consistent scale between:

* people
* trains
* tracks
* doors
* stairs
* buildings
* roads
* pipes
* bridges
* vehicles
* structural members

Avoid arbitrary scale.

Whenever an object has an obvious human reference, use it.

Examples:

* door
* staircase
* handrail
* train door
* platform
* window
* container
* vehicle
* walkway

---

# Futuristic Does Not Mean Decorative

Avoid generic sci-fi design language such as:

* random glowing strips
* arbitrary circular details
* meaningless panels
* excessive greebles
* random antennas
* decorative pipes going nowhere
* impossible structures
* arbitrary neon
* unexplained mechanical components

Futuristic design should come primarily from:

* advanced manufacturing
* efficient structures
* modular construction
* sophisticated infrastructure
* compact machinery
* clean materials
* automation
* maintenance systems
* integrated utilities
* large-scale engineering

Technology should be implied by the construction.

---

# Structural Believability

Large structures must appear capable of supporting themselves.

For:

* bridges
* elevated tracks
* stations
* buildings
* platforms
* parapets
* towers
* large roofs

show believable structural paths.

Use:

* beams
* columns
* trusses
* braces
* support plates
* foundations
* joints
* expansion sections

Do not allow large structures to appear to float without explanation.

---

# Object Catalogue

Per-object rules for trains, railway tracks, train stations, stairs, parapets and guardrails, houses, containers, buildings (primary, secondary and tertiary structure), pipes, wires and cables, bridges and bridge supports are in `references/objects.md`. Read the section for the thing being built.

---

# Repetition

Use procedural repetition for:

* windows
* sleepers
* bolts
* lights
* panels
* structural members
* railings
* pipes
* facade modules

Do not manually duplicate identical geometry. Draw repeated parts as `InstancedMesh` instances of one geometry.

However, introduce controlled variation where appropriate.

Perfect repetition everywhere can make the environment feel artificial.

---

# Geometry Quality

The generated geometry must:

* use BufferGeometry
* have valid positions
* have valid indices
* have correct normals
* avoid degenerate triangles
* avoid unnecessary geometry
* avoid accidental intersections
* avoid z-fighting
* avoid broken topology
* maintain consistent winding
* maintain consistent scale

Use flat shading where the physical surface should be faceted.

Use smooth shading where the physical surface should be smooth.

Do not use smooth shading to hide bad topology.

---

# Polygon Distribution

Spend polygons where they affect the image.

High polygon density is justified for:

* silhouettes
* curved bodywork
* close-up mechanical components
* wheels
* pipes with visible bends
* rounded corners

Low polygon density is acceptable for:

* hidden surfaces
* flat structural panels
* distant components
* simple internal geometry

Never equate polygon count with quality.

---

# Materials

Geometry and materials should remain conceptually separate.

Geometry should describe physical surfaces.

Materials should describe:

* painted metal
* bare metal
* aluminium
* glass
* rubber
* concrete
* ceramic
* plastic
* composite materials

Material boundaries should correspond to actual physical components.

---

# Scale-Aware Detail

Small details must make sense relative to the object's scale.

Do not add bolts that are too small to see.

Do not make panel gaps enormous.

Do not use identical bevel sizes on a train and a tiny electronic component.

Geometry should be proportional to the object.

---

# Procedural API

Prefer reusable procedural functions such as:

```js
createSweep();
createLoft();
createRevolve();
createExtrusion();
createRoundedBox();
createPipe();
createCable();
createRail();
createWheel();
createPanel();
createDoor();
createWindow();
createStair();
createHandrail();
createBeam();
createColumn();
createBracket();
createFlange();
createValve();
createBogie();
createTrainBody();
```

Build complex objects from these reusable concepts rather than writing unrelated geometry generators for every model.

A sweep, with its segment count as the level-of-detail knob:

```js
import * as THREE from 'three/webgpu';

// profile: THREE.Shape in the path's normal/binormal plane; path: a THREE.Curve
export function createSweep(profile, path, { steps = 64 } = {}) {
  const geo = new THREE.ExtrudeGeometry(profile, { steps, bevelEnabled: false, extrudePath: path });
  geo.computeVertexNormals();
  return geo;
}

// a rail head (simplified profile) along a gentle curve, 40 m long
const head = new THREE.Shape([[-0.035, 0], [0.035, 0], [0.035, 0.04], [0.02, 0.06], [-0.02, 0.06], [-0.035, 0.04]]
  .map(([x, y]) => new THREE.Vector2(x, y)));
const path = new THREE.CatmullRomCurve3([new THREE.Vector3(0, 0, 0), new THREE.Vector3(20, 0, 2), new THREE.Vector3(40, 0, 8)]);
const rail = new THREE.Mesh(createSweep(head, path, { steps: 80 }),
  new THREE.MeshStandardNodeMaterial({ color: 0x8a8d90, metalness: 0.9, roughness: 0.35 }));
```

---

# Model Hierarchy

Prefer meaningful groups:

```text
Train
├── Body
├── Windows
├── Doors
├── Bogies
│   ├── Wheels
│   ├── Axles
│   └── Suspension
├── RoofEquipment
└── Undercarriage
```

Objects should remain independently addressable where practical.

This allows later animation, replacement, LOD generation and material changes.

---

# Animation Readiness

Where appropriate, structure geometry so that obvious moving components can later be animated.

Examples:

* train doors
* wheels
* switches
* valves
* fans
* elevators
* station doors
* mechanical arms

Do not bake moving parts into a single inseparable mesh.

---

# LOD

If practical, generate different levels of detail from the same procedural definition.

The LOD system should reduce:

* segment counts
* small components
* hidden geometry
* tiny bevels

without changing the fundamental silhouette.

Never create separate unrelated models merely for LOD.

---

# Quality Priority

Always prioritize in this order:

1. Correct proportions
2. Silhouette
3. Large-scale curvature
4. Structural plausibility
5. Physical construction
6. Surface transitions
7. Major functional components
8. Material boundaries
9. Medium-scale details
10. Small details

Never sacrifice the first six merely to add more detail.

---

# Final Rule

Before adding another detail, ask:

**"Would this exist on the real object, and does its geometry explain why it exists?"**

If yes, model it.

If no, do not add it merely because it makes the object look more "sci-fi".

The target is:

**real engineering, imagined technology.**

Not:

**real-world object + random sci-fi decorations.**
