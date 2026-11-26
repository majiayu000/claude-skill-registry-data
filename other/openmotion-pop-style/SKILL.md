---
name: openmotion-pop-style
description: >-
  OpenMotion — Cut a loud pop-art promo: flat primary colour blocks, Ben-Day dots, thick black outlines, speech bubbles, starbursts and a cut every second. Use for app launches, offers and announcements that must stop the scroll.
---

# OpenMotion · Pop Style

Build the video as a native OpenMotion HTML/CSS/JS composition through the installed OpenMotion production Skill: create or open the project, author the composition, save with revision protection and preview. This library Skill adds creative direction only; it registers no MCP Tool or production route. Treat palette, font and timing values below as starting points; a supplied Brandkit or the user's brand wins. For missing images, voice or music, first discover providers and model IDs with `openmotion_media_use`, then generate with `openmotion_assets_use`; get the user's consent before any paid generation. Never invent quotes, numbers, specs or dates.

**Status:** recipe / draft. No executable template or rendered comparison yet.

**Use for:** app and feature launches, limited offers, event teasers and short social hooks aimed at a young audience.

## Look

| Element | Starting value |
| --- | --- |
| Colour | Flat blocks of yellow `#FFD21F`, hot pink `#FF3E8A`, cyan `#22C3E6`, off-white `#FFFDF5`; outlines `#111` |
| Texture | Ben-Day dot overlay (22 px grid, 15% black); sunburst stripes behind the hero |
| Type | Heavy condensed caps with a 5 px black stroke and a 9 px hard offset shadow |
| Shapes | Speech bubbles, starburst stickers, comic panels; every shape has a 6–8 px black outline and hard shadow |
| Product | The UI on a flat outlined phone, tilted 4–8° |

## Motion

- Change background colour on every cut, roughly every 1.0–1.4 s, with a 3-frame white flash.
- Titles punch in: scale from 140–160% to 100% in 0.3–0.45 s with an overshoot ease.
- Words slam in from opposite sides in 0.28 s; stickers spin in from 0 with a back ease.
- Comic panels drop in one by one (300 ms apart) with a slight tilt.
- Land on a logo and slogan scene and hold it for at least 2 s with a small wiggle.

## Inputs

Required: product name, one short hook line, the UI screen or the key feature. Optional: offer or date, brand colours to swap into the palette, three things to show in panels.

## Avoid

Gradients, soft shadows, thin outlines, more than three colours plus black and white per scene, long sentences, real comic characters or anyone else's mascot.

## Review

Every scene reads in under a second; the hook and product name both appear on screen; outlines are consistent; no text crosses the frame edge during the slams; the file stays light enough for social upload.

## Provenance

Written for OpenMotion after surveying publicly listed workflow names and descriptions in ChatCut's preset gallery (November 2026). Original text; no ChatCut prompts, source code, templates or media are included. Apache-2.0, like the rest of the repository.
