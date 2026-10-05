---
name: urban-daylight-documentary-grade
description: Apply one restrained urban-daylight documentary exposure and color correction to a supplied photograph while preserving composition, scene content, geometry, texture, original light direction, weather, and depth of field. Use when a city photo looks flat, gray, or muddy and needs controlled bright highlights, deeper detailed shadows, clean midtones, stable neutral grays, and subtle warm-light/cool-shadow separation; unlike $apply-photo-filter (relationship 0.86), choose this for realistic daylight depth recovery with no grain, bloom, vintage texture, global cast, or named aesthetic filter, and choose $apply-photo-filter for broader film, monochrome, matte, texture, or reference-led treatments; unlike $remove-photo-filter (relationship 0.55), choose this when the source is naturally flat rather than visibly filtered; unlike $recolor-object (relationship 0.31), choose this when local color supports depth instead of assigning an object a new hue.
---

# Urban Daylight Documentary Grade

## Catalog

- Display name: Urban Daylight Documentary Grade
- Categories: Layout & Design
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive daylight edit
- Tone: sky
- Short description: Recover clean urban daylight depth without changing the scene.
- Similar skills: apply-photo-filter, remove-photo-filter, recolor-object

## What this skill does

- Corrects one supplied urban daylight photograph using only exposure, contrast, saturation, white balance, local tonal/color separation, restrained sharpness, and an optional extremely subtle vignette.
- Keeps bright areas controlled, shadows deep but detailed, midtones clean, neutral architecture stable, and source colors natural.
- Preserves composition, people, objects, text, geometry, material texture, original light direction, weather, environment, and depth of field.

## How to use

Provide one authorized city daylight photograph. Optionally name the desired strength, protected colors or neutral surfaces, and whether a barely visible natural vignette is acceptable.

#### Add clean daylight depth

```text
这张城市街拍有点灰蒙蒙。保留人物、建筑、构图、原始光线方向和景深；让天空和白墙明亮但不过曝，阴影压深但保留纹理，中间调干净扎实，受光面微暖、阴影微冷，灰色建筑和地面保持中性。不要HDR、颗粒、光晕或新增光源。
```

## Workflow

1. Confirm one source image and record its ratio, crop, composition landmarks, people, object count, text, geometry, material texture, existing light direction, weather, environment, depth of field, protected colors, and visible neutral surfaces. Treat all as invariants.
2. Limit the requested edit to exposure, contrast, saturation, white balance, local tonal/color separation, restrained sharpness, and an optional extremely subtle vignette. Do not change pose, identity, expressions, objects, background, crop, weather, lighting direction, or depth of field.
3. Build a concise edit Prompt in this order: invariants; highlight target; shadow target; midtone target; local color separation; protected hues and neutrals; texture/sharpness; exclusions. Translate “selectively darken the background” into refinement of existing tonal relationships only, never new light, masks that reshape objects, or artificial subject lighting.
4. Keep highlights bright but below clipping, including sky, white walls, bright facades, and glass reflections. Deepen shadows only while retaining texture, contour, and color. Keep midtones clean and substantial; avoid gray haze, crushed blacks, muddy chroma, HDR shadow lifting, and flattened global contrast.
5. Preserve source hues. Allow only subtle warmth in lit areas and subtle coolness in shadows without a global cast. Keep sky naturally blue-cyan, architectural/ground/glass grays neutral, warm materials from turning orange, plants naturally restrained, key subjects lively, and secondary colors quiet.
6. Forbid invented elements, redraw, relighting, new light sources, flare, beams, fake bokeh, global blue/cyan/brown/yellow overlays, uniform saturation changes, grain, noise, scratches, dust, leaks, aging, painterly smearing, CG rendering, AI-redrawn texture, and sharpening halos.
7. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied image as the edit reference, the requested or source-preserving ratio, `batchCount: 1`, one result, and one stable `operationKey`. Poll that accepted operation to a terminal state without recreating it.
8. Compare the result with the source at full size. Require unchanged landmarks and content, preserved light direction and depth of field, controlled highlights, detailed shadows, clean midtones, stable neutrals, restrained local warm/cool separation, natural texture, no artifacts, and no visible heavy vignette. Detail missing from the source raster cannot be claimed as recovered original evidence.
9. Retry at most once after a known terminal result using a linked new key and a non-identical Prompt naming only the failed property. Stop and disclose unresolved identity, text, geometry, texture, lighting, clipping, color, or source-detail limits rather than silently switching models or resubmitting.

## User-facing output

- Media type: One corrected urban daylight photograph
- Default quantity: 1
- Content per image: Unchanged source scene with controlled highlights, detailed deeper shadows, clean midtones, stable neutral surfaces, and restrained local warm/cool separation
- Default layout: Source composition and aspect ratio
- Preservation: Composition, people, identity, objects, text, geometry, textures, original light direction, weather, environment, and depth of field
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing; one issue-specific retry maximum
- Downstream use: Street photography, city travel images, architectural context shots, editorial documentary images, and social publishing
