---
name: motion-ui
description: "Make a looping app or product UI promo, 8 to 15 seconds, from the user's screenshots or live site. A phone, tablet or browser window shows their real screens, rebuilt from primitives in their colours and copy, driven like a live demo: a finger or cursor taps, scrolls and types, screens push and expand, sheets and toasts open, the camera focuses, with short callouts and a closing lockup. Claude writes one self-contained HTML canvas file driven by a pure seek(t), checks it with an automated critique, and renders MP4, GIF and poster with real motion blur and a verified seamless loop, square, 9:16 or 16:9 from one film. Use it for an app launch video, an app-store style preview, a feature announcement, a changelog clip or a landing-page hero. Not for screen recordings of a real app. Other styles have their own skills: motion-launch-videos (kinetic type), motion-shapes, motion-cartoon, motion-3d, motion-charts, motion-pixel, motion-particles, motion-photo, motion-captions, motion-overlays and motion-globe."
---

# Motion UI

A product demo you can loop: the device rises in, a finger scrolls the list, taps a card that grows into its screen, taps Save; the button turns, a toast drops in, a callout names each step, and the lockup closes the loop. The UI is the user's own, rebuilt from their screenshots as boxes, text, icons and widgets, so every frame is sharp at any zoom. The whole film is one HTML file that can draw any moment from the time alone, so it previews in any browser, renders frame-exact, and loops without a seam.

The skill folder is `${CLAUDE_SKILL_DIR}`; the reference files call it `<skill>`. If the variable shows up literally or empty in your shell (you opened this file directly, as a subagent or from a copy), it is the folder that holds this SKILL.md: put that absolute path in every command below.

A film lives in the user's project at `videos/<film>/` (`BRIEF.md`, `DESIGN.md`, `src/film.html`, `fonts/`, the built `<film>.html`, `stills/`, `renders/`).

## Ground rules

- **The UI is the user's real UI.** Every screen is rebuilt from the user's screenshots or their live product, in their colours and their copy. Never invent a screen, a feature, a number or a piece of data the product does not have. A stylised simplification (fewer rows, skeleton bars where text does not matter, larger type) is fine, and BRIEF.md says so.
- **True claims only.** Every callout and the lockup come from the product's own live pages, logged with their URLs in `BRIEF.md`. No prices, ratings or numbers the source does not show today. A product with no live site takes its words from the user's brief only. See [reference/brief.md](reference/brief.md).
- **Only what is the user's to use.** No app-store badges, no platform or OS logos, no other company's logo or device trade dress: the device is a generic phone, tablet or browser window. No real people's photos: avatars are initials, photos are flat colour placeholders.
- **Four words a callout, one call to action.**
- **`seek(t)` is pure.** No timers, `Date`, `Math.random`, state or CSS animation; seeded randomness only. Layout is measured once, after the fonts load.
- **One file.** Fonts embedded as base64; nothing loads over the network. The build enforces it.
- **The loop is exact.** In the default hold loop, frame 0 is the lockup at rest and equals the last frame: `loopcheck` reports a max diff of 0.
- **Look before you ship.** Numbers pass while frames look wrong; read the stills and the decoded frames.
- **The user decides what leaves the machine.** Get a yes before any commit, push or upload.

## Workflow

0. **Once per machine.** `node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" doctor` checks Node 20+, playwright-core, a Chromium, ffmpeg with libx264, ffprobe, npm and tar, and prints the exact command for anything missing (usually `npm install --prefix "${CLAUDE_SKILL_DIR}" --no-package-lock`, or `npm i -D playwright-core` in the user's project). Re-run it until it says `DOCTOR OK`.
1. **Brief intake.** Name the video type first (a launch bumper, a feature highlight, a testimonial, an event promo...): [reference/video-types.md](reference/video-types.md) gives each type its length, formats, beats and the styles that fit. Read the product's live site first. Then **ask for screenshots of the 2 to 4 screens the demo should walk through** (full screens at the device's native size, plus the app icon if there is one), and in the same single round of questions ask the message, the formats (an app store preview or a Reel is 9:16, a landing-page hero 16:9, a feed post square; one film renders any of them), duration and device, or use the defaults: 1080 x 1080 only, 12 s, 60 fps, 120 BPM, muted, hold loop, a phone, brand colours from the site's CSS or the screenshots. Fill [templates/BRIEF.md](templates/BRIEF.md) into `videos/<film>/BRIEF.md`, including which screens were rebuilt from which screenshot and what was simplified. With no screenshots and no live product, there is nothing true to show: say so and stop, or make a clearly labelled fictional demo. See [reference/brief.md](reference/brief.md).
2. **Screens, script and copy.** Pick the one path through the product that says what it does (open, act, confirm), as a list of actions: where the pointer goes, what it taps, what changes. Give each step at most one callout of at most 4 words, lifted from the site, and plan the lockup (icon, name, domain). Show the user the steps and the callouts and proceed unless they object; when nobody can answer, write them into BRIEF.md and proceed.
3. **Design spec.** Fill [templates/DESIGN.md](templates/DESIGN.md) into `videos/<film>/DESIGN.md`: canvas and device, the layout of each other format you deliver, palette roles with contrast, type roles, each screen's layers traced from its screenshot (in screen units, with what became bars), the script on the tempo grid, the callouts, the camera and the loop seam. Read [reference/ui-motion.md](reference/ui-motion.md), [reference/engine.md](reference/engine.md) and [reference/springs.md](reference/springs.md).
4. **Build and measure.** Copy [templates/film.html](templates/film.html) to `videos/<film>/src/film.html` and transcribe DESIGN.md into its `FILM` block (edit nothing below it; the build copies the title, the background and the canvas size into the page head). Fetch the fonts, build, and read the measured layout:
   ```bash
   node "${CLAUDE_SKILL_DIR}/scripts/fonts.mjs" videos/<film>
   node "${CLAUDE_SKILL_DIR}/scripts/build.mjs" videos/<film>
   node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" layout videos/<film>    # device box, screen boxes, every text's output px and backdrop
   ```
   Check each text's output size and backdrop in the layout, put callout baselines on the 8 px grid level with the element they name, then write the final numbers into DESIGN.md and FILM together. Author the square first; for each other format, add a patch to `FILM.formats` (a bigger phone and callouts above it at 9:16, the phone beside the callouts at 16:9) and read `layout --format 9:16`. See [reference/engine.md](reference/engine.md) (Formats), [reference/fonts.md](reference/fonts.md) and [reference/core.md](reference/core.md).
5. **Stills and critique.** `node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" stills videos/<film>` runs the automated critique (glyph coverage, UI text size, contrast of every text against its own container, text overflow and collisions, callout words, leader targets, callout clearance from the device, the zoom and each other, the zoom's target kept in frame, taps landing on what they press, crossfades, the device seam, palette roles, the loop, blank frames, the composition of the frame) and the palette gate, and writes stills plus `stills/contact.png`. Read the contact sheet and the full-size stills; fix and repeat until it passes and looks right. Run it again with `--format 9:16` or `--format 16:9` for each other format you deliver (stills go to `stills/9x16/`). See [reference/review.md](reference/review.md).
6. **Render and verify.**
   ```bash
   node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" loopcheck videos/<film>   # hold loop: every diff must be 0
   node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" render videos/<film>      # MP4, GIF, poster
   node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" verify videos/<film>      # ffprobe facts, tags, decoded pixels
   node "${CLAUDE_SKILL_DIR}/scripts/render.mjs" mp4frames videos/<film>   # decoded review frames + PSNR
   ```
   Run the four once per delivered format, adding `--format 9:16` or `--format 16:9` (outputs `renders/<film>-9x16.mp4`, `preview-9x16.gif`, `poster-9x16.png`). Look at `stills/mp4/contact.png` and the full-size frames at each tap, transition and zoom. Report the files, their sizes and the verify, loopcheck and mp4frames lines. See [reference/render.md](reference/render.md) and [reference/loops.md](reference/loops.md).

## Pass criteria

- The screens match the user's screenshots in layout, colour and words, simplified only where BRIEF.md says so.
- Every UI text meant to be read is at least 24 px at 1080 at the camera's rest and has at least 4.5:1 against its own container (3:1 from 40 px); anything smaller is a bar.
- One thing happens at a time: the pointer arrives, lands, presses; the screen answers on the next 16th; a callout names it once it has landed.
- Callouts have at most 4 words, sit clear of the device (also while the camera zooms) and of each other, and their leaders end on the element they name while it is on screen.
- Every delivered format passes the critique, the composition row included, and its loopcheck is 0: a tall frame shows a bigger device with the words above it, a wide one the device beside them.
- Every colour is a palette role; fills that crossfade are one hue or a neutral; scrims, ripples, shadows and the finger are neutral or a tint of what they cover.
- Motion blur on every moving frame, one sample on still ones, never across a cut.
- The deliverable MP4 is H.264, yuv420p, BT.709-tagged in the stream, faststart, exactly DUR x FPS frames.

## Known pitfalls

- A pointer move lands about 0.31 s after it starts (MOVE): start it at least three 16ths before the tap. The critique warns when a tap comes first.
- A card that `expand`s into a screen should be that screen's top, scaled down (build both from one list of layers inside a scaled `group`); otherwise the card crossfades into the screen instead of growing into it.
- Content that scrolls runs under the status bar: add a `fixed` rect in the screen's colour behind the bar.
- Everything in a screen is clipped to the screen; the pointer, the callouts and the lockup are not.
- A device that enters and leaves off the canvas must wait where it leaves to, far enough out that its shadow (2.5 x blur + dy) is gone too; the `device seam` check fails otherwise.
- The finger, a ripple or a scrim over an element tints it; do not park the pointer on what the viewer must read. Lift it out between beats.
- A `set` (a pop) on something visible reads as a glitch. The engine sets only what is hidden (a screen before it enters, the lockup once it has left) or what a real UI swaps at once (a placeholder the moment typing starts).
- In a cycle loop every action must be undone before the end: pop what you push, close what you open, scroll back, toggle back, `clear` what you typed, `blur` the input. The critique's `loop closes` row names what is left.
