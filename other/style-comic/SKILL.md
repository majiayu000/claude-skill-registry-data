---
name: style-comic
description: Comic book style (in testing) — brush-ink outlines with variable width and tapered ends, flat print colours on newsprint, Ben-Day halftone, panels that pop in on the beat, balloons, sound effects on bursts, speed lines. Use it when asked for a comic, cartoon, pop-art, «viñetas», motion comic, onomatopoeia or panels, or when working with styles/comic/.
---

# Style · Comic

**In testing.** Reference: `styles/comic/template.js` (look at `styles/comic/review/sheet.jpg`).
Its first style test was a client piece and lives in the client's private repo.

## Code

`styles/comic/comic.js` → `Comic`. Declare both fonts in the scene (OFL, licences in `fonts/`):

```js
fonts: [
    { family: 'Bangers', src: 'fonts/Bangers-Regular.ttf' },
    { family: 'Comic Neue', src: 'fonts/ComicNeue-Bold.ttf', descriptors: { weight: '700' } },
],
```

- **Time:** `onTwos(t)` (t held on its drawing), `drawing(t)` (drawing number, 12 a second).
- **Ink:** `ink(g, pts, { w, taper, wobble, light, closed, smooth, seed, color })` is a filled
  brush line that swells and tapers; `shape(g, pts, { fill, w, shade, light, seed })` fills,
  runs `shade(g, path)` clipped inside, then inks the outline. Paths: `curve`, `resample`,
  `pathOf`, `ellipse`, `rect`, `starPts`, and `lobes(circles, cx, cy)`, the outline of a union
  of circles (clouds, bushes, round bodies).
- **Halftone:** `dots(g, path, { color, spacing, r, anchor })` (Ben-Day, tile built at output
  resolution); `halftone(g, path, { color, spacing, r0, r1, dir, box })` (graded dots for
  round forms and skies).
- **Page:** `paper(g, env, { bleed })` (newsprint, cached) and `grainPost(ctx, env)` in `post`.
- **Panels:** `panel(g, rect, drawFn, { border, bg })` clips the art and rules the border;
  `enter(t, at, dur, from)` is the pop-in on the beat (overshoot, on twos).
- **Lettering:** `letter` (balloon text, upper case), `balloon({ kind: 'speech' | 'thought' |
  'shout', tail, text })`, `sfx(g, text, x, y, { size, fill, shade })` (extruded, outlined,
  each letter tilted and growing), `burst`.
- **Motion:** `speedLines` (focus lines to a point), `motionLines` (streaks trailing a move).
- **Hands:** `hand(g, pose, size, { side, fill })`, a cartoon hand (thumb + three fingers) in
  one skin, wrist at the origin pointing up. Poses `open` (back to the camera), `backGrip`
  (holding a sheet from the camera's side: the backs of three fingers over it, the thumb
  hidden behind), `thumbFront` (the owner's view of a sheet held at its bottom edge). Drawn as
  a right hand; `side: 'left'` mirrors it.
- **Tubes** (limbs, handles): a wide ink line with a narrower colour line on top (the
  template's mug handle, `limb` in any puppet).

## Style rules

- **Palette** (`Comic.COL`): page `#f4ecd6`, deep page `#e7d9b8`, white `#fffaf0`, ink
  `#1c1a20`, red `#dd3b2d`, yellow `#f6c536`, blue `#2e67ae`, sky `#8fc9e3`, green `#4f9d63`,
  orange `#f28a2e`, pink `#ee8fa6`. Ink is never pure black and the page never pure white. A
  character keeps its own brand colour; everything else comes from the palette.
- **Line:** brush ink with a varying width; open strokes taper; closed shapes carry the heavy
  side away from the light (the light comes from the top left: `light: [0.55, 0.85]`).
  Widths in a 900-wide frame: characters 6–8, props 3.5–5, panel borders 7, details 2.5–3.5.
  Each piece has a fixed seed: **nothing boils**.
- **Colour:** flat fills. Shading only as Ben-Day dots (flat or graded) or a hard cel shape,
  never a soft gradient. Dots on a moving piece are drawn in its local transform so they
  travel with it.
- **One-skin silhouettes:** a form made of several pieces (a hand) inks every piece first and
  fills every piece on top, so only the union's silhouette keeps its line.
- **Panels:** ruled borders of even width, the page as gutter. They pop in on the beat with a
  small overshoot and read left→right, top→bottom. **A panel is a moment:** once its beat has
  passed it holds (settles) instead of replaying its action. Balloons may break a border.
- **Camera (motion comic):** start inside the first panel so it fills the frame (the hook),
  pull back to the page on a beat, a gentle push at the end. Camera moves are smooth; the
  drawings change on twos. The final page holds as a poster.
- **Lettering:** Bangers for sound effects and stamps (extruded, outlined, sitting on a
  burst); Comic Neue Bold upper case in balloons; a document's own text in Comic Neue.
- **Balloons:** the tail points at the speaker from the free side. A thought bubble's trail
  never runs over a face (its circles read as spots): use a speech balloon with «…».
- **Marks** (motion lines, impact ticks) trail behind a move or sit at the ends of a label:
  never across what is held and never across printed text.
- **Hands:** cartoon, thumb + three fat round fingers; lines only between pressed fingers and
  at a bend; no nails. Right side and right view as the **hands** skill says.
- **Forbidden:** soft gradients, pure black or white, lines that boil, anything crossing
  text, hands through what they hold.

## Style checklist

- [ ] Does every outline swell or taper, and is every frame's ink identical where the piece didn't move?
- [ ] Is all shading dots or cel, with no gradient?
- [ ] Does each panel read alone and in order, and hold once its beat has passed?
- [ ] Does any mark, tick, trail or balloon cross printed text or a face?
- [ ] Every hand: right side, right view, one skin, in front of or behind what it holds (never through)?
- [ ] Vertical: SFX, balloons and text inside the safe zone (top 150 / bottom 250 px at 1080×1920)?
- [ ] Static panel backgrounds cached as sprites at the camera's largest zoom (< 150 ms/frame warm)?

## Lessons

- 2026-09-26 · first style test · A vertical page of stacked panels is mostly empty until the last panel lands: start the camera inside the first panel (it fills the frame and is the hook) and pull back to the page on the beat.
- 2026-09-26 · first style test · Pupils that look up vanish under a heavy lid: lift the lid a little whenever the eyes go up.
- 2026-09-26 · first style test · An arm raised from the middle of a round body, elbow inside it, reads as a noodle: attach it at the side, drawn behind the body, with the elbow outside.
- 2026-09-26 · first style test · The other arm resting reads as a mug handle unless it is akimbo in two passes: upper arm behind the body, forearm and hand in front.
- 2026-09-26 · first style test · A thumb seen from its owner's eyes reads as a pointing finger until the mound of the hand shows under the held edge, with the lines of the curled fingers.
- 2026-09-26 · first style test · Nails on the backs of cartoon fingers read as spots at this size: leave them out.
- 2026-09-26 · first style test · Impact ticks above and below a label crossed the text next to it: put them at the label's ends.
- 2026-09-26 · first style test · Graded halftone is drawn dot by dot: caching the static panel backgrounds at the camera's largest zoom took a page from 223 to 144 ms/frame.
