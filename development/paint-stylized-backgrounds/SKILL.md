---
name: paint-stylized-backgrounds
description: "Make stylized background and environment art for films, Shorts, games and illustrations in any style (anime, painterly, cartoon, retro): Blender blockout then paint-over, painting over photos, brushes, atmosphere and light, time-of-day variants, 2.5D parallax, foliage, water and animated background elements. Use for anime background, paint-over, environment art, parallax, day to night variant (\"background anime\", \"paint over\")."
license: MIT
---

# Paint Stylized Backgrounds

This craft skill owns stylized background art: the base render or photo, the paint-over, the light, the colour variants and the motion in the background.
`2d-generalist`, `3d-generalist`, `use-3d-software` and `edit-video` call it. They keep the look and the order of the whole project.

Read `local.md` next to this file first when it exists (machine paths and local rules).

## When to use

- A film, Short, game scene or illustration needs a painted or stylized background plate.
- You must turn a Blender render or a photo into a painted background.
- One background must work at day, evening, night and in rain.
- A still background must move: parallax, wind, water, birds, fireworks, card shine.

## Ask first

When the user calls this skill directly for a new piece, find out what they want before you make anything. Read the
request, attachments and project files, then ask only about what is still unclear and would change the result:
purpose and platform, format (aspect, length, file type), subject details, look (style, references) and constraints.
Ask at most 4 questions in one round, each with 2 to 4 concrete options and your recommended option first (Claude Code:
`AskUserQuestion`; elsewhere a numbered list where "ok" takes the first options). Restate the goal in 2 or 3 lines,
show the cheapest preview of the look before the expensive step, and compare the result with the goal before you hand
it over. When a generalist skill called this one with a brief, use that brief and do not ask again.

## Core rules

1. Render the base in Blender EEVEE with View Transform = Standard. Filmic and AgX grey out flat colours. Use AgX only for stylized realistic.
2. Choose the base by the place. Use a photo for a real location. Use a render for a made-up place. Block out simple shapes and paint more, or model more and paint less.
3. Paint the base bright, in daytime light, without hard shadows. Redraw shadows for each mood on their own layers.
4. Split the art into foreground, middle ground and background layers before you colour or animate. Paint behind every occlusion so the parallax has no holes.
5. Soften the CG edge first: draw lighter bevel lines on object edges and roughen shadow and glow edges. Do this on every object, not on some.
6. Build depth with fog on a clipped layer. Far layers get lighter and lower in contrast. Near layers stay darker and sharper.
7. Use warm light with cool or blue shadows. Tint the dark world colour, because some shadows still go grey. Ghibli-like style uses a yellow-green fill instead of cold blue.
8. Repaint the sky for each mood. A photo filter on the sky looks wrong.
9. Remove frozen people and animals from a plate that will move.
10. Add noise (Overlay or Soft Light) on top to hide the seam between photo, render and paint. Skip it for flat cartoon.
11. Move far layers slower than near layers. Vary every value in a copy so wind and sway never run in sync.
12. Keep a clean daytime master and build every variant from it.
13. In a Blender background, cut clouds and mountains as image cards with a mask, fade far cards bluer, add a fog plane, and tie everything with one low-strength compositor tint.

## Workflow

1. Choose the base (photo, blockout render or detailed render) and the style. Read `references/render-and-blockout.md`.
2. Render with Standard colour, a transparent film and simple lights. Keep passes and layers you need for the paint-over.
3. Crop, fix the perspective, split into layers, then adjust colour. Read `references/paint-over-and-brushes.md`.
4. Paint over: edges, sky, clouds, trees, grass, removals. Add glow, rays, fog and grain.
5. Build the time-of-day and weather variants. Read `references/light-colour-and-time-of-day.md`.
6. Animate: parallax first, then wind, water and other moving elements. Read `references/animate-backgrounds.md`.
7. Run the checks below, then hand the plate to the calling skill.

## Routing

| The task is | Read |
| --- | --- |
| Blender settings for a background render, EEVEE 5.x names, blockout, trees, bushes, grass, toon material | `references/render-and-blockout.md` |
| Paint-over steps, layers, bevel lines, sky and clouds, brushes, glow lines, rain, final touches | `references/paint-over-and-brushes.md` |
| Lights, fog, glow, rays, teal-orange grade, evening, night, rain, stars, vignette | `references/light-colour-and-time-of-day.md` |
| Parallax, camera moves, wind, foliage, water, birds, fireworks, holographic card | `references/animate-backgrounds.md` |
| Blender image cards (clouds, mountains), masks, fog plane, sun glow, god rays, scene order of work | `references/blender-card-backgrounds.md` |
| Leaf planes, Sapling trees, bushes, anime grass, falling leaves, foliage wind | `references/blender-foliage-and-grass.md` |
| Stylized waterfall, pool, ocean, rain, smoke, fire, looping and stepped shader motion | `references/blender-water-and-fx.md` |
| Compositor stack, colour unity, 2D look, finishing checklist, Blender render then paint-over in Krita or Clip Studio Paint | `references/compositing-and-2d3d-process.md` |
| Low-poly rocks, stumps, painted fake depth, Ghibli-style food props | `references/low-poly-scenes-and-food-props.md` |

For NPR toon shading, outlines and painted character textures, read `model-characters` `references/npr-shading-and-painted-look.md`. Do not copy those steps here.

## Checks

- Look at the plate at full size and at thumbnail size. The layers must read far to near.
- Check the colours: no grey wash, no pure black shadows, no clipped glow.
- Check every layer edge for a halo, a hole or a cropped corner after the camera move.
- Play the animation. No two elements move in sync, and every loop closes with no pop.
- Compare the day, evening and night variants side by side. Light sources must stay brighter than their surroundings.
- Check that the style rule held: a flat cartoon plate has no grain, a Ghibli-like plate has soft edges.
