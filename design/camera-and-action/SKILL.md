---
name: camera-and-action
description: "Use when a web page must record itself to video. Camera & Action — the in-page recorder: makes any web page (canvas, WebGL, 2D, bitmap engine, or a device-size stage) record ITSELF into clean MP4/WebM video files — the page's own pixels, never the screen: no macOS pointer, no other app, no browser bar, none of the recorder's own controls. Covers the architecture to pick, the frame pipeline (captureStream + requestFrame + MediaRecorder), the recorder UI and its Settings (\"Camera & Action\"), takes (free, scripted/tour, series), crash recovery, the gates that prove it, the adversarial critic, batch recording to files (one at a time, verified with ffprobe, conformed to exact 60 fps without re-encoding), and every trap already paid. Use whenever the owner says camera&action, camera & action, camera and action, in-page recorder, record the page, record the screen without the pointer, recorder, record this page/episode/scene/tour, make videos of the HTML, or asks to add a record button / v…"
version: "1.0"
ported: 1.0.0
author: "the owner (ported from his Claude Code skills library)"
license: MIT
metadata:
  hermes:
    tags: [owner-library, video, recorder, canvas, WebGL, ffmpeg]
    related_skills: [videoediting]
---
> Ported from the owner's skills library (port 1.0.0, upstream version 1.0; the source hash and
> what it needs are in `manifest.json` next to this file). Paths written `{skill_dir}/…` are this skill's own
> folder, `{skills_root}/<name>/…` a sibling icloneOS skill, `{agent_home}/…` the agent's home. Runs on macos, linux only. Needs `node` on PATH, `ffmpeg` on PATH, `ffprobe` on PATH.
> In this copy a folder of the owner's machine is written `<your project folder>` (in code, the `PROJECT_DIR` environment variable); the owner's own folder and project names are written `sample project` (in the case and joiner they had); the rounds log is named without the folder it sat in on the owner's machine; the reference implementations are the owner's own projects and are not listed; the batch template reads its pages from `--from` or `PROJECT_DIR`.

# Camera & Action — a page that records itself

The owner's standard: **the video is exactly the scene, nothing else.** Not the screen, not the pointer, not the page's own buttons,
not another app — and provably so, measured by pixels. Every frame at the page's full resolution, at its true rate, in a file that
opens everywhere. Everything on screen and in code in **English**; replies to the owner in Portuguese; final reports short.

## 0. The method in twelve lines

1. **Never `getDisplayMedia` / screen capture.** The page already owns every pixel of the scene: record *those*.
2. A video frame is the scene's canvas **at the end of the frame, in the same task that drew it** (WebGL buffers do not survive the task).
3. Everything that is UI — the recorder's own controls included — must have **no code path** into that frame (§2: pick the architecture that makes it so).
4. Frame → an output canvas of the planned size → `captureStream(0)` + `track.requestFrame()` → `MediaRecorder` (MP4/H.264 `avc1` where the browser records it, else WebM VP9/VP8).
5. The video's rate is a **grid of slots** with one slot of credit: a 120 Hz display gives 60 fps, an uneven 60 Hz display loses none.
6. A page that draws nothing is **held** (the last frame re-sent every 0.5 s and at the stop); a hidden page **pauses** the take (`mr.pause()`), so the video never holds a frozen stretch.
7. Slices go to **IndexedDB** as they arrive (1 s; an MP4's at its keyframes): a crash or a navigation loses seconds at most — the next visit rebuilds a "Recovered" take.
8. UX: a small record control (button or menu-bar island), **Shift+R**, Esc held 0.7 s stops, optional countdown, a thumbnail when a take ends → preview with **Save… / Keep for later / Delete**, a Recordings list.
9. Settings section named exactly **"Camera & Action"**: Output · Content · Behaviour · Files · Recordings · Advanced (+ Page, Keys where the page had no settings) — every value typed or stepped, persisted, explained in one line.
10. **Count the frames that are IN THE FILE**, never the frames sent: an encoder that cannot keep up drops frames in silence.
11. **Prove it**: the page's canvas byte-identical with and without the recorder; the same instant recorded with all UI open and closed → identical video; content toggles; file; preview/save; hold; frame; keys; recovery; tour; pause; rate — then an **adversarial critic**.
12. Batch recording to files: **one take at a time** (the Mac's encoder keeps one 3024 × 1964 stream at 60 fps, not two), each file verified with ffprobe, conformed to an exact constant 60 fps **without re-encoding**.

## 1. Before writing code: read the page

Answer these from the code (do not ask the owner what the code can tell you):

| question | why it decides everything |
|---|---|
| What draws the scene? One WebGL canvas, one 2D canvas, a bitmap engine presented to a canvas, several canvases, or DOM? | picks the architecture (§2) |
| Where is the end of a frame — after the LAST pass (post-present passes, overlays drawn on the same canvas)? | the hook goes there; copying at "present" lost the Sample Project robots |
| Is the UI in the same canvas as the scene? | if yes, split the render (B) or move the UI to another canvas (C) |
| Is the page pure in time (`render(t)`, a scripted tour)? | enables tour takes, exact first/last frames, still-page proofs (`?still&t=`) |
| Does it already have Settings, a key map, storage keys, a build step, gates? | integrate into them; never invent a second settings system |
| Does the loop skip frames when idle (governor, "parked")? | the recorder must *hold*, not compose stale buffers |
| Who else uses its files (episodes sharing an engine, an index that opens pages)? | a shared engine module reaches every page — decide and say so |
| Is it embedded anywhere public (website showcase)? | ship that copy without the recorder (`?camera=off` / a build flag) |

Then **measure before building**: frame cost (profile `render`), canvas size at DPR 2, whether the build is reproducible (rebuild the
delivered files and compare bytes), and keep backups of every delivered file.

## 2. Choose the architecture (the heart of the method)

| | the page | how no UI pixel can reach the video | reference |
|---|---|---|---|
| **A** | WebGL scene canvas + DOM UI | copy the GL canvas in the engine's **end-of-frame hook** (same task); the few DOM overlays that belong in the film (captions, scale bar) are **redrawn from their own data** (canvases drawn in their rects, text via `Range.getClientRects`, CSS `box-shadow` redone with `shadowBlur`, cached); UI is DOM and never registered | Sample Project `web/app/record/` |
| **B** | ONE 2D canvas holding scene AND UI | split `render()` in two halves: **scene → `RECORD.scene(cv)` → UI**; content the take leaves out is drawn after the hook; hit-testing order unchanged | Sample Project `page/record.js` |
| **C** | a bitmap engine (e.g. 1-bit 480 × 312) presented to the page canvas | every recorder control lives on a **separate overlay canvas** (`#camui`, `pointer-events:none`, same size); the video frame is the page canvas **copied**, or the same bitmap **presented again** at the video's size (`present(t, …, target, again)`) — the scene laid out whole, never cropped or resampled | example series `sampleproject/mac/camera.js` |
| **D** | any page that must be recorded at a **device's** screen (iPhone, iPad) | a stage: the outer page hosts an `<iframe>` of the device's CSS size loading the same app with `?screen=<id>`; inside it the viewport, media queries and fixed elements are the device's and the recorder records there | Sample Project `record/screen.js` |
| **E** | DOM-only content (no canvas) | be honest: (1) move the scene into a canvas; or (2) Chrome **Element Capture** — `getDisplayMedia({ preferCurrentTab: true })` + `RestrictionTarget.fromElement()` + `track.restrictTo()` records one element subtree only (a permission prompt, Chrome only); or (3) for a page pure in `t`, film frame by frame through CDP screenshots of `?still&t=` and encode with ffmpeg | — |

Rules that hold in every architecture:
- The recorder's own UI is **never** drawn where the frame is taken from. If you catch yourself "hiding" UI before a capture, the architecture is wrong.
- The page's pointer, when the page draws one (a pixel cursor), is **content**: a setting (Always / Tour only / Never). A pointer left out of a take is
  **hidden AND moved off-screen** (−50, −50) — app code tests positions, not `hidden`, and hovered a card under the recorder's window (paid).
- Anything that must vanish only from the video (narrator, clock) is applied while recording, both on page and video (WYSIWYG), unless architecture A/B lets you draw it after the hook.

Details and code skeletons for A–E: `references/architectures.md`.

## 3. The frame pipeline (all architectures)

```
display frame → host draws (all passes) → host calls REC.scene(...) in the same task
  → slot grid: due? (no → mark dirty, count "over the rate")
  → shoot: drawImage(scene canvas → output canvas)  |  present(bitmap → output canvas at video size)
  → first frame only: start the encoder now (captureStream(0) + new MediaRecorder + start(timeslice))
  → track.requestFrame()   (pace "fixed": captureStream(fps) samples by itself)
tick() once per display frame (also on a paused/still page): countdown · Esc held · tour end · max length · retake a dirty frame · heartbeat resend
stop(): resend the held frame → mr.stop() → await slices → Blob → count frames IN THE FILE (MP4 trun) → thumbnail (a frame from inside the take) → IndexedDB → toast/preview/download
```

Non-negotiables (each one paid for):
- **Plan** (`plan()`): format (Auto = MP4 if `isTypeSupported('video/mp4;codecs=avc1')`), size (Screen = the canvas's own pixels; 720/1080/1440/2160 = short side), aspect (never a crop when the page can be laid out again), even numbers, **capped at 4096 × 2304** (H.264 level 5.1 refuses silently above), bitrate = preset × pixel ratio (Better ≈ 10 Mbps at 1080p60 → 28.6 at 3024 × 1964), `videoKeyFrameIntervalDuration` 2 s, timeslice 1 s.
- **Start the encoder inside the first frame** (after it is on the output canvas): the file's first frame is the scene, never black.
- **Slot grid**: `slot = floor((t − t0) · fps/1000 + .25)`; take when `slot − lastSlot ≥ 1`; after a gap of ≥ 2 slots keep one slot of credit. Identity for the gates: `frames + over-the-rate = presented`.
- **Held frames**: heartbeat `resend()` (one pixel drawn onto itself + `requestFrame`) every 500 ms; one more just before `stop()`.
- **Pause** (pill, Shift+P, page hidden): `mr.pause()`, stop the take's clock (`t0 += paused`), and pause a scripted tour with it; resume shifts both.
- **Truthful count**: after stop, read the MP4's fragments (`moof → traf → trun.sample_count`) = frames in the file; report "N frames in the file (M sent)"; a take under 90 % of its rate says which: "the encoder did not keep up" or "the page drew no faster".
- **Save** is called straight from the click (no `await` before `showSaveFilePicker`, or the gesture is lost); fallback `<a download>`.
- WebM from MediaRecorder has no duration: a seek to 1e7 makes the player find it.

Code (tested excerpts, ready to adapt): `templates/recorder-core.js` · `references/recorder-core.md`.

## 4. The recorder's UI and its Settings

- **Control**: a small round red button (top-left) or a menu-bar island `● Rec · Camera` — whatever is coherent with the page's own look. Recording = the control turns red and counts `■ 00:12`; a pause pill beside it.
- **Countdown** (Off / 3 / 5 s): one large digit on the page, never in the video. **Esc held 0.7 s** stops; a tapped Esc cancels a countdown or does the page's own Esc **on key-up** (so a held Esc never closes a window in the film).
- **Thumbnail** when a take ends (never over the open Settings window: it would cover its first rows and eat clicks) → **Preview** (the browser's own `<video controls>` placed over the window's well) with Delete · Keep for later · **Save…** (default; Enter saves, Esc keeps, Space plays).
- **Recordings** list: thumbnail (a frame from inside the take; a recovered take gets one read back from its video), name cut in its middle, facts whole, Open · Save… · × — **every delete asks twice**.
- **Notes**: one line under the control, wide enough for every static text (a note wider than its place is pushed to `window.__errors` so the gates fail); file names and error words are a tail cut to the room left.
- **Settings "Camera & Action"** (typed or stepped values, one-line descriptions, persisted in one versioned key, applied at once):
  Record (the take buttons, what the next file will be, the frame drawn to scale, *what is never in a video*) · Output (Format, Size, Aspect, Frame rate, Quality, Bit rate, Margin, Tiles) · Content (what the page may leave out: pointer, narrator, captions, clock 9:41…) · Behaviour (what Rec records, Shift+R / Shift+P / Shift+S re-bindable — plain keys refused, Countdown, Maximum length, Sound cue, When a take ends: Thumbnail / Preview / Download) · Files (pattern with tokens and a live example, Save…: Ask / Downloads, storage line) · Recordings · Advanced (Slice, Keyframe, Frame clock, Diagnostics, Reset — asks twice) · Page/Keys when the page had no settings of its own.
- Optional opacity rail for the Settings window (100 → 15 %) — the owner loved it in the Showcase.

Full schema with defaults and the exact one-line texts: `references/settings-ui.md`.

## 5. Takes

| take | what it does | where |
|---|---|---|
| **Free** | records what happens until stopped (the page's own interaction, or its animation) | Rec / Shift+R |
| **Tour / scripted** | for pages pure in `t`: restart at t = 0 (or after an intro), lock the page (mouse and keys can't take it over; the recorder shows the user's pointer hollow on its own canvas), stop by itself on the last frame; Page → Pause becomes the take's own pause | Record the tour |
| **Series** | chain pages: `ep01.html?rec=tour&chain=ep02.html,…&back=index.html` — each page records its own tour then opens the next; a take stopped by hand ends the series | Record the series (on an index) |
| **Autostart** | `?rec=tour|free` starts after load (no gesture needed for MediaRecorder); ignored on a `?still` page | address |

A still page (`?still`) never lets the mouse take it over and has no tour to record; a free take of it is how the gates prove "no UI".

## 6. Proof — gates, then the critic

Write a gate file (`tools/<x>-rec-gates.mjs`) with a CDP harness (headless Chrome, `tag`-ged profile) and page-side tools that grab
canvases, decode the take in a `<video>`, and measure pixels. The must-have gates (catalogue, thresholds and the reasons behind them:
`references/gates.md`; harness: `templates/gates-harness.mjs`):

1. **Scene untouched** — the page's canvas byte-identical to the page built *without* the recorder at a list of times, recorder idle and its window open.
2. **No UI in the video** — one take of a still page, the same instant with all UI closed and then open (window, typed field, hover): page canvas 0 px changed; video equal where the UI was (codec floor ≈ 1.3/255; threshold 2.5) and equal to the page canvas.
3. **Content** — what Content leaves out is out (diff confined to it), also on a **paused** page (redraw at begin/stop).
4. **File** — real click starts, real shortcut stops; MP4; decoded length = clock ± 10 %; frames in the file ≥ 97 % of sent; first frame = scene; it moves.
5. **Preview / Save / Delete** — thumbnail → preview → Save… (stub `showSaveFilePicker`) hands the right name and bytes; deletes ask twice.
6–21. Hold · frame/aspect (no ink outside the laid-out scene) · keys (re-bind, refuse plain keys, Esc held vs tapped with an app window open) · crash recovery (reload at 6.6 s) · countdown (red digit on the page, none in the video) · WebM · tour take (locked, its own pause, ends by itself, first/last frame) · pause · rate (30 fps on 60 Hz) · the two frame paths are one picture · settings kept and shared · series · `?camera=off` · small window · **cost** (display rate idle vs recording — valid only when both idle readings ≥ 58 Hz and within 3 %, load < 50) · nothing of the page hovers under the recorder's window.

Then the **adversarial critic** (owner's rule): a fresh agent, `model: opus`, with a brief file (template `references/critic-brief.md`)
— it builds its own copies, reruns the gates, writes its own probes for what the gates miss, looks at cropped pictures, and returns
`verdict_rN.json/.md` (approved, score /10, ≤ 3 tickets with cause + concrete fix + size). ≤ 3 rounds; a fresh critic when the old one's
context passes ~400 k; every verdict logged in `CAMERA_RONDAS.md` (or the project's rounds log). The example series went 7 → 8.5 → 9/10.

## 7. Recording pages into files (batch)

Pattern: `tools/record-series.mjs` (example series) — reuse it as the template (`references/batch-and-files.md`):
- one fresh headless Chrome per page at a laptop-sized screen: `1512 × 982 @2` → a **3024 × 1964** canvas; `--force-color-profile=srgb`;
- set the take (Screen size, 60 fps, quality, pattern `{page}`, clock 9:41), start a **tour take**, wait for it to end by itself;
- save through the recorder's own Save (`Page.setDownloadBehavior` → a folder), check bytes;
- **ffprobe the file**: size, frames, fps = frames / span, largest gap, gaps > 1.5 frames; re-take under 58 fps;
- **one at a time** — measured in the files: 1 at once 59.9 fps · 2 at once 56 · 3 → 50 · 6 → 35 (pages still sent 59);
- finish without re-encoding: `h264_mp4toannexb,h264_metadata=level=5.2` → raw `.h264` → `ffmpeg -r 60 -i x.h264 -c copy -movflags +faststart` = exact constant 60 fps, the right level, index at the front (`tools/conform-cfr.sh`); decode every file whole (`-fps_mode passthrough`, 0 errors) before copying;
- intermediates in scratch, never on the Desktop (iCloud's file provider indexes gigabytes and saturates the machine); `caffeinate -ims -w <pid>`;
- a short `READ ME.txt` with the table next to the files.

## 8. Delivery discipline

Backups of every delivered file (archive folder) · a delivery lock (`.no-deliver`; only `--deliver` copies) · the checked build saved
and the delivered files compared **byte for byte** · the owner's manual (`CAMERA_AND_ACTION.md`) next to the pages · the showcase/embed
copy without the recorder · memory + project docs updated in the same pass.

## 9. Traps already paid (the short list — all of them: `references/traps.md`)

- Copying a WebGL canvas outside the task that drew it (black/stale) · copying at "present" when passes come after it (lost the robots).
- Comparing against a *separate* reference take — measure two instants **inside one take**.
- Frames **sent** ≠ frames **in the file** (a bench said "8 at once keep 60"; the files had 35).
- `JSON.stringify(promise)` is `{}` — await in the page before stringifying.
- A raw CDP Escape stalls the headless display — dispatch `KeyboardEvent` on `document.body`.
- MP4 slices arrive at keyframes (2 s), WebM every slice — recovery needs a take longer than a keyframe or two.
- 4:2:0 chroma blurs 1-pixel tile grids: judge fidelity per area (≈ 1/255 at native size), not per pixel.
- Headless on a saturated machine (load > 50; it reached 900): Chrome does not start, rates are meaningless — wait, say "not measurable now".
- Never `pkill -f <pattern>` (other sessions share names) · a start timer in a shared launcher must be cleared when the thing starts (it killed every session's Chrome at 45 s for 55 min) · in zsh an unmatched glob aborts the whole `rm` — use `find … -delete` and look.
- MediaRecorder stamps frames with the clock's time (VFR jitter) and writes level 5.1 for a 5.2 stream — conform for editors.
- The Desktop gets reorganised: never hard-code its paths; find them (`find ${PROJECT_DIR:?} -maxdepth 6 -path '*<name>'`) and build with candidate lists that never create a stray folder.

## 10. Reference implementations (read them; copy what fits)

The reference implementations are the owner's own projects and do not ship with this copy: §2–§8 carry what they teach, and `templates/` holds the tested pieces.

## 11. How to run a Camera & Action job (checklist)

1. Read the page (§1), measure, back up, check the build is reproducible.
2. Pick A–E (§2); write the contract section in the project's docs first (what is in the video, what never is, the hooks).
3. Build the core (§3) with the host hooks; then the UI and Settings (§4); then takes (§5).
4. Prove (§6): gates green on the target pages (and a regression pass on everything sharing the engine), then the critic, ≤ 3 rounds.
5. Deliver (§8); record the owner's files if asked (§7); update memory, the project docs and THIS skill (§12).
6. Report to the owner in ≤ 10 lines: how to use it, what is never in a video, the measured proof, what was not measured.

## 12. Improving this skill

The owner will improve it over time "to work as I like". After every Camera & Action job: add the new trap to `references/traps.md`,
the new gate to `references/gates.md`, a line to the changelog below, and adjust §0–§11 if the method changed. Keep SKILL.md the
operational core; details go in `references/`.

**Changelog**
- 1.0 — first global version, distilled from Sample Project, Sample Project v9, the example series.
