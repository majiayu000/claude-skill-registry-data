---
name: game-feature
description: End-to-end recipe for adding or changing a CampusCove gameplay feature (housing, doors, keys, tools, work buildings, fishing, open-world phases, interactions, hotbar items). Use at the start of any /game feature that may span Blender assets, the Three.js front, the Colyseus socket and the Laravel API, to decide which layers to touch, in which order, and how to ship it.
---

# CampusCove gameplay feature

CampusCove is a browser 3D social RP game (Garry's Mod / DarkRP feel, low-poly pastel art). One feature usually
cuts through four layers. Decide up front which ones are involved, then work **bottom-up** so each layer has
something real to consume.

```
Blender script (map-src/CampusCove/*.py)        -> skill: blender-asset
  -> out/  -> make assets-optimize -> front/public/assets/** (+ world.manifest.json, catalog.ts)
Laravel API (backend/)                          -> skill: backend-game-data
  authoritative for money, items, ownership, keys, door lock state
Colyseus socket (socket/src/)                   -> skill: socket-message
  authoritative for positions, reach, who sees whom, live door state; calls the API with the player's token
Front (front/src/)
  game/**           pure Three.js, no Vue (scene, town/, collision/, placement/, world/)
  composables/game/ Vue glue per concern (useCityHousing, useHouseKeys, useInteractionTargets, ...)
  views/GameView.vue only assembles composables + key handling; keep it thin
Verify                                          -> skill: playtest-game
```

## 1. Frame the feature (before code)

- Read `docs/OPEN_WORLD.md` if the feature touches buildings, doors, zones, collision or movement: it is the
  phased design doc (phases 0–5b done). Continue its numbering ("phase 6a") when the work belongs to it.
- Check the product rules that look like bugs but are not (memory: economy decisions):
  premium skins never cost coins; houses are **bought** + daily property tax (no more renting); unpaid tax seizes the
  house; furniture deleted on seizure/expiry is intentional; no IP storage. Coins come from gameplay actions
  (reuse `CoinRewardService`), not passive income.
- Write down the player loop in one sentence ("with the key in hand, left click locks"). If two readings are
  possible, ask the user — they make the design calls.

## 2. Where things go

| Need | Place |
|---|---|
| New 3D model / building / tool / skin part | `map-src/CampusCove/build_<thing>.py` (blender-asset) |
| Asset URL | `front/src/game/assets/catalog.ts` (one typed entry, keys = seeder codes) |
| Placement in the world (position, door, bounds, interiorOffset) | `front/public/assets/world.manifest.json`, written by `front/scripts/apply-*.mjs` or the district build, read by `game/world/worldManifest.ts` **and** `socket/src/world.ts` |
| Something the player can aim at / walk up to | `composables/game/useInteractionTargets.ts` (priority order is documented in its header) + prompt label |
| Key | `front/src/config/keybindings.ts` (`KEY_BINDINGS`), handled in `GameView.vue` `onKeyDown` or the owning composable's `onKeyDown` |
| Held item / tool in hand | `game/heldItem.ts` + `game/firstPersonArms.ts` (arms clips: Idle, Walk, Equip, UseDoor, UseKey) |
| Live shared state (doors, positions, furniture sync) | socket room + `useGameRealtime.ts` handler + type in `types/gameRealtime.ts` |
| Persistent state (owner, keys, money, items) | Laravel service + migration + feature test |
| Constants shared with the socket | `front/src/game/gameRoomConstants.ts` — must stay in sync with `socket/src/` |

Never let the client decide something the server can check: the socket re-checks reach, speed, locks
(`socket/src/movement.ts`, `doors.ts`) and the API re-checks ownership and money.

## 3. Build order

1. Assets (if any) → optimize → commit the GLB/JSON outputs with the script.
2. Backend: migration / service / route / test, `make test`.
3. Socket: message handler + validation. `socket/` is volume-mounted with `node --watch`, so edits apply live;
   `make rebuild-socket` only after `package.json` changes.
4. Front: `game/` logic first (testable, no Vue), then the composable, then the minimal `GameView.vue` wiring.
5. Playtest (skill `playtest-game`), two tabs when anything is shared.

## 4. Gates before saying "done"

```bash
cd front && npx vue-tsc -b
cd front && node --experimental-strip-types --test "src/**/*.test.ts"
cd front && npx knip
make test
```

The host has Node 22.13, which cannot run `.ts` tests without `--experimental-strip-types`, so plain
`npm run test:unit` fails with `ERR_UNKNOWN_FILE_EXTENSION` there (fine on Node ≥ 22.18). If knip only reports
`Unlisted binaries: knip`, the local `front/node_modules` is stale: `cd front && npm install`, not a code issue.
`vue-tsc -b` is what `npm run build` runs and is stricter than `make typecheck` (`--noEmit`); a past fix
(`33166c3`) was only needed for `-b`. Add a `*.test.ts` next to pure logic in `game/` or `avatar/`
(`node:test` + `node:assert/strict`, see `src/avatar/avatarAnimationLogic.test.ts`). Report any gate you could
not run.

## 5. Reference skills (vendored, advisory)

General know-how from three open-source skill packs, each with a CampusCove note at the top (r170 gaps, which
project file owns the concern). Load the matching one when the task needs depth; this skill and the other
CampusCove skills win on any conflict. Sources and licenses: `.claude/skills/_third-party/README.md`.

| Need | Skill |
|---|---|
| Slow frames, draw calls, VRAM, shader stalls | `threejs-performance` |
| Something broken or blank, before guessing a fix | `threejs-debug-profiler` (then `playtest-game` to reproduce) |
| GLTF/Draco/texture loading, cloning, disposal | `threejs-loaders` |
| Inspecting or tuning compression (via `optimize-assets.mjs` only) | `threejs-asset-pipeline` |
| Lights, shadows, environment, lightmaps | `threejs-lighting` |
| Color spaces, UV channels, texture memory | `threejs-textures` |
| Mixer, clips, crossfades, bones (avatars, first-person arms) | `threejs-animation` |
| Feedback on doors, keys, purchases, catches, hotbar | `game-feel` |
| First-person camera behaviour | `camera-systems` |
| New actions / keys, accessibility of controls | `input-systems` |
| Laying out a new zone or building, landmarks, flow | `level-design` |
| Vue SFCs, composables, reactivity (keep 3D objects out of it) | `vue` |
| `vite.config.ts`, env vars, asset imports, build (Vite 7 here) | `vite` |
| Room lifecycle, reconnection after a drop, anti-cheat principles | `colyseus-multiplayer` (with `socket-message`) |
| Aiming / raycast picking, hover, placement drag | `threejs-interaction` |
| Weighted drops, rarity rolls, pity timers, seeded randomness | `procedural-gen` (rolls run server-side) |

## 6. Ship

- One commit per playable slice; assets and code for the same slice can be split as `phase Na (assets)` /
  `phase Nb` like `847dd37` / `9e0922e`.
- Message style (match `git log`): `feat(<area>): <what the player gets>` — areas in use: `open-world`, `housing`,
  `game`, `inventory`. Body = short `- ` bullets in player terms first, then tech notes (socket message names,
  files, make targets). Lowercase, no trailing period in the subject.
- Update `README.md` tables / `docs/*.md` when a make target, asset folder or contract changes. Docs are in French;
  code, comments and commits are in English.
