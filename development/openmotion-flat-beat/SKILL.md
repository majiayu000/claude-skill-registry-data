---
name: openmotion-flat-beat
description: >-
  OpenMotion — Make a punchy product promo that hard-cuts full-screen solid colours on the music beat, one rounded word or simple shape per cut, ending on a big wordmark. Use for consumer apps, courses and launches with an upbeat track and a short, chantable message.
---

# OpenMotion · Flat Beat

Build the video as a native OpenMotion HTML/CSS/JS composition through the installed OpenMotion production Skill: create or open the project, author the composition, save with revision protection and preview. This library Skill adds creative direction only; it registers no MCP Tool or production route. Treat palette, font and timing values below as starting points; a supplied Brandkit or the user's brand wins. For missing images, voice or music, first discover providers and model IDs with `openmotion_media_use`, then generate with `openmotion_assets_use`; get the user's consent before any paid generation. Never invent quotes, numbers, specs or dates.

**Status:** recipe / draft. No executable template or rendered comparison yet.

**Use for:** consumer apps, courses and teasers set to an upbeat track.

## Look

| Element | Starting value |
| --- | --- |
| Palette | Cream `#F7F1E8`, coral `#FF5A5F`, navy `#16213E`, sun `#FFD166`, teal `#2EC4B6`; each cut is one flat background colour |
| Type | One rounded heavy sans, 180–260 px for single words, 100–120 px for stacked lines, colour from the same palette |
| Shapes | Simple flat props between words: a striped ball, three dots, a sunburst of 18 rays; no outlines, no gradients |
| Grid | Everything centred; at most three short lines on screen |
| Progress | Optional thin bottom bar filling over the video |

## Motion

- Cut on the beat: measure the track's beats first and place every colour change on one (about 0.5–0.8 s apart at 100–120 BPM).
- Each cut gets one entrance: scale pop from 1.25 or 0.6 with back-out (300–400 ms), a letter-by-letter rise (40 ms stagger), a drop with bounce, or a roll-in for shapes.
- Lists build on consecutive beats on one colour (one item per beat) instead of cutting.
- End on the wordmark with a slightly longer hold (1.5 s+) and one final pulse on the last beat.

## Inputs

Required: the music track or its BPM, product name, 5–8 one-to-three-word lines. Optional: logo, brand palette of up to five flat colours, a key number the brief supplies. Music is generated through `openmotion_media_use` → `openmotion_assets_use` only with consent if the user has none.

## Avoid

Cuts off the beat, gradients or photos, more than three words per cut, two colours in one background, holding any cut longer than 1.5 s before the end card.

## Review

Every cut within two frames of a beat; each word on screen 0.5 s+; text pairs keep 3:1 contrast.

## Provenance

Written for OpenMotion after surveying publicly listed workflow names and descriptions in ChatCut's preset gallery (November 2026). Original text; no ChatCut prompts, source code, templates or media are included. Apache-2.0, like the rest of the repository.
