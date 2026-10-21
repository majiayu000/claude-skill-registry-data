---
name: style-70s-poster
description: Psychedelic 70s poster style (Fillmore, Yellow Submarine) drawn with code. Flat acid colors, thick outlines, concentric echoes, sunbursts, wavy shapes and melting letters. Use it for psychedelic, retro, groovy or concert videos, or when working with styles/70s-poster/.
---

# Style · 70s poster

Approved. Reference: `sandbox/2026-09-24-exquisite-corpse/` (mushroom segment, 6.5–10.5 s).

## Code

`styles/70s-poster/kit.js` → `Groovy`: `PAL` (palettes `acid`, `sunset`, `submarine`),
`sunburst` (full-bleed rays), `rings` (wavy rings), `wavy(pts, amp, freq, phase)`
(the outline breathes), `shape(g, pts, fill, { ink, width, echoes, echoStep })` (flat
shape with an ink outline and **echoes**), `ellipse`, `line`, `melt` (text that drips and
melts into drops) and `path`. Typeface: Shrikhand (`fonts/Shrikhand-latin.woff2`, OFL).

## Style rules

- **Flat and acid:** no gradients or shadows. Every color next to its complement
  (orange/magenta/acid green/violet/yellow). Very dark violet ink, never black.
- **Thick outline on everything that is a figure**, and echoes in 1–2 colors on the
  protagonist.
- **Everything waves, nothing jitters:** deformations are smooth sines of `t` (`wavy`),
  not noise.
- **Motion on the beat:** side-to-side sway per bar, squash on every beat
  (`Motion.pulse`).
- **Letters:** Shrikhand, with outline and echo. When they melt, round drops fall (a few
  bells), not a noise of spikes.
- **Background always moving** (spinning rays, waving rings), but less saturated than
  the figure.

## Style checklist

- [ ] Any gradient, soft shadow or pure black?
- [ ] Do the figures have an ink outline and the protagonist echoes?
- [ ] Does the melt read as drops of paint?
- [ ] Does the figure stand out from the background (size, contrast, echoes)?

## Lessons

- 2026-09-24 · exquisite-corpse · A random column-by-column drip profile reads as spikes: drops = a few bells over a smooth fall (now in `melt`).
- 2026-09-24 · exquisite-corpse · A chorus of small figures on the offbeat (`Motion.pulse(t, bpm, 0.25)`) and ornaments spinning in the corners add density without stealing the lead.
