---
vendored_from: https://github.com/appautomaton/delineate
name: svg-glyph-rain
description: >
  Make or change Rain (rain/): a figure under an umbrella, cut dark out of a flat sky, dots of light flowing
  over their form, in a rain of written characters that trail rings, break on the canopy, run off its rim
  and lie down where they land. Use for a new person or pose, a palette, a set of characters, an umbrella
  that sits wrong, dots that jitter instead of flow, rain too thin or too thick, or a stage that runs slow,
  even if the user never says "skill".
triggers:
  - svg-glyph-rain
  - svg
  - glyph
  - rain

---

# Glyph rain

A person in the rain, and the rain is writing. `rain/notes.md` maps the modules and holds the rules a change
must keep; read it first.

## The bar

- **The figure is a silhouette worth looking at, elegant before it is strong.** Built as a figure is drawn:
  bone, joint to joint, and a width on either side along it (`body.ts`). Seen from behind, looking into
  the rain, the umbrella held out before them. Both wear trench coats, collar up, storm flap, belt and vent:
  a woman drawn long, a man broad in the shoulder and narrow at the belt. Muscle alone reads as a
  mannequin; the coat's line carries the grace. If a part reads as a tube, a block or a joint, its widths
  are wrong.
- **They stand alive.** Breath in the shoulders, weight passing from leg to leg, the hem in the wind, the
  head turning a little (`pose`): slow swells that never fall in step, the feet never moving.
- **No lines.** The figure and the umbrella are shape alone: no outline, no seam, no rib. The coat's parts
  (storm flap, belt, collar) show only as the dots on them turn their run.
- **One becomes the other.** Each stands five seconds and becomes the other over a moment and a half, every
  part eased point by point into the same part of the other, so both are drawn as the same parts, in the
  same order. A new person keeps to that list.
- **A small head.** Seen from behind, a head is little longer than wide; a long head reads as a mannequin.
- **Dots flow, they never jitter.** Every dot runs with the form: around the bone of a limb or torso, along
  it for falling cloth, in rings about the canopy's crown. Over half a second each leaves a short streak
  that says which way the surface turns.
- **The rain is characters, and each one trails rings** that shrink behind it. It strikes the canopy and
  runs off the rim, lies flat where it lands, and leaves rings spreading on the ground.
- **Quiet colour, four tokens, two modes.** Sky, figure, stipple, ink (`palette.ts`), each palette a greyed
  hue given for dark and for light. Dark: a dusk-grey sky, the figure near black, the ink pale. Light: a
  paper sky, the figure a grey wash, the ink dark. The figure stands off the sky by 2.4:1 or more, the ink
  off the sky by 6.5:1 and off the figure by 4:1. Palettes turn by themselves, once a cycle; colours always
  ease in OKLab. No gradients, no shadows; the only glow is the ink's own.
- **A film's clock.** 24 steps a second, drawn only when a step is taken, asleep out of view.

## The task

- **A person**: an entry in `BODIES` (`body.ts`): a `build(pose)` that gives the parts back to front, each
  `part(bone, widths, run)` with its joints passed through `pose.at`, a grip for the hidden hand on the
  shaft, and a reach that sets the canopy's rim just above the head.
- **A palette**: an entry in `PALETTES` with both modes, keeping the contrasts above; measure them before
  looking.
- **Characters**: a set in `glyphs.ts`, or any text through `?glyphs=`. The font stack must hold them.
- **The rain's feel**: the constants at the top of `rain.ts` (depths, sizes, lifetimes) and `rate`.

## Done means

`npm run check` passes, and on `npm run rain` (http://localhost:5360/): `?rate=0&figure=` shows each person
alone and they read as beautiful at a glance; with rain, the canopy gathers it and sheds it off its low rim,
and the ground holds fallen characters and rings. Measure in the browser: 24 frames drawn a second and the
work of each under 5 ms at the 95th percentile. Then tell the user what to look at.
