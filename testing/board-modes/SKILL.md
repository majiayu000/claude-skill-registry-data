---
name: board-modes
description: The overworld board is drawn either laid back under the camera or flat from straight above, and which one is in hand is asked of the board rather than assumed. Applies whenever writing or reviewing anything that draws on the chunk board, projects a point onto it, or reads how far it is tilted.
---

# The two boards

`src/canvas/board.ts` holds two projections, not one.

- **3d**, the board laid back under the camera at sixty degrees: a trapezoid, the far rows smaller than the near ones, sprites standing up out of it.
- **2d**, the board flat from straight above: square cells, no perspective at all, nothing standing above the ground.

Which one is drawn is decided by the shape of the screen, in `viewFor(width, height)`: taller than it is wide is flat, anything else is laid back. The one exception is the player's Flat board setting, which the painter hands to `setBoardFlat` so every screen is drawn flat. Nothing else may decide it.

## A phone is framed close

A screen whose shorter side is under `CLOSE_SCREEN` pixels, either way up, gets the same projection framed round `CLOSE_RADIUS` cells instead of the whole live circle, so its cells stay large enough to read and press. The live circle itself does not shrink: what stands outside the framing is still tracked, just off the picture. Anything sized off the frame reads it from `boardView()` (`span`, `compass`), never from `BOARD_RADIUS`.

## Ask the board, do not assume

`boardView()` answers with the view in hand. Everything a painter needs is on it:

- `mode`, `'2d'` or `'3d'`
- `depth`, how much of a step across the ground survives being drawn
- `rise`, how much of a step into the air survives it, which is none of it flat on
- `squash`, how flat a patch of ground lies, for a shadow or a pool of lamplight
- `aspect` and `span`, the picture's shape and how wide it is in board widths

`GROUND_DEPTH`, `GROUND_RISE` and `GROUND_SQUASH` in `src/canvas/tilt.ts` are the **laid-back** numbers, and they are there for the tools that cut sprite sheets, which are cut for one tilt and cannot follow a screen. Anything drawn on a live board reads `boardView()` instead. A drawing that reaches for the constants is drawing for a camera that may not be there.

## Name the screen before projecting

The projection answers for whichever screen was last named, so `setBoardScreen(width, height)` comes before anything is put through it:

- the painter names it once a frame, before it fits the picture,
- a pointer handler names it after measuring its own box,
- a browser test names it after measuring the board's box, which is why `spotOf` in `e2e/walk.ts` takes the point as a thunk.

## What the flat board does not have

Seen from straight above there is no third dimension left to draw in, so the flat board leaves out anything that only means something with one:

- a shadow is the round patch under the feet, never the thing's own picture leaned along the light,
- the weather is drawn against the glass rather than standing in the world, which is the sky's own older path and is what leaving the camera out of `paintSky` and `batchSky` asks for.

Adding something that stands in the air means saying what it does flat on as well.

## Giving way to the player

In both boards, anything drawn after the player that covers enough of them fades and comes back: `coverOf` and the `VEIL_*` numbers in `src/components/overworld/chunk-canvas/metrics.ts`. It is a fade rather than a switch, and each of a cell's pictures fades on its own.
