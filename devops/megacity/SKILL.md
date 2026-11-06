---
name: megacity
description: Create dense futuristic residential and commercial architecture inspired by Unity's original 2018-2019 Megacity demo. Use for large-scale city blocks, towers, podiums, elevated infrastructure, façades, streets, plazas, service structures and dense urban environments.
---

# Megacity Urban Architecture Style

Target: Three.js 0.187.0, WebGPU renderer (`three/webgpu`) and TSL node materials (`three/tsl`); no WebGL fallback, no GLSL.

## Purpose

Create dense futuristic residential and commercial environments inspired by the original Unity Megacity visual language shown at Unite LA 2018 and GDC 2019.

This is a visual and architectural style skill, not a Unity DOTS implementation skill.

The target city should feel enormous, dense, vertically layered, industrial, futuristic, highly serviced, modular, populated and believable at street level and skyline scale.

## Core Design Philosophy

Treat the city as a gigantic engineered machine.

Prefer:
- dense building clusters
- stacked functions
- strong verticality
- horizontal and vertical infrastructure
- modular façades
- repeated structural bays
- service equipment
- elevated walkways
- transport integration
- visible mechanical systems
- signage and lighting
- balconies and terraces
- vents, ducts, cables and structural frames
- varied building heights

Avoid:
- clean sci-fi toy buildings
- isolated towers in empty space
- excessive ornament
- fantasy architecture
- random greebles
- identical repeated buildings
- decorative geometry without function

Infrastructure comes before decoration.

## Visual Vocabulary

Use terms such as:

tower, slab, podium, block, vertical core, service core, structural frame, structural bay, façade grid, curtain wall, recessed façade, projecting façade, cantilever, balcony, terrace, skybridge, elevated walkway, mechanical deck, service deck, rooftop plant, antenna mast, ventilation array, exhaust stack, utility riser, cable tray, pipe rack, maintenance platform, access ladder, inspection panel, service door, loading bay, docking area, signage band, illuminated strip, façade screen, louver, sunshade, canopy, overhang, recessed entrance, podium arcade, plaza, service alley, pedestrian corridor.

## Massing

Build large masses before details.

Typical composition:
1. lower podium
2. main residential/commercial mass
3. vertical circulation/service core
4. secondary wings or attached blocks
5. balconies and terraces
6. mechanical/service levels
7. rooftop equipment
8. signage and lighting

Use combinations of:
- tall narrow towers
- wide slab buildings
- stepped towers
- offset towers
- stacked volumes
- podium + tower
- twin towers connected by bridges
- irregular blocks
- terraced masses
- recessed upper levels
- projecting sections

Avoid perfect symmetry unless function requires it.

## Density

Density is fundamental.

Buildings should rarely stand alone. Combine:
- primary buildings
- secondary buildings
- service buildings
- utility structures
- pedestrian infrastructure
- elevated roads
- transit infrastructure
- bridges
- signs
- lights
- mechanical equipment

Fill negative space intelligently.

Use three scales:
- macro: towers, blocks, roads, guideways, plazas, bridges
- meso: balconies, structural frames, façade modules, entrances, mechanical decks, walkways, canopies
- micro: vents, pipes, cables, lights, signs, doors, railings, cameras, brackets, access panels

Never use micro-detail to compensate for weak macro architecture.

## Vertical Layering

Create activity at multiple heights:
- ground streets
- raised pedestrian decks
- elevated roads
- transit guideways
- skybridges
- building bridges
- rooftop infrastructure
- mechanical decks
- high-level signage
- aerial transport corridors

Do not design the city as a flat street grid with towers placed on top. Think of it as a three-dimensional transportation and infrastructure network.

## Residential Buildings

Use dense modular forms:
- apartment slabs
- narrow residential towers
- stepped apartment blocks
- podium + tower
- courtyard blocks
- stacked terraces
- mixed-use towers

Façades may use:
- repeated windows
- balcony modules
- recessed balconies
- projecting balconies
- façade frames
- sunshades
- ventilation grilles
- service panels
- vertical cores
- occasional larger glazed areas

Vary composition, not random noise.

## Commercial Buildings

Communicate public activity with:
- larger glazed entrances
- broad openings
- illuminated signage
- retail bands
- canopies
- covered pedestrian areas
- public plazas
- atriums
- loading/service areas
- display surfaces
- vertical advertising/signage zones

Commercial architecture can be more expressive, but remains constrained by structure and function.

## Mixed Use

Prefer mixed-use buildings in dense districts.

A typical building can have:
- retail at lower levels
- offices in intermediate levels
- residential above
- mechanical systems on the roof
- service access to the rear or side

## Façades

Façades should look assembled, not painted onto boxes.

Use:
- structural frames
- mullions
- window modules
- recessed panels
- projecting panels
- curtain walls
- service panels
- vents
- louvers
- parapets
- balcony slabs
- railings
- façade screens
- expansion joints

Use repetition with controlled variation.

## Windows and Glass

Use regular window bays, grouped windows, ribbon windows, recessed glazing, projecting glazing and curtain walls.

Residential buildings generally use smaller repeated window systems. Commercial buildings can use larger glazed areas.

Use the separate glass skill for physical glass response, and the interior-mapping skill for the windows of buildings that cannot be entered.

## Balconies and Terraces

Model the slab, structural connection, railing and drainage edge. Do not simply attach thin rectangles to walls.

Terraces are useful for stepped massing and variation.

## Podiums

Use podiums for retail, entrances, public circulation, parking/service access, loading, mechanical services and transit connections.

A tower should often transition into its surroundings through a podium.

## Mechanical Architecture

Mechanical equipment is architectural.

Use:
- HVAC
- cooling equipment
- ventilation stacks
- ducts
- pipes
- pumps
- service cabinets
- generators
- electrical equipment
- maintenance platforms
- access ladders
- cable trays

Place equipment where real buildings would need it. Do not scatter machinery randomly.

## Roads and Urban Infrastructure

Integrate:
- multi-level roads
- ramps
- pedestrian routes
- transit guideways
- loading roads
- service lanes
- maintenance routes
- bridges
- tunnels
- elevated infrastructure

Roads should connect destinations and services.

## Bauhaus Combination

When combined with a Bauhaus residential/commercial style:

Bauhaus is the architectural grammar.
Megacity is the urban density and infrastructure language.

Bauhaus contributes:
- geometric massing
- functionalism
- clean planes
- strong horizontal/vertical composition
- simple materials
- rational structural grids
- restrained ornament

Megacity contributes:
- density
- vertical layering
- infrastructure
- mechanical complexity
- signage
- transport
- illuminated urban systems
- large-scale visual complexity

Target: **Bauhaus architecture evolved into a massive, highly engineered future city.** Do not turn Bauhaus into decorative retro-futurism.

## Materials

Prefer:
- concrete
- painted steel
- bare aluminium
- stainless steel
- dark glass
- translucent panels
- composite panels
- ceramic/stone-like panels
- rubber
- weathered service metal

Use the material skills (metal, paint, rust, glass, material-composition) for physical response.

Variation should come from roughness, wear, panel replacement, dirt, lighting and material transitions.

## Colour

Use colour structurally.

Accent colours may identify:
- transit
- emergency systems
- commercial zones
- entrances
- service infrastructure
- district identity
- corporate buildings

Avoid rainbow cities.

## Lighting

Use:
- illuminated signs
- window light
- linear architectural lighting
- transit lighting
- street lighting
- under-bridge lighting
- entrance lighting
- emergency lighting
- vehicle lights
- rooftop beacons

Keep physical fixtures, emissive materials and actual illumination conceptually separate.

Use TSL emissive nodes (`emissiveNode`) for emissive surfaces.

Hundreds of real point and spot lights (street rows, entrances, under-bridge, signs that light the pavement) run through r187 `ClusteredLighting`: the `lighting` skill has the setup and the per-light cutoffs; `indirect-lighting` has probe grids for street canyons and podium undersides.

## Signage

Use the signage skill.

Prefer physical sign housings with texture/decal lettering. Use actual geometry for large raised, illuminated or hero lettering.

Do not use TextGeometry for ordinary city signage.

## Procedural Building Generators

Useful generators include:

```
createBuildingMass()
createTower()
createSlabBuilding()
createPodium()
createResidentialBlock()
createCommercialBlock()
createMixedUseBuilding()
createFacadeGrid()
createWindowBay()
createBalcony()
createTerrace()
createCurtainWall()
createStructuralFrame()
createServiceCore()
createMechanicalDeck()
createRooftopEquipment()
createSkybridge()
createPedestrianDeck()
createCanopy()
createServiceAlley()
createLoadingBay()
createBuildingSign()
```

Parameters can include width, depth, height, floorCount, floorHeight, bayWidth, window dimensions, balcony depth, setbacks, podium height, tower dimensions, materials, façade pattern, mechanical density, signage density and lighting density.

## Variation and Districts

Create a small number of architectural families and vary them parametrically.

Vary:
- height
- width
- depth
- floor count
- setbacks
- façade rhythm
- balcony arrangement
- window grouping
- podium configuration
- roof equipment
- signage
- materials
- lighting
- mechanical equipment

Organize districts such as:
- residential
- commercial
- mixed-use
- industrial
- transport
- civic
- service

Each district should have its own tendencies in proportions, materials, signage, lighting and infrastructure density.

## Skyline

At distance prioritize:
1. silhouette
2. building height distribution
3. major transportation infrastructure
4. illuminated areas
5. large façade patterns
6. medium detail
7. micro-detail

Use tall landmarks, medium towers, low podiums, bridges, transit structures and mechanical silhouettes.

Do not make every building equally tall.

## Geometry

Use the procedural-geometry skill.

Prefer:
- sweeps for rails, pipes, ducts and structural members
- lofts for changing building profiles
- extrusions for panels and beams
- revolves for cylindrical mechanical parts
- bevels for hard-surface edges
- insets for recessed panels
- shells for thin architectural surfaces
- repeated modules and instancing for façades

Use real thickness where the object should have physical thickness.

## Performance

The original Megacity demonstrated massive scale using Unity's DOTS/ECS architecture, streaming, culling and LOD techniques. Unity reported 4.5M mesh renderers, 200K building components and 100K audio sources in its mobile demonstration. Apply the lesson, not the Unity implementation.

For Three.js:
- WebGPU only
- TSL materials
- instance repeated geometry
- reuse BufferGeometry and materials
- merge static geometry where useful
- hierarchical culling
- LOD
- stream districts
- cheap distant buildings
- `MeshletDrawingPipeline` for the whole city when it is vertex-bound: one line on the renderer, GPU culling and LOD per 64-triangle cluster (`engineered-environments`, Drawing at scale)
- avoid unique geometry for every window
- avoid thousands of decorative meshes when instancing or textures suffice

One façade module, one draw call for every bay of a building (or a district):

```js
import * as THREE from 'three/webgpu';

// A balcony/window bay instanced over a façade grid, with per-bay tint variation.
export function facadeBays({ bays, floors, bayWidth = 3.6, floorHeight = 3.2, material }) {
  const module = new THREE.BoxGeometry(bayWidth - 0.15, floorHeight - 0.15, 0.4);
  const mesh = new THREE.InstancedMesh(module, material, bays * floors);
  const m = new THREE.Matrix4(), c = new THREE.Color();
  let i = 0;
  for (let f = 0; f < floors; f++) for (let b = 0; b < bays; b++, i++) {
    m.makeTranslation((b + 0.5) * bayWidth, (f + 0.5) * floorHeight, 0.2);
    mesh.setMatrixAt(i, m);
    const v = 0.9 + 0.1 * Math.sin(b * 12.9898 + f * 78.233); // controlled, repeatable variation
    mesh.setColorAt(i, c.setScalar(v));
  }
  mesh.instanceMatrix.needsUpdate = true;
  mesh.instanceColor.needsUpdate = true;
  return mesh;
}
```

Use it with a `MeshStandardNodeMaterial`; instance colour multiplies the material colour. Swap the box for the real bay module (frame, recess, slab, railing) built once.

## Final Rule

The city must feel **built, occupied, serviced and maintained**.

Every major building should answer:
- Where do people enter?
- Where do they live or work?
- How do they move through it?
- Where are the services?
- Where does equipment go?
- How is it maintained?
- How does it connect to transportation?
- How does it connect to neighbouring buildings?
- How does it attach to the ground or structure it stands on?

The target is not a futuristic building. **The target is a believable piece of a gigantic functioning city.**
