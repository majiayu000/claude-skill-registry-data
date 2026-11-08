---
name: mascot
description: "Create an original animated pixel-art mascot (any animal) inside a React Native/Expo app: a zero-dependency pixel-map engine generates sprite-frame PNGs, a PixelPet component animates idle/walk/celebrate/poke states, and every state is screenshot-verified in the iOS simulator. Use when the user runs /mascot [animal], or asks for a mascot, pixel pet, pixel-art character, sprite, avatar, idle animation, waddle, or cute app character."
---

# Mascot

Create ONE original animated pixel-art mascot in the current app. The art is
code: pixel maps rendered to PNG by a zero-dependency engine (no image-gen AI,
no npm installs). Poses change by frame swap; bob/tilt/squash run as native
transforms in a `PixelPet` component. Every generation is deterministic —
regenerating a pack reproduces its PNGs byte-for-byte.

## Pipeline

1. **Interview** — animal from `$ARGUMENTS`, else ask (suggest: cat, bunny,
   panda, frog, fox — any animal works). Then ask the mascot's name. Then one
   prompt: "Defaults: palette from `assets/palettes.json` (cozy/DB16), one
   small accessory, full 7-frame state set. Any overrides?" Apply overrides;
   otherwise proceed. Only ask what is missing.
2. **Vendor** — copy `scripts/engine.mjs`, `scripts/validate-frames.mjs`,
   `assets/palettes.json` into `<app>/scripts/mascots/`, and
   `../../react-native/PixelPet.tsx` into `<app>/components/`. The build
   scripts and generated PNGs live in the app repo, diffable and regenerable
   without this skill. Details: `references/pipeline.md`.
3. **Design the pack** — write `scripts/mascots/packs/<animal>.mjs` following
   `references/animal-recipes.md` (construction) and `references/craft.md`
   (palette, outline, timing). Study `scripts/packs/duck.mjs` first — it is
   the reference implementation.
4. **GATE 1 · art** — generate (`node scripts/mascots/engine.mjs
   scripts/mascots/packs/<animal>.mjs --out <app>/assets/mascots/<animal>`).
   Self-critique the contact sheet against the checklist in
   `references/qa.md` and run at least 2 polish passes BEFORE showing the
   user. Then show the sheet path and wait for the user's "cute enough".
   Do not write component code before this verdict.
5. **GATE 2 · motion** — `node scripts/mascots/validate-frames.mjs` must PASS.
   Then build an inline HTML preview of the animation (port the frames to a
   canvas; timings from `references/craft.md`) and get the user's timing
   approval before touching the simulator.
6. **GATE 3 · device** — typecheck, run the app, drive every state, and save
   per-state screenshots to `<app>/docs/mascots/<animal>/qa/`. Protocol:
   `references/qa.md`.
7. **Report** — evidence links (contact sheet, QA screenshots), the regen
   command, and which files were added/changed.

## Reference routing

| When | Read |
|---|---|
| First run in an app, pack anatomy, engine/validator CLI | `references/pipeline.md` |
| Drawing the animal (ears, tails, silhouettes) | `references/animal-recipes.md` |
| Palettes, outlines, shading, animation timing | `references/craft.md` |
| Reviewing art, polish passes, simulator QA, evidence | `references/qa.md` |
| Wiring PixelPet, progress mapping, character switcher | `references/app-integration.md` |

## NEVER

- NEVER ship art without the user's explicit "cute enough" — polish passes
  before that verdict are yours to run unattended; the verdict is not.
- NEVER add a dependency — the engine uses only `node:` builtins; PixelPet
  only `react-native`. If something seems to need a library, redesign.
- NEVER hand-edit generated PNGs — change the pack, regenerate, revalidate.
- NEVER put pixel art in the component — components animate frames; all art
  lives in packs.
- NEVER claim QA done without per-state screenshots saved on disk.
