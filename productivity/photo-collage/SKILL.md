---
name: photo-collage
description: Arrange two to ten supplied photos into one intentional multi-panel or artistic collage while controlling source fidelity, crop, hierarchy, spacing, overlap, borders, material, and visual rhythm. Use for artistic photomontage, surreal or conceptual collage, analog paper collage, editorial mixed media, clean grids, masonry, polaroid or scrapbook compositions, moodboards, and street-art collages; do not use for fashion lookbooks, multipage layouts, posters, photo-real scene fusion, carousels, local image repair, or single-photo styling.
---

# Photo Collage

Turn supplied photos into one designed canvas. Keep original photos as source assets; use generation only when the requested collage needs integrated paper, texture, overlap, or decorative treatment.

## Catalog

- Display name: Photo Collage
- Categories: Layout & Design
- Status: Ready
- Route label: Source-faithful collage composition
- Tone: cyan
- Short description: Arrange original photos into one intentional collage.

- Similar skills: compose-lookbook, create-social-carousel, create-image-deck
## What this skill does

- Assigns a role and importance to every supplied photo before choosing a layout.
- Protects faces, products, gestures, and other focal regions when cropping photos into panels.
- Converts an artistic theme into one visible construction idea instead of adding random collage decoration.
- Chooses deterministic composition for clean layouts and a collage-capable image route only for genuinely generative treatments.
- Checks source coverage, crop safety, hierarchy, spacing, and absence of invented people, products, or text.

## How to use

Attach two to ten photos and describe the layout, mood, output ratio, and which image should lead.

#### Create a clean photo grid

```text
Arrange these six travel photos into one clean 4:5 grid with the mountain portrait as the main image.
```

#### Create an editorial collage

```text
Turn these product photos into one restrained editorial collage with overlapping paper frames.
```

#### Create a scrapbook collage

```text
Make one playful scrapbook collage from these party photos without changing anyone's face.
```

#### Create an artistic collage

```text
Turn these family archive photos into an artistic collage about fragmented memory while keeping everyone recognisable.
```

## Workflow

### 1. Compile the source manifest

Number every input and resolve:

```yaml
image_role: hero | support | detail | texture | background
importance: dominant | secondary | accent
focal_regions: faces | people | product | gesture | landmark | text
preserve: identity | product | clothing | color | markings | source text
may_crop: yes | constrained | no
```

Use the actual uploaded images. Do not replace an available original with a prose reconstruction. Ask only when the hero image, required inclusion, or crop permission is materially ambiguous.

### 2. Select one layout mode

Read [references/layout-modes.md](references/layout-modes.md) and choose one:

- `clean-grid`: aligned cells, consistent gutters, minimal decoration;
- `masonry`: mixed aspect ratios with controlled rhythm;
- `editorial-overlap`: one hero with a few subordinate overlaps;
- `polaroid-scrapbook`: framed photos with restrained paper artifacts;
- `moodboard`: photos plus purposeful material or palette samples;
- `street-art`: expressive layers, torn paper, marks, and graphic interruptions.
- `artistic-collage`: concept-led photomontage, surreal, analog, archival, abstract, or mixed-media construction.

Do not use `lookbook` as a synonym. Route a product-detail module set to `$product-detail-page`; keep a coordinated fashion lookbook as its own pending Atom. Treat a single outfit-breakdown as an ordinary collage only when the user explicitly requests that format.

For `artistic-collage`, read the artistic directions in [references/layout-modes.md](references/layout-modes.md). Resolve one theme, one visible construction idea, and one source-fidelity level before selecting surface style. Examples of construction ideas include memory revealed through translucent layers, one subject repeated across time slices, architecture cutting through a portrait silhouette, or a product transitioning from halftone print into photography. Reject directions whose only idea is adding tape, stickers, torn edges, noise, or unrelated found imagery.

### 3. Plan geometry before style

Resolve canvas ratio, margins, gutters, panel count, hero share, overlap order, border treatment, and background. Keep every required source visible once unless repetition is requested. Crop around declared focal regions; never cut through a face, product identity feature, or necessary gesture merely to fill a cell.

For clean grid, masonry, evidence-preserving, or text-heavy work, prefer deterministic crop and composition so source pixels and typography remain controllable. Use a model only when integrated material, irregular overlap, generated background, or expressive edge treatment is part of the requested result.

### 4. Select the execution route

- Prefer the verified `ai-collage-maker` commercial workflow for two to ten supplied images when the requested result is a visibly generative collage.
- Prefer deterministic layout for clean grids, precise borders, exact text, or strict source fidelity.
- For artistic collage, prefer `ai-collage-maker` when multiple originals must remain recognisable through material integration; prefer GPT Image 2 when a stronger conceptual construction or short integrated typography is central; consider a broad multi-reference synthesis model when reference capacity or interpretive combination is the demonstrated constraint.
- Use a style-first model only when exact copy and source fidelity are explicitly secondary. If sources must remain pixel-identical, let the model generate only background, texture, masks, or decorative layers and finish deterministically.
- Use a multi-reference image model only when the dedicated collage route cannot express the treatment or demonstrates a capability failure.
- Never use Image Combiner: it owns one unified photographic scene, while this Skill owns visibly separate photo panels or layers.
- Default to one output and `batchCount: 1`.

### 5. Compile a compact Prompt

Use the cleaned Photo Collage seed only for `street-art`; use the API's chaotic multimedia default only for an explicitly experimental maximalist request. Neither is the general baseline.

Submit short natural prose:

```text
Create one [ratio] [mode] collage from Images 1–[n]. Make Image [x] the hero and use the others as [roles]. Keep every supplied photo recognisable and protect [focal regions]. Use [layout geometry] with [specific material treatment]. Add no new people, products, logos, or readable text.
```

For artistic collage, replace generic style language with the chosen construction idea and fidelity level: state what is layered, repeated, erased, fragmented, cut through, or transformed, and which source traits must survive.

Do not ask the model to randomize the focal point, palette, or material system unless the user requests randomness. Do not enumerate decorative styles that are unrelated to the photos.

### 6. Execute and accept

Upload every original, execute through WeShop OpenAPI when using a model route, and poll to terminal state. Keep the originals unchanged and record them in the website case study using numbered original/source asset fields.

Accept only when:

1. One collage canvas is returned with the requested ratio, panel/layer structure, and output count.
2. Every required source appears once and remains recognisable; no source is silently replaced or omitted.
3. Faces, bodies, products, clothing, landmarks, and approved source text retain the promised fidelity.
4. The hero is immediately clear; secondary photos, gutters, borders, overlaps, and negative space form an intentional rhythm.
5. Crops protect declared focal regions and do not create accidental decapitation, amputations, product truncation, or unreadable detail.
6. No invented subject, duplicate photo, fake annotation, filler text, watermark, unrelated decoration, or accidental scene fusion appears.

For `artistic-collage`, additionally require the theme to remain understandable through the chosen construction, every material and transformation to support that idea, and the result to show intentional tension or rhythm rather than random maximalism. Judge source drift against the declared `pixel-preserving`, `appearance-preserving`, or `interpretive` level.

### 7. Retry one failed property

Retry once with only the failed property changed: strengthen a source lock, widen a crop, simplify overlaps, remove decoration, or reassert one hero. If a clean layout drifts, stop regenerating and compose it deterministically. Change routes only for demonstrated capability mismatch. Record inputs, route, parameters, Prompt revision, execution ID, terminal state, error/refund state, and failed acceptance item.

When this Skill selects GPT Image 2, use `quality: "medium"` and `imageSize: "2K"` by default; change either only when the user explicitly requests another tier.

Every GPT Image 2 call in this Skill defaults to Medium at 2K; use another tier only when the user explicitly requests it.

## User-facing output

- Media type: One finished photo-collage image plus a compact source and acceptance record
- Default quantity: 1 separate collage image
- Content per image: Two to ten supplied photos arranged as visible panels or layers
- Default layout: Source-driven; 4:5 when the user requests a social collage but supplies no ratio
- Video output: No
- Model policy: Prefer deterministic composition for clean layouts and `ai-collage-maker` for generative collage treatments
- Downstream use: Social photo collections, editorial layouts, moodboards, memory collages, product stories, and printable photo arrangements
