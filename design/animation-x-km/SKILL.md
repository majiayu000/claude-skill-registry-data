---
name: animation-x_KM
description: >-
  Plain-English animation command chooser. Use this when Kosta asks which animation command/skill to use, or wants an animation made but has not picked the style yet.
metadata:
  hermes:
    command_priority: 95
    tags: ['animation', 'chooser', 'motion-design']
---
# Animation X

This is the friendly menu for the animation stack. Load it when the user says `/animation_x`, asks what animation tools exist, or gives a vague animation brief.

## Which command to use

- `/animation_lab` — best default. Use for a polished visual exploration, 4-8 directions, contact sheet, or when unsure.
- `/animation_title` — cinematic title cards, intros, trailers, kinetic captions, promo clips.
- `/animation_explainer` — math/science/technical explainers, equations, diagrams that move.
- `/animation_web` — designed HTML/CSS/JS videos, overlays, captions, scene transitions, social clips.
- `/animation_from_website` — turn a URL or existing website into a video walkthrough/promo.
- `/animation_live_visuals` — TouchDesigner/live generative visuals, audio-reactive stage visuals, experimental shader-like looks.
- `/animation_3d_scene` — Blender/3D scenes, cameras, materials, particle sculptures, object animation.
- `/animation_generative_art` — p5.js/canvas loops, particles, flow fields, interactive sketches.
- `/animation_ui_motion` — app/web UI transitions, microinteractions, easing, choreography.

Default recommendation: if the user does not know which one to pick, use `/animation_lab` and make a contact sheet of the strongest directions.

## Output standard

For quick explorations, produce a short MP4 or GIF plus a still/contact sheet when useful. For polished work, render a clean MP4 for the requested surface and verify it with `ffprobe` before calling it done.

## Naming note

Telegram shows this command with underscores because Telegram slash commands cannot contain hyphens. Hermes resolves the hyphenated skill name normally elsewhere.
