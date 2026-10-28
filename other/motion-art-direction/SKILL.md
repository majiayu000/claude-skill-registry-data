---
name: motion-art-direction
description: "Use when a film needs a look before any scene code — ads, launch teasers, brand films, type-led films with no screenshots, or whenever a draft looks flat (white ground, small tiles, centered text, fades, slow camera drift, logo opener). Locks .motion/look.md at Gate 0 (3 text sketches → challenger locks the tone blind → reference board → look.md + 3 key frames → owner sees them) and owns the scene step's first templates (cut-rhythm, composition-grid, kinetic-type). Richness from area-weighted value contrast, type as a large object, composition, rhythm and motion density — a purposeful gesture at every moment (letter/word kinetics, one recurring geometric actor, animated objects, 3D where it serves), prompt-motion.com as the density reference — never from effects."
versions:
  fuse-motion: "1.0.0"
user-invocable: false
references: references/dials.md, references/gate-zero.md, references/reference-board.md, references/prompt-patterns.md, references/composition.md, references/type-as-image.md, references/objects.md, references/rhythm.md, references/contrast.md, references/bans.md, references/templates/look.md, references/templates/kinetic-type.md, references/templates/composition-grid.md, references/templates/cut-rhythm.md
related-skills: motion-method, motion-craft, motion-render, motion-review, motion-assets, fuse-design:design-method
---

<objective>
Own the ART DIRECTION of a film: the visual system every state is built inside. It is
locked in `.motion/look.md` and its 3 key frames, which the owner sees and approves at
**G0** before any scene code. It also owns the first templates of the scene step.

It exists because the first real ad (fusengine.ch) was rejected as "trop simplet,
horrible": a white ground, small blue tiles, centered text, fades and a slow camera
drift. The fix that followed (depth-by-effect) was rejected as AI slop. The direction is
now fixed: a film reads rich through **value contrast** (two large planes far apart in
lightness, a full-bleed ink or accent field on one state in three), **type as a large
object** (one word ≥ 4× its label, cropped by the frame), **composition** (flush-left,
asymmetric, never centered) and **rhythm** (cuts and gestures on a tempo grid). The owner
approved that still look and asked for more animation, after prompt-motion.com: so
**motion density** — a purposeful gesture in progress at every moment (no span over 0.75 s
without one, the final CTA still ≤ 1.2 s, beats every 0.5–1 s), type moving at letter and
word level, one recurring geometric actor, animated objects, and 3D where the expert judges
it serves. Decorative effects, fades and drift are banned outright.

The method mirrors `fuse-design:design-method` (dials, obligations, screen-holding floor,
Gate 0, absolute bans, slop test, blind sketches), transposed to film. This skill points
to those files instead of copying them.
</objective>

# Motion Art Direction

## Agent Workflow (MANDATORY)

Contract §8 order. It is the only order, in every fuse-motion file:

| Step | Who | What |
|------|-----|------|
| Brief + beat map | `motion-expert` via `motion-method` | `.motion/brief.md` (`genre`, register) + `.motion/beats.md` |
| 1 Sketches | `motion-expert` | 3 text-only tone candidates ([gate-zero.md](references/gate-zero.md)) |
| 2 Tone lock | `fuse-ai-pilot:challenger` | Judges the 3 sketches blind and locks ONE tone |
| 3 Board | `motion-expert` + fuse-browser | 6 refs = 3 traits × 2 for the locked tone → `board.png`, `refs.md` ([reference-board.md](references/reference-board.md)) |
| 4 Look | `motion-expert` | Every field of [templates/look.md](references/templates/look.md) + 3 key frames in words |
| 5 **G0** | owner | Sees the key frames + look.md and approves in their own message |
| 6 Scene | `motion-expert` | cut-rhythm → composition-grid → kinetic-type; `motion-render` gives mechanics only |
| Review | `motion-critic` via `motion-review` | Frames vs look.md; hard-fail IDs live only in `motion-review` references/hard-fails.md |
| Scripts | `fuse-ai-pilot:sniper` | Validation after scene code |

**No `.motion/scene/*` file is written before look.md and the 3 key frames exist and the
owner has seen and approved the key frames.** The harness does not enforce G0 yet: the
`motion` scope gates G1/G2 only, so this rule holds because the agent stops.

---

## Overview

| Area | Core rule | Reference |
|------|-----------|-----------|
| **Dials** | 7 numbers, argued. VALUE_CONTRAST area-weighted ≥ 60 + full bleed on ⌈N/3⌉ states; TYPE_SCALE ≥ 4; largest type ≥ 180 px; HOLD ≥ 0.25 s/word; MOTION_DENSITY ≥ 1 gesture/s, ≤ 0.75 s gesture-free, CTA still ≤ 1.2 s. Equal to the critic floors | [dials.md](references/dials.md) |
| **Gate 0** | §8 order; every look.md field + key frames seen by the owner, or no scene code | [gate-zero.md](references/gate-zero.md) |
| **Board** | After the tone lock: 3 traits × 2, open/mid/end stills, one borrow / one don't | [reference-board.md](references/reference-board.md) |
| **Composition** | 6-col flush-left grid, never centered, key word ≥ 4×, bleed, camera moves on a cut ≤ 2 beats | [composition.md](references/composition.md) |
| **Type** | 2–4 words per beat, letter/word kinetics (stagger, slam, scale jump, split) rotated, frame 0 at full value | [type-as-image.md](references/type-as-image.md) |
| **Objects** | One recurring actor (travels, wipes, splits, floods, becomes the CTA); objects that stand for the product; 3D by judgment, justified | [objects.md](references/objects.md) |
| **Rhythm** | Cuts and gestures on the tempo grid, a beat every 0.5–1 s, ≤ 0.75 s gesture-free, CTA built then still ≤ 1.2 s | [rhythm.md](references/rhythm.md) |
| **Prompt patterns** | 10 prompt-motion.com prompts summarised; 6-block brief, state chains, density | [prompt-patterns.md](references/prompt-patterns.md) |
| **Contrast** | ink / paper / accent in OKLCH, planes ≥ 20 %, no mid-tones, accent as a plane | [contrast.md](references/contrast.md) |
| **Bans** | B1–B23 mapped from the canonical list to grep checks + critic IDs | [bans.md](references/bans.md) |

Units everywhere: px at the 1080 px-wide output frame, OKLCH L 0–100.

---

## Critical Rules

| # | Rule | Check |
|---|------|-------|
| 1 | No file under `.motion/scene/` before look.md + 3 key frames exist and the owner approved them | look.md `approval` filled |
| 2 | Tone = one extreme, locked blind by the challenger over 3 text sketches written before the board | Quote in look.md |
| 3 | Area-weighted VALUE_CONTRAST ≥ 60 on every state; a lone paper plane fails | `auditFrame().valueContrast` |
| 4 | Ink or accent plane ≥ 50 % on ≥ ⌈N/3⌉ states | `validateRhythm`, `auditFrame().fullBleed` |
| 5 | Hero frame: TYPE_SCALE ≥ 4, largest type ≥ 180 px, flush-left, never centered | `auditFrame()` + still |
| 6 | Frame 0 shows the opening statement at full value | `notOnFrame0` guard, still at t = 0 |
| 7 | A gesture in progress at every moment: ≤ 0.75 s gesture-free, final CTA still ≤ 1.2 s, ≥ 1 primary gesture/s; no drift | `validateDensity` (lib.js), `MOVES` guards |
| 8 | No crossfade, no dissolve, no opacity-only reveal; behaviours rotated, never twice in a row; one primary gesture at a time | Bans sweep, `validateDensity` |
| 9 | Cuts and gestures on the tempo grid ±1 frame; ≥ 0.25 s/word on screen; CTA built over ≥ 2 gestures | `validateRhythm` |
| 10 | Brand never before the pain | `validateRhythm` |
| 11 | Every ban B1–B23, no exception, no look.md override | Bans sweep |
| 12 | Everything a pure function of `t` (`motion-render` seek contract) | Stills twice → same sha256 |
| 13 | Borrow grammar only — never logos, footage, music, copy, exact layouts | refs.md |
| 14 | One recurring actor; every 3D beat has a job and a style reason in look.md and the beat table | look.md `actor`, `objects`; `validateRhythm` (`d3`) |

---

## Architecture

```
brief.md + beats.md (motion-method)
└── G0  3 text sketches → challenger (blind) locks the tone
        → reference-board.md → refs/NN-{open,mid,end}.png → board.png + refs.md
        → look.md (templates/look.md) + 3 key frames ← dials, contrast, composition,
          type-as-image, rhythm, bans                 → owner sees key frames, approves
scene/ — classic scripts after motion-render's lib.js, each within the hook ceiling `FUSE_SOLID_MAX_LINES`
  1 cut-rhythm.md       rhythm.js: STATES (+ gestures) → CUTS → BEATS/DURATION/GESTURES/STILLS, validateRhythm + validateDensity, ground, showState
  2 composition-grid.md grid.js: grid, .plane, #world + camera(t) + MOVES guards, auditFrame()
  3 kinetic-type.md     kinetic.js: letterStagger · slam · scaleJump · splitWord · maskReveal · pushReplace · swap · accentSwitch · safeBezier
  (objects.md           the actor and objects; motion-render timeline-seek / webgl-scene for CSS 3D and lit three.js)
→ stills G1 → draft + critic G2 → master
```

---

## Reference Guide

### Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Dials** | [dials.md](references/dials.md) | Writing the dials block; a still reads grey, uniform, empty or flat |
| **Gate 0** | [gate-zero.md](references/gate-zero.md) | After the beat map; any look.md field missing |
| **Reference board** | [reference-board.md](references/reference-board.md) | After the challenger lock |
| **Composition** | [composition.md](references/composition.md) | Grid, key frames, camera |
| **Type as image** | [type-as-image.md](references/type-as-image.md) | Copy per state, kinetic set, easing |
| **Objects** | [objects.md](references/objects.md) | The actor, the object vocabulary, transforms, 3D by judgment |
| **Rhythm** | [rhythm.md](references/rhythm.md) | Tempo, density, cut table, CTA build and still |
| **Prompt patterns** | [prompt-patterns.md](references/prompt-patterns.md) | Writing the brief; planning the state chain; "it lacks animation" |
| **Contrast** | [contrast.md](references/contrast.md) | Colour roles, planes, full bleed, inversion |
| **Bans** | [bans.md](references/bans.md) | Before look.md, before stills, any "add an effect" or "add a fade" reflex |

### Templates (scene step order)

| Template | When to Use |
|----------|-------------|
| [look.md](references/templates/look.md) | Writing `.motion/look.md` for G0 |
| [cut-rhythm.md](references/templates/cut-rhythm.md) | 1st scene block (`rhythm.js`): tempo map → states + gestures, rhythm + density validators, grounds, hard cuts |
| [composition-grid.md](references/templates/composition-grid.md) | 2nd (`grid.js`): 6-col grid, planes, camera without drift, per-frame audit |
| [kinetic-type.md](references/templates/kinetic-type.md) | 3rd (`kinetic.js`): letter stagger, slam, scale jump, split, mask, push/replace, swap, accent switch |

---

## Best Practices

### DO
- Derive look.md from the locked tone field by field; argue every dial in one line.
- Describe the 3 key frames with grid positions, px sizes and planes before any code.
- Run `auditFrame()` and the bans sweep on every still.

### DON'T
- Fix a flat draft with an effect, a fade or a drift — fix value, scale, crop or rhythm.
- Fix an under-animated draft with ambient loops — add purposeful gestures (letters, the actor, objects, details).
- Add 3D without a job or without its reason in look.md.
- Spend the accent on small objects; a plane < 20 % does not count.
- Let the tempo slip "because it looked right" — snap to the grid.

---

## Forbidden

- Scene code before the owner has seen and approved the key frames (G0).
- Any item of [bans.md](references/bans.md), whatever look.md says.
- Logo or brand before the pain; a centered, uniform-size, faded-in sentence as a state.
- Unseeded randomness, wall-clock time, rAF loops, CSS animations/transitions in a scene.
- Third-party logos, footage, music or exact layouts in the film; `board.png` shipped publicly.
- Describing a reference from memory — open it or drop it.
