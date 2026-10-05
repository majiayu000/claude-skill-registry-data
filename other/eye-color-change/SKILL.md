---
name: eye-color-change
description: Change only both iris colors in one supplied portrait while preserving identity, pupil size, sclera, catchlights, eyelids, gaze, facial structure, skin, hair, clothing, lighting, and background. Use for natural contact-lens or eye-color previews; do not use for eye-shape changes or medical simulation.
---

# Eye Color Change

## Catalog

- Display name: Eye Color Change
- Categories: Portrait
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: rose
- Short description: Preview one natural iris color without changing the eyes.
## What this skill does

- Produces one portrait with one bilateral iris-color change.
- Edits the irises only and preserves pupil, sclera, catchlights, lids, lashes, and gaze.
- Keeps identity, skin, expression, hair, clothing, and scene unchanged.

## How to use

Provide one sharp portrait with both irises visible and name one target color.

#### Preview hazel eyes

```text
Change both irises to natural hazel-green with realistic radial detail and unchanged catchlights.
```

## Workflow

1. Confirm both irises are visible and large enough; record target hue, saturation, and naturalness.
2. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
3. Edit only iris pigment; preserve pupil geometry, sclera, vessels, catchlights, eyelids, lashes, gaze, facial landmarks, skin, hair, clothing, crop, and lighting.
4. Forbid glowing eyes, mismatched sides, eye enlargement, contact-lens graphics, text, or panels unless explicitly requested.
5. Inspect bilateral color, iris texture, light consistency, gaze, and identity. Retry only failed iris detail.

## User-facing output

- Media type: One edited portrait image
- Default quantity: 1
- Content per image: One person with one iris-color treatment
- Default layout: Preserve source composition; no collage
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Contact-lens preview, beauty planning, and personal visualization
