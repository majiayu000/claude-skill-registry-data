---
name: pipes
description: "Create believable procedural pipework, ducts and conduits in Three.js: mains, branches, bends, flanges, valves, supports and hangers, colour-coded by service. Use for any pipe, duct, cable tray or conduit on a structure, a building, a plant, a ship or a street."
---

# Pipes

Target: Three.js 0.187.0, WebGPU renderer (`three/webgpu`) and TSL node materials (`three/tsl`); WebGPU only, no WebGL fallback, no GLSL strings.

Create pipework that reads as an engineered service, not as decoration. Build it from procedural geometry, drawn through one pipework system (an instanced unit-shape set, below). Do not model each pipe by hand with separate cylinder meshes.

The target is a **working service of a large engineered place**: everything carries something (air, water, coolant, steam, power), goes somewhere, and is supported, joined and maintained.

## Core priorities

1. the route: where the pipe comes from and goes to, along structure
2. support: nothing hangs in the air
3. joints: flanges where lengths meet, bends where it turns
4. clearance: never across a walkway or a door at head height
5. colour: one colour for one service, the same everywhere
6. valves, meters and tags: a few, where someone would need them
7. the small things last

## Vocabulary

- **Main**: a large pipe (0.6 to 3 m across) along a street, a soffit or a rack; **branch**: a smaller pipe off it, at a tee; **stub**: a short branch capped or into a wall.
- **Bend**: a turn of 1.5 diameters' radius on the centreline, never a kink; two bends make an **offset**; an **expansion loop** (a U out and back) every few hundred metres on a long hot main.
- **Flange**: a disc 1.3 diameters across, a third of a diameter thick, with a bolt ring; one at every joint of lengths (every 6 to 12 m on a small pipe, every 60 m on a main) and at every valve.
- **Valve**: a body (a box or a drum a little larger than the pipe) between two flanges, with a hand wheel on a stem for small pipes, or an actuator box for large ones; **meter**: a small box with a dial on a branch.
- **Support**: a pipe on a floor or a roof stands on **saddles** (a cradle on a short post); along a wall it rides on **brackets** (an arm from the wall with a clamp round the pipe); under a soffit it hangs from **hangers** (a rod from above to a clamp); several pipes together lie on a **rack** (a ladder of steel they all rest on). A support every 8 to 12 diameters, and at every bend and valve.
- **Lagging**: a hot or a cold pipe is wrapped: a smooth jacket of a larger diameter with bands every few metres, pale aluminium or dull cladding.
- **Duct**: a rectangular run for air, with stiffening ribs every metre or so, joined by flanged collars, with a louvred grille or a diffuser at its ends.
- **Conduit** and **cable tray**: small round conduits in rows on a wall, clamped every 2 m; trays as ladders or troughs under a soffit, cables lying in them.

## Rules

- Pipes follow structure: along a wall at one height, under a soffit, along the top of a rack, down a column. They turn square (with bends), not on the diagonal, unless a sweep over an obstacle calls for it.
- A pipe meets a surface square and goes into it (a wall, a floor, a machine). It does not stop in the air.
- A pipe never floats: every run has supports, at the spacing above, and the supports reach a surface.
- Decide once where services run (buried, in utility corridors, or exposed) and keep to it. Exposed pipework belongs on structures (plants, machine houses, stations, industrial yards), on the walls and roofs of buildings (downpipes, conduits, air units) and in yards; not strung on poles or from building to building.
- Clearance: 2.3 m over a walkway, floor or platform; nothing across a door or a window; nothing through a vehicle's envelope.
- Colour-code by service, the same everywhere in the scene. Pick one scheme and hold it: industrial practice (BS 1710 and similar) uses green for water, silver-grey for steam, brown for oils, yellow ochre for gases, light blue for air, violet for acids and alkalis, orange for electrical services; a stylised scheme (cream coolant, brick-red steam, brown process, blue-grey water, pale grey air ducts, dark power conduits, dark flanges) works as well if it is consistent. A service's colour is the pipe's paint; the bends and flanges may be bare steel.
- Scale: a main's diameter from 0.6 to 3 m; a branch from 0.15 to 0.5 m; a conduit 0.05 to 0.1 m; a duct 0.4 to 2 m on a side. Bend radius 1.5 diameters. Flange 1.3 diameters across.
- Materials (the `metal`, `paint` and `rust` skills): painted steel for mains, galvanised or stainless for small pipes and conduits, aluminium jackets on lagging; rust only where water runs (wet industry, outdoors), not in a clean plant.
- Futuristic, not Victorian: smooth jackets, cast fittings with rounded corners, flush clamps, actuators and sensor boxes rather than big hand wheels, a line of light or a status lamp at a valve where it helps; no bare rivets, no gate valves with great wheels.
- Nothing flat laid on a floor as a sheet; marks are drawn in shaders. Signs and tags are the `signage` skill's job.

## Performance

- Every pipe, bend, flange, valve and support is an instance of a unit shape: a whole district's pipework is a few draw calls.
- A straight length is one instance scaled to its length and radius; a bend one torus instance; a flange one short wide cylinder.
- Pipes with a radius under 0.15 m are drawn with 8 sides, under 0.5 m with 12, larger with 24.
- Nothing is drawn twice: a bend replaces the corner of the two straights it joins (shorten each straight by the bend radius).
- Collision: register mains and anything a walker could reach as solid (a capsule per straight in the collision registry); conduits and small pipes high on a wall are not.

## A pipework system on an instanced unit-shape set

Keep one set of unit shapes and one `InstancedMesh` per shape, service and side count. A **pipe** is a unit cylinder along z (radius 1, length 1) scaled to the length and the radius; a **bend** is a quarter torus of bend radius 3 and tube radius 1 (1.5 diameters), scaled uniformly by the pipe's radius; a **flange** is a short wide cylinder (radius 1.3, length 0.67) scaled by the radius; **valves** and **clamps** are unit boxes scaled to size. Callers add parts in world space; `build()` makes the meshes once.

```js
import * as THREE from 'three/webgpu';

const SIDES = r => (r < 0.15 ? 8 : r < 0.5 ? 12 : 24);
const UNIT = {
  pipe: n => new THREE.CylinderGeometry(1, 1, 1, n, 1, true).rotateX(Math.PI / 2),
  bend: n => new THREE.TorusGeometry(3, 1, n, 8, Math.PI / 2),
  flange: n => new THREE.CylinderGeometry(1.3, 1.3, 0.67, n).rotateX(Math.PI / 2),
  box: () => new THREE.BoxGeometry(1, 1, 1),
};
const Z = new THREE.Vector3(0, 0, 1), q = new THREE.Quaternion();

export function createPipework(materialFor) {             // materialFor(service) -> node material
  const lists = new Map();
  const place = (shape, service, r, matrix) => {
    const key = `${shape}|${service}|${SIDES(r)}`;
    if (!lists.has(key)) lists.set(key, []);
    lists.get(key).push(matrix.clone());
  };
  const pipe = (service, a, b, r) => {
    const d = b.clone().sub(a), len = d.length();
    q.setFromUnitVectors(Z, d.normalize());
    place('pipe', service, r, new THREE.Matrix4().compose(a.clone().add(b).multiplyScalar(0.5), q, new THREE.Vector3(r, r, len)));
  };
  const build = () => new THREE.Group().add(...[...lists].map(([key, ms]) => {
    const [shape, service, n] = key.split('|'), mesh = new THREE.InstancedMesh(UNIT[shape](+n), materialFor(service), ms.length);
    ms.forEach((m, i) => mesh.setMatrixAt(i, m));
    return mesh;
  }));
  return { pipe, place, build };
}
```

## The pipe kit

`scripts/pipe-rack.js` is a parametric model, **"Pipe rack"** (id `pipes`): one module of a run, ready to be repeated.

- A module of 1 to 5 parallel pipes along Y, from y = 0 to y = `length`, their centrelines `stand` above the z = 0 plane they are carried from (a floor, a wall, a soffit: the caller turns the module). The pipes vary in size across the rack (1, 0.6, 0.8, 0.5, 0.7 of the diameter).
- A flanged joint at y = 0 (two discs 1.3 diameters across with a gap and a nut ring on each), so modules set end to end join.
- Lagging bands every 2 m when `lagging` is on.
- A valve on the first pipe at mid-length: a body between two flanged joints, a stem, an actuator box, and a status lamp on top. No hand wheel.
- Supports down to the plane every 4 m or so (the module's length divided into whole bays): a **rack** (a beam across under the pipes on a post at each end, a clamp round each pipe), or a **saddle** under each pipe on its own post; each post on a base plate. Or none.
- An end bend at y = `length`, of 1.5 diameters' radius, out of the plane, into it, left or right, with a tail of two diameters.
- Three levels of detail from the one definition: `high` (bevelled flanges, bolts, rounded valve boxes, 12/20/28 sides by radius), `medium` (12 sides, no bolts), `low` (8 sides, no valve, no lagging, no supports).
- Parameters: `pipes` 1..5, `length` 3..24 m, `diameter` 0.15..1.2 m, `spacing` 1.4..3 diameters, `stand` 0.3..2.5 m, `supports` rack / saddles / none, `flanges`, `lagging`, `valve` (toggles), `bend` none / out / in / left / right, `color` (the service paint).

The kit is written against the procedural-models library shipped beside it, `scripts/procedural-models.js` (geometry kernel, construction parts, a model registry and instanced fields by distance; imports only `three/webgpu` and `three/tsl`), and `registerModel(pipeRack)` adds it there. That library's API: a model is `{ id, name, kind, params: [...], build(spec) -> { layers: [{ name, geo, mat }], figure } }`, where each param is `{ key, label, type, min, max, step, value }` (or `options` for a select), each layer is one material's triangles, and `spec.detail` is `'high' | 'medium' | 'low'`; `createModel(id, spec)` returns one mesh group, and `createField(id, spec, matrices, { distances })` draws many instances of one design, each at a level chosen by its distance from the camera (`distances: [highWithin, mediumWithin]` in metres), and `field.update(camera)` re-sorts them when the camera moves.

**Laying a run.** A run is copies of the module set end to end along a line, stretched a little so a whole number of modules fills it exactly:

```js
import * as THREE from 'three/webgpu';
import { createField } from './procedural-models.js';

// a run on the floor from a to b (y up): the module's Y goes along the run, its z (the stand) goes up
export function pipeRun(a, b, spec, moduleLength = spec.length) {
  const dir = b.clone().sub(a), runLength = dir.length(); dir.normalize();
  const n = Math.max(1, Math.round(runLength / moduleLength)), stretch = runLength / (n * moduleLength);
  const side = new THREE.Vector3().crossVectors(dir, new THREE.Vector3(0, 1, 0)).normalize();
  const basis = new THREE.Matrix4().makeBasis(side, dir, new THREE.Vector3(0, 1, 0));
  const matrices = [];
  for (let i = 0; i < n; i++) {
    const at = a.clone().addScaledVector(dir, i * moduleLength * stretch);
    matrices.push(new THREE.Matrix4().copy(basis).setPosition(at).multiply(new THREE.Matrix4().makeScale(1, stretch, 1)));
  }
  return createField('pipes', { ...spec, bend: 'none' }, matrices, { distances: [45, 160] });
}
```

Put the end bend on the last module only (a separate model with `bend` set), and the valve on one module in several, not on every copy.
