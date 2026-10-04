---
name: terraces
description: How a step between terrace levels works in the overworld, what a cliff tile is, and how both boards draw it. Applies whenever changing terrace levels, walkability, placement of anything on the ground, or how the board draws a step.
---

# Terraces and cliffs

`levelAt` in `src/overworld/terrace.ts` says how high a cell stands. A level only counts where the cell belongs to a 2x2 block standing at least that high, so a cliff is never one cell wide. The first step stands above the beaches and wetlands, so the sea and the low shore beside it are both level 0 and a coast meets open sea without a cliff.

The steps belong to the generation (`world.terraceSteps`). The first generation climbs through 3 levels and is frozen. The second climbs through 20 evenly spaced ones (`SECOND_TERRACE_COUNT`), a cliff about every ten cells. Anything written as a count of levels has to be carried over as a height (`levelBelow`), the way the cave water table is, since a level means a different height in each generation.

In the second generation a town is flat: every cell within two cells of its footprint (`plateauAt`) stands on its middle's level. Only cells in a 2x2 block wholly inside that circle count, so its edge obeys the 2x2 rule like any other step and leaves no lone cell. The town's own footprint (`townAt`) is squared off the same way, since a plain circle leaves one cell sticking out at each of its four points. The cliff where the slope resumes is outside the town, so no lot, street or plaza is ever on a face. Past the levelled ground the town's skirt (`townSkirts`) lets the ground stand one more level off the town's for every step out, counted in king's moves so diagonals count as one, until the natural slope catches up. The town meets the country in a staircase of one-level cliffs with no ledge between them, so nothing can be placed on it and stranded. Where two skirts reach a cell it keeps within both.

## The edge tile is the cliff

A cell standing higher than **any** of its eight neighbours is a face (`isFace` in `src/overworld/cliff.ts`). Diagonals count: a cell touching lower ground only at a corner is where the ring's inside corner is drawn, and that tile is as much the cliff as a side.

- Nobody walks on a face, unless a seam runs through it (`blocksWalk`). Water on a face is always a seam: a pool never sits at a dry drop, so it pours into more water. A natural pass (`isPassAt`) is a band three cells wide crossing a cliff every twenty cells along it, offset by a seeded hash per stretch and level, so a walk beside a terrace is never far from a way up. A road or a route on a face is always a seam, corners and diagonal-only faces included, so no street is ever cut by a cliff. A natural pass seams a face only where it leads somewhere (`leadsThrough`): lower ground straight beside it, and where the faces beside it turn a corner, every one of those faces a way through too (water, a road or a route counts). A pass face touching lower ground only at a diagonal, or a corner joined to a single other seam, reaches the high ground only diagonally, so it stays a cliff. Faces on two opposite sides are a straight cliff line, the usual way through.
- Underground every face is a seam (`isSeam` answers yes at `Depth.Cave`), corners included, so no cliff ever crosses a cave passage. A cave's rock walls are not faces: they are `wall` cells, raised a level only for drawing.
- Nothing is placed on a face, seamed or not: no scenery, no rolled landmark, no spawn, no phenomenon and no player start. `Chunk.getFaceCells()` is the set to leave out.

## Lava

A volcano's water is lava (`isLavaAt` in `src/overworld/ground.ts`, `Chunk.getLavaCells()`). Nobody walks on it, whatever the cliffs around it say, and nothing is placed on it: no landmark, spawn, phenomenon or player start. Any other water stays walkable. Ice pools are water drawn as ice, and a spawn on one draws from the biome's ice pool (see `spawn-surfaces`).

## Water at a step

Water is never a cliff unless the lower ground beside it, diagonals included, is water too. Then the two are one fall. Water that would stand at the lip of a dry drop is dried to ground by the lip rule in `src/overworld/ground.ts`. Every 2x2 block of water stands on one level, so a cell's water depends only on the water below it and the lip rule reads the finished answer there.

## Drawing it

The cliff art is the biome's `face` terrain: the 3x3 ring autotile and its inside corner piece. `terrainCell` lays it whole on a dry, unseamed face as the `cliffs` step, picked for the neighbours standing at least as high, after the paving and before the blends between two countries. A cliff tile never takes a blend on top of it. An open sea draws no shore of its own, so dry ground of another country beside it lays the sea's hollow `blend` ring at the `shore` step, turned with the camera like any shore. Both boards draw that same cell.

- **Flat board:** the ring lies on the edge tile like any other layer.
- **Laid-back board:** a cliff tile always comes from the bottom row of the ring (or the bottom of the inside corner piece), picked with the neighbourhood turned so the low side reads as south and drawn turned back, so the rock face looks the same whichever way the step falls. Every quad corner sinks to the lowest of the four cells meeting there. A face tile therefore runs from the ground above it to the ground below, stitched at both edges, with no wall and no gap. The WebGL scene (`src/canvas/three/board-scene.ts`) and the canvas fallback (`src/components/overworld/chunk-canvas/index.tsx`) follow the same rule, and so does picking a cell under the pointer.
