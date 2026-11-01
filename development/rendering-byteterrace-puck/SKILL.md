---
name: rendering
description: "Maps Puck's SDF renderer and GPU code. Use for mapCore, the mesh bake, HLSL kernels, sdf-isa.hlsli, SdfOp, C#/HLSL layouts, world.shaders.reload, field scopes, GPU cost. Sculpting: sdf-authoring."
---

# Rendering

A map of Puck's GPU presentation code: where each part lives, the contracts
that bite when you change it, and how to see a change. [Rendering](../../../docs/rendering/README.md)
and its handbook explain the renderer; package READMEs own the detail. When this
file and the code disagree, the code wins and this file is corrected in the
same change.

Rendering is presentation: floats are legal, and nothing here may feed back
into simulation state. The deterministic contract lives with the fixed-point
query evaluator (`SdfFieldEvaluator`) and `maths-usage`.

## Camera bloom

The [bloom decision](../../../docs/decisions/rendering.md#bloom-is-a-cameras-scatter-applied-once-before-tonemapping)
owns the design; the [frame handbook](../../../docs/rendering/sdf/handbook/frame-rendering.md#camera-bloom)
owns authoring and pass order. `SdfWorldPackage.WithBloom` declares the endpoint's
optional output-relative pyramid; `SdfBloomRecorder` records its down/up passes.
`SdfWorldPasses.Entry.OpticalBloom` gates transport, diagnostic, full screen
fidelity and disabled views before allocating. Keep that gate and `world.bloom`'s
reported bypass reasons aligned. Direct root views export the named `bloom` image
for `place.bloom`; filmed cameras use `bloom-apply`. The direct image
`BloomDirect` binds the composite's output member. A named image publication
must retain its storage through graph replacement and carry its readable layout,
just as the default image does. Optional absent bloom binds the shared stand-in.
Keep root placement's optional input stable across enable/disable: a graph still
rendering while its replacement builds must not lose its per-frame leased binding.
Never bloom portal/window/mirror transport or raw screen textures. Never sharpen
the scatter. Every diagnostic except the bloom-only view bypasses optical scatter.

`Shared/bloom-filter.hlsli` uses cell-edge reflection and conservative cell
integration. Unit-sum taps alone only preserve constants: edge clamping duplicated
a corner impulse's energy, and point resampling odd levels changed their mean.
Keep the constant, impulse and odd-grid witnesses in `BloomEnergyLawTests`; include
the final placement tent and FP16 storage. Fractional radii blend symmetric kernels
at adjacent integer widths, rather than combining their interpolation with the
resampling. Placement can minify the retained source envelope during a shrinking
layout transition. Integrate its entire footprint, including edge hats; the axis's
three cached pairs are not a tap limit. Keep the 2×, 4×, 10× and one-pixel placement
constant/impulse witnesses. Renormalizing truncated taps still discards energy.
`CameraBloom` is a value; `WorldBloomLawTests` covers on/off allocation.
Seat lens selection happens beside pose selection from the active endpoint's program.
`PlaceViews` derives optical placement from the resulting snapshots, including routed
seats and camera-mode overrides. Never infer it from unused boot-world programs.
Publish that demand for the next `BeginFrame` reconciliation. Reconfiguring from
placement mixes newly selected capture-fill/environment reads with footprints
already formed for the current frame and can make a capture refuse or crash.

Pin exposure and local adaptation for on/off captures, and record each EV with
`world.exposure`. Use `world.rate pause` to hold one simulation tick for the pair.

For a motion burst, arm it inside a sustained pan and inspect its reported ticks:
an eight-tick pan can finish before the first of eight asynchronous captures lands.

## Mesh pipeline limits

Draw selection reads the retained `SdfWorldTables` staged draw span, the same
records whose boxes and GPU records were uploaded. Never borrow the frame source's
mutable draw list across staging: a portal handoff can clear it while the retained
count still names the previous records.


The frame rasterizes baked geometry. `SdfCompositionFrameSource` allocates the
live transform table and reports an actual `[world.render] envelope`; it builds
no worst-case probe. `WorldRigidAssets` emits local creation templates once and
supplies `SdfMeshInstance` roots and identities. `SdfMeshPathBake.Dress` expands
the shared mesh into copies without program or palette duplication. Animated
creation fields use root and motion-owner deltas; CPU pose scratch remains per
actual shape. Bake groups keep separate bounds and detail even when they share
a motion slot; the lattice frame and instance selector are independent. Use
`boundInSlotFrame` for rest-pose offsets on a moving owner's slot; a world-axis
offset would move the bake's box away from the geometry when that owner starts turned. A skin
past 255 members throws before queuing, instead of attaching excess members
to the root. Volume overflow is explicit. Scope depth is 4, screen bindings 32,
and derived faces follow authored screen indices. `SDF_MAX_INSTANCES` bounds
one bake program, not a per-world render budget.

A retained separate bake group must still ride the newly planned `Slot`, even
when its instance selector and local geometry stay unchanged. Rigid draw poses
are picking metadata; `SdfMeshDraw.MotionIdentity` names the stable body/surface
for both whole-list and changed-record uploads. Rigid copies include the entity
address and pose-discontinuity epoch in that identity, so teleports and reseats
seed the previous mesh matrix at the new pose, including authored meshes.
Rigid root followers observe
portal carry history, reseeding when it expires. Isolation also filters rigid
templates, parented paints and volumes, text and authored meshes.

`SdfMeshLibrary` retains an age-ordered byte budget derived from available
machine memory, evicting oldest geometries rather than clearing the library.
Brick storage is allocated on its first bake/upload request. Measure draw/vertex
counts, actual transform rows, program/material bytes, region residency and
bakes; the lead measures frame times and edit-to-running on a quiet machine.

## Evidence-preserving diagnostics

`world.debug-view colliders|contacts` uses the beauty path through temporal
resolve, sky, glass, fog, exposure and the root tonemap/sharpen. Keep
`DebugViewModes.PreservesScene`, `sdfDebugPreservesScene` and the temporal epoch
key together. Diagnostic marks belong only to `AnnotationWriter.EmitDiagnostics`'s separately
reserved overlay channel; its masks protect every causal footprint, including
overflow beyond the sixteen visible pins. Focus removes chroma outside those
footprints without changing luminance. Keep masks exact rather than coalescing
them into spatial bins: those bins show as rectangular chroma islands in focus.
Beyond the mask reservation, conservatively protect overflow and leave focus
off. Place badges beside witnesses with short leaders; collisions overflow to
the report rather than forming a screen-wide leader band. Never paint a diagnostic into history,
the visibility buffer or lighting.

`WorldDiagnostics` separates collision-versus-authored-field from
field-versus-baked-mesh. The latter reuses the irradiance scene's retained
triangle hierarchy only when its exact draw records and delivered document
version match and the bake has settled. The client document is not necessarily
the server's object: compare `WorldDocumentVersion` by value, never their
definition references. `SdfMesh.BakeCell` comes from the actual
contour lattice, survives cache storage and material renumbering, and supplies
the hit triangle's half-cell-diagonal budget. No saved baseline or allowlist is
involved. A second `SdfWorldPicker` per instance asynchronously reads cluster
depth without stealing pointer requests; discard results across camera, mesh,
program or view changes.

`WorldDiagnosticGeometry` must read each compiled collider as physics does.
For `RoundedBox`, `Extent` is the inner box and `Radius` is its spherical
offset: sample its faces, edge fillets and corner fillets, then apply `Rotation`.
Distance queries inverse-rotate and subtract the radius after measuring the
inner box. Treating this kind as an unrotated sharp box creates metre-scale
false findings and also misclassifies buried union surfaces. Compare witnesses
with `FixedSurfaceQuery` and the contact narrowphase. Chamfered authored Boxes
can still yield real inward discrepancies from their conservative inside
colliders; neither the fillet nor the chamfer is an error-budget allowance.

Opposing planar face interiors of touching boxes are inside their union, not exposed collision boundaries; certify that local relation before comparing them with the exterior mesh. Edges and corners stay measured, except against the mesh where no free ball of the hit triangle's half diagonal reaches the witness (`WorldDiagnosticGeometry.OpensOnto`): the fillet groove along an edge three filleted boxes share is in the field and the colliders but under the bake's cell, and counts `enclosed`. Only exact collider distances may close such a void; a bound's blocks a ball only when its centre lies inside. Mesh diagnostics use `WorldDiagnosticMeshQuery` and the retained scene's
`TryNearestSurface`, not normal-ray hits. The nearest query reuses both levels
of the trace hierarchy and tests world-space triangle distances (object-space
nearest points are wrong under nonuniform scaling). It includes edges and
zero-distance witnesses. The search radius is four times the sum of
collision/arithmetic precision and the scene's largest bake half diagonal; only the returned
triangle's own precision enters its budget. A miss is unknown. Grounded checks
require the nearest retained support surface to be walkable; a missing or
unqualified hit is unknown too. `coverage.comparisons` counts red, clean and
unknown witnesses separately from causal findings. Never add a fillet, bound
or snap-reach allowance, or suppress authored-field findings to quiet the mesh
audit. The owning decision is [diagnostic evidence](../../../docs/decisions/rendering.md#a-diagnostic-view-never-covers-its-evidence).

Captures on the synthesized overlaid root retain the beauty image, annotated
image and JSON together. Attach the companion to `WorldRootGraph.OverlayInstance`,
which serves the screenshot, not `ComparisonLiveRoot`, which is the beauty
source. The capture companion waits for both display encoders;
its closure owns pixels and JSON before background encoding starts. Custom
authored roots need an equivalent beauty/overlay split before they can supply
a triplet. See [scene diagnostics](../../../docs/reference/commands.md#scene-diagnostics)
for commands, coverage and the GPU handoff checks.

## Where things live

| Area | Code | Explanation |
|---|---|---|
| Program model and ISA | `src/Puck.SignedDistance` (`SdfOp`, `SdfShapeType`, `SdfBlendOp`, `SdfDomainOp`, `SdfProgram*.cs`, `SdfProgramBuilder*.cs`, `SdfOpRoles`) | [program model](../../../docs/rendering/sdf/handbook/program-model.md), [Lipschitz](../../../docs/rendering/sdf/reference/lipschitz-and-field-correctness.md) |
| CPU interpreter and queries | `src/Puck.SignedDistance/Queries` (`SdfFieldEvaluator`, its `Bounds`, `Cull` and `Certificates` partials, `BakedWorldQuery`) | [queries and determinism](../../../docs/rendering/sdf/handbook/queries-and-determinism.md) |
| Mesh bake | `src/Puck.SdfVm` (`SdfMeshPathBake`, `SdfMeshLibrary`, `SdfMeshStore`, `SdfMeshRegionArena`); `src/Puck.SignedDistance/Baking` (`SdfSampledLattice`, `SdfDualContouring`) | [mesh bake](references/mesh-bake.md) |
| GPU engine | `src/Puck.SdfVm` (`SdfWorldResidency`, `SdfWorldTables.*.cs`, `SdfWorldPasses`, `SdfWorldPassRecorder`, `SdfWorldPipelines`) | [`Puck.SdfVm` README](../../../src/Puck.SdfVm/README.md), [frame rendering](../../../docs/rendering/sdf/handbook/frame-rendering.md) |
| Kernels | `src/Puck.SdfVm/Assets/Shaders/Sdf`: `isa/` (generated), `field/` (the interpreter the bake samples through: `mapCore` in `sdf-map.hlsli`, the part walk in `sdf-parts.hlsli`), `frame/` (the visibility record, the mesh tables, reprojection), `shade/`, `sky/`, `debug/`, and under `passes/` one `*.comp.hlsl` wrapper per dispatch plus the stage modules | [kernels](references/kernels.md) |
| Generated kernel declarations | `src/Puck.SdfVm.Model` (`SdfIsaHlsl`, `SdfRenderHlsl`, `SdfKernelInterfaces`, `SdfSkyKindsHlsl`) and `src/Puck.Shaders.Model` (`ShaderDeclarations`); written by `src/Puck.Shaders.Generator` before any kernel compiles | [sync pairs](references/sync-pairs.md) |
| Cameras and views | `src/Puck.SdfVm/Views`; `WorldViewInstances`, `WorldScreenBinder.*` | [motion and views](../../../docs/rendering/sdf/handbook/motion-and-views.md) |
| World data into frames | `src/Puck.World.Client` (`WorldFramePresenter`, `WorldSceneEmitter`, `WorldPlacementStamper`, `WorldCreationInstances`); `CreationStampEmitter` | `puck-world` skill |
| Shader packages, pipelines, render graph | `src/Puck.Shaders` (`RenderGraphRuntime`, `ShaderPipelineRenderNode`, `ShaderPipelineCompiler`), `build/Shaders.targets` | [shaders reference](../../../docs/reference/shaders.md), [runtime contracts](references/runtime-contracts.md) |
| Backends | `src/Puck.Vulkan`, `src/Puck.DirectX` and their `.Presentation` projects | [contributing: GPU support](../../../docs/development/contributing.md#gpu-support-and-shader-builds) |

Find the existing mechanism before adding one: `puck references`,
`puck declarations` and `puck search -M 0` (the `symbol-analysis` and
`content-search` skills).

## Which dispatch owns the code

A view is a chain of separate dispatches: `mask` → `bake` (only while the
residency's bake is pending: `sdf-mesh-bake-mask`, `sdf-mesh-bake`, the one
`mapCore` call site) → `shadow-near`, `shadow-far`, `shadow-second` (graphics,
the cascades) → `mesh` (graphics, in two occlusion phases with the occlusion
kernel between them, `SdfMeshOcclusion`) → `pyramid` (the ambient occlusion's
depth pyramid from the mesh target) → `surface` (each pixel's visibility record from the mesh
target: normal, screen-space AO, the cascades' soft shadows into K;
`passes/sdf-surface-stage.hlsli`) → `views` (materials and lighting) →
`resolve` (reduced or temporal views) → `sky` → `composite`. A view of a
program with a glass shape (`SdfProgram.HasGlass`) inserts `glass-clear` →
`glass` (graphics, the glass draws alone) → `glass-shade` after `views`
(`SdfWorldPackage.WithGlass`), and every later pass reads `glassLit` in the
lit image's place. The surface and
views passes share one head and entry (`passes/sdf-pixel-pass.hlsli`,
`passes/sdf-pixel-entry.hlsli`) and call no field query. The table in
[kernels](references/kernels.md#the-frame) says what each writes.

- **AO and soft shadows are estimated in the surface pass and filtered in
  views.** The estimates (`sdfMeshAmbient`, `sdfMeshShadow` and their shared
  4×4 tap pattern `sdfMeshPattern`, `passes/sdf-surface-stage.hlsli`) are the
  surface pass's, written into the visibility record; views only averages them
  over a 4×4 window (`sdfViewsFilter`, `passes/sdf-views-stage.hlsli`) before
  shading. A wrong occlusion or shadow value (a dark band, a missing crease,
  acne) is the estimate's, so an edit to the views lighting code changes
  nothing; the window and the pattern's tile are a pair. A side turned from a
  light is never queried: its slot holds `SDF_SHADOW_UNQUERIED`
  (`frame/sdf-shadow-visibility.hlsli`), which decodes as fully visible, and
  the window's shadow average takes only queried pixels (`sdfShadowQueried`).
  An unmeasured slot averaged in lights a one-pixel line along every
  terminator and rounded edge the cascades shadow (indoors, a cosine just
  above zero under the 100 klx sun), and no debug view shows it, since
  `shadow` shows the average without its cosine. The average also leaves out neighbours whose normal
  turns away, so a crease's two lit faces keep their own shadows. A sunlit spot on a wall's top under a slab is the
  filter's (`sdfMeshShadowGap`): a tap counts the light hidden only inside the
  light's cone over the point, and the penumbra is the nearest in-cone
  blocker's. `world.debug-view ao`
  and `world.debug-view shadow` show the filtered values, and `world.ao` toggles
  the occlusion live.
- **Every raster pass culls draws by a host box** (`SdfMeshBox`, `SdfMeshCull`,
  applied in `SdfWorldPassRecorder.Choose`): a view's frustum, a
  cascade's light box and the receivers it shadows. A box is the mesh's
  position bounds through the draw's matrix and carry, so a draw whose vertex
  stage moves vertices any other way (members' slots, a displacement) must have
  no box (`SdfMeshBox.TryOf` returns false) or it vanishes while visible. A
  missing object that `world.cull off` brings back is the cull's;
  `gpu.vertices` in `world.counters gpu` counts what each pass draws. The same
  box chooses each kept draw's level of detail (`SdfMeshDetail`): the view's by
  its error in display pixels over the box's nearest depth, with the 1.1-pixel
  band kept per draw in the recorder, a cascade's by its texel. A draw with no
  box draws its merged mesh, so a skinned body never coarsens. A shape that
  changes when `world.detail 0` is set is the level's.
- **The mesh pass also culls by occlusion** (`SdfMeshOcclusion`,
  `passes/sdf-mesh-occlusion.comp.hlsl`, the default `world.cull occlusion`):
  phase one draws the previous frame's visible set through a counted indirect
  draw (`IGpuRecorder.DrawIndirectCount`), the kernel builds a farthest-depth
  pyramid from the target's fourth channel (forward depth) and tests every kept
  box, phase two draws the newly visible over phase one's target and depth. The
  recorder moves the mesh target between the phases itself and returns it in
  its attachment layout. The early occlusion dispatch binds a sampled filler;
  only the late set binds the target after its transition. Vulkan requires the
  descriptor's image layout even when the selected kernel branch never samples
  it, and rewriting one shared set changes both recorded dispatches.
  Draws a kernel issues are counted on the GPU past the
  counter rows (`GpuKernelCounters.DrawnWords`), so `gpu.draws` and
  `gpu.vertices` include them. An object `world.cull frustum` brings back is the
  occlusion's. The vertex stage's draw is pushed index plus `SV_InstanceID`
  (`sdfMeshRasterDraw`): keep the instance term, Vulkan's indirect draws carry
  the draw there.
- **Reprojection interpolates displacement.** `sdfPreviousPoint` in
  `frame/sdf-reprojection.hlsli` adds the triangle's weighted vertex movements
  to the current hit. Unchanged vertices return that hit exactly before any
  barycentric calculation: a long, thin triangle's float Gram determinant can
  cancel to zero, and rebuilding a second world position can invent motion on
  a still surface. `SdfReprojectionDeviceLawTests` includes this thin-triangle
  witness on both backends. Check the static `motion` view when history fails
  to accumulate; unchanged geometry must show valid, zero object motion.
- **A receiver's depth belongs to the output ray.** Different jittered rays
  hitting one grazing plane can have very different ray distances. Project each
  tap's tangent plane onto the output pixel's unjittered ray before storing or
  validating its receiver depth (`sdfHistoryReceiverDistance`). Identity and the
  relative depth tolerance stay unchanged. The reprojection device witness
  maps two samples at distances 64 and 32 onto the same receiver depth 128.
- **Stationary reconstruction keeps a complete jitter window.** The resolve's
  history surface retains each phase's color, coverage, transport and weight.
  Replacing one phase and summing in fixed order removes periodic newest-phase
  bias and keeps samples the current neighborhood misses. Moving and reactive
  pixels use the clipped resolve while their window fills. A stationary window
  keeps its validated receiver while the footprint still sees it; choosing a
  new thin adjoining face each phase can reject the window on the next phase.
  The window describes an output footprint, which can sample different receiver
  identities on opposite jitter phases at a static silhouette. If ordinary
  receiver validation rejects it, retain the bounded window only after proving
  the unjittered camera is exactly unchanged, every tap is nonreactive, and each
  visible tap's previous point equals its current point. This extra motion check
  runs only for rejected footprints. A displaced camera keeps ordinary receiver
  rejection; a stationary current receiver alone does not prove no disocclusion.
  The package owns
  `TemporalPeriod` and `HistorySurfaceWords`; the generator carries both into
  HLSL. A layout change needs a host with the matching history allocation before
  loading its kernels. Account for this output-sized history in GPU memory.
  Preserve a constant coverage component exactly before half packing and after
  averaging the phases: bound the convex mean by its samples. A rounded value
  just below one becomes 0.9995 in half storage and invents a background share
  on an opaque surface. The analytic resolve device witness checks full coverage.
- **Coincident exposed faces cannot accumulate a stable receiver.** Check
  `world.debug-view material-id` when a static patch changes identity or never
  completes its phase window. Separate meshes sharing an exposed plane can
  alternate winners as jitter or a refresh changes rasterization. Fix the
  authored overlap, rather than weakening receiver rejection. A slab owns its
  horizontal finish; a wall or lintel meeting it ends at the slab's underside.
- **A seat's character fade is view-local.** `SdfViewSnapshot.StampFade` supplies
  a transform-slot range and opacity through `SdfFrameBlock`; the mesh and glass
  fragments call `frame/sdf-stamp-fade.hlsli` before writing depth or glass sums.
  Cache new view-only offsets in `SdfFrameBlock.ViewOffsets`, outside the outer
  type's initializer reached by `WriteMeshBake`, so they do not invalidate meshes.
  Keep the opaque fragment free of `earlydepthstencil`: discarded pixels must
  reveal the room. Shadow passes and independently filmed mirror/portal views
  receive no fade. Vulkan requires `shaderDemoteToHelperInvocation` at device
  creation and capability 5379 in `VulkanShaderCapabilities`; `clip` compiles to
  that feature even when the live opacity is one.
- **Every light answers through one interface,** `shade/sdf-light.hlsli`; a new
  light kind is a branch there and nowhere else.
- **Cel shading is an optional material response, not a whole-image filter.**
  `world.toon` and `render.toon` feed `SdfFrame.Toon` through the generated pass
  block. `shade/sdf-toon.hlsli` shapes lights; `sdf-toon-outline.hlsli` reads
  depth/normal edges in views, before temporal resolve. Keep screen pictures,
  portal pictures, sky and self-emission out of both the banding and ink. Nested
  worlds take the live enable override but retain their own document tuning.
  The tuning belongs to the lighting cadence signature, never the bake closure.
- **The frame shades luminance in nits, and each view's composite applies its
  exposure** (`SdfPhotometry`, `SdfViewExposures`, the pass block's `exposure`).
  A light record carries illuminance or intensity over π; emission, sky layers
  and displays are nits. A new constant meant as a display colour (an outline,
  a grid, a placeholder glass) is divided by `passGroup.exposure` or it vanishes
  outdoors and blows out indoors. A window's view and a sky layer's view publish
  nits under the window share of their exposure (`SdfViewSnapshot.Unexposed`,
  `SdfPhotometry.WindowAdaptation`), and the opening applies the rest of the
  viewer's. A point or spot light's falloff is exactly zero at its range, each
  view shades only the lights its frustum may reach (`SdfLightSelection`, the
  pass block's `lightMask`), and a static one is occluded by the irradiance
  volume's visibility bits (`SdfLight.IsTraced`, `sdfMeshLightVisibility`): a
  fixture that lights through a slab is an anchored light or a volume that
  holds no probe there. `world.exposure` reads each view's EV and meter.
- **The irradiance volume is read once a pixel** (`sdfMeshProbesAt`), and that
  gather supplies indirect light, reflections and traced static-light visibility.
  Each probe publishes its own measured cubes, without neighbour filtering.
  Visibility uses a 12×12 octahedral first-hit surface map, one bounded ray
  per texel. Each word packs ray distance and two signed normal bytes;
  negative distance marks a measured miss. Four reflected angular taps reconstruct compatible surface patches before
  testing signed receiver gaps and blocked coverage. Radial depth interpolation rejects
  coplanar receivers at grazing angles, so no mean/squared-distance pair remains.
  Keep `SdfMeshProbeDepth.Visibility` and `sdfMeshProbeDepthVisibility` together.
  The sky cube comes from the same full-reach radiance rays as bounced light.
  Surface support stays within the angular taps; no neighbour vetoes or suspect sets return.
  The first sweep caches FP16 normal gradients from each texel's local angular
  neighbourhood. Interpolate compatible quadratic coefficients and intersect
  their entering root; a tangent alone shadowed
  the visible side of sparsely sampled curved geometry. The sparse-curve law
  checks against exact mesh segments. No triangle-footprint clipping is used.
  Gather weights are trilinear share × a half-spacing smooth distance fade in front of the receiver × depth
  visibility. The actual receiver is biased by `NormalBias` metres, never by
  spacing; clamping the lookup must not move the visibility-test receiver.
  The volume has three nested levels (8 m and 32 m cells past the tier's
  window); a receiver reads the finest level holding it, and where none of that
  level's probes measured it, the same probes answer past their reach, blocked
  only by surfaces they measured, with no traced static light. Nothing a camera
  sees reads an unmeasured surface as black.
  Relocation (`SdfMeshIrradiance.Place`) keeps a probe clear of geometry within
  its own cell; every lookup uses its recorded offset. Placement takes the nearest clear exit; its short rejection rays
  stop at one spacing, with no openness score. Debug with `world.probe` after bakes and GI settle;
  its exact reference segment distinguishes sampling errors from cube content.
  Local adaptation consumes this same gather, so an irradiance error also
  changes exposure. See [mesh GI](references/mesh-gi.md) for sampling, storage,
  boundary behavior and the fixed-camera checks on both backends.
- **Glass is a material, a group and a pass, never a blend.** A palette slot's
  `glass` (`SdfGlass`, material row 21) makes its shapes bake into groups of
  their own (`SdfMeshBakeGroup.Glass`; the stampers emit them as instances
  apart from the opaque ones) and draw in the glass raster pass over the opaque
  image (`passes/sdf-mesh-glass.frag.hlsl`, `passes/sdf-glass.comp.hlsl`). The
  mesh pass, the cascades and the irradiance trace skip glass draws
  (`SdfMeshDraw.Glass`). Thickness is the glass sums, signed ray distances the
  raster accumulates with atomics (`frame/sdf-glass.hlsli`): never read a glass
  shape's thickness from its mesh. One glass layer a pixel; glass through glass
  is the opaque image. The handbook's
  [glass section](../../../docs/rendering/sdf/handbook/frame-rendering.md#glass-after-the-opaque-image)
  states the limits.
- **Camera history uses the camera's sample grid.** The first recorder can be
  a shadow cascade, so `TemporalOf` receives the recording's `RenderWidth` and
  `RenderHeight`, never its pass-local `Width` and `Height`. A still camera's
  `world.debug-view motion` stays stationary with shadows both on and off.
- **A settled capture holds its residency's frame.** Under
  `world.debug-view motion` the held frame keeps the motion it was presented
  with (`SdfWorldTables.HoldsFrame`, the `held` argument of
  `SdfTemporalHistory.Prepare`); every other view settles it as a still frame,
  so a temporal view converges over the held renders. Settling motion history
  on a held upload makes every capture of the motion view read still. A frame
  held for a settled capture also culls by box rather than by the occlusion
  test and rates no work (`WorldFramePresenter.CullOf`/`RatesOf`), so the still
  owes nothing to earlier frames' visible set or rated updates; under
  `world.lockstep` every frame also presents the completed tick and advances
  presentation by the ticks completed, and its frames (`SdfFrame.TickLocked`)
  have the residency trace the irradiance window to the end before rendering
  (`SdfMeshIrradiance.Stage`; the asynchronous trace otherwise lands probes at
  wall-clock moments as the window follows the first view's camera) and adapt
  exposure over the frame's own presentation time
  (`SdfViewExposures.SecondsOf`); an ordinary settled still under lockstep
  converges over one fresh jitter period (`FrameCaptureRequest.ConvergeOver`),
  since without it a temporally resolved view's still depends on how many
  frames the display rendered before the hold (five stills of one paused tick
  differed by up to 141 levels on 12-17% of pixels). Together these make stills
  of one tick repeat across Worlds to a 1-level per-render residue.
- **A named-camera layout slot reconstructs; a screen's camera does not.**
  `world.temporal` reaches every view `WorldFramePresenter.ViewQuality()`
  dresses: seat views, the operator pose and `views.layouts` slots that name a
  camera. A camera view a screen films and a session view take a reduced
  quality (`WorldScreenBinder.CameraViewQuality`,
  `WorldSessionSceneEmitter.ReducedQuality`) whose `Temporal` is off, and
  `SdfViewQuality.Restrict` ANDs it, so they never jitter.
- **A settled capture cannot show what changes between frames.** Flicker
  (jitter moiré on a screen, a still scene whose pixels change), ghosting and
  trails show only in a presented capture (`FrameCaptureMode.Presented`:
  `puck_capture_frame` with `mode: "presented"`, `frames: 8`, or
  `world.screenshot <path.png> presented 8`), which holds and settles nothing
  and reports each frame's changed pixels and luma change against the one
  before. A still scene with `world.temporal on` that changes in a presented
  burst is flickering; a clean settled still proves nothing about it.
- **A `views.graphs` pane is not an SDF image.** It is a render-graph instance
  with its own shader; it reloads with `pipeline.reload`, not
  `world.shaders.reload`.

## Editing kernels

- **Check screen eligibility before reading a screen table.** A material is
  not a screen index: `sdfScreenSurfaceShades` checks the sentinel, bounds and
  source before `material - SDF_SCREEN_MATERIAL - 1` names a screen. Temporal
  ray helpers need that check before their own table reads too; a later sample
  function's guard cannot protect them. An ordinary material becomes a huge
  unsigned index otherwise, which can lose the Vulkan device while Direct3D 12
  returns zero for the out-of-bounds read.
- **One `mapCore` call site.** The bake (`passes/sdf-mesh-bake.comp.hlsl`) is
  the only GPU kernel that walks the field, and it does so through one rolled
  `[loop]` over its samples. Every call site is a full inlined copy of the
  interpreter, costing register pressure, compile time and a driver translation
  on every cold boot, so more samples go through that loop, never through a new
  call. Never add `[noinline]`: a real SPIR-V call loses the device on NVIDIA's
  Vulkan driver.
- **Keep each pixel kernel's include closure its own.** A pixel kernel includes
  the common head (`passes/sdf-pixel-pass.hlsli`), only its own stage module,
  then the entry; a stage module includes what it reads beyond
  `passes/sdf-world.hlsli` itself. The shader cache keys, and a reload
  recompiles, by include closure, so routing a stage module through another
  wrapper makes an edit to it recompile both kernels.
- **The bake kernels include `passes/sdf-bake-world.hlsli`, never
  `sdf-world.hlsli`.** Their compiled bytecode keys the stored meshes
  (`SdfMeshBakeIdentity`), so their closure holds only what the bake reads:
  their own interface (`isa/sdf-mesh-bake.interface.hlsli`: a pass block of
  `SdfWorldPackage.BakeValues` alone, stamped with the field's fingerprint), the
  field interpreter and the field's generated vocabulary (`isa/sdf-isa.hlsli`).
  A light, exposure, view, pass-block value, pass resource or World table goes
  in `isa/sdf-render.hlsli`, the world interface or after
  `SdfWorldPackage.FieldTables`, and leaves the bake's bytecode byte for byte as
  it was on both backends. SPIR-V orders its constants by first use in the whole
  source, dead code included, so a lighting, screen or view module in the
  closure would move a stored mesh's key. Add to the bake's closure only what
  the bake reads, and check with `puck mesh identity --against`.
- **Keep control flow uniform around barriers and groupshared gathers.**
  Inactive lanes still reach the barriers.
- **Hot reload compiles kernel sources only.** With `Puck.World` running:
  `world.shaders.reload src/Puck.SdfVm/Assets/Shaders/Sdf`, then
  `world.shaders.status` (`unchanged` means no shipped kernel compiles the code
  you edited). A host ABI, buffer-layout or C# ISA change needs a rebuild: the
  reload keeps the previous kernels when a tree's kernels do not match the
  host's interface, so a kernel reading a field the C# side just gained keeps
  running its previous build. Change the C# layout and the HLSL layout together
  ([sync pairs](references/sync-pairs.md)).
  Mesh raster and cascade vertex/fragment stages are composition-owned (`SdfMeshRasterPass`), so
  edits to them need a rebuilt boot too. A shared `frame/sdf-mesh.hlsli` edit can reload its compute
  readers while the raster stages keep their deployed bytecode; a successful reload is no proof
  that a vertex-stage performance experiment took effect.
- **No signed `%` of a value that can be negative.** NVIDIA's Vulkan driver
  answers a signed remainder (`OpSRem`, which DXC emits for `%` on `int`) of a
  negative operand wrongly where Direct3D 12 answers it right: lift the value to
  non-negative and wrap it as `uint`, as `sdfMeshIrradianceSlot` does.
- **One walk in `mapCore`.** NVIDIA's Direct3D 12 driver on Turing (the RTX
  2060) takes a second walk chosen by a program-uniform flag (a linear
  all-segment walk beside the instance merge) for instanced programs too, so
  every bake group samples the whole program; Vulkan on the same card does not.
  A program with no instance lists every segment as a world segment, so the
  merge covers it. When one backend's bake disagrees, compare
  `[sdf.mesh-bake] done` on both: a group that empties on one backend alone (an
  axis line under the floor) is the walk ignoring its mask.
- **Index local arrays by constants only.** NVIDIA's Vulkan compiler keeps a
  dynamically indexed local array, a `static const` table included, in
  per-thread local memory. Unroll the loop to the array's length and guard the
  body (`if (i < count)`), or pick the element by comparison; DXC's SPIR-V
  unroller leaves a loop with a `break` rolled. RenderDoc's pipeline-executable
  statistics show the spill as "Local Memory Size" (the low 32 bits).
- **Bindings are generated.** No kernel declares a binding or register by hand;
  a new resource is a member of `SdfKernelInterfaces`.

## Changing the instruction set

First ask whether the new op, shape or blend composes from existing vocabulary;
if it does, ship it as a `SdfProgramBuilder` method emitting existing
instructions. A real new instruction touches every partner in one change, and a
GPU parity pass alone does not finish it:

1. **C# model.** The enum, `SdfProgramBuilder` (its `RequireDefined` maximum),
   `SdfProgram` validation and packing, the Lipschitz analysis, its row in
   `SdfOpRoles.Of`, and the part-program key for a new parameter.
2. **Cull margins.** `MaxSmoothBlendRadius` (blend halo), `MaxScopedFieldReach`
   or `HasUnmaskableInfluence`.
3. **Generated declarations.** `isa/sdf-isa.hlsli` is generated from the C#
   model by `SdfIsaHlsl`; building `Puck.SdfVm` regenerates it, and
   `puck shaders generate` writes it on demand. The define's name is the enum's
   prefix plus the member in upper snake case (`SdfOp.CellDisplace` is
   `SDF_OP_CELL_DISPLACE`), and its value is the member's: members are numbered
   densely in declaration order. Never hand-write a `#define` for an ISA value;
   add the enum member and regenerate. Give the instruction a call in
   `SdfEncodingProbe` that passes every field it packs
   (`SdfEncodingProbeLawTests` refuses one that is missing). Regenerating also
   rewrites `SdfIsaFingerprint.cs`. `sdf-isa.hlsli` is the field's vocabulary
   alone, and its fingerprint keys the bake: a constant only the renderer reads
   (a light, the exposure, the visibility record, mesh records, the debug views)
   is declared in `SdfIsaHlsl.DeclareRender`, which writes `isa/sdf-render.hlsli`.
4. **Every GPU call site.** `mapCore` (rigid-leaf fast paths included) and the
   compiled part walk in `sdf-parts.hlsli`; a blend also needs `blendShape` and
   the material-winner rules in `sdfComposeCandidate`.
5. **CPU interpreter.** `SdfFieldEvaluator` interprets it or refuses it by name.
   Its blend switch falls through to union, so a missing arm silently turns a
   new blend into a union in contact and queries. Add its bounds rule
   (`SdfFieldEvaluator.Bounds.cs`) and cull rule (`SdfFieldEvaluator.Cull.cs`).
6. **Document surface.** Carry the parameters through `CreationCanonicalizer`
   and the stamp emitters or refuse the value there, then `puck schema`.

When two lanes both add an instruction, the merge conflicts in generated files
(`sdf-isa.hlsli`, `sdf-render.hlsli`, `SdfIsaFingerprint.cs`): resolve the C# model, then
regenerate with `puck shaders generate` or a build of `Puck.SdfVm`. Never
hand-merge a generated file; `puck shaders generate --check` (and CI) only
compares and fails naming the file that drifted, it writes nothing.

## Field contracts that bite

- **One accumulator.** `mapCore` carries one running distance for the whole
  program. An intersection-family blend annihilates every earlier shape it does
  not overlap; field ops (`Onion`, `Dilate`, `Displace`) grow every earlier
  solid once the accumulator holds more than one object.
- **A subtraction is exact only where its subject is nearest.** Inside a carved
  void the contact field reads phantom surfaces; extend the carve past every
  point a body can reach, or build the void from union geometry.
- **An instance bound is an influence sphere** tested per sample. It must cover
  the primitive's reach, its field ops and its blend halo, or the bake clips the
  geometry at the sphere.
- **A field scope is a real per-sample cost.** Scoped segments skip the segment
  early-out and rigid planning. Never wrap one primitive in a scope for its
  Lipschitz factor; make the primitive 1-Lipschitz. Scope clamps
  (`SdfProgram.FieldScopeClamps`, `world.budget`) are field bounds, not measured
  GPU cost.
- **Unbounded is a state, not a number** (`SdfBoundAlgebra.Unbounded`); bounds
  compose through the set operations in `SdfBoundAlgebra`.
- **Deterministic versus presentation geometry:** use
  [sdf-authoring](../sdf-authoring/SKILL.md#render-only-versus-deterministic);
  the fixed-point evaluator supports `SdfShapeType.Path` through `SdfPathSolid`.

## Capacity and emission

- Program words and instances grow on upload, and the dynamic-transform region
  grows to the frame's table, whose rows are the program's slots plus one root
  per rigid copy (a body), so a `world.reload` or a new body grows it mid-run.
  A frame that supplies fewer transforms than
  `RequiredDynamicTransformCapacity` throws, because a slot rendering at
  identity is a bug. Fix the emission so the frame supplies the transforms it
  needs; increasing a reserve cannot supply missing transform rows.
- A `GpuRegion` grows under whichever policy `GpuResidency.Select` gave it
  (`GpuRegion.Grow`): a staged region carries its destination on the GPU, and a
  ring or in-place region replaces its host-visible buffers and owes each the
  whole region; the owner retires what it returns after the following upload's
  fence, which also covers earlier readers and a staged carry. Create replacement
  buffers, retirement bookkeeping and the CPU shadow before publishing growth;
  a failed allocation preserves the old buffers, contents, capacity and bindings.
  `SdfWorldTables.EnsureDynamicTransformCapacity` prepares motion history before
  growing the region and publishes capacity only after both succeed. A device with
  a large host-visible device-local heap (resizable BAR, as on the lead machine under
  both backends) gives a small per-frame table a ring, while the CPU fake
  device's default profile stages every region, so a region path written or
  tested for one policy alone passes the device-free suites and fails on the
  lead machine. Test a region path under every policy, as
  `GpuResidencyLawTests.ARegionGrowsUnderEveryPolicyAndEverySlotReadsItExact`
  does.
- Large GPU buffers give their memory back. Both arenas (`DirectXHeapArena`,
  `VulkanMemoryArena`) free a resource's own heap (one past half a shared
  heap) as it empties and keep only a shared one spare; a kept large heap takes
  later small buffers and is pinned for the run. A staged `GpuRegion` slot's
  staging buffer shrinks to twice its flush (`GpuRegion.StagingFloorBytes`
  floor) once it holds four times more, and a relocated mesh region shrinks to
  its need (`GpuRegion.Shrink`). Upload heaps are system memory: a staging
  buffer kept at a whole region's size costs the process that much working set.
- The mesh region keeps no host copy of its meshes. Its host copy is the draw
  records alone (`GpuRegion.Shadow`); a placed mesh's words are owed without a
  compare (`GpuRegion.OweSourced`) and the upload's flush writes them from the
  `SdfMesh` arrays (`SdfWorldTables.WriteSourcedMeshWords`, an
  `IGpuRegionSource`). The irradiance scene likewise reads its triangles through
  each mesh's positions and indices, never a copy. A new consumer of baked
  triangles reads the `SdfMesh` arrays rather than copying them: the debug
  world's meshes are about 1.1 GB of managed arrays, and every copy costs that
  much again in working set.
- A scoped creation emits one instance, a scope-free one an instance per shape
  (`CreationStampEmitter.PerCopyInstanceCount`). `world.budget` prints the live
  cost sheet.

## The baked mesh

Every view renders meshes the program is baked into, with no field walk in the
frame. Read [mesh bake](references/mesh-bake.md) before changing the bake, the
contour, grouping, the mesh region or the store, or when a baked mesh looks
wrong. The contracts that bite most often:

- **One contouring:** `SdfSampledLattice` through `SdfDualContouring`; never
  write a second mesher.
- **A landed mesh is its planar polygons** (`SdfMeshPlanarMerge`, in
  `SdfMeshPathBake.Land`): a flat face's interior vertices go and every outline
  vertex stays, so no pixel changes. A change that moves or renormals a vertex
  there, or drops an outline vertex, does change pixels.
- **A landed mesh carries two coarser levels** (`SdfMeshCollapse`, after the
  merge in `Land`; `SdfMesh.Levels`): half-edge collapses over the mesh's own
  vertices, each with its measured error. The region lays a level's indices and
  materials after the merged ones', so its triangles are numbered after them. A
  draw pushes its level above its index (`SdfKernelInterfaces.MeshLevelShift`,
  in a counted indirect draw's identity too), its record holds each level's
  first triangle (`SdfMeshRecord.LevelTriangleWord`), and both raster vertex
  stages add it to the vertex id (`sdfMeshLevelIndex`). Never pass the level as
  a first vertex: Direct3D 12's `SV_VertexID` counts from zero whatever the
  draw's first vertex, so the draw fetches the merged mesh's first triangles and
  objects go missing. The surface pass reads the triangle the pixel names with
  no level of its own. Everything that reads `SdfMesh.Indices` (the
  irradiance trace, the audit, the diagnostics' nearest query) reads the merged
  mesh, level zero. Each pass's choice is `SdfMeshDetail` beside the box cull, in
  `SdfWorldPassRecorder.Choose`; `world.detail 0|1|2` forces one level
  everywhere, and `world.detail auto` restores the choice.
- **Large static unions have independently drawn chunks** (`SdfMeshChunks`, before the merge). Their contour edges
  partition the surface, and every seam edge stays fixed at every level. The store holds the pieces; only those pieces
  enter the region. See the [mesh bake](references/mesh-bake.md#groups-poses-and-materials).
- **A field diagnostic is a bake lattice, never a pixel-kernel walk.**
  `SdfFieldSlice` (`world.slice`) queues points lattices with gradients on the
  bake and draws the distance bands and `|grad d|` on the CPU from the answers.
  A per-pixel field view would put a second interpreter copy in a pixel kernel.
- **Winding is one contract across three places.** The bake winds outward
  faces counter-clockwise (`SdfDualContouring`), both backends declare a
  counter-clockwise face front (`GpuGraphicsPipelineDescription`, the two
  pipeline factories), and the opaque mesh pass culls back faces
  (`SdfMeshRasterPass.Description`; the shadow and glass pipelines cull
  nothing). A mesh not from the bake is drawn in both windings
  (`WorldPlacementStamper.MeshOf`). Probe facing with `SV_IsFrontFace` in the
  mesh fragment stage and `world.debug-view depth`, on both backends.
- **A mesh is a function of its geometry.** Groups are keyed by
  `SdfMeshGeometryBuilder`; anything the bake samples that the instructions do
  not hold leaves a stale mesh drawing after an edit until the builder hashes
  it.
- **Baked meshes persist across runs** (`SdfMeshStore`), keyed by geometry and
  the bake's identity: the bake kernels' bytecode and the IL of every method
  the bake's code reaches, across the `Puck` assemblies, read from the build
  (`SdfMeshBakeClosure`). No list names the bake's files: code it calls is
  covered, code it does not call is not, a checkout's path is not, and a miss
  logs the part that changed (`[sdf.mesh-bake] miss …`). A hot-reload update to
  a type the closure declares members of folds into the code identity
  (`SdfMeshBakeClosure.Reads`, `CodeRevision.AppliedTo`), and the residency
  follows it before each plan and stage; an update anywhere else keeps the
  store. `puck mesh identity
  --build <dir> --against <dir>` names the members that differ between two
  builds before any boot.
- **`puck mesh audit --world <file>` checks a bake without a GPU or a person
  looking**, against the CPU field; `--cpu` bakes offline so a contour or field
  change shows with no boot. Run it before calling a bake change done.

## Performance and cost

Judge cost by counted work, code and disassembly; a wall-clock or GPU-timestamp
reading is evidence beside the counts of the same run on a quiet machine, never
the verdict alone.

```text
world.cadence off      # a still scene otherwise skips frames and reads near zero
world.rates off        # far or small work (far cascade, small windows, screens, bodies) otherwise updates at least 30 or 15 times a second
world.debug-view rates # tint each rated item by its tier; world.rates lists each one's size and tier (worlds/debug/range.md)
world.counters gpu     # per-pass counted work: dispatches, shape evaluations, texels, uploads
world.gpu-timing on    # per-pass timestamps; `world.gpu-timing timeline` orders each node's latest span on the queue's clock with the idle gap before it
world.budget           # program words, instances, scopes, segments
```

`world.counters gpu` runs to hundreds of kilobytes in a world with many graph
instances, past the 1 MiB an MCP result carries, so ask for what you need:
`world.counters gpu summary` (one `draws vertices texels dispatches` line per
node), `node sdf:world` (a node and the nodes under it), `pass sdf.world$mesh`
(a pass label, or its prefix by whole segments, in every node that has it; it
drops the lifetime, owned-bytes and outside lines) and `counter vertices` (a
count-name prefix). They combine, and `--json` takes them too. A text reading
past `WorldCountersCommandModule.GpuTextBudget` characters prints the summary
under a note. A pass label is not a node name: `node sdf.world$mesh` is refused
with a hint to use `pass`. The counts are read back a few frames late: the first
reading after a camera pose or a lever change can still show the previous
frames' work, so read twice and keep the second. A settled capture's held frame
culls by box alone, so a reading taken just after one shows the mesh pass
without the occlusion test.

Attribute shading cost by toggling the live levers (`world.shadows`, `world.ao`,
`world.indirect`, `world.render-scale`) and isolate the raster with
`world.debug-view depth`. Compare the whole frame, not one pass. `puck counters`
boots a workload on both backends and `puck counters compare <before> <after>`
holds two reports to each other; a deterministic count must agree on both
backends. `world.debug-view` lists the diagnostic images. For a frame-time bar,
`host.frames` on the windowed host gives produce, simulate and their sum per
iteration (avg, p50, p99, max) and the worst iterations split into their
phases (simulate, begin, produce, present, wait) with their collections and the
pacer's lateness ([Puck.Launcher](../../../src/Puck.Launcher/README.md)).

- **A window whose extent swings rebuilds on a backoff.** A window a moving
  camera crosses (the endless fall's floor and ceiling paintings) requests a new
  extent every few frames; a resize build the request outran is discarded, and
  each discard doubles the advances the node waits before the next resize build
  (at most 32), cleared by an install (`ShaderPipelineRenderNode.Build.cs`,
  `AnExtentSwingingFasterThanItsBuildsBacksOffAndASettledOneInstallsAtOnce`).
  Without the backoff such a window builds and discards a graph every frame.
  Holding a window's larger allocation instead (a shrink delay in the
  scheduler's footprint quantisation) keeps full-resolution windows rendering
  and makes the fall GPU-bound at 30 Hz.
- **A program's bake plan is made on its build thread.** The composition
  source hands each program its background build finishes to
  `ISdfFrameSource.ObserveBuilds`, the residency plans it there
  (`SdfMeshPathBake.PlanAhead`), and the first frame that draws it re-plans only
  the groups it cannot keep (`SdfMeshBakeGroup.Refresh`). Editing either file
  changes the bake identity: check `puck mesh identity` before booting.
- **Static placement emissions survive program rebuilds.** `WorldStaticPalettes`
  keeps each immutable row's `SdfProgramBuilder.Emission`: instructions and
  profile tables, plus its volumes and mesh draws. A response emits the swapped
  rows alone. The cache also checks the prototype, palette ids and extent,
  resolved frame, text catalog and isolation mask. Retained recolor windows
  bind to the new builder's material scope; never retain the old builder through
  a scope. A same-sized mesh draw list stages changed records even when meshes
  swap, while the arena leaves existing mesh addresses standing.

## Seeing a change

- A lockstep frame waits for its composition's program build and its mesh bake.
  A completed mesh is still pending until `Dress` includes it: a load can finish
  between dressing and preparation, and testing only the worker would certify
  the partial mesh list. `IRenderGraphPackageFactory.WaitingOf` keeps a rendered
  package incomplete while its bake passes and readbacks continue. The host
  holds that tick; exposure adapts once the complete frame supplies its meter.
  A capture freezes the authored frame, then dresses newly completed meshes.
- Lockstep irradiance waits for both the current static scene's build and its
  probe trace (`SdfMeshIrradiance.Stage`). Waiting only for the trace can render
  no volume on the first frame, or the preceding scene on a replacement frame.
  The CPU irradiance law compares the first staging of each against a completed
  trace; looping staging calls until a write appears would hide that defect.
- An image source owns its extent even when a buffer graph consumes it. Propagate
  its demand without multiplying by the buffer consumer's zero pixel footprint
  (`RenderGraphScheduler`), or a cold conversion can finish building and never
  install. A package whose last frame is incomplete cannot stand unchanged
  (`RenderGraphRuntime.WithUnchanged`): its pending sources still need renders.
  A retained "building" reason alone does not prove a worker is still building;
  inspect the live schedule and completed build as well.
- Screen-light reproduction must compare source bytes, not just graph publication
  numbers. `MachineVideoSourceUpload` numbers uploads, while a queued machine's
  video read takes its latest completed native frame. Equal publications can
  therefore feed different images to `ScreenEmission`. Lockstep uses the existing
  synchronous machine advance before rendering. A fence wait, readback or GPU
  validation can mask this worker race by changing pacing; diagnose the CPU
  video bytes and native frame version before changing GPU barriers.
- Build: `dotnet build src/Puck.SdfVm -c Release -nodeReuse:false` runs DXC
  (needs `dxc` on `PATH`). A Windows build of one project builds DXIL only, and
  a World run of it refuses `--backend vulkan`; run Vulkan from a solution
  build or with `-p:PuckShaderSpirvEnabled=true`. A build of one suite under
  `tests/` builds SPIR-V (`tests/Directory.Build.rsp`). Shader outputs come
  from the per-user shader cache; never copy bytecode between trees.
- Run it and look: start a World with `puck_world_start`
  ([puck-world](../puck-world/SKILL.md#the-live-world-is-shared); `windowed: true`
  only for a granted GPU leg), edit, `world.shaders.reload`, capture, and end it
  with `puck_world_stop`. A claim about
  how something renders rests on an inspected capture; say which backends you
  looked at. A boot bakes the groups the mesh store does not hold; a reboot of
  an unchanged world loads its completed meshes, and an empty `--cache-dir`
  bakes all of them. A cold debug-world bake can span thousands of rendered
  frames, while simulation advances many ticks per frame. Before capturing the
  finished scene, use `world.wait bakes <seconds>` and require its settled
  result, then check for `[sdf.mesh-gi] done` in the log. A tick wait or
  `world.wait ready` alone does not establish that all meshes are present.
  `world.rate pause` also stops tick waits: several timing reads separated by
  `world.wait` then repeat the same completed GPU window. Use separate control
  requests spaced in wall time when measuring a paused scene.
- Device-free suites: `dotnet test tests/Puck.SignedDistance.Tests -c Release --no-build`
  after a `-nodeReuse:false` build (ISA packing, Lipschitz, bakes) and `tests/Puck.Shaders.Tests`. Cross-backend
  parity (`puck parity --world <file>`) needs a parity world with its contract
  beside it, and none exists while the debug world is the one live world; until
  one does, compare the two backends' captures and counts yourself.
- Capture fixtures in a sandbox without a desktop monitor must replace both
  the debug desktop graph and its screen producer with `source.color`, and
  remove that screen's `padPointer`. Offscreen hosting alone still tries to
  open the authored capture source. Use a private copy of the whole package
  with the same entry filenames: a renamed wrapper changes document identity,
  so garden/night back-references can instantiate another debug world. Keep
  device-machine screens intact and disclose the desktop substitution in the
  capture report. After a suit change, allow its rule to run and check the
  residency's `[sdf.mesh-bake] done` log before capturing with
  `world.wait bakes <seconds>`: a tick wait alone can show the old mesh
  stretched over the new rig. Clear an operator camera with
  `view.override camera auto` before switching to a following motion layout.
- GPU captures, device faults and the validation layers:
  [kernels](references/kernels.md#captures-faults-and-validation).

## References

| File | Read it for |
|---|---|
| [references/kernels.md](references/kernels.md) | The shader build, hot reload, the frame's passes, the visibility record, bindings, diagnostics, captures and device faults |
| [references/sync-pairs.md](references/sync-pairs.md) | Every C#↔HLSL coupling and which side is generated |
| [references/mesh-bake.md](references/mesh-bake.md) | The bake's contouring, groups, mesh region, store and `puck mesh audit` |
| [references/mesh-gi.md](references/mesh-gi.md) | Probe visibility, the volume boundary, CPU bounce sampling and exposure |
| [references/runtime-contracts.md](references/runtime-contracts.md) | The render-graph runtime's invariants, before changing `RenderGraphRuntime`, a recorder, a capture path or pacing |

## Route adjacent work

| Skill | Route there for |
|---|---|
| `sdf-authoring` | Sculpting creations: primitives, blends, palette, rigs, bake work and bytes. |
| `puck-world` | What world-document sections mean and console verbs' semantics. |
| `puck-dsl` | `.puck` grammar and the compile/lint verbs. |
| `maths-usage` | Fixed-point primitives for the query evaluator. |
| `dotnet-performance` | Host-side C# hot paths. |
| `verification` | The landing bar, GPU legs and how to read a failed check. |
