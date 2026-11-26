---
name: openmotion-ink-ribbon
description: >-
  OpenMotion — Make a promo where one glossy ribbon sweeps through the frame and ties together outlined type, icon steps and the product name. Use for fintech, payments and workflow products whose story is a smooth flow from start to finish.
---

# OpenMotion · Ink Ribbon

Build the video as a native OpenMotion HTML/CSS/JS composition through the installed OpenMotion production Skill: create or open the project, author the composition, save with revision protection and preview. This library Skill adds creative direction only; it registers no MCP Tool or production route. Treat palette, font and timing values below as starting points; a supplied Brandkit or the user's brand wins. For missing images, voice or music, first discover providers and model IDs with `openmotion_media_use`, then generate with `openmotion_assets_use`; get the user's consent before any paid generation. Never invent quotes, numbers, specs or dates.

**Status:** recipe / draft. No executable template or rendered comparison yet.

**Use for:** payments, banking, logistics and workflow tools that can be told as three steps joined by one continuous motion.

## Look

| Element | Starting value |
| --- | --- |
| Palette | Deep green `#0E3A2C` or paper grey `#E9ECEF` grounds; ribbon blue `#2EA8F0` to pale `#BDE6FF`; ink `#111` |
| Ribbon | A wide SVG path with a gradient across its width and a soft highlight edge |
| Type | Clean grotesk; outlined repeat of the product name as a background pattern; solid black for the closing lockup |
| Icons | 2–3 circular line icons (document, shield, check) in one row |
| Accent | One sparkle mark that leads the eye; highlight the key word with a blue box |

## Motion

- The ribbon draws itself along its path in 900–1200 ms and keeps a slow drift; it passes behind type, never over the read word.
- Copy writes on word by word behind a moving sparkle (about 150 ms per word).
- Icons pop in left to right with a 150 ms stagger; the last one morphs into a check.
- Close on the product name typing on, a tagline with one highlighted word, held 1.5 s.

## Inputs

Required: product name, logo, a three-step flow in plain words, one closing question or call to action. Optional: brand colours for ground and ribbon.

## Avoid

More than one ribbon, ribbons crossing the read text, busy textures, steps that the product does not actually perform.

## Review

The ribbon is continuous from first to last shot; every line is readable with the ribbon behind it; the three steps match the product's real flow; lockup holds 1.5 s.

## Provenance

Written for OpenMotion after surveying publicly listed workflow names and descriptions in ChatCut's preset gallery (November 2026). Original text; no ChatCut prompts, source code, templates or media are included. Apache-2.0, like the rest of the repository.
