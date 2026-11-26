---
vendored_from: https://github.com/appautomaton/delineate
name: svg-monoline-geometric
description: >
  Draw flowers in glass in the monoline geometric style on this project's Monoline card (monoline/): one
  pen on three angles, broken stems, blocks cut in two, dots in clusters, glass drawn by formula. Use for a
  new plant, garden or bottle in the vase, a palette that looks muddy or repeats, stems that cross or crowd,
  or a card that moves wrong, even if the user never says "skill".
triggers:
  - svg-monoline-geometric
  - svg
  - monoline
  - geometric

---

# Monoline geometric

Ikebana drawn as a metro map. `monoline/notes.md` maps the modules and holds the rules a change must keep;
read it first.

## The bar

- **One pen, three angles.** Stems and branches are drawn with the one pen (`PEN`, round-capped, a hero's
  stem a little heavier) and run only at 0, 45 or 90 degrees. Flower heads may radiate; only the hero
  may be drawn round.
- **Lines break.** A line is pieces, gaps and dots (`run`): reeds above the water, every stem below it.
- **Shade is a cut.** Leaves and petals split along the spine into a light half and a dark half, lit from
  the upper left. No gradients, no shadows.
- **True plants, true colours.** Each plant is from a Garden climate, drawn as its kind looks, coloured
  only inside the hue window it declares.

## The task

- **A plant**: add it to its garden in `plants.ts` with a role and a hue window, drawn with `pen.ts` in the
  manner of its neighbours, painting only in role tokens.
- **A garden**: an entry in `GARDENS` with at least a line, a hero and an accent whose colours do not collide.
- **A bottle**: eight points a side in `BOTTLES`, lip to foot, x from the axis.
- **A wrong palette or arrangement**: change the rule in `palette.ts` or `arrange.ts`, never one seed.

## Done means

`npm run check` passes, and on `npm run monoline` (http://localhost:5350/): the new thing reads alone at
`?seed=`, a `?sheet` of twelve shows no two cards alike in colour and no stems crossing, and `?layers`
shows each layer clean. Then tell the user what to look at.
