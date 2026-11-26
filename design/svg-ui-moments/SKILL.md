---
vendored_from: https://github.com/appautomaton/delineate
name: svg-ui-moments
description: >
  Make or change Moments (moments/): a monochrome specimen sheet of twenty tactile UI micro-interactions
  driven by real, interruptible nonlinear physics across five materials (rubber, viscous, mechanical, taut,
  fluid), each playable by click, drag, scrub, or hover, with a calm loop mode, optional procedural sound,
  and day and night paper. Use for adding a new micro-interaction tile, tuning spring feel or nonlinear
  curves, fixing gooey SVG cohesion, waterline ink inversion, squash-and-stretch volume conservation,
  pointer interruption, procedural Web Audio feedback, light/dark contrast, or stage idle-sleep and frame
  pacing, even if the user never says "skill".
triggers:
  - svg-ui-moments
  - svg
  - ui
  - moments

---

# UI moments

Twenty monochrome UI controls that move by **nonlinear physical law** rather than flat CSS `ease-in-out`.
Read `moments/notes.md` first for the module map and the invariants every tile must keep.

## The bar

- **Monochrome exposes timing.** No brand hues, no rainbow gradients, no glow crutches. Value contrast
  (ground, recessed well, mid ink, crisp active solid, overhead rim light, soft contact shadow) carries
  the entire form, so flat easing, clipped strokes, or hesitant transitions have nowhere to hide.
- **Nonlinear motion is the whole craft (anti-slop laws).** A bare high-damping spring from rest (`ζ ≥ 0.7`)
  still reads as a polite linear `ease-out`. Every tile in Moments earns its liveliness through at least
  one of five explicit nonlinear techniques:
  1. **Anticipation & delayed tail**: wind up before launching (*Jelly Pad* pre-hop crouch, *Squash Play*
     pillow compression mid-morph) or delay the trailing edge 65–85 ms behind the leading edge (*Stretch
     Toggle*, *Gooey Tab Bar*, *Worm Dots*) so the silhouette elongates dramatically before snapping shut.
  2. **True 2nd-order inertia, never 1st-order lerp**: even multi-element fields (*Magnet Grid*'s 42 dots)
     run on individual `Spring` oscillators so elements whip inward and overshoot elastically rather than
     creeping asymptotically via `x += (target - x) * k`.
  3. **Nonlinear acceleration & threshold snap**: gravity torque `∝ sin(θ)` on *Domino Row*, exponential
     launch `u^2.15` on *Paper Plane*, quintic push `easeInOutQuint` on *Swipe Confirm* and *Download Ring*,
     and sticky tension → sudden pinch-off recoil on *Merge Drops* (never constant-speed linear orbits!).
  4. **Exact volume conservation outside rotation**: squash/stretch computes `squash(s) = (exp(s), exp(-s))`
     with world-aligned floor squash outside body rotation (*Jelly Pad*, *Squash Play*).
  5. **Geometry-exact polarity inversion**: SVG `<mask>` over the filtered metaball in *Gooey Tab Bar*,
     live sine `<clipPath>` in *Tide Progress*, wide mid-grey crossover in *Stretch Toggle*, and live
     `getComputedTextLength()` strikethrough in *Checklist*.
- **Five distinct physical materials (`MATERIALS` in `physics.ts`)**:
  - `mechanical` (`ω 38, ζ 0.62`; detents/rocker/reels tuned `ζ 0.50–0.52` for crisp over-center snap):
    *Detent Dial*, *Domino Row*, *Rocker Switch*, *Odometer*.
  - `rubber` (`ω 18, ζ 0.30`; deep pillow squash & silicone rebound `ζ 0.20–0.46`):
    *Stretch Toggle*, *Jelly Pad*, *Swipe Confirm*, *Squash Play*, *Worm Dots*.
  - `taut` (`ω 34, ζ 0.085`; expressive harmonic whips & bouncy staged morphs):
    *Paper Plane*, *Elastic String*, *Download Ring*, *Bell Toggle*, *Menu Morph*, *Checklist*.
  - `viscous` (`ω 13, ζ 0.48`; sticky tension, concave metaball necks, mutual recoil):
    *Gooey Tab Bar*, *Merge Drops*.
  - `fluid` (`ω 11, ζ 0.32`; sloshing waves, spring dot lattices, quartic ripples):
    *Tide Progress*, *Magnet Grid*, *Ripple Pad*.
- **Real interaction, not a canned video.** Every tile feeds pointer press, drag, scrub, velocity-on-release,
  or hover directly into the same physics state that Loop mode drives via `demo(cycleTime, dt)`. Calling
  `ctx.interact()` grants a quiet user-ownership hold without breaking per-tile Loop clocks on resume;
  interrupting any control mid-flight preserves velocity and never snaps or teleports.
- **Quiet when still, crisp at any refresh rate.** Analytical spring stepping behaves identically at
  60 Hz, 120 Hz, and 144 Hz. Every `.moment-card` isolates paint with `contain: layout style paint` and is
  culled individually by `IntersectionObserver` so off-screen tiles never tick. Settled tiles sleep between
  beats even in Loop mode (so every `demo()` must call `ctx.wake()` whenever it starts a beat or drives
  continuous motion), and `schedule()` guards re-entrant `ctx.wake()` inside `frame()` so a single shared
  RAF never multiplies. Never read layout (`getComputedTextLength`, `getBoundingClientRect`) inside
  `step()`/`render()`, skip redundant attribute writes, bypass SVG blur filters when a gooey blob sits
  still, and sleep the RAF loop completely when settled in Play mode.
- **Tactile Web Audio that actually fires on first touch.** `SoundEngine` (`sound.ts`) layers short
  bandpass noise bursts over resonant body oscillators through a master `DynamicsCompressorNode`, awaits
  async `ctx.resume()` rather than dropping the first click, announces itself with a subtle chime when
  toggled on, and stays silent during Loop auto-playback until the reader touches a tile.
- **Both lights earn their frame.** Night is matte obsidian with porcelain solids; Day is delineate's warm
  bone paper with charcoal ink — value hierarchy re-balanced per surface (`--m-dial-hi/lo`, `--m-rocker-*`),
  never a CSS `invert()` shortcut.

## Adding a new tile (agentic DX recipe)

1. Pick the matching material family file (`tiles/rubber.ts`, `tiles/viscous.ts`, `tiles/mechanical.ts`,
   `tiles/taut.ts`, `tiles/fluid.ts`) and export a `TileSpec` (`slug`, `name`, `material`, `hint`, `mount`).
2. Draw inside the shared `200 × 140` viewBox returned by `createStageSvg()` using only semantic CSS tokens
   (`--m-ink`, `--m-paper`, `--m-well`, `--m-well-deep`, `--m-mid`, `--m-soft`, `--m-border`,
   `--m-border-strong`, `--m-card`, `--m-lip`, `--m-ink-dim`, `--m-shadow`, `--m-sheen`, `--m-dial-hi/lo`,
   `--m-rocker-*`).
3. Share one physics state between user events (`stagePoint`, `VelocityTracker`, `ctx.interact()`, `ctx.sound()`)
   and Loop choreography (`demo(cycleTime, dt)`). Always call `ctx.wake()` inside `demo()` when triggering
   a beat or driving continuous motion so per-tile idle-sleep wakes immediately. Gate any delayed sound
   inside `step()`/`render()` on a `userActive` flag so Loop mode stays silent when Sound is enabled.
4. For viscous tiles, create a unique filter id via `uniqueId(...)` with `createGooFilter` (`-30%` / `160%`
   bounds) and use a synchronized SVG `<mask>` (not `<clipPath>`) whenever foreground strokes invert across
   the metaball.
5. Register the tile in `tiles/index.ts` (alternating adjacent silhouettes) and inspect it magnified at
   `?tile=<slug>` in both `?light=night` and `?light=day`.

## Done means

`npm run check` passes and `npm run moments` (http://localhost:5380/) looks museum-grade in a real browser:
- Inspect full sheet in both **Night** and **Day** at desktop (`5 × 4`) and narrow (`2 × 10`) viewports:
  even visual weight, zero clipped SVG strokes or filter edges, crisp contrast on every label and hardware
  surface, and zero console errors.
- Inspect mid-motion filmstrips of the signature morphs (*Stretch Toggle* wide mid-pill elongation, *Gooey
  Tab Bar* continuous metaball bridge + masked icon inversion, *Merge Drops* sticky tension → snap recoil,
  *Paper Plane* rocket launch with trailing wake, *Download Ring* elastic pill-to-ring-to-check-pill,
  *Squash Play* deep pillow-squash + mid-press polygon morph, *Tide Progress* split-polarity waterline +
  calm Play meniscus, *Elastic String* full-height S-wave whip) and verify every beat reads nonlinearly.
- Verify direct interaction (click, drag, early-release recoil on *Swipe Confirm*, circular drag on *Detent
  Dial*, bidirectional swipe on *Domino Row*, pointer sweep across *Elastic String* and *Magnet Grid*,
  crisp audible feedback on first gesture when Sound is toggled on) and confirm the RAF loop sleeps cleanly
  (`0` idle DOM mutations) in Play mode even after tapping or triggering *Magnet Grid*.
