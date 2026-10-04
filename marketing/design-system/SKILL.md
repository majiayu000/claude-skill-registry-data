---
name: design-system
description: Define a reusable visual design grammar for film titles, posters, key art, lower thirds, thumbnails, social assets, press materials, and programmatic motion graphics using approved references, exact text, safe zones, and accessibility constraints.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Design System

1. Read `../../references/DESIGN_SYSTEM.md`, visual bible, approved references, campaign brand, and release requirements.
2. Write `06_release/artwork/design_system.json`.
3. Define palette roles, typography hierarchy, title treatment, grid/spacing, motifs, image treatment, safe zones, watermark rules, motion behavior, contrast, and forbidden shortcuts.
4. Reference project `REF-###` assets rather than copying an external campaign.
5. Keep exact title/release text separate from generative imagery.
6. Run `scripts/design_system.py 06_release/artwork/design_system.json` before producing a coordinated asset family.
7. Route still output to `marketing-art`/`imagemagick` and animated output to `motion-graphics` or `programmatic-video`.

Done when promotional and editorial graphics can be produced as variants of one coherent visual system.
