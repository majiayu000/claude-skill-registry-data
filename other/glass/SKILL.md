---
name: glass
description: Create realistic architectural, vehicle, train and porthole glass with Three.js TSL on WebGPU. Use for windows, windscreens, canopies, station roofs, portholes, building windows, bottles and transparent panels.
---

# Glass

Target: Three.js 0.187.0, `three/webgpu` and TSL node materials from `three/tsl`; WebGPU only, no WebGL fallback, no GLSL strings.

Base the material on physical transmission rather than simply lowering opacity. Use the physical node material model where appropriate: transmission, IOR, thickness, attenuation, roughness, specular response and environment reflections.

## Realistic glass

Consider:

- transmission
- IOR
- thickness
- attenuation/tint
- roughness
- Fresnel reflection
- environmental reflection
- subtle normal variation
- edge behaviour
- seals and frames
- scratches/dirt where visible

Glass should not automatically be perfectly clear, perfectly smooth and perfectly flat.

## Train and vehicle windows

For train windows:

- recess glass into the body
- use actual rounded window geometry
- follow body curvature
- model the rubber/seal frame separately
- give the glass appropriate thickness
- keep the seal physically adjacent to the glass

## Edge distortion

For curved vehicle or architectural glass, create subtle view distortion that increases toward the edges.

Use an edge mask based on geometry/UV/view relationships where appropriate. The effect should be strongest near the glass boundary and transition smoothly into the central viewing area.

The goal is optical plausibility, not a visible "shader effect".

Avoid excessive refraction that makes the window look like water.

## Roughness variation

The clean centre can be clearer and smoother while edges can have slightly different roughness due to curvature, seals, contamination and manufacturing.

Use subtle variation.

## Dirt and scratches

If requested, layer very low-amplitude imperfections over the glass:

- fine scratches
- fingerprints
- dust
- condensation
- streaks

These should affect roughness/normal/transmission subtly rather than simply drawing coloured lines.

## Portholes

Round windows in ships, stations, habitats and submarines. They hold a pressure difference, so everything about them is heavier than a building window.

Construction, outside to inside:

- **glass**: a disc with real thickness, not a plane. 15 to 40 mm for a ship's side light, 50 to 150 mm or more where the pressure difference is large (submarines, vacuum). The outer face can be flat, bevelled at the rim or slightly domed.
- **seal**: a dark rubber ring between glass and frame, 5 to 15 mm visible. Keep it physically touching both.
- **frame**: a flanged ring, its face width about a tenth of the diameter, standing proud of the hull by a few centimetres, with a lip that overlaps the glass edge.
- **bolt ring**: bolts on a circle through the flange, every 15 to 25 cm along the circle, never fewer than 6.
- **inner glazing**: where the pressure difference is large, a second pane on the inside with an air gap of a few centimetres, set in its own thinner ring. The gap shows as a second faint reflection.

Sizes: 0.3 to 1.2 m across. 0.3 to 0.45 m for ship cabins and hatches, 0.5 to 0.8 m for station corridors, up to 1.2 m for observation ports. Larger than that is a viewing window, not a porthole.

Optics and ageing:

- refraction strongest at the rim, where the bevel or dome bends the view; the centre stays clear
- a grime ring at the seal: higher roughness and a slight darkening in the outer 5 to 10 % of the radius
- condensation on the cold side (inside on a ship in cold water, outside of a warm station's inner pane): raised roughness in soft patches, heavier towards the bottom
- at night or in darkness, an interior glow from behind, or the lit scene beyond showing through; do not leave a lit porthole black

Build it procedurally: a `LatheGeometry` from a 2D profile for the flanged frame (and for a domed glass), a short `CylinderGeometry` for a flat thick disc, a `TorusGeometry` or thin lathe ring for the seal, and one `InstancedMesh` for all bolts of all portholes. No model files.

```js
import * as THREE from 'three/webgpu';
import { uv, length, smoothstep, mix, float } from 'three/tsl';

export function createPorthole({ diameter = 0.6, glassDepth = 0.04 } = {}) {
  const r = diameter / 2, fw = diameter * 0.1, g = new THREE.Group();
  const profile = [[r, -0.02], [r + fw, -0.02], [r + fw, 0.03], [r + 0.01, 0.04], [r - 0.01, 0.03]]
    .map(([x, y]) => new THREE.Vector2(x, y));
  const frame = new THREE.Mesh(new THREE.LatheGeometry(profile, 48),
    new THREE.MeshStandardNodeMaterial({ color: 0x5c6166, metalness: 0.8, roughness: 0.45 }));
  frame.rotation.x = Math.PI / 2;                       // lathe axis y -> porthole axis z

  const rim = smoothstep(0.82, 1.0, length(uv().sub(0.5)).mul(2.0));   // cap UVs are radial
  const glassMat = new THREE.MeshPhysicalNodeMaterial({ transmission: 1, ior: 1.5, metalness: 0 });
  glassMat.roughnessNode = mix(float(0.03), float(0.3), rim);          // grime ring at the seal
  glassMat.thicknessNode = mix(float(glassDepth), float(glassDepth * 2.5), rim);   // stronger bend at the rim
  const glass = new THREE.Mesh(new THREE.CylinderGeometry(r, r, glassDepth, 48), glassMat);
  glass.rotation.x = Math.PI / 2;
  g.add(frame, glass);

  const count = Math.max(6, Math.round((Math.PI * 2 * (r + fw / 2)) / 0.2));   // a bolt every ~20 cm
  const bolts = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.012, 0.012, 0.015, 6), frame.material, count);
  const m = new THREE.Matrix4();
  for (let i = 0; i < count; i++) {
    const a = (i / count) * Math.PI * 2;
    bolts.setMatrixAt(i, m.makeRotationX(Math.PI / 2).setPosition(Math.cos(a) * (r + fw / 2), Math.sin(a) * (r + fw / 2), 0.035));
  }
  g.add(bolts);
  return g;
}
```

For a whole ship or station, share the materials and put every porthole's bolts in one `InstancedMesh`.

The cheap far version: a flat disc with the same glass shader (or the same rim and grime masks on an opaque reflective material), the frame as a flat ring, no bolts. Switch at the distance where a bolt is smaller than a pixel or two; the disc and ring keep the porthole's read at any distance.

## Building windows

Vocabulary:

- **opening**: the hole in the wall; its depth is the **reveal**, the wall thickness seen at the sides and head (10 to 40 cm in masonry, 5 to 15 cm in light cladding)
- **frame**: fixed to the opening, 5 to 10 cm wide on the face
- **sash**: the frame of an opening light, inside the main frame, 4 to 7 cm
- **sill**: the ledge at the bottom, projecting 3 to 6 cm past the face outside, sloped to shed water; a board inside
- **head**: the top of the opening, often a lintel
- **mullions** (vertical) and **transoms** (horizontal): bars dividing the window into lights; glazing bars divide a light into panes
- **fixed lights** and **opening lights**: opening ones have a sash, so their glass sits a little further back and their frame is thicker

Construction rules:

- set the glass back from the wall face by 5 to 20 cm; a pane flush with the facade reads as a sticker
- model the reveal as real geometry: four inner faces of the opening, lit and shadowed like the wall
- the sill projects and casts a thin shadow line under the window
- frames and mullions are real geometry, slightly proud of the glass
- the glass is thin, flat and the same material for every window of a building

Punched windows versus curtain wall:

- **punched windows**: separate openings in a solid wall, with reveals, sills and lintels; houses, masonry and most older buildings
- **curtain wall**: a continuous grid of glass and spandrel panels hung in front of the structure; mullions on a regular module (1.2 to 1.5 m wide, a floor tall), no reveal, glass nearly flush with the mullion caps, opaque spandrel panels at floor slabs

How windows read from the street:

- by day: dark. The room behind is darker than outside, so the glass reads as the reflection of the sky and the buildings opposite over a dark interior
- at grazing angles: almost all reflection
- at night: some lit, warm or cool, most dark; never all lit, never a uniform glow
- reflections of the sky make the upper floors lighter than the lower ones; reflections of the street opposite keep the lower floors darker

Use real transmissive glass for windows the viewer can look through into a modelled space. For the windows of buildings that cannot be entered, especially when there are many of them, use the `interior-mapping` skill: a flat pane whose shader draws blinds, curtains and a blurred room with parallax, far cheaper than glass plus rooms. Model the reveal, sill and frame in geometry either way.

## Performance

Do not make every glass surface expensive. Use full optical treatment for hero glass and simpler variants for distant windows.

For large windows, prefer geometry that follows the surface rather than pretending a curved window is a flat rectangle.
