---
name: openmotion-doc-promo
description: >-
  OpenMotion — Tell a short documentary-style brand story: one real person, a specific moment, honest subtitles, a cut to the product doing its job, and a quiet end card. Use for app and service promos that show a moment instead of listing features.
---

# OpenMotion · Doc Promo

Build the video as a native OpenMotion HTML/CSS/JS composition through the installed OpenMotion production Skill: create or open the project, author the composition, save with revision protection and preview. This library Skill adds creative direction only; it registers no MCP Tool or production route. Treat palette, font and timing values below as starting points; a supplied Brandkit or the user's brand wins. For missing images, voice or music, first discover providers and model IDs with `openmotion_media_use`, then generate with `openmotion_assets_use`; get the user's consent before any paid generation. Never invent quotes, numbers, specs or dates.

**Status:** recipe / draft. No executable template or rendered comparison yet.

**Use for:** app, tool and service promos, customer stories and founder notes where one believable moment sells better than a feature list.

## Look

| Element | Starting value |
| --- | --- |
| Frame | 2.39:1 letterbox inside 16:9; handheld drift of 4–6 px; warm practical light against teal shadows |
| Grade | Soft teal shadows `#173037`, warm highlights `#F2A55E`, lifted blacks, gentle vignette |
| Type | Lower-third name and role in a plain sans with a 4 px accent bar; mono timestamp in a corner; centred subtitles with soft shadow |
| Product | The real interface shown full screen, scaled to fill 80% of the frame |
| End card | Product name in a serif, one honest line underneath, same warm light |

## Motion

- Three beats in about 8–15 s: the person and the problem, the product working, the person afterwards with the end card.
- Hard cuts between beats; each shot carries a slow push or pull of 8–12%.
- Subtitles reveal word by word at the spoken pace and never sit over the face.
- On the product beat, show a before-to-after change happening on screen (a scan, a progress pass, a check appearing every 400–500 ms).

## Inputs

Required: the product's real UI recording or screenshots, the one moment to tell, the exact line the person says. Optional: a filmed person, location, brand colours.

If no footage of a person exists, the person and room are generated through `openmotion_media_use` → `openmotion_assets_use`; approve one test clip before generating the rest, keep the same person and light across clips, and label the person as generated. Use the user's real interface for every product shot.

## Avoid

Invented testimonials or numbers, fake interfaces, stock montage, more than one claim, a generated person presented as a real customer.

## Review

The story reads with the sound off; subtitles match the line exactly; the UI is the real product; generated people are labelled; the end card holds 2 s.

## Provenance

Written for OpenMotion after surveying publicly listed workflow names and descriptions in ChatCut's preset gallery (November 2026). Original text; no ChatCut prompts, source code, templates or media are included. Apache-2.0, like the rest of the repository.
