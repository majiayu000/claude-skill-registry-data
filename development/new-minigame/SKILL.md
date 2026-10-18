---
name: new-minigame
description: Add a new mini game to the Mini Game Portal (folder, game.json manifest, pages, thumbnail, tests, docs). Use when the user wants to start a new game or add a page/tool to an existing game.
---

# Add a mini game to the portal

The portal and the Rsbuild config discover games from `src/games/<id>/game.json`.
No central registry needs editing.

## Steps

1. Pick a short id (`[a-z0-9_-]`), create `src/games/<id>/`.
2. Write `game.json` (schema: `src/portal/manifest.ts`):
   ```json
   {
     "id": "<id>",
     "title": "My Game",
     "version": "0.1.0",
     "description": "One or two sentences for the portal card.",
     "tags": ["three.js"],
     "pages": [
       {
         "id": "play",
         "entry": "pages/play.ts",
         "title": "My Game",
         "label": "Play"
       },
       {
         "id": "level-viewer",
         "entry": "pages/level-viewer.ts",
         "title": "My Game · Levels",
         "label": "Levels",
         "dev": true
       }
     ]
   }
   ```
   - `play` is served at `/games/<id>/`; other pages at `/games/<id>/<page-id>.html`.
   - `dev: true` pages show as tool buttons on the portal card.
   - Links must be relative (the build may be hosted in a sub-folder): portal = `../../`, sibling page = `<page-id>.html`, main page = `./`. Never use a leading `/`.
   - The game builds into its own self-contained `dist/games/<id>/` (own Rsbuild environment, picked up automatically). Load runtime files relative to the page (`new URL('models/x.glb', location.href)`) or import them, never from the portal root; a game-only file in the root `public/` needs a `gamePublicFiles` entry in `rsbuild.config.ts`.
   - The play page's main menu (and pause / results screens) must offer an **All games** button when `portalUrl()` (`src/shared/portal-link.ts`) is not null - installed as a PWA there is no browser back button.
3. Entry files: the default HTML template has `<div id="root">`. Import page CSS from the entry.
   Use three.js unless the user asked otherwise. Reuse `src/shared/*`:
   - `debug-panel.ts` (left tool menu), `url-state.ts` (bookmarkable state), `stats-overlay.ts` (F3)
   - `rng.ts` / `noise.ts` for anything procedural (seeded!)
4. Portal screenshot: in the play page call
   `installThumbnailCapture('<id>', () => { renderer.render(scene, camera); return renderer.domElement; })`,
   run `npm run dev`, open the game, press **F9** -> writes `src/games/<id>/thumbnail.jpg`.
   - Audio: the game's audio class (WebAudio / `Audio`) must start silent when `isMutedByUrl()` (`src/shared/mute-param.ts`, `?mute=1`) is true. **When you open the game in the browser pane to test, always add `mute=1` to the URL** - no sound while creating / editing, unless the task is a sound fix (then no param, low volume).
5. Add the game to `GAME_LIST` in `src/portal/release.ts` (card order). Work in progress? Give it `hideInProd: true` there: the release build gives the game no portal card but still builds it, so people with the link (`games/<id>/`) can play it. The dev server and `build:test` list it. Remove the flag to release.
6. Restart `npm run dev` after adding a new game folder / page (entries are read at startup).
7. Tests in `tests/<id>/`, a `test:<id>` npm script and a CI job (`testing` skill); keep game logic DOM-free so it is testable in node.
8. Write the docs short (`AGENTS.md` "Write short"). Add `src/games/<id>/README.md` (high level: what it is, screenshot, how to play, feature list, links) and `src/games/<id>/DETAILS.md` (pages, keys, rules, architecture), and a row in the root `README.md` table.
9. Verify: `npx tsc --noEmit -p tsconfig.json`, `npm run lint`, `npm run test`, `npm run build`.

## Patterns worth copying from rally

- Fixed-step simulation + render interpolation (`src/games/rally/game/rally-game.ts`).
- `benchmark(n)` method exposed on `window.__<game>` to measure ms/frame even when the tab is hidden.
- Tool pages built on a shared shell (`src/games/rally/debug/viewer-shell.ts`).
