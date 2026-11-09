---
name: motion-photo
description: "Make a looping product or photo reel, 8 to 15 seconds, from the user's own images (product shots, screenshots, cutouts, venue photos). Photos drift in crops (Ken Burns), reveal through wipes, circles, splits and shapes, float as parallax cutouts, slide past in a carousel or stack, compare in a before/after slider, assemble into a mosaic and carry price and feature tags on leader lines. Claude writes one HTML canvas file driven by a pure seek(t), critiques it (image resolution, text contrast on the pixels behind it, subjects kept in every crop) and renders MP4, GIF and poster at 9:16, 1:1 or 16:9 with motion blur and a seamless loop. Use it for a product reel, a collection drop, a screenshot tour, an event recap or a before and after. Not for stock photos or images the user may not use. Other styles have their own skills: motion-launch-videos (kinetic type), motion-shapes, motion-cartoon, motion-3d, motion-charts, motion-pixel, motion-particles, motion-ui, motion-captions, motion-overlays and motion-globe."
---

# Motion photo

The user's own pictures, moving like a product reel: a hero shot pulls back while the name rises over it, the product floats off its set with two tags drawn to it, a slider sweeps from the old finish to the new, the colourways slide past on cards, and the lockup assembles from a strip of photos. The whole film is one HTML file with the images embedded, and it can draw any moment from the time alone, so it previews in any browser, renders frame-exact, and loops without a seam.

The skill folder is `${CLAUDE_SKILL_DIR}`; the reference files call it `<skill>`. If the variable shows up literally or empty in your shell (you opened this file directly, as a subagent or from a copy), it is the folder that holds this SKILL.md: put that absolute path in every command below.

A film lives in the user's project at `videos/<film>/` (`BRIEF.md`, `DESIGN.md`, `assets/`, `src/film.html`, `fonts/`, the built `<film>.html`, `stills/`, `renders/`).

## Ground rules

- **Only the user's own images.** Every picture is one the user made, owns or has licensed, and BRIEF.md's Assets table says which, file by file. No stock photos, nothing downloaded from the web, no screenshots of other companies' products, no photos of people who have not agreed to appear. Images you make yourself for a demo (renders, drawings) are logged the same way.
- **True claims only.** Every title, tag and price comes from the product's own live pages, logged with their URLs in `BRIEF.md`; every tag names its fact (`fact: 'F2'`) and the critique fails one that does not. No prices or numbers the source does not show today. A product with no live site takes its words from the user's brief only. See [reference/brief.md](reference/brief.md).
- **Four words a beat, one call to action.**
- **`seek(t)` is pure.** No timers, `Date`, `Math.random`, state or CSS animation; seeded randomness only. Images are decoded, measured and pre-scaled once in `build()`, never while drawing.
- **One file.** Fonts and images embedded as data URLs; nothing loads over the network. The build enforces it.
- **The loop is exact.** In the default hold loop, frame 0 is the lockup at rest and equals the last frame: `loopcheck` reports a max diff of 0.
- **Look before you ship.** Numbers pass while frames look wrong; read the stills and the decoded frames.
- **The user decides what leaves the machine.** Get a yes before any commit, push or upload.

## Workflow

0. **Once per machine.** `node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" doctor` checks Node 20+, playwright-core, a Chromium, ffmpeg with libx264, ffprobe, npm and tar, and prints the exact command for anything missing (usually `npm install --prefix "${CLAUDE_SKILL_DIR}" --no-package-lock`, or `npm i -D playwright-core` in the user's project). Re-run it until it says `DOCTOR OK`.
1. **Brief intake and the images.** Name the video type first (a launch bumper, a feature highlight, a testimonial, an event promo...): [reference/video-types.md](reference/video-types.md) gives each type its length, formats, beats and the styles that fit. Read the product's live site first. Then **ask for the images** (the hero shot, 3 to 8 more, and a cutout PNG with transparency if the product should float), where each came from, and in the same single round the message, the formats, duration and palette, or use the defaults: 1080 x 1080 master, rendered at 9:16 for a social product reel (Reels, TikTok, Shorts) and at 1:1 for feeds, 12 s, 60 fps, 120 BPM, muted, hold loop, a background colour taken from the photos. Copy the images into `videos/<film>/assets/`, and fill [templates/BRIEF.md](templates/BRIEF.md) into `videos/<film>/BRIEF.md` with an **Assets** table: each file, what it shows, its size in pixels, and its source. With no images of the user's own, there is nothing true to show: say so and stop, or make a clearly labelled fictional demo from images you make. See [reference/brief.md](reference/brief.md) and [reference/video-types.md](reference/video-types.md).
2. **Shot list and copy.** Look at every image (Read it) before choosing. Pick one picture per beat and the move that shows it best (a pull-back on the hero, a parallax float for a cutout, a slider for two versions of one shot, a carousel for a range, a mosaic for the lockup), and for each image note its focus (the point that must stay in frame: a face, the product) and its subject box, as fractions of the image. Give each beat at most 4 words, and tags only for facts in the brief. Show the user the shot list and proceed unless they object; when nobody can answer, write it into BRIEF.md and proceed.
3. **Design spec.** Fill [templates/DESIGN.md](templates/DESIGN.md) into `videos/<film>/DESIGN.md`: canvas and formats, palette roles, type roles, the images (focus, subject, the largest size each is shown at), every scene (layers, frames, moves, springs, masks, tags) on the tempo grid, each other format's patch, and the loop seam. Read [reference/photo-craft.md](reference/photo-craft.md), [reference/engine.md](reference/engine.md) and [reference/springs.md](reference/springs.md).
4. **Build and measure.** Copy [templates/film.html](templates/film.html) to `videos/<film>/src/film.html` and transcribe DESIGN.md into its `FILM` block (edit nothing below it; the build copies the title, the background and the canvas size into the page head). Fetch the fonts, build, and read the measured layout:
   ```bash
   node "${CLAUDE_SKILL_DIR}/scripts/fonts.mjs" videos/<film>
   node "${CLAUDE_SKILL_DIR}/scripts/build.mjs" videos/<film>
   node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" layout videos/<film>    # text sizes and cap tops, frames, each image's pixels and largest shown size
   ```
   Put text baselines on the 8 px grid from the reported cap heights, then write the final numbers into DESIGN.md and FILM together. Author the square first; for each other format add a patch to `FILM.formats` (at 9:16 the picture above the words, at 16:9 beside them). See [reference/engine.md](reference/engine.md) (Formats), [reference/fonts.md](reference/fonts.md) and [reference/core.md](reference/core.md).
5. **Stills and critique.** `node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" stills videos/<film>` runs the automated critique (glyph coverage, assets embedded and declared, each image's resolution, focus and subject kept in every crop, text contrast measured on the pixels behind it, words per beat, tags citing facts, live area, collisions, palette roles, the loop, blank frames, the composition) and writes stills plus `stills/contact.png`. Read the contact sheet and the full-size stills; fix and repeat until it passes and looks right. Run it again with `--format 9:16` and `--format 16:9` for each other format you deliver (stills go to `stills/9x16/`). See [reference/review.md](reference/review.md).
6. **Render and verify.**
   ```bash
   node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" loopcheck videos/<film>   # hold loop: every diff must be 0
   node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" render videos/<film>      # MP4, GIF, poster
   node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" verify videos/<film>      # ffprobe facts, tags, decoded pixels
   node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" mp4frames videos/<film>   # decoded review frames + PSNR
   ```
   Run the four once per delivered format, adding `--format 9:16` or `--format 16:9` (outputs `renders/<film>-9x16.mp4`, `preview-9x16.gif`, `poster-9x16.png`). Look at `stills/mp4/contact.png` and the full-size frames at each transition, carousel step and slider stop. Report the files, their sizes and the verify, loopcheck and mp4frames lines. See [reference/render.md](reference/render.md) and [reference/loops.md](reference/loops.md).

## Pass criteria

- Every image is the user's own and has a row in BRIEF.md's Assets table; every tag and price cites a fact.
- No image is shown larger than 1.15 times its own pixels; the focus of every image stays inside its crop, and its subject in frame, at every format.
- Display type at least 3:1 and small print at least 4.5:1 against the pixels actually behind it (a scrim or a quiet part of the picture where needed); at most 4 words of display type a beat.
- One picture per beat, one move per picture; Ken Burns moves slow and in one direction; transitions vary (circle, wipe, split, a shape, a cut).
- Every text layer and tag inside the live area, baselines on the grid, no text colliding with text.
- Every delivered format passes the critique, the composition row included, and its loopcheck is 0.
- Motion blur on every moving frame, one sample on still ones.
- The deliverable MP4 is H.264, yuv420p, BT.709-tagged in the stream, faststart, exactly DUR x FPS frames.

## Known pitfalls

- A Ken Burns zoom below 1 on a cover-fit photo would show the frame's edge: the engine holds it at 1. Zoom in from above 1 instead, or use `fit: 'contain'` on a matte.
- A square photo cannot fill a 16:9 or 9:16 frame without losing a third of itself: the crop check says when the subject goes. Give that format a framed photo instead of a full-bleed one (a patch in `FILM.formats`).
- A drifting full-bleed layer with a depth is overscanned automatically to keep the canvas covered, so it is shown larger than its frame: its resolution row counts that.
- Text over a photo that passes in the square can fail at 9:16, where the crop puts something bright behind it. Check the contrast row at every format.
- The palette gate (mixed inks) does not apply to photographs: the engine marks no accent frames. Every drawn colour (type, tags, frames, scrims) is still a palette role.
- Keep the files small: the build embeds them whole, so a 4000 px photo shown at 1080 px weighs four times what it needs to. The resolution row says when a file could be smaller, and to what size.
- A cutout needs a real alpha channel (PNG or WebP). A JPEG "cutout" on white shows its white box.
