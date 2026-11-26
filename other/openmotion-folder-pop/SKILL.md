---
name: openmotion-folder-pop
description: >-
  OpenMotion — Make a product promo where feature icons burst out of a folder and settle in a ring around the logo. Use for SaaS and all-in-one app launches with 4–8 named features.
---

# OpenMotion · Folder Pop

Build the video as a native OpenMotion HTML/CSS/JS composition through the installed OpenMotion production Skill: create or open the project, author the composition, save with revision protection and preview. This library Skill adds creative direction only; it registers no MCP Tool or production route. Treat palette, font and timing values below as starting points; a supplied Brandkit or the user's brand wins. For missing images, voice or music, first discover providers and model IDs with `openmotion_media_use`, then generate with `openmotion_assets_use`; get the user's consent before any paid generation. Never invent quotes, numbers, specs or dates.

**Status:** recipe / draft. No executable template or rendered comparison yet.

**Use for:** launches where one product holds many parts: files, workspaces, suites.

## Look

| Element | Starting value |
| --- | --- |
| Background | Soft cool grey `#EDF1F4` with a white centre glow; no texture |
| Container | One flat folder or app window in a deep ink `#13303A`, rounded 16–18 px |
| Feature tiles | Rounded squares (radius ≈ 27% of size), one solid colour each from a 4–6 colour set, e.g. `#3B74FF`, `#9C5CFF`, `#FF6F5B`, `#2DC9A0`, `#F4B532`; white glyph inside |
| Labels | Geometric sans, bold, 22–26 px, on small white pills under each tile |
| Layout | Tiles on an ellipse filling ~70% of the frame width; a thin dashed orbit line joins them; logo and tagline in the centre |

## Motion

- Container scales in (400 ms, slight overshoot), then wiggles ±5° for ~400 ms as anticipation.
- Lid opens; tiles pop out one by one every 100–120 ms, travelling 500–650 ms with a back-out ease and a small rotation that settles elastically.
- The dashed orbit draws around the ring in about 1.2 s once the last tile lands.
- The container shrinks into the product mark while the wordmark and tagline rise underneath (500 ms).

## Inputs

Required: product name, logo, 4–8 real feature names, a one-line tagline. Optional: brand colours, UI screenshots, a call to action.

## Avoid

More than eight tiles, long feature names that wrap, icons that all share one colour, tiles crossing the logo, invented feature names or user counts.

## Review

Every label is on screen and readable; the orbit never cuts through text; the logo is the focal point at the end.

## Provenance

Written for OpenMotion after surveying publicly listed workflow names and descriptions in ChatCut's preset gallery (November 2026). Original text; no ChatCut prompts, source code, templates or media are included. Apache-2.0, like the rest of the repository.
