---
name: make-selfie
description: Turn one supplied everyday person photo into one realistic solo selfie, or combine two supplied person photos into one realistic two-person selfie while preserving each identity separately. Use for arm-length phone selfies, mirror selfies, casual travel selfies, or selfie group portraits; do not use for filters, illustration, face swapping, or adding unprovided people.
---

# Make Selfie

## Catalog

- Display name: Make Selfie
- Categories: Portrait
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: rose
- Short description: Turn one or two everyday photos into one realistic selfie.
## What this skill does

- Converts one ordinary person photo into one solo phone or mirror selfie.
- Converts two ordinary person photos into one two-person selfie without blending their identities.
- Reconstructs camera distance, arm/phone relationship, gaze, casual crop, wide-angle perspective, light, and everyday background.

## How to use

Provide one or two supplied person photos and name arm-length or mirror selfie, setting, mood, orientation, and who holds the phone.

#### Make a solo selfie

```text
Turn this daily portrait into a natural arm-length window-light selfie at home.
```

#### Make a two-person selfie

```text
Combine these two people into one casual cafe selfie, with person 1 holding the phone and person 2 beside them.
```

## Workflow

1. Read `references/source-mapping.md`. Confirm accept exactly one or two person sources; more people require another dedicated composition workflow.
2. Bind identity, hair, age, skin tone, and recognizable clothing cues per source. For two sources, bind left/right position and phone holder before prompting.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Describe a photographic selfie: arm-length or mirror mechanism, phone/lens position, gaze, proximity, crop, slight wide-angle perspective, setting, and coherent available light. Forbid illustration, style filters, beauty retouching, face blending, duplicate people, extra people, text, UI chrome, split screen, or collage.
5. Inspect each identity independently plus person count, phone/arm plausibility, gaze, scale, occlusion, anatomy, perspective, lighting, crop, and background. Retry only the failed identity or geometry.

## User-facing output

- Media type: One realistic selfie image
- Default quantity: 1
- Content per image: Exactly the one or two supplied people in one selfie scene
- Default layout: One continuous phone-camera frame; no collage
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Personal social photos, travel memories, and casual group portraits
