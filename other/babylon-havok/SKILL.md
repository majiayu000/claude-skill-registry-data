---
name: babylon-havok
description: Engine-layer conventions for Babylon.js and Havok in this project — scene and node structure, the render/physics loop split, material and mesh budgets, glTF asset loading, WebGPU/WebGL2 dual-path rules, disposal and memory hygiene, and the Inspector. Use when touching anything that talks to Babylon or Havok directly, or when a rendering, loading, or physics-integration question comes up.
---

# Babylon.js + Havok

The engine layer. Everything in here is _presentation and integration_ — the game
rules live in the simulation layer and must not import from Babylon (see `game-dev`).

## Side-effect imports must be in the file that calls the API

Babylon patches families of methods onto Engine and Mesh from separate modules:
`thinInstanceSetBuffer` from `Meshes/thinInstanceMesh`, `createDynamicTexture`
from `Engines/Extensions/engine.dynamicTexture`. Without the import the method
is `undefined` — a TypeError at best, a silent no-op at worst — and the type
checker cannot see it, because the method is declared on the interface either
way.

**A sibling's import will hold yours up.** These are global patches, so a file
that forgets one still works as long as anything else in the bundle imports it.
That is not working, it is coincidence: lazily load the sibling, or delete it,
and the caller breaks with no diff of its own to explain why. `headlights.ts`
sat in exactly that state, propped up by three other modules.

**WebGPU needs its own import, always.** `Engines/Extensions/*` patches the
WebGL engine; `Engines/WebGPU/Extensions/*` patches the WebGPU one. Both, every
time. Import only the first and it passes locally, passes CI and passes every
headless harness — all of which fall back to WebGL2 for want of a GPU — and
then the sky is black on the phone. This project has been bitten by it twice.

Since nothing without a GPU can catch it at runtime, catch it statically:
`tests/engine-imports.test.ts` scans `src/engine` for the calls and asserts the
caller imports the modules itself. Strip comments before matching — a file that
*explains* the trap is not a file that uses the API, and making that failure go
away by adding imports it doesn't need is worse than the failure.

## The layering rule, concretely

```
src/sim/       pure TypeScript. No Babylon import. Deterministic. Vitest-testable.
src/engine/    Babylon + Havok. Reads sim state, draws it. Owns meshes and materials.
src/platform/  input, audio, storage, PWA. Browser APIs live here and nowhere else.
```

A lint rule forbids `src/sim/**` importing `@babylonjs/*`. If you find yourself
wanting to break it, the thing you're building is in the wrong directory.

**Where does Havok sit?** Physics is simulation, not presentation — but Havok is a
WASM module with its own world state, so it can't be pure. Resolution: the physics
world is owned by `src/sim/physics/`, wrapped behind a narrow interface that the rest
of the sim calls. Babylon's `PhysicsAggregate` convenience bindings tie bodies to
meshes and are therefore engine-layer only; the sim drives Havok bodies directly and
the engine layer reads transforms out to position meshes.

## Loop

Babylon's `runRenderLoop` is the _render_ loop. Do not put game logic in it, and do
not use Babylon's built-in physics stepping tied to render frames — that is
variable-dt physics and produces frame-rate-dependent handling.

```ts
engine.runRenderLoop(() => {
  accumulator += Math.min(engine.getDeltaTime() / 1000, MAX_FRAME_S);
  while (accumulator >= FIXED_DT) {
    world.step(FIXED_DT, input.snapshot());
    accumulator -= FIXED_DT;
  }
  view.sync(world, accumulator / FIXED_DT); // interpolate meshes from sim state
  scene.render();
});
```

Step Havok manually inside `world.step`, at `FIXED_DT`, never from the render loop.

## Initialisation order

Havok is WASM and loads asynchronously. Await it before creating any physics body,
and load it exactly once for the process. A test suite that initialises Havok per
test will be slow and will eventually flake.

Renderer selection: try `WebGPUEngine` and fall back to `Engine` (WebGL2) on failure
or on missing `navigator.gpu`. Both paths must be exercised — a change verified only
under WebGPU is not verified, because a large share of iOS devices are still WebGL2.

## Meshes and materials

Mobile GPUs are tile-based; the costs that matter are draw calls, overdraw, and
material switches — not raw triangle count.

- **Instance everything repeated.** Buildings, streetlights, road segments, parked
  cars: thin instances (`thinInstanceAdd`) for static repeats, `createInstance` when
  each needs its own node. A city built from individually-created meshes will not run.
- **Share materials aggressively.** One material per texture atlas, not per object.
  Material count is a first-class budget.
- **Freeze what doesn't change** — but read `freezeWorldMatrix` literally. It
  freezes the **world** matrix, not the local one, so it is right for scenery
  and wrong for anything parented to something that moves. Freezing a car's
  merged interior left it sitting at the world origin while the body drove off.
  If it has a moving parent, do not freeze it. `material.freeze()` and
  `scene.freezeActiveMeshes()` carry no such trap.
- **Merge static geometry per chunk** at generation time rather than drawing hundreds
  of small meshes.
- Keep shadows off or extremely limited on mobile. Real-time shadow maps are usually
  the single most expensive thing in a mobile scene; prefer baked or blob shadows.

## What merging meshes actually saves

`Mesh.MergeMeshes` is the main draw-call lever, and it is easy to over-estimate:

- **Merging parts that share a material removes draw calls.** This is the real
  win. Collapsing one car's static parts by material took it from ~44 draws to
  ~20, with no visual change.
- **Merging parts with _different_ materials does not.** The
  `multiMultiMaterial` form produces one mesh carrying a `MultiMaterial`, but a
  sub-mesh per material still issues its own draw call. It saves state changes,
  not draws. Budget on that basis, or a plan built on "merge everything into one
  mesh" will miss by several times.
- **It bakes world positions.** Merge while the parent is still at the origin
  with identity rotation, or every merged object is built around wherever the
  parent happened to be at the time.
- **Attribute sets must match exactly**, or it throws `Cannot merge vertex data
that do not have the same set of attributes`. Box and cylinder primitives
  carry UVs; hand-built `VertexData` with only positions and normals does not.
  Group by attribute signature as well as material rather than padding with zero
  UVs — invented UVs break silently the first time that material gains a
  texture, and the extra draw call is one, not many.
- **Merging destroys names.** Anything found by a name lookup must be held by
  reference instead. Doing that is an improvement anyway: `getChildMeshes` with a
  predicate allocates an array on every call, and these lookups tend to live in
  per-frame code.

Exclude from a merge: anything that moves independently, anything toggled on its
own, anything alpha-blended into a later rendering group, and anything with
children.

## Disposal and memory

iOS is the tightest memory environment we target, and an endless streamed city
allocates continuously. Leaks here are fatal, not untidy.

- Every `dispose()` must also dispose materials and textures if not shared — Babylon
  does not cascade by default. `mesh.dispose(false, true)` disposes materials/textures.
- **"Materials are shared" is a claim to check per material, not a blanket rule.**
  Most of a vehicle's are shared across its whole profile; its registration
  plates, door decals and lightbar are built per id and are not. Disposing the
  mesh tree with `disposeMaterialAndTextures = false` on the strength of a
  comment leaked all of those on every cop despawn. Track per-entity resources in
  an explicit `owned` list built where they are created — recovering them later
  by walking the mesh tree and matching names is the approach that breaks the
  first time something is renamed.
- **A material or texture leak is invisible in `scene.meshes.length`**, which is
  the figure a harness naturally samples. Sample `scene.materials.length` and
  `scene.textures.length` as well. And check that the scenario actually
  _exercises_ the disposal path: `city-inspect --stream` teleports across the
  whole city without ever despawning a vehicle, so `pruneRemoved` is never
  called and the route reports a clean bill however bad the leak is. That is why
  `--despawn` exists. Reverting the fix and re-running is the only way to know a
  leak check has teeth.
- Dispose Havok bodies when their chunk unloads. An orphaned body keeps simulating.
- Pool and reuse chunk meshes rather than create/dispose churn.
- `scene.blockMaterialDirtyMechanism = true` around bulk changes.
- Never hold a mesh reference in sim state. Sim holds ids; the engine layer maps
  id → mesh.

## Assets

glTF/GLB only, loaded via Babylon's `SceneLoader`. Compress with Draco for geometry
and KTX2/Basis for textures — KTX2 matters a lot on mobile because it stays compressed
in GPU memory, where a PNG does not.

Load asynchronously with a visible loading state, and never block the first frame on
a non-essential asset.

## Inspector

`scene.debugLayer.show()` behind a dev-only flag. It's the fastest route to
diagnosing draw-call counts, material duplication, and orphaned nodes. Do not ship it
in the production bundle — import it dynamically so it tree-shakes out.

## An unlit StandardMaterial carries its colour in `emissiveColor`

`disableLighting = true` does exactly one thing: it stops Babylon emitting the
`LIGHT0..n` defines, so the shader's per-light loop never runs and `diffuseBase`
stays at its initial `vec3(0.)`. The final colour in `default.fragment` is

```
clamp(diffuseBase * diffuseColor + emissiveColor + ambient) * baseColor
```

so with `diffuseBase` pinned at zero **the entire `diffuseColor` term is
multiplied out, whatever it is set to**. A white `diffuseColor` with a black
`emissiveColor` and lighting disabled renders pure black.

`baseColor` is where a thin instance's per-instance colour arrives —
`baseColor.rgb *= vColor.rgb`, gated on `VERTEXCOLOR || (INSTANCESCOLOR &&
INSTANCES)`. So the recipe for "the instance colour is the output colour" is
**black diffuse, white emissive, lighting disabled**.

This cost a long debugging session on #26: the city's signage and street lighting
material had it the other way round, and every neon sign and lamp head in the
game drew as an invisible black quad. Everything upstream was correct and every
diagnostic said so — 58 to 140 thin instances a chunk, right material, in
frustum, in `scene.getActiveMeshes()`, bounds spanning the chunk. Nothing was
wrong anywhere except the pixels.

Two things worth taking from that beyond the recipe:

- When geometry is provably submitted and still not visible, the next suspect is
  the _material's colour arithmetic_, not the culling, the bounds or the
  transform. Read the actual shader source in `node_modules` rather than
  reasoning about what the property names imply — `emissiveColor` is added again
  under `EMISSIVEASILLUMINATION` and not otherwise, which is not guessable.
- `thinInstanceSetBuffer('color', ...)` silently rewrites the kind to
  `instanceColor` (`VertexBuffer.ColorInstanceKind`) for native's benefit. That
  is why `INSTANCESCOLOR` is keyed on `isVerticesDataPresent('instanceColor')`
  and why looking for a `color` buffer to explain a missing tint finds nothing.

## Output is not gamma-corrected unless you ask for it

No image processing is enabled at the tier this game ships to, so a value the
shader computes at 0.10 displays at 0.10. That looks black. The same figure
through an sRGB curve would be about 0.35 — a perfectly visible mid-grey.

Tune emissive and ambient constants against _linear_ output, and if a surface
looks black when the arithmetic says it should be visible, suspect this before
retuning. Two rounds of the #26 window work were spent brightening a wall that
the maths said was already bright enough.

## Engine extensions need a side-effect import per backend

Babylon patches many engine methods on from separate modules, and with deep
imports those are not pulled in automatically. Worse, **there is one module per
backend**, and they target different classes:

```ts
import '@babylonjs/core/Engines/Extensions/engine.dynamicTexture'; // ThinEngine
import '@babylonjs/core/Engines/WebGPU/Extensions/engine.dynamicTexture'; // WebGPU
```

`WebGPUEngine extends ThinWebGPUEngine`, **not** `ThinEngine`, so the WebGL
extension never reaches it and the method is simply `undefined`. Importing the
class itself — `DynamicTexture` — is not enough; it is the _engine method_ that
is missing, and the failure surfaces as `createX is not a function` deep inside
Babylon.

**This is a blind spot in every environment available here.** Software rendering
has no WebGPU, so the fallback to WebGL2 always applies and the WebGL extension
always suffices. A missing WebGPU extension therefore looks completely fine
locally, in CI, and in any headless browser — and fails only on real hardware
with a working WebGPU implementation, which today means an iPhone on iOS 26.

So: when adding anything that needs an engine extension, import both variants
without waiting to see a failure, because you will not see one. And treat "it
renders here" as evidence about the WebGL path only. See #6.

## Hand-built quads: the winding is left-handed and the atlas UVs are not obvious

Building geometry directly with `VertexData` — the right call for a handful of
per-chunk quads that each need their own UV rectangle, where instancing would
mean a custom attribute and a plugin to read it — hands you two conventions that
are easy to get backwards and that fail in ways which do not look like what they
are.

**Winding.** Babylon is left-handed by default, so a front face is wound
_clockwise_ as seen from the front. Wind it the other way and, with
`backFaceCulling` on, the front face is culled and the back face renders. The
symptom is not a missing object: it is a correctly placed, correctly lit,
correctly coloured surface with its content **mirrored**. That reads as a UV
problem and sends you to the wrong file.

**Atlas V.** For a `DynamicTexture` atlas sampled by hand-written UVs, the cell
row comes out right with the obvious mapping while the orientation inside the
cell does not — the panel shows the right artwork, 180° round. Because the
_content_ is correct, nothing looks like a UV bug until the artwork has
lettering in it and you get close enough to read it. Determine this by looking
rather than deriving; the interaction between `invertY`, the V direction and the
front-face winding is not worth reasoning about from first principles when one
screenshot settles it.

**And the meta-lesson, which is the expensive one:** a wide shot cannot judge
legibility. Four wide angles of the city all looked fine while every billboard
in the world was mirrored, and the bug was obvious within one second of framing
a single board square-on. When a feature's whole point is that it is _read_, the
review harness needs a shot that frames one — found in the scene rather than
hard-coded, since which objects exist depends on the seed. See the billboard
shot in `tools/city-look.mjs`.

## World-space UVs on shared-material instances need a material plugin

Thin instances of one unit box, scaled non-uniformly, cannot get a
constant-size-in-metres texture through the box's own UVs: every instance has the
same 0..1 range, so a 6 m shop and a 40 m tower get windows seven times different
in size. Deriving the coordinate from `vPositionW` and the world normal fixes it,
and a constant floor height falls out for free.

`MaterialPluginBase` is the way to do that without losing the single
`StandardMaterial`, the single draw call per chunk, the per-instance `vColor` or
the fog. The stock paths do not work and it is worth knowing why:
`Texture.coordinatesMode` is consumed only by the reflection/refraction path and
every mode is camera- or reflection-relative; `uScale`/`vScale` are per-material
constants, which is the stretching restated; `TriPlanarMaterial` has no emissive
channel, is not a dependency here, and never sets `THIN_INSTANCES` so it drops
the world matrix.

Three details that are easy to get wrong:

- **The injection point decides what the effect interacts with.**
  `CUSTOM_FRAGMENT_BEFORE_FOG` runs before fog, so an emissive addition fades
  into haze with the surface — correct for ordinary buildings.
  `CUSTOM_FRAGMENT_BEFORE_FRAGCOLOR` runs _after_ fog and tone mapping, so the
  same code punches through haze at any distance — correct for landmarks, wrong
  for everything else. `CUSTOM_FRAGMENT_UPDATE_ALPHA` sits inside `#ifdef
DIFFUSE` and compiles out entirely, with no warning, on a material with no
  diffuse texture.
- **Write both shader languages.** The varying is `vPositionW` in GLSL and
  `fragmentInputs.vPositionW` in WGSL, and `getCustomCode` takes the language as
  its second argument for exactly this reason. `isCompatible()` returns true for
  GLSL only by default and the plugin manager **throws** on a WGSL material, so
  override it deliberately. WGSL cannot swizzle-assign, so rebuild the colour
  rather than adding into `color.rgb`.
- **Override `getClassName()`.** The base returns `'MaterialPluginBase'`, and the
  class name keys the generated `MATERIALPLUGIN` define — two plugins reporting
  the base name collide.

CI has no GPU and always falls back to WebGL2, so the WGSL branch cannot be
verified here at all. Same blind spot as the engine extensions above; see #6.

## Side-effect stubs fail silently — turn the warnings on

Babylon 9 replaces tree-shaken augmentations with stub functions that **do
nothing, throw nothing, and log nothing** by default. `thinInstanceSetBuffer`
without `import '@babylonjs/core/Meshes/thinInstanceMesh'` accepts the matrices,
returns normally, and draws zero instances. A whole city was generated, uploaded
and silently discarded.

The stubs are deliberately quiet — engine internals call augmented methods as
feature checks, so warning by default would spam every frame — but that means
_your_ calls are quiet too. Opt in during development:

    import { SetMissingSideEffectWarningsEnabled } from '@babylonjs/core/Misc/devTools';
    if (import.meta.env.DEV) SetMissingSideEffectWarningsEnabled(true);

`_IsSideEffectImplemented(fn)` feature-detects a specific method, since a stub is
truthy and `typeof` says "function".

This is the same failure as the WebGPU `dynamicTexture` bug in a new costume, and
the general rule now has two halves: **a Babylon feature that is not part of the
core class needs a side-effect import, and its absence is invisible.** When
something you built does not appear, check the import before checking your maths.

## Far clip and fog distance are one decision

Exp2 fog at density 0.0075 leaves 0.6% of an object's colour at 300 m and 0.01%
at 400 m. Babylon's default far plane is 10000, so the renderer was shading well
over a kilometre of city that the fog then erased completely — 59 draw calls down
to 50, and a fifth of the frame time back, for one line.

Set `camera.maxZ` from the fog falloff rather than by feel, and treat the two as
a single tunable: changing one without the other either wastes fill or clips
visible geometry. Anything that turns fog _off_ — a debug flyover, an inspection
harness — must raise `maxZ` too, or it trades a fogged city for a clipped one.

## Reading Havok's collision events consumes them

`HP_World_GetCollisionEvents` plus `HP_World_GetNextCollisionEvent` walks a list
that the walk itself destroys. A second walk in the same tick returns a
different, usually empty, result — measured here as 64 differing reads out of 180
steps of a box resting on the ground.

So drain once, inside `step`, into an array, and let everything else read that
snapshot. Exposing the walk directly means the first consumer silently starves
every other one, and the failure is indistinguishable from "no collisions
happened" — which is exactly how it presented: cars visibly shoving each other
across the map while the event list stayed empty.

Two more things about collision events specifically:

- **Bodies raise nothing until opted in** with `HP_Body_SetEventMask`, and the
  omission is silent. Collisions still resolve correctly; only the reporting
  disappears. Opt in the handful of bodies that matter, never the whole city.
- **The EventType members are Emscripten objects carrying `.value`, and the
  declared numeric enum in the .d.ts is wrong.** The real bits are 1, 2 and 4 —
  flags, not sequence — so a literal copied from the typings both fails to OR and
  names the wrong events. Read `.value` off the module and verify it, the same
  rule as `MotionType`.

## When the typings and the runtime disagree, believe the runtime

Havok's `.d.ts` has been wrong three times now in this project: `MotionType`
members declared as numbers but objects at runtime; `EventType` declared 0-based
when the real values are 1/2/4 bit flags; and
`HP_World_GetNextCollisionEvent(world: number, …)` declared as a plain number
while every sibling call takes `HP_WorldId`.

None of these fail loudly. A wrong `MotionType` leaves a body static, a wrong
event mask opts into nothing, and both look like a physics bug rather than a
typings bug. When something physical is not happening, probe the actual runtime
value before rereading your own maths — it takes one throwaway test and settles
it outright.

## Handedness

Babylon is **left-handed**. A positive rotation about X carries +Z toward -Y, not
toward +Y. Hinged parts rotated by the "obvious" sign swing the wrong way — the
bonnet and boot both opened downward into the body and disappeared, leaving what
looked like an open bay with no lid. Nothing errors; the part is simply somewhere
you did not expect.

The same catches flat geometry: `CreatePlane` faces -Z, so a decal on the +X
flank needs -90 degrees about Y. Get it backwards and the plane is backface-
culled and the artwork silently vanishes.

Both are cheap to verify and impossible to notice from a test. Rotate the part to
its extreme and look at it.

## One description of the world, not two

Anything that exists in both the simulation and the view — ground extents, world
bounds, chunk size, vehicle dimensions, spawn points — is **published by the
simulation and read by the view**. Never as a constant in each.

Two constants describing the same thing will diverge, and the divergence is silent:
nothing fails, nothing warns, the game simply becomes wrong in a way that is
invisible from the gameplay camera. This has already happened once here — a 400 m
visible ground against a 4000 m collision ground, so the car drove off the visible
world and kept going. It was found by a wide-angle screenshot, not by any test.

When you catch one of these, fix the structure rather than the number: move the
value into simulation state and have the view read it, so the next change cannot
recreate the bug.

## Never

- Import Babylon from `src/sim/`.
- Step physics from the render loop.
- Create a mesh or material inside the render loop or a per-tick system.
- Use `scene.registerBeforeRender` for gameplay logic.
- Ship the Inspector or debug materials in a production build.
- Duplicate a world dimension as a constant in both the sim and the view.

## Screen-space geometry parented to the camera

A strip parented to the camera — a rear-view mirror, a reticle, a letterbox —
has two traps that both present as "nothing draws", with no error and no warning:

- **The default near clip is 1.0** and a camera that never sets `minZ` keeps it.
  A plane placed at `z = 1` is clipped away entirely. It still renders its
  target every frame; you pay for it and see nothing. Place it well past the
  near plane and scale its width and height with the distance.
- **`CreatePlane` already faces −Z, which is toward a camera looking down +Z.**
  The instinct is to rotate by PI so it "faces the camera". That points it away
  and it is backface-culled. No rotation is the correct orientation.

Both were hit building the mirror, the second one _after_ this file already
recorded the −Z facing rule for other geometry. Reading a rule is not the same
as recognising the situation it applies to.

## Second render passes are affordable only if budgeted as one

A `RenderTargetTexture` with `renderList = null` renders the whole scene again.
Left at defaults that roughly doubles draw calls, which no phone has spare.
Three knobs make it viable, and they should all be set deliberately at
construction rather than discovered later:

- A **short `maxZ` on the target's camera** — this is what actually cuts the
  geometry submitted, not the target's resolution.
- **`refreshRate`** above 1. A glanced-at strip does not need 60 Hz.
- A **small target**. 512×128 is more than a 90-pixel strip needs at any device
  ratio worth serving.

Tie all three to the quality tier and return `null` on the lowest one, rather
than shipping a worse version of the effect. A feature that halves the frame
rate on the device it was added for is not a feature. Note that Babylon's
`scene.getEngine().drawCalls` does not count render-target passes, so the stats
overlay under-reports once one exists.

Never set `scene.activeCameras` just to add a second camera: that switches the
whole scene to the multi-camera path. A render target drives its own camera
through `target.activeCamera`.

**`renderList = null` includes the mesh that displays the target.** This is a
real feedback loop and it is the third trap in the same feature: the strip's
material samples the render target, the target renders every mesh in the scene,
and the strip is a mesh in the scene. Whenever the strip enters the target
camera's frustum the driver is asked to sample a texture it is drawing into and
reports `GL_INVALID_OPERATION: Feedback loop formed between Framebuffer and
active Texture`.

It is intermittent, because whether the strip is in that frustum depends on
where the parent camera has swung to — which makes it look like something
else's bug. Exclude the strip and any furniture around it with a **layer mask**,
not a renderList: default masks are `0x0fffffff`, so giving the furniture a mask
of `0x1` and the target's camera `0x0fffffff & ~0x1` excludes exactly those
meshes and nothing else. A renderList would have to name every mesh in a
streaming world.

## An intermittent error needs the control run in both directions

The mirror's feedback loop above was attributed to clustered street lighting for
several commits, and the reasoning looked sound: the errors appeared with the
lamps on, and turning the lamps off made them stop. The control that was never
run is the other one — the mirror with the lamps **off**, which still produced
fourteen errors in eight seconds.

Turning the lamps off had removed the errors because it also removed the mirror:
the two were wired to the same switch by the very commit that was diagnosing
them. The A/B compared "lamps and no mirror" against "lamps and mirror" and read
the result as being about lamps.

When feature A and feature B are suspected of colliding, the test is four runs,
not two — and if A's gate already disables B, the gate has to come out before
any of them mean anything. The cost of getting this wrong was a real feature
deleted for months and a comment block in three files confidently explaining a
bug that did not exist.
