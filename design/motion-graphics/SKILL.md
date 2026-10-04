---
name: motion-graphics
description: Plan and render reusable film and campaign motion graphics such as title cards, lower thirds, watermarks, end cards, text overlays, framing treatments, fades, and transitions using stable GFX identities and verified text.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Motion Graphics

1. Read `../../references/MOTION_GRAPHICS.md` and, when present, the design system.
2. Give each graphic a `GFX-###` ID and source IDs.
3. Use exact verified names, titles, dates, URLs, and calls to action.
4. Protect story action, faces, subtitles, and title-safe regions.
5. Render ordinary overlays with `scripts/motion_graphics.py` and FFmpeg.
6. Route richer code-driven animation to `programmatic-video`.
7. Register rendered graphics/media outputs and run applicable QC.

Done when the requested graphics package is reproducible, traceable, and visually safe for its destination.
