---
name: draw-scene
description: Draw an illustration (scene, character, map route, product shot, social-media art) as an SVG or PNG by writing a short YAML scene that the scenec compiler checks and renders, with no image model and no need to see the result. Use when asked to illustrate, draw, make a cover, carousel, reel frame, e-learning scene, journey map or ad variation; also "ilustrar", "desenhar", "fazer uma ilustração".
license: MIT
compatibility: Needs Node 20+ and network access to npm for npx; no image model and no browser.
allowed-tools: Bash(npx @guilhermebkel/scenec *)
---

# Draw a scene

You write a YAML scene. `scenec` compiles it to SVG and tells you, in text, what is wrong with it: warnings (fields it did not understand, objects out of frame) and art-director critiques (overlaps, empty space, low contrast). You never need to look at the picture.

## Workflow

1. Pick the closest recipe in `recipes/` and copy it to a working file, for example `scene.yaml`:
   - `explainer-reel`: vertical 9:16 explainer frame
   - `carousel`: square or 4:5 carousel slide
   - `personalized-wrapped`: personalized "year in review" card
   - `e-learning`: course scene with people and a screen
   - `illustrated-story`: story or history scene
   - `journey-map`: route over the map of Europe
   - `ad-variations`: ad with variations
   - `product-illustration`: product illustration
2. Change the content. Prefer `group:` (ready-made sets such as a workspace) and `canvas.shot` over placing every piece by hand. Look up names in `references/catalog.md`, or run `npx @guilhermebkel/scenec catalog assets`.
3. Check: `npx @guilhermebkel/scenec check scene.yaml`. Read `warnings` and `art`. Exit code 1 means there is something to fix.
4. Fix and check again. Stop after 5 cycles; if something still fails, say what is left instead of looping.
5. Render: `npx @guilhermebkel/scenec render scene.yaml -o out --png`. Deliver `out.svg` and `out.png`.

## Rules

- Never edit the SVG by hand. Change the scene and render again.
- A warning that says "you meant X" is almost always right: apply it.
- Field names and values are listed in `references/dsl.md`. Do not invent fields.
- Colors come from the theme or from `canvas.colors`; use names like `primary` and `accent` before hex values.
- Custom SVG assets go under `assets:` and are sanitized; external links and scripts are removed.
- `npx @guilhermebkel/scenec schema` prints the full JSON Schema if you need it.

## Files

- `recipes/*.yaml`: 8 scenes that compile with zero warnings and zero critiques.
- `references/dsl.md`: the scene language (generated).
- `references/catalog.md`: assets, groups, kits, themes, poses (generated).
