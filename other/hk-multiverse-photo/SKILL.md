---
name: hk-multiverse-photo
description: Transform supplied Hong Kong, city, street, vehicle, skyline, or harbor photographs into bold multiverse-collision still images that preserve source geometry while combining real photography, flat 2D animation, and dimensional 3D/cel rendering. Use for Spider-Verse-inspired city edits, cyberpunk universe collisions, distinct style fields, phase-wheel sectors, vehicle timeline portals, tram interchange scenes, Douyin/9:16 batches, selective frame revisions, coherent multi-image series, or original HK//VERSE archive annotations. Generate an original visual system without copying characters, official logos, or film frames. Do not use for video unless the user explicitly asks for motion.
---

# HK Multiverse Photo

## Overview

Build high-impact multiverse stills from real photographs without losing the photographed place. Treat the source as geometric truth, give every frame one unmistakable primary universe, and make each incoming universe differ through medium, material, local physics, and spatial behavior—not hue alone.

Default to still images. Never turn a batch into a video unless the user explicitly requests video.

## Non-Negotiable Contract

- Preserve the source camera, crop, landmark geometry, street direction, subject identity, vehicle direction, signage placement, and crowd structure throughout the multiverse pass. If the user requests a geometry change, complete it as a separate base-edit prepass, inspect the revised base, and then treat that revised image as the fully locked source.
- Keep at least one clearly photographic anchor. A default frame contains a real-photo base, one flat 2D field, and one dimensional 3D/cel field.
- Assign one primary universe to roughly 45–60% of the readable scene. Carry its palette and material logic into the background so it reads as the world, not a foreground sticker.
- Add two to four incoming fields with distinct silhouettes and rendering systems. They may overlap, but each must remain identifiable at thumbnail size.
- Use spatial mechanisms: hard-edged cell fractures, render-pass seams, angular space shards, volumetric elliptical apertures, render-layer perspective displacement, phase lines, or radial sector mapping. Displace only an alternate render layer; never move the source subject, wheel, building, horizon, rail, wire, or reflection origin.
- Never use paper tears, curled paper, tape, glue, poster scraps, white ripped edges, or visible paper fibers.
- Do not copy official characters, official spider logos, movie titles, or a specific film frame. Use the original `HK//VERSE` identity for annotations.
- Generate a clean image plate first. Add exact text and diagrams later as a deterministic vector overlay.
- Preserve approved images and approved regions. When the user asks for a local change, edit that failure without redesigning the whole frame.

Read [references/universe-atlas.md](references/universe-atlas.md) before assigning U01–U05. Read [references/collision-layouts.md](references/collision-layouts.md) before choosing the collision geometry. Read [references/annotation-system.md](references/annotation-system.md) only when annotations are requested.

## Workflow

### 1. Inspect and Lock the Source

View every supplied image before editing it. Record:

- hero subject or visual anchor;
- protected people, vehicles, signs, architecture, horizon, and road geometry;
- dominant scene hook such as a wheel, vanishing point, moving car, tram wires, repeated windows, waterline, or reflections;
- usable negative space for later annotation;
- already approved regions or frames that must not change.

For a series, keep a revision ledger with each frame's source path, current output path, status (`mutable` or `locked`), primary universe, active palette, exposure target, and annotation state. Derive a series contract from approved frames: shared neutral, one recurring phase accent, exposure/black-floor range, typography family, and annotation stroke language. Never silently unlock an accepted frame.

If a target image is missing, ask for it. Otherwise proceed without asking the user to restate aesthetic details already visible in the conversation or references.

### 2. Write a Frame Contract

Create a compact internal plan before generating:

```yaml
source_hook: "the photographed structure that drives the collision"
primary: "U0X, 45-60%, foreground and background behavior"
incoming:
  - "U0X, region, medium, collision mechanism"
  - "U0X, region, medium, collision mechanism"
# Repeat incoming entries until the chosen layout's required count is met (2–4).
photo_anchor: "specific untouched or lightly treated region"
geometry_locks: ["landmark", "person", "vehicle direction", "legible sign"]
seams: "non-paper spatial boundary design"
reflection_lock: "source-to-reflection mapping, or none"
phase_map: "optional sector angles and reflection mapping"
palette_guardrails: "dominant family, accent limits, and colors to reduce"
output: "crop, dimensions, clean/tagged variants"
```

Do not force identical percentages or layouts across a series. Reuse the universe identities, not the same split.

### 3. Choose a Photo-Specific Collision

Use the strongest photographed hook to choose the mechanism:

- dominant wheel or circular landmark → angular phase sectors;
- long street or vanishing point → depth slices, field planes, or a distant aperture;
- moving vehicle → vehicle-as-time-axis with uneven perpendicular wormholes;
- tram queue, rails, and overhead wires → multiverse interchange with route volumes and matching rail reflections;
- skyline plus water → building-specific universes and source-locked reflection columns;
- stacked facades → irregular floor-level cell fractures and displaced spatial shards.

See [references/collision-layouts.md](references/collision-layouts.md) for the full selection matrix and failure modes.

### 4. Build Real Medium Contrast

For every field, change at least three of these five dimensions:

1. contour language;
2. shading model;
3. surface material;
4. spatial geometry;
5. local motion or physics.

A field that changes only color is not a new universe. Flat 2D regions need broad shapes, deliberate linework, and controlled detail. 3D/cel regions need volume, panels, specular logic, or hard-surface depth. Photo regions retain optical texture, natural perspective, and plausible light.

Keep the global palette balanced. Do not wash the whole frame in cyan, pink, or black and white. Limit Noir to a deliberate region, and distribute 2D animation across more than one side when the series has become repetitive.

Translate subjective directions such as “more feminine” into explicit visual axes: lyrical curvature, finer line weight, graceful rhythm, softer hard-surface transitions, refined ornament, or quieter contrast. Preserve face, body, clothing, and perceived identity. Do not default to pink, makeup, sexualization, cultural costume, or automatically assign one universe. Ask one concise clarification only when the target frame or intended design axis cannot be inferred.

### 5. Generate the Clean Plate

Use the available image-editing generator with the source image attached. In the prompt, state in this order:

1. source invariants and protected geometry;
2. primary universe and its background behavior;
3. incoming fields, exact regions, and distinct mediums;
4. collision mechanisms tied to scene geometry;
5. light and reflection correspondence;
6. crop and output size;
7. hard exclusions, especially paper language, duplicate subjects, invented text, and global color washes.

For Douyin, default to a static 9:16 composition at 1080×1920. Preserve the original crop when it already fits; crop or outpaint with scene continuity, never stretch.

Do not ask the image model to render archive labels, legends, barcodes, or long readable text. Preserve real signs where possible; do not invent substitute wording.

### 6. Inspect and Revise Surgically

Inspect the generated result at original detail and at thumbnail size. Test these gates:

- **Primary-world gate:** the main universe is obvious without reading a label.
- **Medium gate:** 2D, 3D/cel, and photo regions differ in construction, not only saturation.
- **Fidelity gate:** protected people, vehicles, architecture, directions, and key signs remain coherent.
- **Collision gate:** seams arise from the photographed hook and never resemble torn paper.
- **Causality gate:** sky rays, reflections, shadows, rails, and motion traces map back to their source universe.
- **Restraint gate:** the background supports the primary world; secondary decoration does not bury the scene.

Fix all compatible user-named failures in one scoped frame pass while explicitly preserving successful regions. When requested fixes conflict, resolve the highest-impact structural failure first and state what remains. If the user says the result is “too restrained,” amplify the primary world’s background, material transformation, and subject-state contrast—not bloom alone.

When the user asks for a restrained primary background, reduce its contrast, texture density, and accent coverage without reducing PRIMARY below 45% or making its material identity ambiguous.

For a batch, lock every accepted frame and revise only the named images.

### 7. Add Deterministic Annotation When Requested

Keep the clean plate. Then create a transparent SVG overlay following [references/annotation-system.md](references/annotation-system.md). Use exact user-visible text, adaptive placement, and the original `HK//VERSE` mark; avoid faces, vehicle silhouettes, and the scene’s hero feature.

“Approved clean plate” means it has passed the internal visual gates and has been frozen as a separate file. Pause for explicit user approval only when the user asks for a staged checkpoint; when clean and tagged variants were requested together, continue directly to the overlay after internal QA.

Use [scripts/make_annotation_svg.py](scripts/make_annotation_svg.py) with a JSON configuration, then composite the SVG over the clean plate using an available local renderer. Never regenerate the artwork merely to add labels.

### 8. Validate and Deliver

Run the structural image check:

```bash
python3 scripts/validate_image.py /absolute/path/to/output.png --profile douyin
```

This verifies file readability, dimensions, orientation, and aspect ratio; it does not replace the visual gates above.

For a series, also inspect one contact sheet at thumbnail size. Confirm that every primary universe is distinct, the shared neutral/accent and exposure remain coherent, 2D regions do not repeatedly occupy the same side, and locked frames are byte-for-byte unchanged.

Deliver non-destructively:

- `*_clean.png` for the artwork;
- `*_tagged.png` when annotations were requested;
- the SVG and JSON annotation sources when created.

Report the absolute output paths and summarize which frame contract was used. Do not claim a visual requirement passed unless the result was inspected.

## Prompt Skeleton

Use this as a construction aid, not as a literal fixed prompt:

```text
Edit the supplied photograph as one original multiverse-collision still.
LOCK: [camera, composition, identities, landmarks, vehicle direction, signs].
PRIMARY [U0X, 45–60%]: [palette + material + foreground/background behavior].
INCOMING [U0X]: [region + 2D/3D/photo medium + mechanism].
INCOMING [U0X]: [region + medium + mechanism].
# Repeat INCOMING for the chosen layout's full 2–4 field count.
PHOTO ANCHOR: [specific retained region].
COLLISION: [scene-hook-driven seams, no paper].
CAUSAL LIGHT: [sky/reflection/shadow mapping].
OUTPUT: static [crop and size], clean plate, no UI or added text.
AVOID: global color wash, timid filter-only styling, duplicate subjects,
ghost vehicles, altered direction, paper tears, official logos or characters.
```
