---
vendored_from: https://github.com/appautomaton/delineate
name: svg-sdf-glass
description: >
  Make or change Glass (glass/): a solid of clear glass that follows the reader's pointer over a page of words
  or a Garden drawing, refracting it, and melts from one shape into the next (ring, tetrahedron, octahedron,
  sphere, rounded cube, capsule), raymarched as signed distance fields in one WebGL2 shader; the pages under it
  melt into one another as 2D distance fields. Use for a new shape, a
  glass that reads as plastic or as a flat lens, refraction that tears or swims, a shadow that floats, new words
  or drawings under the glass, a melt between pages, colours by day or night, or a stage that drops frames,
  even if the user never says "skill".
triggers:
  - svg-sdf-glass
  - svg
  - sdf
  - glass

---

# SDF glass

A solid of glass held over the page. `glass/notes.md` maps the modules and holds the rules a change must
keep; read it first.

## The bar

- **It is glass, not a filter.** Light enters, bends, crosses the solid and bends again on the way out
  (index about 1.45): what lies behind is magnified, turned over and softened where the glass is thick.
  Edges go dark where the light inside cannot get out; the faces catch a soft window of light. No colour
  of its own, no dispersion: grey glass over paper and ink.
- **Shapes melt, and so do pages.** One shape becomes the next by easing between their distance fields,
  swelling a little rounder as it goes; one page becomes the next the same way in two dimensions, words
  pooling into a drawing and a drawing into words. Never a cross-fade of two pictures.
- **It sits on the page.** It floats past a sphere's focus, so a sphere shows the words turned over and
  whole. Its shadow falls down and to the right, soft at the rim and lighter at the core where the glass
  gathers light, and is never cut by the stage's edge.
- **The light is the site's; the colours are Glass's own.** Day or night is the reader's choice on
  delineate's page, kept under its key. Each light has a few quiet pairs of paper and ink, and each turn
  of the light eases into that light's next pair: the first by day is the site's own paper, and by night
  the paper is dim, its hue just there, the ink a soft light. The page around the stage wears what the
  stage does, frame by frame.
- **Smooth under the hand.** It follows the pointer at the screen's own rate, the raymarching done only
  near the solid and its shadow, and sleeps out of view.

## The task

- **A shape**: a distance function in `shader.ts`, about one unit across, added to `SHAPES` in the order
  it melts; keep it within the bound the shader marches.
- **The glass's feel**: the index, absorption, blur and room in `shader.ts`; the height, follow, spin
  and timing in `show.ts`. Moving the light means moving `FALL` with it.
- **What lies behind**: the lines in `WORDS` and the Garden drawings in `PICTURES` (`pages.ts`), shown in
  turn. A drawing needs an outline that reads as a silhouette at a glance; `build.ts` copies each beside the
  page. `source.ts` draws a page's mask, `field.ts` measures it in a worker, and the shader lays paper and
  ink on the field.
- **A pair of colours**: `palette.ts`, in the light it belongs to. Judge it alone with `?tones=<name>`, and
  by night look that the glass still catches light at its edges and its shadow still reads.

## Done means

`npm run check` passes, and on `npm run glass` (http://localhost:5370/): every shape read alone with
`?shape=` looks like cut glass, each change melts, the words stay crisp outside the glass and soften only
within it, by day and by night in every pair, over the words and over `?picture`; a turn of the light
eases with no seam between the stage and the page around it; words melt into each drawing and back, and
no frame is dropped while the next page is measured; pushed into a corner, the shadow stays
whole. Measure in the browser: every frame the display offers kept while the glass moves. Then tell the user what to look at.
