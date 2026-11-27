---
name: game-3d
description: "Build a 3D game with three.js (Electron for Steam): engine, layout, asset and VRM pipeline, test recipe, Steam checklist. Use for any 3D game or walkable world."
---

# 3D game

Decided 2026-10-07 (plan: `/mnt/project-files/game-dev/PLAN.md` in the Claude Setup project).
The HQ office is the test run; the first real game turns yskills' vacation photos and stories
into a cozy walk-around game that can go to Steam.

**Starter kit, read once at project start:** [`starter/README.md`](starter/README.md): chibi
roadmap, figure pipeline, standard models with licences, and the learnings from Company XY's figures.

## 1. Engine: three.js, Electron for Steam

Threads run in cloud Linux containers with Chromium and no screen, so the engine must run and
be looked at headless. three.js does; Unity, Unreal and Godot need an editor or a GPU on
yskills' PC for every visual check, so they are out (Godot stays the fallback if a game ever
needs consoles). Electron ships the same Chromium we test in; `steamworks.js` gives achievements,
cloud saves and the overlay. Vampire Survivors, CrossCode and GoreScript shipped this way.
Trade-offs to say in PLAN.md: about 250 MB download, no consoles, no photo-real graphics.

Tauri instead of Electron (game-dev plan, 2026-10-07): a smaller download, but Steam features must be written in Rust by hand. Godot mobile notes (low-poly-and-sources, 2026-10-24): use the Mobile renderer, not Forward+; MultiMesh draws thousands in one call but always renders all and needs an AABB; keep transparent objects few and join meshes ahead of time.

Stack (versions checked on npm 2026-10-07; take the current ones): `three` 0.186,
`@pixiv/three-vrm` 3.5, `three-mesh-bvh` 0.9 (collision against the level), `@dimforge/rapier3d-compat`
0.21 only when a game needs real physics, `@sparkjsdev/spark` 2.3 (Gaussian splats), Vite +
TypeScript, Vitest, Playwright, `electron` 44 + `electron-builder` + `steamworks.js` 0.4,
`@gltf-transform/cli` to shrink models. All MIT or Apache. Start on WebGL; switch a game to the
WebGPU renderer only when its scenes need it (Electron and every browser run WebGL).

## 1b. From a wish to a build brief (reference first)

The look: captures of the top portal games in `design/reference/` before the first build, rule in `operator/roles/designer.md` (`claude-setup/.claude/skills/operator/roles/designer.md`) (Art direction first: palette, type and pillars decided before the first build, nothing from `ui-review/SLOP.md`).

How the game plays comes first: the Game Designer writes `design/GDD.md` (core loop, run length, difficulty table, feedback, ad hooks, three researched references) from `operator/templates/game-design.md` (`claude-setup/.claude/skills/operator/templates/game-design.md`) before the first build; `node <game-3d skill folder>/scripts/gdd-check.mjs design/GDD.md` (run in the game repo) must pass (rule: `operator/roles/game-designer.md` (`claude-setup/.claude/skills/operator/roles/game-designer.md`)).

How it sounds is next: the Audio role writes `design/AUDIO.md` from `operator/templates/audio.md` (`claude-setup/.claude/skills/operator/templates/audio.md`) before the build touches sound; `node <game-3d skill folder>/scripts/audio-check.mjs` (run in the game repo) must pass, with every file under `assets/audio/` in `assets/manifest.json` (rule: `operator/roles/audio.md` (`claude-setup/.claude/skills/operator/roles/audio.md`)).

yskills says what they want in one sentence, pictures or a story; the team turns it into a
concrete brief before any build. Order, every time:

1. **Find the bar.** WebSearch the most popular games or features of that kind (Steam top
   sellers and reviews, itch.io, YouTube devlogs): what players praise, what they complain about.
   Pick the three to five patterns that make the best ones good (camera, controls, pacing, art
   direction, onboarding), with a link each, in `design/REFERENCES.md`.
2. **Write the brief** into `PLAN.md`: the wish in yskills' words, the references and the
   patterns taken from them, the places and characters, the story beats as quests, the look
   (`design/DESIGN.md`, cozy pastel unless the wish says otherwise), the slices with acceptance
   criteria in `features.json`, the Steam decision (yes or later), and prices for anything that
   costs money. Open questions get one recommended pick and a card.
Literal mode and the cost rules: the last block of `operator/briefs.md`.

3. **Build to that bar**: the gate's `design-critic` gets the references next to the
   screenshots (a reference *picture* is the pick from a Designer vote card, saved under
   `design/reference/`; the links in `REFERENCES.md` alone give the critic nothing to compare); a slice that falls short of them is not 5/5.

Pictures and stories are inputs, never the art: photos become references and splat postcards
(§3), stories become `story/` files.

- 2026-10-17 (research/game-route): the first game is a small casual one-mechanic 3D low-poly game shipped in days, which proves the route; the big cozy vacation game stays the Steam candidate.

## 2. Folder layout

**New game: `projects/<name>.json` with `"kind": "game"`, then the `new-project` workflow** (`publish`
skill; the starter is `publish/templates/new-game/`, not `game-3d/starter/`, the figure kit): a static Vite + three.js repo (a 30-second coin dash to replace, rules in `src/rules.ts` with
Vitest, `window.__gameReady` for `templates/shots.mjs`), live at `https://<name>.yverse.workers.dev`,
no D1, no login. Its layout below is what you grow it into. Without the workflow, one repo per game,
scaffolded with the `scaffold` skill (Vue is optional: a game is a Vite app
whose `index.html` holds one canvas; i18n, legal pages, CI and the Worker Preview stay).

```
assets/manifest.json     every file: name, path, source, licence, author, usedFor (templates/manifest.json)
assets/characters/<n>/   model.vrm + licence.json copied from the VRM meta
assets/moves/            *.vrma shared by all characters (or Mixamo .fbx, retargeted at load)
assets/kits/<kit>/       CC0 kit models as .glb, one folder per kit
assets/splats/<place>/   .spz or .ply made from photos
assets/audio/
story/                   <place>.de.md, <place>.en.md, quests.json, i18n lines
src/platform/            platform.ts (interface), web.ts, crazygames.ts, steam.ts (steamworks.js); the web starter keeps all portals in one src/platform.ts
src/scenes/<place>/      layout, lights, spawn and camera spots
src/entities/            player, npc, prop
src/systems/             walk, camera, dialogue, quests, save
src/ui/                  panels: one open at a time, Esc or a tap outside closes
tests/unit/ tests/shots/ tests/perf/
electron/                main.mjs, preload.mjs (templates/electron-main.mjs), electron-builder.yml
steam/                   app_build.vdf, depot vdfs, store texts de/en, capsule images
```

`vite.config.ts` builds with `base: './'` (relative paths) so one build runs on the Worker, in
CrazyGames' iframe and in Electron (`file://`). Game rules (quests, saving, scoring) live in plain TypeScript with no renderer import, so Vitest
covers them. Stories are data: threads turn yskills' messages into `story/` files, never code.

## 3. Assets and characters

- **A world that reacts** (NPC reaction ladder, scenario points, sound from sources, secondary motion, cheap wet streets, what to skip on the web): [`refs/living-world.md`](refs/living-world.md); crowd tiers in [`refs/crowds-and-lod.md`](refs/crowds-and-lod.md).
- **No file without a manifest row.** `node scripts/check-assets.mjs assets/manifest.json`
  fails on a file with no row, a row with no file, or a licence that forbids a paid game
  (CC-BY-NC, personal use, VRM meta `commercialUsage: personalNonProfit`). It runs in `verify`.
- **Characters: VRM only** (why: [`starter/learnings.md`](starter/learnings.md), Decisions). A model may be loaded from
  a link (VRoid Hub, BOOTH, a shared card) at runtime: the game shows the VRM meta (author,
  commercial use, allowed users) before use and refuses one that forbids games. Make or remix in VRoid
  Studio (free), pick from VRoid Hub, BOOTH or Sketchfab after reading the licence; the game
  refuses a model whose VRM meta forbids games. Ten original roster characters, never look-alikes.
- A plain GLB has no humanoid bones or expressions and would stand as a statue, so it is not accepted as a character; FBX or MMD PMX go through Blender plus the VRM add-on to .vrm (hq-characters HANDOFF, 2026-10-07).
- Loading from a link today: a thread curls the file, reads the licence from it and shelves it. Artifact pages cannot fetch VRoid Hub, BOOTH or Sketchfab pages (no CORS); an in-page link box only works for CORS-open direct hosts (GitHub raw, some CDNs). Show the licence before keeping (hq-characters HANDOFF, 2026-10-07).
- The VRM sample "Vita" (AvatarSample_F) reads in its VRM 0 meta as: everyone, commercial, credit unnecessary, modification and redistribution allowed; E, F and G are Vivi, Vita and Victoria from OpenGameArt `vroid-studio-cc0-models` (hq-characters HANDOFF, 2026-10-07).
- VRM loader security for user-supplied files: block external URIs inside the glTF and accept only png and jpeg portraits (hq-characters HANDOFF, 2026-10-07).
- **Moves are shared files**, not baked into models: VRMA from vrm.dev, or Mixamo FBX (free
  with an Adobe account, unmaintained) retargeted at load with `vrm-mixamo-retarget` or
  three-vrm's `loadMixamoAnimation` example; Quaternius Universal Animation Library is CC0.
- **Places**: build from CC0 kits (Kenney, Quaternius, Poly Haven) in the project's DESIGN.md
  taste, with the photos as references. Shrink every .glb in CI with gltf-transform (meshopt or
  Draco, KTX2 textures at most 2048 px).
  Exception (office research, 2026-10-07) [judgement]: Draco, meshopt and KTX2 need decoder files (extra requests, wasm); for low-poly atlases of a few MB skip them under the 16 MB Artifact limit, and meshopt is the lighter decoder.
- **Shrinking**: `gltf-transform optimize in.glb out.glb --compress meshopt --texture-compress webp` (flags vary by version). Meshopt covers geometry, morph targets and keyframe animation while Draco is geometry only, so animated characters use meshopt; the Draco decoder is about 10x larger. Resize textures first, then WebP (download size) or KTX2 (GPU memory) (low-poly-and-sources, 2026-10-24).
- **One palette texture** shared by all kit props (UVs on colour cells) = one material and one draw call; textures are usually 80 % or more of a GLB and all GPU memory (low-poly-and-sources, 2026-10-24).
- **Splats** (3D photos): 30 to 200 photos of one place, trained on yskills' PC (Postshot,
  Windows + NVIDIA: free plan trains, export needs Indie 17 €/month; Brush is open source) or a
  paid service, loaded with Spark as vistas and photo spots. No collision: never a floor.
- **AI props**: Meshy (free tier CC-BY, 20 $/month for commercial), TRELLIS.2 (MIT, needs a
  GPU); Tripo's free tier is non-commercial (sources conflict; treat it so until the ToS is read). One prop at a time, cleaned in the style pass.
- Meshy free is CC BY 4.0 (credit Meshy, the models become public), 100 credits a month at 20 per model (about 5 models); paid, about 10 to 20 USD a month (sources disagree on the price), gives private ownership and no credit (3d-route, low-poly-and-sources, 2026-10-18/24).
- **Look**: `MeshToonMaterial` with a `gradientMap` whose `minFilter` and `magFilter` must be `NearestFilter`; the map is a 3 to 5 pixel `DataTexture` of grey steps (low-poly-and-sources, 2026-10-24).
- **Export from Blender** (low-poly-and-sources, 2026-10-24): a flat or unlit look in glTF is `KHR_materials_unlit` ("Shadeless" in the exporter). The exporter writes Metal/Rough PBR and unlit only, PNG or JPEG, roughness from the green and metallic from the blue channel, tangent-space normals only, emission via Principled. Procedural nodes (noise, voronoi, wave) are not exported by glTF, FBX or USD (MaterialX partial): bake them to textures or rebuild as an engine shader. A Blender toon made with Shader to RGB into a Color Ramp set to Constant (Eevee only) gives hard bands but breaks the PBR chain (AO, soft shadows, SSR, SSS) and does not export to glTF [U]: rebuild it as `MeshToonMaterial` or bake. Vertex colours are glTF `COLOR_0`, used in three.js with `vertexColors: true` [U, not confirmed].
- **Manifest rule, extended** (low-poly-and-sources, 2026-10-24): besides name, URL, author and licence, a row records the version, the date retrieved, a screenshot of the terms for BOOTH and hosted AI, and whether the asset ships in the bundle (`templates/manifest.json` shows the optional fields).
- Spending on assets or services needs yskills' word first (CLAUDE.md money rule).

## 4. Testing in cloud threads

- **Unit**: Vitest on the rules, no renderer.
- **Screenshots**: in a new game `npm run shots -- [url] [--out dir]` (`scripts/shots.mjs`) builds, then
  runs the installed Chromium (`/opt/pw-browsers/chromium`) with `--use-angle=swiftshader
  --enable-unsafe-swiftshader --ignore-gpu-blocklist` and a fixed seed, and captures every spot of
  `test/game.mjs` (`spots`: the bot plays `steps` decisions first) at 390 and 1440 px. An older game
  copies `templates/shots.mjs` (camera spots by `?spot=`). New shots go through `design-critic`; the PR shows them.
  A page opened with `?paused=1` paints only inside `advanceTime()` and CSS fades run on the real
  clock: paint once with `advanceTime(16)` and wait about 700 ms before every screenshot (`settle()` in `scripts/lib.mjs`).
- **Play it, not just look at it**: a game exposes three hooks (`src/hooks.ts` in the starter):
  `window.render_game_to_text()` (the visible state as JSON: mode, score, time, positions),
  `window.advanceTime(ms)` (play that much game time at once; open the page with `?paused=1` so it
  is the only clock) and `window.__playInput(x, z)` (hold a direction). `test/game.mjs` is the one file
  a new game fills in (`decide` from the text, `min`, `stepMs`, `spots`); `npm run play -- [url] [--out dir]`
  (`scripts/play.mjs` + `scripts/lib.mjs`, copy all three into an older game; the url comes first; a Worker Preview or the live url plays as is, no url builds and serves `dist/`) plays a whole round,
  keeps three screenshots and fails on a page error, a round that never ends or a score under
  `min`. Rewrite `game.mjs` together with `rules.ts`: `min` is about 60 % of what the bot scores; a bot that dies is fine, one that cannot move is not. Run it on the Worker Preview before every gate; add each new state a bot needs to the text.
  QA after every slice, not at the end (idea from OpusGameLabs/game-creator, written in our words).
  `play` and `shots` build first when they have no url; a Preview or live url is shown as deployed.
- **Perf budget per scene** (`tests/perf`, reads `renderer.info` after one frame): under 300
  draw calls (mobile about 150, a guess), under 500 000 triangles, textures at most 2048 px; asset budgets are split by target (next bullet).
  SwiftShader cannot measure frame rate: yskills' PC runs the perf scene once per milestone and
  the number goes into PROGRESS.md.
- **Asset budgets by target** (CrazyGames technical docs, via the 5a table; the Steam number is our own guess): **browser first load about 20 MB** (CrazyGames allows 50 MB, 20 MB for the mobile homepage; a free demo is the same build), stream chapter 2 and splats after first play; total browser build at most 250 MB and 1500 files. **Steam build**: assets under 150 MB are a comfortable default, Electron adds about 250 MB on top and Steam uploads only changed chunks. Splats: about 500k per scene, SPZ only (third-party figure, unchecked). Add the 20 MB first-load check to `tests/perf` for the web build (not there yet).
- **Per-asset defaults** for low-poly web games (low-poly-and-sources, 2026-10-24; common practice, no primary source): mobile character 3 to 10k triangles, mobile prop 300 to 1,500, PC character 20 to 80k, Polycount's mobile figure about 1 to 3k with 512 px maps; shaders and overdraw hurt mobile more than triangles. Our proposed defaults: character 3 to 8k, prop 100 to 1,500, scene under 150k visible triangles on web, 1 material per object, 512 to 1024 px textures. The scene numbers above (500k) are the test ceiling; `starter/figures.md` (full figure at most 100k) and `refs/.../profiling-and-budgets.md` (30 to 80k / 5 to 20k) are other contexts.
- **LOD** is usually not worth it for stylised web games under about 5k triangles per object; instancing and culling matter more [U]. Godot has visibility-range LOD (low-poly-and-sources, 2026-10-24).
- **Greybox before art** (a level's metrics card, `?look=grey` from the layout's blocks, bot walk and sightline checks, blind plays, the greybox gate, footprints kept by the art pass): [`refs/greybox.md`](refs/greybox.md) (vacation-game, 2026-11-24).
- **A map of a real place** (country outline + real elevation as terraced diorama, stations at real coordinates, travel animation): [`refs/real-map-overworld.md`](refs/real-map-overworld.md) (vacation-game, 2026-11-12).
- **Realistic figures and crowds** (SFW game base, LOD chain 10k/5k/2k/700, three-tier crowds with instanced skinning): [`refs/crowds-and-lod.md`](refs/crowds-and-lod.md) (vacation-game research, 2026-11-10).
- **Instance or merge**: merged geometry loses per-object frustum culling, so merge only parts smaller than the viewport. Rule of thumb: instance 100+ identical objects, merge static non-identical parts (low-poly-and-sources, 2026-10-24).
- **Electron smoke**: CI runs the packaged app under `xvfb-run`, waits for the first frame and
  quits; Steam calls are stubbed outside Steam (`platform/web.ts`).
- **Gate preview**: the web build deploys to a Worker Preview like every project, so the
  evaluator plays the branch in a browser.
- **Local test server** must send `charset=utf-8`: Python's `http.server` alone garbles "Büro" and a click on it fails (set `extensions_map` for .html and .js and '' as octet-stream); copy the page files, never symlink (hq-characters HANDOFF, 2026-10-07).

## 5. Steam checklist

| Step | Who | Cost or time |
|---|---|---|
| Steamworks partner account (partner.steamgames.com): identity, bank, tax interview (W-8BEN, needs a Gewerbe) | yskills | free |
| Steam Direct fee per game | yskills | 100 $, back after 1 000 $ revenue |
| Store page: capsules 920×430, 462×174, 1232×706, 748×896, 600×900; 5 screenshots 1920×1080; trailer; texts de + en | threads make, yskills uploads | 1 to 5 days review |
| Content survey (gives the IARC label; without it the game is hidden in Germany) | yskills, from the thread's draft answers | free |
| Coming-soon page live 2 weeks; release at the earliest 21 days after the fee (Valve onboarding doc, read 2026-11-10; an older note here said 30) | calendar | |
| Builds: Windows + Linux depots (Linux covers Steam Deck), `electron-builder --dir`, uploaded by `steamcmd` through the `steam-deploy` action (`templates/steam-deploy.yml`) with a builder account whose Steam Guard config is a repo secret | yskills makes the builder account once; threads do the rest | free |
| Build review, release click | yskills | 1 to 5 days |
| Money: Steam keeps 30 %, pays monthly by bank; Gewerbe income, Kleinunternehmer is fine | yskills | |

### Wishlists, demo, Next Fest

Steam is a bet on an audience that already exists (`docs/research/2026-10-18-game-money.md`), so build it before launch:

- **Store page early**: the coming-soon page goes live at least 2 weeks before release, in practice months, and starts collecting wishlists.
- **Demo = the free chapters** of the browser build, uploaded as its own Steam app; the demo and full game can share one Cloud save through the Shared cloud APP ID field.
- **Wishlist target before Next Fest**: set a number first and join the fest only when the page is near it. Third-party benchmarks (HowToMarketAGame, Feb 2026, search summary only): wishlists before the fest track wishlists gained (r 0.825), median 806 wishlists in the fest, demo conversion median 16 % (12 to 20 %). No data for narrative games.
- **Track**: chapter-1 finish, chapter-2 start, wishlist click (`operator/roles/analytics.md`).
- **Price**: a 1 to 2 hour game is about 5 to 15 USD in 2026 guides (search summaries); start at 4.99 to 6.99 EUR, 9.99 only with 2+ hours, because Steam refunds under 2 hours played. Browser purchase at the same price; see `docs/research/2026-11-10-paid-games-and-service.md`.

### Saves and Steam Cloud

- Write one JSON save file (versioned, `{version, data}`) to a fixed folder; never rely on Chromium `localStorage` in the Electron build (it lives in the profile folder Steam does not sync). The web build keeps `localStorage`/IndexedDB behind the same `save.ts` interface.
- Auto-Cloud (Steamworks, Cloud settings; no code): one Root path per file group, OS restriction left on **Cross-Platform** (Valve's recommendation: a file locked to one OS never syncs to another later); add Root Overrides for Windows (e.g. `WinAppDataLocal`) and Linux (e.g. `LinuxXdgDataHome`) pointing at the same save folder. Keep machine-specific settings (video quality) out of cloud files. Steam drops a `steam_autocloud.vdf` next to the saves; ignore it.
- Test Windows to Steam Deck sync on a real client before release (`steamworks.js` also has its own overlay issues on Linux).
- Source: partner.steamgames.com/doc/features/cloud, read 2026-11-10.

Only yskills' hands: account, tax interview, fee, first upload, release click. Everything else
is a thread's job; when yskills must act, give the exact Steamworks page and the field names.

## 5a. CrazyGames checklist (web portal, free; checked 2026-10-17 against docs.crazygames.com)

The starter's `src/platform.ts` already wires the SDK (loaded only inside CrazyGames or with
`?platform=crazygames`, so the own site makes no third-party request): `loadingStart/Stop`,
`gameplayStart/Stop`, `midgame()` between rounds, `rewarded()` for an optional bonus. Both ad calls
resolve on finish, error or no fill, and the game is frozen and muted while one runs.

| Step | Who | Rule |
|---|---|---|
| Developer account at developer.crazygames.com | yskills (free, once) | the only hands step |
| Build: `npm run verify`, zip the contents of `dist/` (index.html at the zip root) | thread | relative paths only; initial download at most 50 MB (20 MB for the mobile homepage), total 250 MB, 1500 files |
| Basic Launch: upload, fill English title, description, controls, orientation | thread drafts, yskills submits | no SDK needed, ads off, live 7 to 21 days (500 plays), then they pick winners by playtime (10+ min good), day-1 retention (10 to 15 %), 1-minute conversion (80 %+) |
| Covers: landscape 1920x1080, portrait 800x1200, square 800x800, plus a landscape preview video and a portrait gameplay video (720x1280, about 13 s, real gameplay; the portal requires both) | Designer thread, vote card | the game's title only, no border, no store logos, no plain screenshot, originals only |
| Check in their QA tool in the developer portal | thread | English text and English fallback for any unknown locale, never German or another language (QA box; test `fr-FR` to `en`), readable at 907x510 and 800x450, physics the same at 144 Hz, PEGI 12, no own fullscreen button, no cross-promotion, no ads from anywhere else |
| Accept the Terms and the PEGI attestation, "Submit for approval" | yskills (his one tap, last step) | a thread stops with everything filled and says so in one line |
| Full Launch (only if selected) | thread | SDK on (already), land in gameplay with at most one click, works with AdBlock, ads only at natural breaks, never chained, rewarded optional and never required |

What earns (money route: `docs/research/2026-10-18-game-money.md`; the own-site line is a plain reading, not measured): only the portal's ads inside CrazyGames
(or Poki); the own site earns nothing without ads of its own, which need yskills' Impressum and
Datenschutz. A game's own-site legal page and the portal package are part of "done" (`operator` §1).

Checked by a real upload (2026-10-18, Hedgehog Garden): the English fallback and the portrait video were the two rules this table lacked. Not verified: review outcome; cover specs and limits were read from
the official docs on the date above, so re-read them before submitting. Payout terms (Tipalti,
minimum, split) are not published as a rule: confirm in the dashboard before counting on money.

Store art (Igelgarten crazygames-listing, 2026-10-18): covers and gameplay shots are rendered natively at 1920x1080, 800x1200 and 800x800 (headless Chromium, software WebGL, the bot at the wheel, seed 1), never upscaled.

## 5b. Tools: what is installed and why (checked 2026-10-07)

Plugin directory, skills.sh and the ECC index were searched (`toolbox` `find.mjs`,
`SearchPlugins`, `SearchSkills`). Nothing in the Anthropic Directory fits a cloud three.js
team: the Unity plugin is for Unity, CellCog and Mojulo are generation services. One candidate
to read on the PC later: `parallax-threejs` (community: three.js and GLSL debugging, visual
regression tests; needs its own MCP servers). The two best community skill packs were read in
full and vendored as text into `refs/` (licences in `THIRD_PARTY.md`); a game thread reads the
ones its slice needs:

| Folder under `refs/` | Use it for |
|---|---|
| `gamedev-skills/threejs-scene-setup`, `threejs-gltf-loading`, `threejs-materials-lighting` | current three.js API (r186: `setAnimationLoop`, `Timer`, physical lights, DRACO/Meshopt/KTX2) |
| `gamedev-skills/camera-systems`, `game-feel`, `level-design`, `audio-design` | the follow camera, juice, pacing, adaptive music |
| `gamedev-skills/performance-optimization` | frame and asset budgets (engine-neutral) |
| `gamedev-skills/steam-publish` | SteamPipe, depots, branches, store page (engine exports there are Godot/Unity; our Electron path is §5) |
| `threejs-game-skills/threejs-gameplay-systems` | Vite + TypeScript scaffold (`assets/threejs-vite-game`), physics choice, genre notes |
| [`game-ux`](../game-ux/SKILL.md) (ours), [`controls-baseline`](../game-ux/refs/controls-baseline.md) | controls floor, mouse look, HUD, onboarding, idle NPCs |
| `refs/low-poly.md`, `refs/asset-sources.md` (ours) | sourced low-poly budgets, shading, rigging and glTF rules; the pick-the-best-source table with licence checks (2026-10-25) |
| `threejs-game-skills/threejs-aaa-graphics-builder` | `references/visual-scorecard.md`: the 10-point look check the design critic uses with the references |
| `threejs-game-skills/threejs-qa-release` | Playwright canvas inspector, bot playtest, release checks |

Libraries are per game via npm (§1); nothing global to install. Blender's official connector
(PC only) and VRoid Studio stay yskills' PC tools (`toolbox` catalog `data-web.md`). When a
better tool appears, fix this table and the catalog, not a thread's memory.

Verdicts that cost a search each:

- Autodesk Fusion: free personal use is non-commercial with revenue under 1000 USD a year, and it is CAD, not a game-base tool: skip (3d-route, 2026-10-18).
- Do not install OpusGameLabs/game-creator: no licence file (all rights reserved by default), its money step is a crypto wallet and it deploys to GitHub Pages; copy only the ideas (QA after every step, play hooks) (game-route, 2026-10-17).
- Selling 3D models comes last, from assets our games already made: Fab pays 88 % but needs clean topology, which AI meshes rarely have [inferred]; CGTrader payout is 55 % rising to 80 % by yearly sales since 2026-09-15 and sellers report falling sales (game-route, 2026-10-17).

## 6. Lessons

- 2026-10-07 (HQ characters): test every loaded model in a browser with a real sample file before
  review. VRM 0 models face +z, so their bones' x and z rotations mirror (arms came out flipped,
  fingers flat, a wave that pointed). Walkers need A* over a floor grid from the furniture boxes,
  giving way instead of overlap, a stride that follows distance walked, ease in and out at about
  1 m/s; prove it headless by tracking the closest two walkers. A dialogue scene puts the card
  beside the speaker, never over her. Base64 text grows a third: size upload caps accordingly.
  Convert hex colours with `convertSRGBToLinear()` under sRGB output and keep tone mapping off on
  pastel scenes.

- 2026-10-07 (HQ office, test run): a walkable room needs a real third-person controller
  (capsule against the room mesh with three-mesh-bvh, keyboard plus touch stick, a follow camera
  that never clips through walls); moves as shared VRMA files; every model through the manifest
  with its licence shown; perf budget and fixed-clock screenshot spots in the tests; scene,
  entities and systems kept apart so the office lifts into a Vite game unchanged.

- 2026-10-07 (HQ office HANDOFF vs HQ characters HANDOFF): yskills decided at 09:02 that `assets/manifest.json` stays silent: no licence or money-use text anywhere in the UI. That wins for HQ; "every model through the manifest with its licence shown" (above) and "show the licence before keeping" (§3) stand for products, where a CC-BY licence still needs its credits file.

- 2026-10-06 (hq-characters HANDOFF, hq-game findings): single-file Artifact pages: three-vrm 1.x needs three r140 or newer; r147 is the last with the `examples/js` globals; switching r128 to r147 needs RGBFormat gradient textures changed to RGBAFormat; load GLTFLoader from the jsdelivr `examples/js` path. (The starter above uses r186 modules.)
