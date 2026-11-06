---
name: station-maglev
description: Create realistic futuristic train stations, platforms, railway infrastructure and maglev guideways with procedural Three.js WebGPU geometry. Use for stations, platforms, rails, guideways, switches, supports, power systems, pedestrian circulation and station accessories.
---

# Train Stations and Maglev Infrastructure

Create believable, high-quality transportation infrastructure for a futuristic setting (city, district, station, ship) using procedural Three.js geometry.

Target: Three.js 0.187.0, WebGPU renderer (`three/webgpu`) and TSL node materials (`three/tsl`); no WebGL fallback, no GLSL.

Use Three.js BufferGeometry, Groups and ES6 JavaScript modules. Do not use GLB, GLTF, FBX, OBJ or pre-made meshes unless explicitly requested.

The target is not "a sci-fi train station". The target is a **real transportation system imagined for the future**.

## Core priorities

Always prioritize:

1. believable railway geometry
2. correct scale and proportions
3. coherent track alignment
4. structural support
5. passenger circulation
6. maintenance access
7. power and control infrastructure
8. safety systems
9. architectural identity
10. small decorative details

Do not add details before the infrastructure makes sense.

# Maglev Track Vocabulary

## Guideway

Treat the maglev route as an engineered guideway, not two conventional rails.

A guideway can contain:

- structural beam or slab
- magnetic propulsion/levitation assemblies
- vehicle guidance surfaces
- power conductors
- sensor/control equipment
- inspection access
- drainage or service channels
- expansion joints
- cable conduits

Choose the guideway architecture deliberately.

Possible forms:

- central beam
- twin beam
- U-shaped guideway
- box guideway
- elevated concrete/steel guideway
- enclosed guideway
- open guideway

Do not automatically copy conventional railway tracks.

## Sweep the route

Generate the guideway along a procedural path.

The path may contain:

- straight sections
- circular/large-radius curves
- vertical transitions
- station approaches
- ramps
- switches

Use a sweep/loft system rather than placing many disconnected boxes.

Maintain consistent cross-section orientation along the route. Frenet frames (what `ExtrudeGeometry` with `extrudePath` and `TubeGeometry` use) twist on straights and S-curves; frame the profile against a fixed world up instead.

```js
import * as THREE from 'three/webgpu';

// Sweep a closed 2D profile [[x, y], ...] (x across, y up, metres) along a curve.
// The profile's up stays on world up, so the section never rolls or twists.
// Repeat a profile point at hard corners; flip the index order if faces point inward.
export function sweep(curve, profile, segments, up = new THREE.Vector3(0, 1, 0)) {
  const pos = [], idx = [], n = profile.length;
  const p = new THREE.Vector3(), t = new THREE.Vector3(), side = new THREE.Vector3(), u = new THREE.Vector3();
  for (let i = 0; i <= segments; i++) {
    const s = i / segments;
    curve.getPointAt(s, p); curve.getTangentAt(s, t);
    side.crossVectors(t, up).normalize(); u.crossVectors(side, t);
    for (const [x, y] of profile)
      pos.push(p.x + side.x * x + u.x * y, p.y + side.y * x + u.y * y, p.z + side.z * x + u.z * y);
  }
  for (let i = 0; i < segments; i++) for (let j = 0; j < n; j++) {
    const a = i * n + j, b = i * n + (j + 1) % n;
    idx.push(a, a + n, b, b, a + n, b + n);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setIndex(idx); g.computeVertexNormals();
  return g;
}
```

Sample the curve by arc length (`getPointAt`), with segments dense enough on curves and sparse on straights.

## Curvature

Avoid abrupt direction changes.

Use smooth path curvature and physically plausible transition sections.

Distinguish between:

- curvature caused by the ground the route runs on
- curvature deliberately introduced into the railway route
- local vertical/horizontal transitions

The railway should feel intentionally engineered relative to its surroundings.

# Maglev Components

Where visible, model believable components such as:

- guideway
- magnetic stator/coil assemblies
- levitation/guidance surfaces
- linear motor sections
- power busbars
- control boxes
- sensors
- cable trays
- junction boxes
- inspection covers
- access panels
- mounting brackets
- expansion joints
- support bearings

Do not expose every mechanism everywhere.

Some systems can be enclosed within the guideway.

The visual model should communicate that sophisticated equipment exists without requiring every electromagnetic component to be literally modelled.

# Supports

Elevated guideways require believable structural support.

Use:

- columns
- piers
- crossheads
- bearings
- brackets
- braces
- foundations or mounting interfaces

For large spans, use beams, trusses or appropriate structural systems.

Do not let guideways float.

Avoid identical cylindrical supports everywhere unless the design genuinely calls for modular columns.

Use procedural variation in height and configuration where appropriate.

# Track Connections and Switches

A switch should look like an engineered mechanism.

When creating branching routes, include:

- smoothly diverging guideways
- structural transition
- switching mechanism
- power/control equipment
- inspection access
- appropriate support geometry

Do not simply intersect two tracks.

The transition between routes should be geometrically coherent.

# Stations

A station is a system rather than a building.

Model it hierarchically:

```
Station
├── Guideway
├── Platforms
├── Structural roof
├── Columns/supports
├── Passenger circulation
├── Safety systems
├── Lighting
├── Signage
├── Utilities
├── Mechanical systems
└── Maintenance access
```

## Platforms

Include:

- platform slab
- edge treatment
- safety boundary
- drainage
- lighting
- access routes
- structural support
- signage
- doors/barriers where appropriate

Platform dimensions should relate to the train dimensions.

Do not place the platform unrealistically close to moving equipment.

## Platform edge

For a maglev system, choose a believable safety concept.

Possibilities include:

- platform screen doors
- physical edge barriers
- marked safety boundary
- recessed guideway
- controlled boarding interface

Do not arbitrarily combine incompatible systems.

# Station Roofs

Large roofs need structure.

Use:

- primary beams
- secondary members
- columns
- trusses
- curved shells
- panels
- expansion joints

A large unsupported roof should not appear magically thin.

For futuristic architecture, use efficient structural forms rather than arbitrary floating surfaces.

Sweeps, lofts and shells are preferred for curved roofs.

# Passenger Circulation

Stations must explain how people get from the surroundings to the platform.

Consider:

- stairs
- ramps
- elevators
- escalators
- pedestrian bridges
- concourses
- ticket/access areas
- barriers
- waiting areas

Use real stair geometry and believable clearances.

Handrails and guardrails should generally be swept along paths.

# Station Accessories

Use procedural reusable components for:

- benches
- bins
- ticket/access gates
- information boards
- platform signs
- emergency equipment
- fire extinguishers
- cameras
- lighting fixtures
- speakers
- ventilation grilles
- service cabinets
- electrical cabinets
- maintenance doors
- handrails
- barriers
- bollards
- clocks/displays
- route maps

Do not populate every station with every accessory.

Choose accessories according to function and location.

# Lighting

Separate physical lighting fixtures from light emission.

A fixture should have:

- housing
- mount
- diffuser/lens
- cable/service connection where visible

Use an emissive node (`emissiveNode` on a node material) for the visible light source, and real lights, light probes or baked lighting for illumination.

Concourses and platforms carry hundreds of fixtures: give the ones whose light is seen a real point or spot light with a short cutoff and run them through r187 `ClusteredLighting` (the `lighting` skill); bounce light under canopies and in halls comes from a `LightProbeGrid` (`indirect-lighting`).

Do not make every surface emissive.

# Station Glass

Use the glass skill for:

- platform screen doors
- station canopies
- enclosed walkways
- observation areas
- windscreens

Glass should have actual thickness/recessed geometry where appropriate and subtle reflection/transmission.

Avoid perfectly flat black transparent planes.

# Signage

Use the signage skill.

Ordinary station information should normally be texture/decal based on physical sign geometry.

Use actual geometry for raised, illuminated or hero lettering.

A station should have a coherent information system:

- station name
- line/route
- platform number
- direction
- exits
- emergency information
- service/maintenance identifiers

Do not add random text merely for visual detail.

# Trackside Infrastructure

Between stations, the route can contain:

- cable trays
- service walkways
- control boxes
- sensors
- inspection panels
- emergency access
- maintenance platforms
- drainage
- structural expansion joints

Use repetition but introduce controlled variation.

Do not place equipment at arbitrary intervals without a reason.

# Maintenance and Safety

A believable transportation system needs access for technicians.

Provide plausible:

- inspection walkways
- ladders
- access hatches
- maintenance platforms
- equipment cabinets
- isolation points
- emergency walkways

Safety systems should be visually legible without overwhelming the scene.

# Station in Context

The station belongs to its surroundings.

Consider its relationship to:

- residential districts
- commercial areas
- roads
- pedestrian paths
- utility corridors
- service tunnels
- other transport lines

A station should have an obvious reason to exist at its location.

Avoid dropping a station into an empty environment.

The surrounding architecture should reinforce the transportation network.

# Modular Construction

Stations should be assembled from reusable modules.

Useful generators: `createGuideway`, `createMaglevBeam`, `createGuidewaySupport`,
`createStationPlatform`, `createPlatformEdge`, `createStationColumn`, `createStationRoof`,
`createStationScreenDoor`, `createTracksideCabinet`, `createCableTray`,
`createMaintenanceWalkway`, `createRailings`, `createStationLight`, `createStationSign`,
`createEmergencyEquipment`, `createTrackSwitch`.

Use parameters for:

- station width
- platform length
- train dimensions
- guideway width
- support spacing
- roof height
- curve radius
- module spacing

# Geometry Rules

Use:

- sweeps for guideways, rails/guide surfaces, conduits and handrails
- lofts for tapered supports and station roof transitions
- extrusions for structural panels and beams
- revolves for wheels, bearings and circular components
- bevels for manufactured edges
- shells for substantial panels and enclosures
- recesses for access panels, doors and equipment

Avoid primitive stacking when a continuous surface is more appropriate.

# Train-to-Station Relationship

Always consider the train when modelling the station.

Check:

- train width
- door positions
- platform height
- boarding gap
- roof clearance
- vehicle envelope
- platform screen door alignment
- stopping position

A beautiful station with incompatible train dimensions is a bad model.

If the train dimensions are unknown, create a clearly parameterized station based on assumed vehicle dimensions rather than inventing unrelated proportions.

# Performance

Stations can contain thousands of repeated objects.

Use `InstancedMesh` or shared geometry where appropriate for:

- lights
- bolts
- supports
- sleepers where applicable
- panels
- railings
- signs
- repeated cabinets

Keep hero geometry detailed and repeated background infrastructure economical.

Generate LODs from the same procedural definitions where useful.

# Final Rule

The viewer should be able to look at the station and understand:

**where the train goes, where the passengers stand, how the structure is supported, how the station is maintained, how it receives power, and how people safely move through it.**

If those things make sense, then add the futuristic design language.
