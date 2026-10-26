---
name: canvas-2d
description: Use when making browser games or visualisations with the HTML Canvas 2D API and no engine — fixed logical resolution with scaling, game loop with fixed time step, pointer input for mouse and touch, drawing characters and UI from shapes only, hit testing, and performance. Also use when a canvas looks blurry on high-DPI screens, input coordinates are off, or a "shapes only" game looks unfinished.
---

# Canvas 2D games

Default: one `<canvas>`, a fixed logical resolution (e.g. 960×540) scaled to the window, a fixed-step update loop, Pointer Events, everything drawn in code (no image assets) unless the project allows them.

## Resolution and scaling

```ts
const W = 960, H = 540;
function resize() {
  const scale = Math.min(innerWidth / W, innerHeight / H);
  const dpr = devicePixelRatio || 1;
  canvas.style.width = `${W * scale}px`;
  canvas.style.height = `${H * scale}px`;
  canvas.width = Math.round(W * scale * dpr);
  canvas.height = Math.round(H * scale * dpr);
  ctx.setTransform(scale * dpr, 0, 0, scale * dpr, 0, 0); // draw in logical units
}
```

- Convert pointer positions back to logical units with the canvas's `getBoundingClientRect()` and the same scale.
- Recompute on `resize` and orientation change; support both landscape and portrait if mobile matters.

## Loop

- `requestAnimationFrame` for rendering; accumulate elapsed time and run `update(FIXED_DT)` in a while loop; cap the accumulator after a tab switch.
- Keep update deterministic (seeded RNG, fixed step) so automated "bench" players can measure difficulty.

## Making shape-only art look finished

- Silhouette first: a character must be recognisable as a filled shape. Then add 2–3 tones (base, shadow, highlight) and an outline.
- Use rounded rectangles (`ctx.roundRect`), consistent stroke widths and a limited palette.
- At small sizes switch to simpler drawings (level of detail): full detail above ~12 px, a rounded block with an outline at 8–12 px, a dot in team colour below that.
- Give the UI hierarchy: one large number, smaller labels, panels with padding and rounded corners.
- Add "juice" with restraint: hit pause (a few frames), screen shake, particles, floating numbers, and a sound for each meaningful action.
- Separate overlapping units visually (draw-time offsets) rather than moving them in the simulation, so game logic and tests are unaffected.

## Performance

- Batch by state: set `fillStyle` once, draw many paths, avoid `save/restore` in inner loops.
- Pre-render static backgrounds to an offscreen canvas and `drawImage` it each frame.
- Avoid `shadowBlur` and `filter` in hot paths; they are expensive.
- Text: cache measured widths; `fillText` with many fonts per frame is slow.
- Measure with a stress scene (thousands of units) and keep the frame time under budget on modest hardware.

## Verification loop

1. Unit tests for update logic (no canvas).
2. Playwright: open each screen, assert no console errors, take screenshots at desktop and phone sizes.
3. A bench that runs the simulation headless across seeds and asserts difficulty ranges.

## Pitfalls

- **Blurry output:** forgetting `devicePixelRatio`.
- **Touch scrolling and zooming** steal input: `touch-action: none` on the canvas.
- **Fonts:** a web font may not be loaded on the first frame; wait for `document.fonts.ready` or use system fonts.
- **Sub-pixel lines** look fuzzy; align 1 px strokes to `x + 0.5`.
- **`clearRect` with a transform** clears in transformed space; reset the transform or clear the logical rectangle.
