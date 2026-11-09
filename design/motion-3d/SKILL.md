---
name: motion-3d
description: "Make a looping 3D motion-graphics film, 6 to 20 seconds, from a short brief. Real extruded, bevelled 3D type and SVG logos, plus boxes, spheres, tori, cylinders, cones and capsules, lit by a key light with soft shadows on a seamless floor, turning, flipping, hopping and orbiting on springs under a moving camera. Claude writes the film as one self-contained HTML file (a small WebGL2 renderer, no libraries) driven by a pure seek(t), checks it with an automated critique, and renders it to MP4, GIF and poster, square, vertical or wide, with real motion blur and a verified seamless loop. Use it for a 3D logo sting, a 3D title or wordmark reveal, an abstract 3D product teaser, a spinning badge, or a social loop with 3D type. Not for photoreal product renders, imported 3D models or characters. Other styles have their own skills: motion-launch-videos (kinetic type), motion-shapes, motion-cartoon, motion-charts, motion-pixel, motion-particles, motion-ui, motion-photo, motion-captions, motion-overlays and motion-globe."
---

# Motion 3D

Chunky extruded type and simple solids in a clean studio: a floor that melts into the background, one key light, soft shadows, a camera that drifts. The whole film is one HTML file that can draw any moment from the time alone, so it previews in Chrome, renders frame-exact, and loops without a seam.

The skill folder is `${CLAUDE_SKILL_DIR}`; the reference files call it `<skill>`. If the variable shows up literally or empty in your shell (you opened this file directly, as a subagent or from a copy), it is the folder that holds this SKILL.md: put that absolute path in every command below.

A film lives in the user's project at `videos/<film>/` (`BRIEF.md`, `DESIGN.md`, `src/film.html`, `fonts/`, the built `<film>.html`, `stills/`, `renders/`).

## Ground rules

- **True claims only.** Every word on screen comes from the product's own live pages and is logged with its URL in `BRIEF.md`. A product with no live site takes its words from the user's brief only. See [reference/brief.md](reference/brief.md).
- **Only what is the user's to extrude.** Type from an open font, the user's own SVG logo, and primitives. Never another company's logo or a model of someone else's product.
- **Four words a beat, one call to action.**
- **`seek(t)` is pure.** No timers, `Date`, `Math.random`, state or CSS animation; seeded randomness only. Geometry is built once, after the fonts load.
- **One file.** Fonts embedded as base64; the renderer is inline; nothing loads over the network. The build enforces it.
- **The loop is seamless.** The default is a cycle loop: every spin and orbit turns a whole number of times, every keyed move comes back (a full turn counts), and `loopcheck` finds the seam as smooth as any other instant.
- **Look before you ship.** Numbers pass while frames look wrong; read the stills and the decoded frames.
- **The user decides what leaves the machine.** Get a yes before any commit, push or upload.

## Workflow

0. **Once per machine.** `node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" doctor` checks Node 20+, playwright-core, a Chromium, ffmpeg with libx264, ffprobe, npm and tar, and prints the exact command for anything missing. WebGL2 runs on the GPU, or on Chromium's software renderer when there is none (slower, same pixels every time). Re-run it until it says `DOCTOR OK`.
1. **Brief intake.** Name the video type first (a launch bumper, a feature highlight, a testimonial, an event promo...): [reference/video-types.md](reference/video-types.md) gives each type its length, formats, beats and the styles that fit. Read the product's live site, then ask at most one round of questions (the word or logo to build, the message, which formats to deliver (1:1, 4:5, 9:16, 16:9), duration, palette). Defaults: 1080 x 1080 only, 10 s, 60 fps, 120 BPM, cycle loop, the template's palette or the brand's colours. For a logo, ask for the SVG. Fill [templates/BRIEF.md](templates/BRIEF.md) into `videos/<film>/BRIEF.md`. See [reference/brief.md](reference/brief.md).
2. **Copy and staging.** 1 to 3 beats: the hero (the word or the logo), what moves round it, a call to action in flat labels. At most 4 words of 3D type. Show the user and proceed unless they object; when nobody can answer, write them into BRIEF.md and proceed.
3. **Design spec.** Fill [templates/DESIGN.md](templates/DESIGN.md) into `videos/<film>/DESIGN.md`: palette and materials, the light, the camera and its moves, every object with its size, place, material and motion on the tempo grid, the loop, and what changes in each other format. Read [reference/3d-design.md](reference/3d-design.md), [reference/engine.md](reference/engine.md) and [reference/springs.md](reference/springs.md).
4. **Build and frame.** Copy [templates/film.html](templates/film.html) to `videos/<film>/src/film.html` and transcribe DESIGN.md into its `FILM` block (edit nothing below it). Fetch the fonts, build, and check the framing:
   ```bash
   node "${CLAUDE_SKILL_DIR}/scripts/fonts.mjs" videos/<film>
   node "${CLAUDE_SKILL_DIR}/scripts/build.mjs" videos/<film>
   node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" layout videos/<film>    # triangles, on-screen boxes at 0 s
   node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" at videos/<film> 0 2.5 5 7.5   # sharp stills to look at
   ```
   Move the camera (target, distance, pitch) until the hero sits in the live area with room to move. For each other format, add `--format 9:16` (or `16:9`, `4:5`) to `layout` and `at`, and write its patch in `FILM.formats`: the camera fits the hero by itself, the patch redesigns the rest (engine.md, Formats). See [reference/fonts.md](reference/fonts.md) and [reference/core.md](reference/core.md).
5. **Stills and critique.** `node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" stills videos/<film>` runs the automated critique (glyph coverage, words, the 3D type inside the live area through the loop and big enough to read, mesh counts, label contrast and placement, the loop and its cycles, the composition's balance) and writes stills at every key moment plus `stills/contact.png`. Run it once per delivered format, with `--format 9:16` and so on (stills land in `stills/9x16/`). Read them for silhouettes, intersections, shadows and legibility; fix and repeat. See [reference/review.md](reference/review.md).
6. **Render and verify.**
   ```bash
   node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" loopcheck videos/<film>   # purity 0, the seam continuous
   node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" render videos/<film>      # MP4, GIF, poster (start it in the background)
   node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" verify videos/<film>      # ffprobe facts, tags, decoded pixels
   node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" mp4frames videos/<film>   # decoded review frames + PSNR
   ```
   Run `loopcheck`, `render`, `verify` and `mp4frames` once per delivered format, with the same `--format` (the outputs carry it: `renders/<film>-9x16.mp4`, `preview-9x16.gif`, `poster-9x16.png`). Look at `stills/mp4/contact.png` and a strip of the whole film. Report the files, their sizes and the verify, loopcheck and mp4frames lines. See [reference/render.md](reference/render.md) and [reference/loops.md](reference/loops.md).

## Pass criteria

- The hero reads in every frame of every delivered format: 3D type inside the live area at every sampled moment, its cap height at least 60 px on screen, front faces light against the background.
- The composition row passes at every delivered format, and each format looks designed for its frame, not a square picture floating in it.
- Nothing passes through anything: no ring through a letter, no orb through the floor, no letter through its neighbour while it flips.
- One key light, soft shadows grounding every object on the floor; the floor meets the background with no visible horizon.
- Every spin and orbit a whole number of turns per loop; every keyed value back where it started.
- Motion blur on moving frames; flat labels sharp.
- The deliverable MP4 is H.264, yuv420p, BT.709-tagged in the stream, faststart, exactly DUR x FPS frames.

## Known pitfalls

- A torus spinning about its own axis looks still; tilt it and orbit it (`loop: { orbit: [1, 0] }`) so the tilt turns.
- Anything whose lowest point dips below the floor is cut by it. Keep `pos.y` at least the object's lower extent.
- The palette gate is not run for 3D: shading, antialiasing and motion blur make in-between colours at every silhouette. The lighting is hue-preserving (a surface is its colour times a light level, plus white), so surfaces keep their hue.
- Thin strokes and small counters in a light face extrude into slivers and break the bevel; use heavy display faces (Unbounded 800 to 900, Archivo Black).
- A letter flipping about x sweeps through its neighbours if the tracking is tight; give flipping type +30 to +60 tracking.
- The software renderer is slow: without a GPU, a 1080 x 1080 subframe with 4x MSAA and soft shadows takes 0.1 to 0.3 s, so the 10 s demo renders in 4 to 8 minutes (slow drifts take 2 subframes, fast flips up to 9). Keep scenes under about 100k triangles, and moves that need dozens of subframes rare.
- In a narrower format the camera's distance is multiplied by the fit, keys included: a patch sets `camera.dist` as it would be at 1:1, and a patch that sets `pitch` or `target` changes the fit too (it is measured from the rest camera).
- Contrast is checked on the material colours, but the lit front face is darker than its colour by up to a third: keep light type on a dark background or the reverse.
