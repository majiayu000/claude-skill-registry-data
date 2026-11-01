---
name: sdf-authoring
description: "Authors creations: shape rows, primitives, blends, folds, palettes, paints, render lanes, rigs, bake work and bytes, creation stats. Use to sculpt or fix a part. Grammar: puck-dsl; GPU: rendering."
---

# Authoring a Puck creation

A creation is a `puck.creation.v1` document: a palette, a list of shapes, and
optional rig, motion, text, volume, and noise sections. Shapes are signed
distance fields composed by blends, not meshes: a cut is a subtraction, a
fillet is a blend radius, and repetition is a fold rather than copies.

**Where it lives.** On disk in a world document at `prototypes[].document`. The
console addresses those same rows as section **`creations`**, keyed by prototype
id: `world.row.set creations moth …` edits what the file spells
`prototypes[id=moth].document`. Read `references/loop.md` before driving it
live.

## The author frame

Every creation position, rotation, joint, pivot, axis, and camera offset is
authored in one frame that is a **180° yaw about +Y away from the engine's**:

| Author axis | Points |
|---|---|
| +Y | up |
| +Z | the front the subject faces, toward a front-facing camera |
| +X | screen-right as you look at that front, which is the subject's own **left** |

So a shape authored at +X appears on the viewer's right, on the character's left
side. Getting this backwards is the most expensive mistake in this surface, and
it looks like a correct sculpt mirrored rather than like a bug. The conversion
is exact axis negation, `(x, y, z) → (−x, y, −z)`, and it is its own inverse
(`src/Puck.World.Authoring/Authoring/CreationFrame.cs`). The frame is a document
fact: it applies identically in raw JSON and in a `.puck` shape row.

Scalars, camera yaw and pitch, and chain goal and pole do **not** convert.
Shape position, rotation, and joint convert; `curve.a/b/c` remain shape-local
and ride that converted pose. Repeat and polar fold origins do not convert, so
an author-space position `[x, y, z]` needs origin `[-x, y, -z]`
([composition](references/composition.md#domain-folds)). Palette
`inset.origin` and `inset.rotation` do not convert either: author them in the
shader's winning frame ([surface](references/surface.md#inset)).
[rig](references/rig.md#what-crosses-the-author-frame) lists every field.

## Authoring in `.puck`

`.puck` is the checked-in source for shipped creations:
`worlds/debug/avatars/moth.puck` sculpts the whole Moth as
`shape` rows inside `prototypes { prototype "moth" { document { } } }`. A shape
row is `shape Type "name" { field: value ... }`: array-valued fields take
brackets with no colon (`position [0, 1.02, 0]`, `scale [x, y, z]`), scalar
fields take a colon (`material: charcoal`, `exponent: softness`), and
`let name = value` binds a reusable constant; the Moth names its palette slots
this way (`let charcoal = 2`, then `material: charcoal`). `profile`, `domain`,
`swings`, `slides`, `panel`, `curve` and every other per-shape facet are
ordinary nested blocks with the same field names the JSON form uses. The
grammar, `let`/`template`/`for` and the CLI verbs belong to `puck-dsl`; load it
before writing `.puck` source beyond shape rows.

Check an edit offline before booting it, straight from the source:

```bash
puck compile <file>.puck --validate
puck creation stats --world <file>.puck --prototype <id>
```

`compile --validate` runs document validation: representation guards and the
panel/trim/cells creation-scope refusal fire here (PUCK030), over every
`prototypes[]` document whether or not a placement uses it. It does **not** run
emission or contact construction, so the Path contact refusal and a residual
nonuniform `Scale` on a solid placement pass it and fail only under
`creation stats`.
`creation stats`, `creation shape` and `mesh audit` read a `.puck` source
directly, compiling it in memory with its relative `basis` resolved from the
source's own directory; a compiled JSON copied elsewhere loses that basis.

`puck decompile` is one-way: it discards every `let`, `template`, and `for`.
Decompile once to import a hand-authored JSON document, then edit the `.puck`.

## The loop

A world booted with `--world <file>.puck` transpiles in memory
(`PuckWorldLoader`), and authoring against that live process needs no restart:

```
world.row.set creations <id> document.shapes[name=<shape>].<field> <json>
world.row     creations <id> document.shapes[name=<shape>]
world.wait    <ticks>
world.screenshot <abs-path.png>
```

`world.row.set` replaces a whole field: a vector such as `scale` or `position`
takes the full `[x, y, z]`, a rotation the full quaternion.
`world.row.step creations.<id>.document.shapes[name=<shape>].<field> <delta>`
steps a numeric scalar and refuses a vector. `world.row` reads the field back,
so confirm each edit with it. Edits land at the tick boundary, one per row per
tick. A `parent` carries only its animated delta, never its rest pose or
scale, so rescaling a parent moves no child: edit the children's base poses
too.

`world.reload` recompiles the `.puck` from disk (basis chain included) and
discards unsaved row edits; `world.save` writes each live edit into the source
that authors it (an imported file included), retaining unrelated text. A row
generated by a template or
a `for` can be edited live, but `world.save` refuses it by name: edit the
template or loop, or save to a JSON target whose `basis` names the source.

`world.screenshot` only **arms** a capture. Fence it with `world.wait` and
confirm the `[capture] … -> <path>` line on **stderr** before reading the file.
Read-backs land on stdout, refusals and capture confirmations on stderr, so
capture both streams. The verb surface, the offscreen recipe, and the sculpting
library are in `references/loop.md`.

## Choosing geometry

The vocabulary is much wider than sphere-box-cylinder, and reaching for boxes
when a profile or a warp would do is what makes a sculpt read as blocky. Start
from what you want the surface to *do*:

| You want | Reach for | Notes |
|---|---|---|
| A softly swelling mass, squarish or round on demand | `Superellipsoid` + `exponent` 2..8 | 2 is an ellipsoid, 8 is nearly a box; the sleek middle is 2.5–4 |
| A slab with a shaped outline | `Prism` + `profile` | rounded rect, chamfered rect, ellipse, regular polygon, or a convex hull |
| A tapering limb or fin | `Prism` + `taper` | 0 is a triangle, 1 is a rectangle |
| A tube, cable, horn, braid, or lock of hair | `Sweep` + `curve` | quadratic Bézier, tapered radius, bulge, up to 4 helical strands; uniform scale only |
| A part that swells or pinches along its length | `flare` | a scale profile along one axis with a mid-span bulge |
| A leaning or S-curved mass | `shear` | polynomial offset of one axis driven by another |
| A local dent or swelling | `bumps` | up to 4 gaussian pushes |
| An organic wobble over the whole form | `warp` | a bounded sine warp of the point, each axis driven by the next |
| Fine even relief: dimples, corrugation, a hammered skin | `displace` | a sine product added to the field, real geometry |
| A rounded slab, a stadium, a capsule from any primitive | `elongate` | the cross-section swept over a box of half-extents, 1-Lipschitz |
| Scattered, tumbled, recoloured copies | a `jitter` fold | a hashed repeat; render only |
| Self-similar shells, a Droste zoom | a `logSphere` fold | render only |
| Softened edges | `rounding` (curved) or `chamfer` (45° bevel) | never both on one shape |
| A hollow shell | `onion` | |
| Repetition: ribs, teeth, plates, spokes, fins | a `domain` fold | repeat, polar, symmetry, wallpaper; one fold, not N shapes. Refuses a `panel` on the same shape |
| Cellular or faceted relief: scales, chitin, hammered metal | `cells` | needs its own scope; see the scope rules |
| A stripe, ring, panel outline or mouth line | a palette `paints` entry | colour drawn at the hit, never sculpted relief; see "Surface and look" |

Exact scale conventions per primitive (a torus is not what you would guess), the
facet-admission matrix, every ceiling, and every refusal message are in
`references/shapes.md`. Check it before authoring a primitive you have not used
here: `scale` means something different for a torus, a capsule, and a revolved
prism.

In `.puck` a fold is a call in the shape's `domain` array, such as
`domain [ repeat(spacing: [0.1, 1, 1], limit: [2, 0, 0]) ]`, with per-axis
vectors. A bounded repeat spans `-limit..+limit`, so a limit of n draws `2n+1`
copies; an even count needs a composition such as a symmetry fold over an odd
repeat ([composition](references/composition.md#domain-folds)).

## Composition, and the two scope rules that bite

Blends run from `Union` through the smooth and chamfer families to the round
seams: `GrooveUnion` carves a recessed seam along the intersection curve of two
solids, `PipeUnion` lays a bead along it, and both have subtraction twins. Reach
for a groove when the seam should follow that intersection; it removes a
separate cutter shape, but it still forces the creation-wide scope.
`StairsUnion`, `StairsSubtraction` (`steps`) and `Morph` (`morph { lane, from,
to }`) compose at the pop of a scope the shape opens for itself
([composition](references/composition.md#blends)).

Two rules decide whether facets are available at all:

1. **Per-shape scope.** `dilate`, `onion`, `panel`, `flare`, `shear`, `bumps`,
   `warp`, `displace`, `erode`, and `cells` each make the shape request its
   own field scope, as does a stairs or morph blend. A
   non-uniformly scaled sphere or ellipsoid does not: it bakes into the
   1-Lipschitz exponent-2 superellipsoid gauge. A warped shape whose scope is
   free clamps only itself at its own pop: `creation stats` shows
   `scoped clamps 1 (0 shared)` and `globalStepScale 1`, and no other shape
   marches shorter. Only when that depth is already occupied (the shape sits
   in a group or creation scope) is its bound shared at the enclosing pop, and
   only an unscoped chain taxes the program-wide step scale. So a warp does not
   by itself soften a whole model: read the shared and global clamps
   `creation stats` prints before naming the cause of a soft image.
2. **The creation-wide scope.** If a creation has a `noise` facet, an engraved
   text run, **or any shape blend outside `Union` and `SmoothUnion`**, the whole
   static creation emits inside one scope, and `panel`, `trims`, and `cells`
   are refused on **every** shape in it, whatever the placement kind.

The second rule surprises people: one `Subtraction` anywhere costs panels,
trims, and cellular relief everywhere, and so does a groove or a pipe. Keep the
creation all-union and use `panel`, or split prototypes. In an already scoped
creation, explicit cutter shapes can replace panel shorthand; each costs shape
budget but no extra scope depth. Groove and pipe blends reach deterministic
field contact; panels and trims do not.

In pooled emission, `group` collects interacting shapes into one instance and
forwards their authored blends; ungrouped shapes use Union defaults. A group
opens a shared scope when needed, and grouped shapes cannot carry panel, trims,
or cells. Static emission ignores `group` and walks the list in order, so a
group cannot keep a subtraction off its siblings on a static placement. The VM
admits four scope levels. [composition](references/composition.md) has the
formulas, folds, groups, panels, trims and shared-clamp diagnostics.

## Bake work and residency

There is no per-creation shape cap or fixed registration pool. A rigid creation
bakes once in its own space; its bodies share that geometry and palette, with one
root transform and draw each. Independently moving parts add transform slots;
static shapes in a part share its slot. Spawning rigid copies does not rebuild
the field program. Catalog looks emit only for bodies wearing them, at detail
chosen by projected size.

Panels expand to two field operands, trims to two more each, and glyphs to one
per non-whitespace glyph. These increase bake work rather than consume a stamp
budget. `puck creation stats` reports field instructions, bake groups and encoded
bytes. Read actual mesh vertices, draws, baked groups and resident bytes from
`world.counters gpu` and `world.budget` after the bake settles. `detail: true`
saves contact work; its render field still bakes normally. Edit-to-running stays
under 30 seconds, checked on a quiet machine by the lead.

The limits retained protect representations or per-pixel work: 255 skin members
per bake group (refused by group name if exceeded), 24-bit GPU indices, the
material sentinel, 64 bounded volumes and 32 screen bindings. Scopes nest to 4.
Derived faces follow the world's highest authored screen index.

## Surface and look

The palette (up to 32 slots) carries far more than a colour: `specular`,
`roughness`, `metal`, `coat`, `sheen`, `emissive` (switched by a render lane
with `emissiveLane`), `wrap` and `soften` for skin, `fill` for a warm interior
fill, `weathering` for chips and scratches over a revealed `under` substrate,
`inset` for a refracted layer beneath the surface (how an eye is authored: a
radial paint ramp of pupil, iris, limbus and sclera stops under a cornea, not a
dark sphere), and `paints` for detail that is colour rather than form: stripes,
trims, panel outlines, a mouth line. A paint is drawn crisp at the hit; relief
finer than the bake's cell (5 mm refined, 15 mm on smooth parts, 2 to 15 mm on a
body's round sections) frays into
jagged steps, so never sculpt a millimetre-proud stripe. Painted metal and
clearcoat read only against something to reflect: the world's sky `panel`
highlights. Ranges, defaults and examples are in `references/surface.md`.

## Binding to state

Nothing in the renderer knows what health, charge, or speed are. A look row
carries up to four anonymous **render lanes**, each an expression over world
state. Only body registration supplies those lanes: an inhabited placement
needs a look, kit, and body capacity. Static, animated, and attached placement
registrations supply zero lanes. Use bare `hp` or `airPose[$body]` in a lane,
and `bodyState($body, flightFuel)` for one of the body's own action-state slots;
`state.hp` is driver/binding spelling and reads the wrong row here. Shapes and
materials read a lane by index:

| Consumer | Reads the lane |
|---|---|
| `shapes[].erode` | in the bake: erodes a shape away over a lane range with a ragged front, frozen at the value the bake read |
| `palette[].weathering.lane` | at shading time, every frame: chips and scratches, with a static floor |
| `palette[].emissiveLane` | at shading time, every frame: `emissive × saturate(lane)` |
| `volumes[].intensityLane` | at shading time, every frame |

Erosion is geometry, and every view draws baked meshes. A bake reads the lanes
when a new program arrives (at boot, usually 0), and the mesh keeps that
erosion until the program next changes; a lane change alone never rebakes. So
**erode cannot show or hide a part live**, and a part that only appears as its
lane rises bakes empty. Show live state with weathering, `emissiveLane` and
volume intensity, or move a part away with rig motion driven by a state row.
See [surface](references/surface.md#render-lanes).

Author the meaning in the document's own cell names and the lane expression; the
engine only ever sees a number. A reversed `from`/`to` range runs the fold
backwards.

## Making it move

`parent` is the skeleton: it names an **earlier** shape whose animated motion
carries this one, so chains resolve in one pass and can never cycle. On top of
that, `swings` (up to 8) rotate about a pivot and `slides` (up to 4) translate,
both driven by a named `driver` reading a signal or a state row (`state.hp`).
Directional locomotion reads `travelDirection` and the planar accelerations,
and a driver naming a world `dynamics` row trails and settles instead of
tracking. A driver can ride an earlier driver's cycle (`driver.<name>`) and
scale its cadence or weight by a world `curves` row (`cadenceBy`, `weightBy`).
`chains` plus `effectors` give CCD inverse kinematics with plant windows for
feet, a `replant` latch, and `align`. `frames` snapshot base poses. A behaviour
the vocabulary cannot express is a new signal, member or op, never a client
special case. A shape carrying `domain` folds may not also carry a swing or
slide. Details, caps, every refusal, and the Moth's driver map are in
`references/rig.md`.

**Blends between shapes that move apart (owner's ruling).** A pooled `group`
bakes one mesh at the pose its program arrives in, and each vertex then rides
one shape's slot, so a smooth or non-union blend joining shapes with different
motion owners (a swing, slide, effector chain or frame not shared through
`parent`) stretches its seam as they move. It is a warning, not an error:
PUCK122 in `puck compile --validate`, `puck lint` and `puck creation stats`
names the creation, the two shapes, what moves each and the blend
(`CreationMotion.MovingBlends`). Once the shapes' relative pose holds still the
engine bakes the group again there (the
[settle rebake](../rendering/references/mesh-bake.md#groups-poses-and-materials)),
so a pose that settles reads right and continuous motion keeps the stretched
seam. When the seam must hold while the shapes move, give them one owner: put
the swing or slide on a shape both parent under, or take the moving shape out
of the group and accept a union crease.

## Render-only versus deterministic

A solid placement requiring deterministic field contact refuses `Revolve` and
domain folds that cannot expand; a `Path` prism profile (extruded, a fill or a
stroke) is admitted, since the fixed-point evaluator reads its edge table as
the kernel does. `flare`, `shear`, `bumps`, `erode`, panels,
trims, cells and sweeps validate but are omitted from contact geometry (cells
keep the base primitive). Creation `noise` is not omitted: a relieved creation
collides as the surface its bake draws, one field collider per stamped copy
whose field is the creation's own fixed-point program (its contact shapes and
the relief over their union), so a body stands on the drawn rock
([shapes](references/shapes.md#contact-admission)). For an arched or otherwise convex
outline that must collide, a clockwise `Convex` profile (at most 32 vertices)
or a union of admitted primitives keeps the shape. See
[shapes](references/shapes.md#contact-admission). Every view still renders a
shape contact omits.

## Verifying

Source first, then structure, then pixels:

1. `puck compile <file>.puck --validate` catches structure, budget and scope
   refusals.
2. `puck creation stats --world <file>.puck --prototype <id>` validates the
   whole world, emits text-free prototypes at unit scale to report static and
   pooled rest-pose clamps, and builds the world's deterministic contact field,
   solid placements included, even with a prototype filter. Exit 1 means
   validation, emission, or contact failed; read the diagnostic. A pass does not
   prove live motion or appearance.
3. `puck creation shape --world <file> --prototype <id> [--shape <name>]` (live:
   `creation.shape`) says whether each shape's distance is exact, a bound or
   uncertified, whether the fixed-point evaluator takes it, and what contact
   makes of it. `world.slice <placement> <x|y|z> <path.png>` draws the field's
   distance bands live.
4. Run the game and look: a claim about how something reads is not verified
   until you have looked at a capture (`references/loop.md`).
5. Audit what the boot baked:
   `puck mesh audit --world <file>.puck --prototype <id> --group <shape> --images <dir>`
   names the shapes at each group's worst clusters, in the author frame, and
   says which way the mesh faces against the field's gradient at the worst
   sample: opposed directions with both shapes at 0 mm is a sliver between
   two surfaces, not a bake fault.
   Frayed edges show as face normals off the gradient; a cutter whose field is
   only a lower bound (a stretched ellipsoid, a non-uniform scale) shows as a
   loose field; give that cutter an exact primitive instead. The
   [rendering skill](../rendering/references/mesh-bake.md#auditing-a-bake) owns how the audit
   reads a store.

Run every `puck` verb from your lane's private copy of the head's CLI
(`verification`).

## References and routing

| Where | Read it for |
|---|---|
| `references/shapes.md` | Every primitive's scale convention, profiles and lifts, which facets each admits, every ceiling and refusal message, contact admission |
| `references/composition.md` | Blends with formulas, domain folds, groups, scopes, trims, panels, the budget arithmetic |
| `references/surface.md` | Palette fields, weathering, inset, paints, render lanes, volumes, the render fields a look depends on |
| `references/rig.md` | parent/joint/swings/slides, frames, chains, drivers, effectors, parts, cameras, text runs |
| `references/loop.md` | Console verbs, capture recipes, the offline `puck creation` verbs, the sculpting library for C# authoring |
| `puck-dsl` | `.puck` grammar (`let`/`template`/`for`, the one-spelling rule), CLI flags, PUCKnnn diagnostics not specific to a creation field |
| `puck-world` | World sections around a creation (`looks`, `placements`, `render`, `state`), console semantics, booting `--world` |
| `rendering` | The SDF VM, ISA, kernels, shaders, the bake's internals, GPU cost and captures |
