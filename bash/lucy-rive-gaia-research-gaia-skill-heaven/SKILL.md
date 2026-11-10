---
name: lucy-rive
description: Build, verify and review Lucy's live Rive character for a Skill Heaven state gate (Heaven, Hell, Zero, Ultra) — gold master to script-free .riv, acceptance viewer, gate evidence, Rive cloud file, owner visual gate. Pointer to the canonical skill in gaia-research/lucy. Triggers on "/lucy-rive", "Lucy rig", "Lucy Alive", "Rive Lucy", "next Lucy gate", "rig Hell/Zero/Ultra".
---

# Lucy · Rive character — pointer

The canonical skill lives with the character source, in
[`gaia-research/lucy`](https://github.com/gaia-research/lucy) at
`.agents/skills/lucy-rive/SKILL.md` (local checkout: `~/lucy`). **Read it in
full before any Lucy rig work** — it carries the gate order, canon per
state, toolchain facts (Rive CLI, Editor MCP limits, cloud file ids), the
pipeline commands, and the lessons that each already cost a build.

If `~/lucy` is missing: `gh repo clone gaia-research/lucy ~/lucy`.

What stays in this repo (the consumer side):

- Product state + timing: `packages/site/src/lucy-scene/scene.ts`
  (`SceneState`, `SCENE_TIMING`), lifecycle `useSceneLifecycle.ts`.
- The character seam and semantic contract:
  `packages/site/src/lucy-scene/LucyLive.tsx` (`LucyCharacter`).
- The finished atmosphere (do not change it to suit the rig):
  `packages/site/src/lucy-scene/atmosphere/`; review switches `?lucy=off`,
  `?atmo=off`.
- Glass wings are a hero effect layer, not character
  (`src/assets/hero-commission/v01/`, `WING_CONFIG*` in
  `variations/hero/useHeroEngine.ts`).
- Raster production rules: `.agents/skills/lucy-image-production/SKILL.md`.

Never advance to the next state before the owner's visual approval of the
current one is recorded (gaia-skill-heaven#153).
