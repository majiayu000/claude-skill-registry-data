---
name: demo-animation
description: Generate a simple desktop-oriented self-playing HTML product demo. Use for legacy demo walkthroughs with an intro screen, dashboard mockup, sidebar captions, timeline controls, cursor animation, highlights, piano music, and ending screen. Prefer demo-animation-v2 when the user needs mobile support, fullscreen controls, touch gestures, or the packaged template engine.
metadata:
  version: 1.1.0
---

# Demo Animation

Generate a simple self-playing HTML product demo. Output: `demo/index.html`.

For most new demo requests, prefer `demo-animation-v2`. Use this skill when the user asks for the legacy desktop-oriented demo style or when a smaller, simpler demo is enough.

## Workflow

1. Read the project README, app entry points, and relevant UI files.
2. Identify the product name, tagline, visual style, font stack, and 6-10 features to showcase.
3. Draft a brief demo step list. If the project is unclear, ask one concise question; otherwise proceed.
4. Generate a single self-contained `demo/index.html` file with no external dependencies except Google Fonts.
5. Include intro, dashboard mockup, animated cursor/highlights, sidebar captions, timeline controls, optional piano music, ending screen, and replay.
6. Validate that all referenced IDs exist, controls work, and the file opens directly in a browser.

## Legacy Reference

If you need the original desktop architecture, read `references/legacy-demo-engine.md`. It contains the older detailed CSS, layout, animation, music, and quality checklist guidance.

## Rules

- Keep the generated UI realistic for the actual product.
- Keep wait times reasonable: 800-1500ms for reading, 300-600ms for animations.
- Do not add network dependencies beyond Google Fonts.
- Do not use this legacy skill when the user explicitly requests mobile-first, touch, fullscreen, or highly responsive behavior; use `demo-animation-v2` instead.

## Output

Write to `demo/index.html`. Tell the user:

```text
Demo created at `demo/index.html`. Open it in a browser to preview. Click "Watch Demo" to start the animation.
```
