---
name: render-qa
description: Catch broken renders before anyone sees them - checks every rendered video or image for wrong duration, grey or black borders, cut-off or overlapping text and wrong prices or numbers, using a contact sheet. Use after every render and every re-render.
author: sant1jmnz
tags:
  - video
  - quality
  - ffmpeg
---

1. Confirm the target duration BEFORE rendering.
2. After rendering: `ffprobe` duration (fail if it's off by more than 10%), resolution and aspect ratio.
3. Extract one frame every 3 s (`ffmpeg -vf fps=1/3`) and build a contact sheet.
4. Look at the sheet: no grey/black borders (common headless-browser viewport bug), no cut-off or overlapping text, prices and figures correct.
5. If something fails: fix the template and re-render (max 4 iterations). Repeat the check on EVERY re-render.
6. Deliver a table: file, duration, checks passed, contact-sheet path. Don't send anything to anyone without the user's OK.
