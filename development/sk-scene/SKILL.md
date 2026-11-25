---
name: sk-scene
description: Builds and fixes the visuals of a short in Remotion inside its own folder src/videos/<id>/, using shared components from src/shared/, keeping text inside the platform safe zones, and reviewing rendered stills before claiming anything is done. Use when the user says "build the scenes", "make this shot", "the text is cut off", "move the caption", "add motion", "change the colours or font", "open the studio", "render a still", or "check the layout". Steps 8 and 9 of sk-pipeline.
---

# sk-scene: build the picture, then look at it

**Announce:** "Using sk-scene for <id>."

Rules: §5 (`docs/soul/03-visuals.md`) and the files in `docs/visuals/` for each
type in `visual`, §6 colour and type, §7 safe zones and captions
(`docs/soul/05-caption.md`), §12 motion (`docs/soul/09-motion.md`), §13 files.
The § wins over this file.

## Layout

```
src/videos/<id>/  entry.tsx  <Name>.tsx  scenes.tsx  Cover.tsx  timing.ts  narration.json  voice.json
src/shared/       theme.ts font.ts timings.ts
                  frame/ (ShortsTemplate, SafeZones, SafeCheck, Watermark, Backdrop)
                  caption/ (Captions, TypeStage)  audio/ (BackgroundMusic, Sfx)  motion/ (anim)
```

Each video has its own `entry.tsx` with its own `registerRoot`, so a half-built
video never breaks another video's bundle. **A video never imports another
video.** Something two videos need goes to `src/shared/<kind>/`, written against
`theme.ts` and the safe zones, not copied between folders.

The canvas is per video (`video.json` → `format`). Read size and safe area from
`useFormat()` / `safeFor()` in `src/shared/format.ts`; `W` and `H` in `theme.ts` are the
portrait defaults only. Landscape promos: `docs/promo/README.md`.

## Steps

0. **Storyboard first, approved before code.** After `bun run tts`, run
   `bun run storyboard <id> --init` and fill in every shot: `camera`, `onScreen`,
   `text`, `transition`, `sfx`, anchored to the word that names the change. Show it to
   the user (preview, Storyboard tab) and wait for approval; set those shots to
   `approved`. Build only approved shots, mark each `built` after you have looked at its
   still, and change the storyboard before the scene when the plan changes.
   After any change to the words (script edit, `bun run tts`, `bun run cut`), run
   `bun run storyboard <id> --sync`: shots whose line changed go back to `planned` and
   need the user's approval again before their scenes change.
   Schema and rules: `docs/storyboard.md`.
1. **Check `src/shared/` before writing a component.** It already handles the
   9:16 frame, theme and safe zones. For interface components (cards, tags, code,
   chat, agent UI, product flows, backgrounds) take them from **Knowns UI**, in its
   own tokens, instead of drawing new ones (§5; recipe in `docs/promo/real-ui.md`).
   Other borrowed code is rewritten against `theme.ts`, with its source and licence
   in a comment. Avoid runtime dependencies that fetch
   data while rendering: a re-render must produce the same file.
2. **Time from the voice, never by hand.** Use `src/shared/timings.ts`:
   `sceneTimings(voice, fps, outroHold)`, `totalFrames(voice, fps, outroHold)`,
   `wordsInScene(...)`, `wordAt(voice, t)`. Anchor a shot to the word that names it
   with `frameAtWord(voice, fps, sceneId, word, nth?)`, so the picture shows what is
   being said; it throws at build time if the word is gone from the script.
3. **Maps and globe (visual `satellite-map` / `globe`).** List camera shots in
   `src/videos/<id>/map.json`, then `bun run satellite <id>` (imagery, one mosaic per
   scale) and `bun run geo <id>` (coasts, borders, rivers). Draw with `SatelliteMap`,
   `VectorLayer`, `Route`, `Pin`/`Measure` from `src/shared/map/`; Vietnam has a ready
   `VietnamMap` with the archipelagos. For the planet, `Globe`, `GlobeLine` and
   `GlobeReveal` (pull out from a scene to Earth). Rules: `docs/visuals/satellite-map.md`,
   `docs/visuals/globe.md`. Distances on frame come from `distanceKm`, not from a quote.
4. **Build in the studio:** `bun run dev <id>`.
5. **Two motion rules (§12):** no shot stands still while the voice is speaking,
   and no shot is empty. On-frame text is a fact the ear cannot catch (a number, a
   name), never a copy of the caption, and at most `onFrameTextMaxSceneShare` of scenes.
6. **Keep `Watermark` (if used) after the `<Sequence>` blocks** so it renders on top.
   **Sound effects (optional):** 2–3 per video, each cued to a word with
   `frameAtWord(voice, FPS, scene, word)` and passed as `sfx={...}` to `ShortsTemplate`.
   Only where the facts are already funny or sharp, never on a sentence or a death
   toll. Ids, rules and cases: `docs/shots/sfx/` (one card per effect).
7. **Type-check and boundaries:** `bun run check`.
8. **Still-first review.** Before any full render:
   ```bash
   bun run still <id> --frame=<N>     # → out/<id>/still-<N>.png
   ```
   Pick frames where something is hard: the densest text, the first frame of each
   scene, the moment a number appears, the last frame. Render with the `SafeCheck`
   overlay on (§7) so the three unsafe edges are drawn over the frame.
9. **Open every still and look at it.** A static check passing is not the frame
   being right: text clipped by a parent's width, a caption under the platform's
   buttons, a number covered by the like column only show up in pixels. Do not
   say a scene is done until you have opened its still.

## Verify

- [ ] no import from another `src/videos/*` folder; `bun run check` clean
- [ ] every visual type in `visual` has had its `docs/visuals/` file read
- [ ] stills rendered for the hard frames, opened, safe-zone overlay clear
- [ ] no static shot under speech, no empty shot
- [ ] probe and test images stay out of the hand-off set (§13)

Next: `sk-render`.
