---
name: backrooms-dreamcore
description: Create one personalized Backrooms Level-0/dreamcore space dossier and, when requested, a reference-led photoreal still or short shot from a supplied character, pet, object, or scene image. Use for “my Backrooms”, image-specific liminal-space transformations, and dossier-first dreamcore work; unlike `restyle-room` (relationship 0.58), choose this when Level-0 grammar and the personalized space interpretation matter; unlike `generate-video` (0.66), choose it when the reference, spatial tendencies, and dossier own the result. Do not use for lore Q&A, generic horror imagery, psychological assessment, or ordinary room restyling.
---
# Backrooms Dreamcore

## Catalog

- Display name: Backrooms Dreamcore
- Categories: Video
- Status: Ready
- Route label: Personalized Level-0 space dossier and visual route
- Tone: lime
- Short description: Turn one supplied reference into a restrained, photoreal liminal-space dossier and optional media.
## What this skill does

- Classifies one reference as a subject-led, scene-led, or mixed source and preserves the requested identity, spatial structure, mood, or detail.
- Produces a compact space dossier that turns four optional atmospheric choices into clear spatial constraints.
- Generates only on request, with Level-0 visual grammar primary and the supplied reference grafted in without poster-like spectacle.

## How to use

Provide one supplied image, whether subject or scene takes priority, four choices or permission to use fast mode, the requested output medium, ratio, and any must-keep reference facts.

#### Example

```text
用这张办公室照片做我的后室切片。先问我四个选择题，再给一个空间档案；我确认后生成 16:9 的真实摄影感静帧，保留窗边那张红椅子。
```

## Workflow

1. Require one supplied character, pet, object, or scene image. For mixed sources, ask whether subject identity or space structure has priority. Do not infer personality, diagnosis, fate, or mental state from the image or answers.
2. Unless fast mode is requested, ask four concise choices about entrance, repetition, light, and the one reference element to preserve. Translate them into bounded/open, frozen/flowing, solitary/traces, natural/artificial, and orderly/chaotic tendencies.
3. Write one dossier: a space name, source type, preserved core, three-to-five sentence space description, fluorescent/recording filter, one or two restrained anomalies, and a self-contained media brief. Continue directly through the supported API route without a client-side payment confirmation.
4. Apply Level-0 grammar before reference details: mundane repeating carpet/wallpaper/ceiling grid, fluorescent illumination, deep perspective, low dynamic range, old-camera or surveillance texture, and sparse occupants. Keep the space primary; forbid on-image copy, logos, generic monster-poster framing, fantasy architecture, and gore.
5. For a still, route to GPT Image 2 Medium at 2K through the native WeShop path, preserving the declared reference role. For a moving shot, hand off one atomic brief to `$generate-video`; use `$animate-image` only for bounded motion of an accepted still. Select video models through the current catalog and never hard-code a provider model.
6. Create one durable `operationKey` for each intended image or video run, persist its reference roles and normalized fields, poll only the accepted `executionId`, and treat an ambiguous create result as outcome-unknown rather than resubmitting.
7. Inspect the dossier-to-output link: preserved source facts, Level-0 grammar, photorealism, ratio, no unwanted text, spatial plausibility, and no accidental diagnostic claim. Repair only the failed stage or report the bounded failure.


## User-facing output

- Media type: One Markdown dossier, optionally one still or one short MP4
- Default quantity: One dossier; media only when requested
- Content per artifact: Preserved source role, tendencies, Level-0 visual contract, and observable acceptance checks
- Default layout: User-requested ratio; source ratio for optional media when unspecified
- Model policy: GPT Image 2 Medium/2K for stills; existing current video route for one requested shot
- Downstream use: Approved atmospheric stills, inserts, or a dedicated video workflow
