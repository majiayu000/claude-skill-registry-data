---
name: video-lens
description: "Local video analysis, nothing uploaded: scenes, keyframes, Korean OCR, on-device speech transcript, audio sync, and frame-accurate UI motion (duration, easing, stagger, CSS). 영상 분석, 영상 요약, 화면 글자, 애니메이션 타이밍, easing."
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/vl.py *), Bash(node ${CLAUDE_SKILL_DIR}/scripts/declared.mjs *)
---

# video-lens
You cannot watch video. This skill measures it and gives you text first, a few labeled
images second, exact frames last. Everything runs on this Mac.
`vl.py` below means `python3 ${CLAUDE_SKILL_DIR}/scripts/vl.py`.

## 1. Run once
`vl.py analyze VIDEO --out <scratchpad>/vl-<short-name> [flags]`
- No scratchpad: omit `--out`; the default folder is unique to the video. Never a shared path such as
  `/tmp/vl-clip`: other sessions may analyse other videos there. An `--out` that holds another video's
  analysis is refused (exit 2); pick another folder instead of deleting it.
- Motion question (timing, easing, stagger, "is this animation good"): `--mode motion`.
  Long recording: add `--start/--end` around the animation. Carousel, marquee or page scroll:
  add `--motion-mode scroll`. Retina screen recording and px values will go into CSS: `--dpr 2`
  (otherwise leave 1 and say so).
- Content question (summary, what or when something is shown or said): `--mode content`.
  English speech: `--lang en-US`.
- A question about what is shown or said is content, even on a short clip with speech. Omit `--mode` only
  when motion may matter too (auto: <= 120 s and quiet or silent is motion, > 120 s is content, else both;
  both on a short talk adds the motion stage and lists slide swaps as scene changes).
- Over 15 min of video: set the Bash timeout to 600000. A killed run resumes from cache;
  rerun the same command.
- A URL input is downloaded with yt-dlp (<=1080p) and analysed locally.
stdout is the report (<=6,000 chars). Read it before anything else. Its line `OUT = <path>`
is the folder every later command takes where it says OUT.

## 2. Read in this order and stop when answered
report (stdout) > timeline.md or `vl.py text` > overview.jpg (+ overview_motion.jpg in mode both) > sheets (motion/Mxx_sheet.png,
sheets/kf_NN.jpg, `vl.py zoom`) > single frames (`vl.py frame`).
Every view line in the report shows its token cost (`≈` = estimated before the zoom is written). A table cut
to fit ends in `+N rows: vl.py rows OUT --kind K --from N`; run it only if you need those rows.

## 3. Content
- Summary of the whole video: Read timeline.md in full.
- "When is X said or shown": `vl.py text OUT --grep "X"` instead of reading everything. Lines read
  `start-end KIND text`: TEXT is on screen from start until end, SAY is spoken from start to end.
- "What is on screen at T": `vl.py text OUT --from T --to T+1 --kind ocr` (PERSISTENT lines are logos,
  watermarks or a title held through most of the video).
- Visual question: Read overview.jpg, then only the kf sheets for the time range (the report
  lists each sheet's span). Keyframes marked `same as` are repeats; skip them.
- Before quoting an OCR line with conf < 0.6, or any number or name that matters, look at
  that frame: `vl.py frame OUT --t T --roi x,y,w,h`.
- Cite times as mm:ss. Say what was measured (times, OCR, transcript) and what is your inference.

### Scene digest (only on request)
Run it only when the user asks for captures or a scene-by-scene summary ("장면별로 캡처해서 정리해줘"), never by
default. It needs a content (or both) analysis in OUT.
1. `vl.py digest OUT [--scenes N]`: scenes are the chapters of a URL that has them (or of a file downloaded with
   `yt-dlp --write-info-json`), else screen states merged at cuts to N (default 6 + 2 per 10 min, at most 30). It writes
   one frame per scene (the screen state shown longest in it) and numbered sheets, and prints per scene the time,
   chapter, on-screen headline and first sentence, plus each sheet's token cost. Menu bars, clocks and watermarks are
   left out of the scene text.
2. Read the sheets (a single frame only when its cell is unclear). Write `OUT/digest/captions.json` as
   `{"S01": "...", ...}`: 1-2 plain lines per scene in the user's language, from what you see and the scene's text and
   speech (all in `OUT/digest/digest.json`). Do not invent what neither shows.
3. `vl.py digest OUT --captions OUT/digest/captions.json` writes `digest.md` and a self-contained `digest.html`. A
   missing or unknown scene id is refused (exit 2): fix the captions and rerun. A rebuild whose scenes moved sets the
   old captions aside as `captions.stale.json`: write them again for the new scenes.
Tell the user where both files are, and copy them where the user asks (`digest.md` needs `frames/` beside it).

## 4. Motion: measure first, look second
1. Read the element table. Noise and micro events are only counted; ignore them unless asked.
   0 motion events but the user saw motion: rerun with `--roi x,y,w,h` or `--pix-threshold 5`.
   Events on the `Scene changes` line (mode both) are slide swaps or cuts, not UI motion. `instant (<= 2
   frames)` in the easing column means the change took at most 2 frames: no easing or duration to quote.
   A `Repeats` line summarises one transition repeated (loop, carousel): one curve and duration fitted across the
   repeats, each with its own start; quote those and the starts. The table keeps one row for it plus the outliers
   (repeats the shared fit clearly misses, with their own fits).
2. Read one sheet per event you report (motion/Mxx_sheet.png, ~900 to 1,600 tokens); an event without a
   sheet (only the largest get one): `vl.py zoom OUT --event Mxx`; for a `Repeats` group read one sheet.
   Check in order:
   a) boxes sit on whole UI elements (not half a card, not two cards); if wrong, rerun with `--roi`
      (a Scroll line means one box over the scrolling area; that is expected);
   b) timing-map colours run in the order of the reported delays;
   c) dots lie on the fitted lines; a systematic miss means the wrong model: read `types` and notes;
   d) name WHAT moved from the filmstrip. That is your job; the numbers are not.
3. Never re-estimate a time, duration or easing from images. Quote the numbers with their bounds:
   "400 ms (range 393-427), cubic-bezier(0.2,0,0,1) = md3-standard, RMSE 0.004, ±1 frame = 16.7 ms".
   `name ~ other` in the easing column means a near tie: say the curve cannot be told apart from it. The note "X
   fits almost as well ... the ranges hold its reading" means the recording cannot separate the custom curve from X
   (a small element, codec damage beside a neighbour): quote both, with the ranges.
   `cubic-bezier(...) ~ a, b, c` with the note "named curves tie" means the recording cannot name the curve (named
   curves of different shapes fit equally well): quote the bezier and name a, b, c as equally likely.
   The `Curves:` line under the table gives each named curve's bezier.
   Note `start uncertain`: quote the start range and t50, not one start. A custom curve's start and
   duration trade against its flat start and flat end, so give their ranges.
   Scroll/carousel travel comes with its share of unreliable steps; say so when it is above 10 %.
4. confidence low: `vl.py zoom OUT --event Mxx`, Read the grid it marks `Read this` (the crops are
   optional), and say what is uncertain. Note "entered from beyond the ... edge" (or "left past"): the element
   slid across the frame edge or a clipping container; it is read as a pure slide timed from the part that
   stays visible, its start (end) assumed just beyond that edge, and `(at least)` marks its travel as the least
   the hidden frames allow; quote it with that assumption. A `fade` row whose box is the whole crop, note "backdrop
   (scrim)": the page behind a sheet or dialog dimmed (or cleared) under an overlay; quote its timing as the overlay's
   opacity, beside the sheet's own row. Note "grew from nothing": the element was missing from one
   rest frame and opaque whenever seen, so it scaled from (to) 0; quote scale(0) as assumed, not seen. When the note
   says it started (ended) with a strip of it still inside that edge (a box-shadow's fringe), that state was seen: the
   travel is measured, not assumed. `?`
   before the easing, or the note "start state not observed" or "farther out", means the start state was not seen:
   the easing is unknown, say so and use declared.mjs when the page URL is available. Note "already running at the
   first frame" or "still running at the last frame": the range cut the motion; rerun with a wider `--start/--end`.
5. Answer with: one row per element (delay, duration ± range, easing name + bezier, travel in CSS px,
   types, stalls); its channels (translate, fade, ...) share that one timing and curve, so list them as
   properties of the row, never as separate animations. Only rows named `Mxx.n channel` (the channels split: the
   first row says why) get a timing per channel. Then the stagger step, the CSS snippet (motion/css.txt; printed
   in the report when short), then your critique. Label numbers measured, fitted or suggested.
6. Page URL available and Chrome installed:
   `node ${CLAUDE_SKILL_DIR}/scripts/declared.mjs URL --out <scratchpad>/decl`
   (`--trigger "hover SELECTOR"` for hover or click transitions, `--render FPS SECONDS` for a clip).
   It prints one line per animation (target, properties, delay, duration, curve) and the path of
   `declared.json`, which holds every field (`keyframe_easings` is a CSS animation's curve). With `--render`,
   `vl.py analyze <scratchpad>/decl/render.mp4 --mode motion` measures the rendered clip for comparison.
   Declared values win for CSS; measured values show what the user actually sees (stalls,
   JS or canvas motion). State both when they differ by more than one frame.

## 5. Budget and tools
- Start with the report + at most 3 images + at most 6 frames; ask before going far beyond.
- Do not extract frames with ffmpeg by hand or Read frame folders. If the tool fails, quote its
  one-line error.
- Do not Read analysis.json whole; use `vl.py rows` or `vl.py text`.

## 6. Privacy
All processing is local (ffmpeg, OpenCV, macOS Vision, macOS on-device speech, whisper.cpp).
Keep the user's media on the Mac: do not hand it to another tool or service that uploads it.
Speech order with `--asr auto`: subtitle stream > sidecar .srt/.vtt >
Apple SpeechTranscriber (on device) > whisper.cpp large-v3-turbo (installed locally) > none.
If the report says no transcript, rerun with `--asr whisper`; never upload audio instead.

## 7. Accuracy you can quote
Quote the bounds the report prints (ranges, near ties, notes); they already carry the uncertainty, so do not
re-verify a reading the report marks high confidence. Summary of `vl.py selftest` on synthetic CFR and VFR clips:
- Motion, named curves at 60 fps: start within 1 ms, duration within 3.5 %, stagger step within 1.1 ms, travel within
  1 px. Custom curves: t50 within 2.3 ms, the truth inside the reported start and duration ranges. 30 fps: one frame.
- Edge slides, long-tail drawers, overshoot pops, repeats: start within 1 ms, duration within 0.6 %. Pops over
  other content: duration -3.7 to +4.2 %. Closing drawers and dimming backdrops can read short: quote their ranges.
- Cuts within one frame; Korean slide OCR exact at >= 16 px glyphs; speech CER 2.4 % (whisper) to 3.7 % (Apple) on
  clean TTS; audio onsets within 2 ms; sync within 2 ms of the truth.
Per-case bounds and review-fixture numbers: reference/accuracy.md (read only when a case is not covered above).

## 8. Limits
Flat-ish backgrounds segment best; photo or gradient backgrounds fall back to one box with low
confidence (use --roi). 3D/perspective shows only as a shear flag; 3D carousels read as scroll
with approximate travel. Lists without row backgrounds give one element per part of a row (avatar, text, badge,
separator); the Stagger line still steps between rows. 1 to 2 px separators that fade in are tracked only once visible:
they can split and read their travel up to 45 % off; take a row's timing from its other parts. Two elements that touch
only through static content (a chip sliding beside a badge that pops, both over one text line) read as one box with
split channels: `--roi` around each. No speaker labels, no
tempo, no language auto-detect. 30 fps recordings halve timing resolution; ask for 60 fps. Real noisy or
multi-speaker Korean speech is unmeasured.
Field meanings, thresholds and failure modes: reference/fields.md.
