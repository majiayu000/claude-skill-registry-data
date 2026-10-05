---
name: procedural-game-art
description: Design, implement, and audit deterministic game visuals generated entirely from code rather than hand-authored or image-model assets. Use for engine-free games, procedural illustration, vector or mesh-based UI, coherent art-direction systems, seeded variation, runtime or baked atlases, resolution-independent rendering, visual conformance tests, screenshot automation, and fixing seams, clipping, inconsistent texture, or composition drift across game screens and store assets.
---

# Procedural Game Art

Build an art system, not a pile of pictures. Express the visual language as reusable data and transformations so gameplay, UI, icons, screenshots, and store capsules share the same source of truth.

## Start with an art grammar

Before implementing screens, define a compact grammar:

- Palette roles: paper, primary ink, secondary ink, light, warning, success.
- Primitive vocabulary: ribbons, polygons, hatching, stipple, silhouettes, glyphs.
- Line hierarchy: outline, structural line, interior hatch, weathering.
- Type hierarchy: title, heading, label, body, changing number.
- Composition rules: margins, focal region, safe area, foreground baseline.
- Motion rules: which marks move continuously, step on a shutter, or stay fixed.

Put these values in one theme/config module. Do not tune them independently in every screen.

## Separate semantic data from drawing

Use three layers:

1. **Semantic plan** — plain data describing houses, characters, labels, lights, tiles, and their states.
2. **Cut/bake layer** — deterministic functions that turn semantic data into meshes, paths, text runs, or atlas cells.
3. **Compositor** — draws ordered layers, clipping, texture, weather, and final color treatment.

Keep game logic out of drawing functions. A renderer should receive a snapshot and produce a plan without changing gameplay.

## Make variation deterministic

- Seed every procedural choice from stable identity: world seed, screen kind, entity index, or atlas cell.
- Never consume gameplay RNG for decoration.
- Quantize low-frame-rate effects such as flicker or paper jitter when continuous noise looks synthetic.
- Ensure planning the same state twice produces byte-identical geometry or the same normalized draw list.

## Build reusable primitives first

Implement the smallest complete kernel before full screens:

- Transform and clip stacks
- Fill, stroke, outline, and erasure/destination-out
- Seeded noise and wobble
- Hatch fills with a consistent lighting convention
- Text measurement by visible cap height
- Layer ordering and alpha composition
- Logical-to-device-pixel mapping

Prove each primitive on a conformance sheet. Read [references/conformance.md](references/conformance.md) before declaring the kernel stable.

## Choose runtime, bake, or hybrid output

- **Runtime:** use for changing numbers, interactive states, physics, and responsive composition.
- **Baked atlas:** use for expensive deterministic shapes that repeat often.
- **Hybrid:** bake stable furniture and compose live state, text, particles, and animation over it.

Keep atlas metadata in logical units. A higher-resolution bake must not change gameplay geometry or layout.

## Compose screens from shared scenes

Do not redraw the same world separately for the menu, map, ending, icon, and capsule. Expose reusable scene functions and camera/composition parameters.

Store graphics are separate compositions, not blind crops:

- Landscape capsules need intentional side bleed and a safe central title area.
- Portrait capsules should recompose subjects rather than crop landscape art.
- Icons need one readable subject and edge-to-edge ground/background treatment.
- Generate exact target dimensions and inspect the final raster, not just the master scene.

Read [references/composition.md](references/composition.md) when creating store assets or adapting a scene across aspect ratios.

## Validate visually and structurally

Add tests for facts code can prove:

- Every planned atlas cell exists.
- Every draw stays within its clip or approved bleed.
- Text fits its measured region.
- A scene is deterministic for a given seed and state.
- All runtime states have an art path.
- Store outputs have exact dimensions and full-edge coverage.

Then render representative states and inspect them. Tests cannot judge hierarchy, awkward tangencies, mismatched texture, or whether a composition reads at thumbnail size.

## Work in review loops

For every visual change:

1. Render the exact target dimensions.
2. Compare against the approved reference or previous version.
3. Inspect edges, seams, type, focal hierarchy, and repeated motifs.
4. Change the shared rule when multiple outputs show the same defect.
5. Add a regression test for any objective failure.
6. Re-render every downstream composition that consumes the rule.

Do not patch raster output after generation. Fix the scene, grammar, camera, or compositor that produced it.

## Avoid common failures

- Do not call code-generated visuals “AI-generated images.” Describe them as procedural art if no image model produced the pixels.
- Do not use independent random calls inside drawing code.
- Do not allow UI code to invent a second visual language.
- Do not stretch a scene to fit a new ratio.
- Do not trust transparent margins to disappear in the final icon or capsule.
- Do not accept “technically within bounds” when the subject is visibly cropped.
- Do not preserve a prototype renderer after it becomes a second source of truth.
