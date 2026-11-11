---
name: edit-style
description: "Turn a raw talking-head take into a dynamically edited 1080x1920 reel: full-face, full-graphic and split layouts that switch every 2 to 5 seconds, real UI and official-logo panels, captions on every word timed by Whisper, voice plus synthesised SFX (no music bed) mastered to -14 LUFS, and hard QA gates (caption sync on the final render, A/V length, loudness, colour, framing, contact sheet, claims). Also covers writing the script so it does not read as AI. Use when asked to 'edit this reel', 'make it look edited', 'add captions / dynamic layout / graphics', or 'write a reel script'."
author: Johann (@johannships)
version: 1.4.0
---

# Edit style: dynamic vertical reels from a raw take

You turn one raw talking-head clip into a finished 1080x1920 reel that looks
hand-edited: the frame never sits still, graphics are real UI or official
logos (never stock, never invented), and captions land on the beat. Nothing is
dragged on a timeline. Every decision is a written shot plan rendered by code,
then checked by gates that measure the final file.

Part of a pipeline: `reel-ideation` (ideas, scripts, record sheet) ->
`footage-ingest` ("the card is in": copy, sort, pick takes, conform) ->
**edit-style** (short-form edit) or `longform-edit` (YouTube long-form) ->
`reel-captions` (post text) -> `trial-post` (trial reels) -> `reel-scorecard` (72 h read).

## Requirements

Claude Code on a computer (not Claude.ai: it needs a shell and ffmpeg).

| need | for | install |
|---|---|---|
| ffmpeg + ffprobe (with `ebur128`) | every cut, composite, gate | `brew install ffmpeg` / `apt install ffmpeg` |
| Python 3.9+ and Pillow | captions, cue alignment | `pip install pillow` |
| a local Whisper | word timestamps | see the `use-local-whisper` skill |
| OpenCV (optional) | framing gate, crop solver, face-first gate | `pip install opencv-python-headless` + YuNet model (see `tools/face_box.py`) |
| Node + Playwright (optional) | headless screen capture | `npm i playwright && npx playwright install chromium` |
| Remotion (optional) | animated graphic panels | `npx create-video@latest`; a full panel studio is in github.com/johannships/reels-engine |
| swiftc, macOS only (optional) | iPhone HDR to SDR | `xcode-select --install` |

Install check: `sh tools/check_setup.sh` (exit 0 = ready).

## Inputs

- `raw.mov` (or mp4): one take, phone or camera, any orientation.
- `script.txt`: what was said, spelled the way it must appear on screen. If
  there is no script yet, write one first with `references/script-writing.md`.
- Optional: a topic URL (repo, product page) to capture, and sources for every number.
- From `footage-ingest`: a SHIP line (hook clip > body clips > IG ending / bio ending). Clips recorded one line
  per clip are joined in step 2; each join is a place dead air hides.

## Pipeline (one folder per reel: every file for this reel lives inside it)

`transcribe.py` below is `use-local-whisper/scripts/transcribe.py`. Parallel
edits never share a work folder: one reel, one folder.

0. **Conform camera footage first** (`footage-ingest/scripts/conform.py`): constant 30 fps, TV range, and the
   mirror if the creator wants selfie view. The mirror goes on the raw camera clip only, BEFORE captions, logos,
   cards or screen captures are composited; those are never mirrored. Check the mirrored frame for backwards text.
1. **Check the source.** `ffprobe -v error -select_streams v:0 -show_entries stream=color_range,color_transfer,r_frame_rate -of csv=p=0 raw.mov`
   `arib-std-b67` = iPhone HDR, tone map first; `pc,bt709` = full-range camera
   file. Exact handling: `references/source-footage.md`.
2. **Cut retakes, then pauses.** Transcribe raw (`transcribe.py raw.mov`),
   keep the LAST take of any repeated line, never cut mid-word. Then
   `python3 tools/tighten.py cut.mp4 tight.mp4` (-50 dB, never -38 dB).
   Joining one-line clips: set each in and out point within 0.08 s of the first and last word (refine the edge
   on the audio RMS, not on Whisper), look at the first and last 0.5 s of every clip (no reaching for the
   camera, no settling in), and write the join times of the final timeline to `joins.json`.
3. **Transcribe the tightened take**: `transcribe.py tight.mp4` gives `tight.words.json`.
4. **Write the shot plan** (`shots.json`): one row per shot,
   `{layout, anchor_phrase, content}`. `anchor_phrase` is script text matched
   against `words.json` so the shot starts when those words are said. Never
   hand-type timestamps. Layout rules: `references/edit-craft.md`.
5. **Capture and fetch assets.** Screens: `node tools/capture_clock.js <url> shots/s3 6`
   (headless, frame-exact). Logos: the brand's official press page or site
   SVG only. Open every asset and look at it before use.
6. **Frame the face per take**: `python3 tools/face_box.py tight.mp4 --model yunet.onnx --solve full`
   (and `--solve pip`). Never reuse crops from another take.
7. **Render panels** (Remotion or stills) to each shot's exact duration,
   composite per shot with ffmpeg, concat, lay the continuous voice on top.
   Run renders under `nice -n 15`. Look-dev on stills, then one full render.
8. **Mix and master** (`references/edit-craft.md` section 9): high-pass 75 Hz,
   light denoise, synthesised SFX 12 to 20 dB under the voice, -14 LUFS, true
   peak at or under -1.5 dBTP.
9. **Captions, timed on the FINAL audio**: `transcribe.py final_nocaps.mp4`, then
   `python3 tools/make_cues.py script.txt final_nocaps.words.json --fix fix.json`, then
   `python3 tools/burn_captions.py final_nocaps.mp4 cues.json final.mp4 --caps`.
   Text comes from the script, timing from Whisper. `--y 0.38` on PIP shots.
10. **Gates** (below). Fix and re-run until all pass.

## Layouts

| layout | what | when |
|---|---|---|
| FULL | face fills the frame (head-top 13%, chin 85%) | hook, personal beats, close |
| GFX | full-screen real UI, stat or claim card, no face | each key beat, the CTA |
| PIP | graphic on top, face in a rounded card at the bottom (y 1086, 1080x834, radius 48) | naming a tool while still talking |

Switch every 2 to 5 s. **Open on the face from frame 1** (FULL or PIP): never
a graphic, title card, screen recording or logo-only opener; openers without a
face test badly. Break to GFX on each key beat, land the CTA on GFX, close on
FULL. If the topic is a named brand, show its official logo in the first 2 s
as a clean panel beside or over the face, never instead of it.

## Two endings per keyword reel

Comment-keyword DM automations usually work on Instagram only, so a "comment
KEYWORD" ending wastes TikTok, YouTube and Facebook traffic. Export two files:

- `final.mp4`: Instagram, ends on the recorded "comment KEYWORD" clip.
- `final-bio.mp4`: everywhere else, ends on a recorded "check the link in my bio" clip.

Make the swap invisible: hide the join under a full-screen GFX card, use one
continuous bio clip (no micro-cuts), match scale, colour and loudness, 60 to
100 ms audio crossfade, and frame-check the join. Both files go through every gate.

## QA gates (all must pass; write results to QA.md)

| # | gate | tool | pass |
|---|---|---|---|
| 1 | framing | `face_box.py final.mp4` | head-top > 3%, chin < 94% on every sample |
| 2 | caption sync per chapter, on the final render | re-transcribe final, `caption_sync_gate.py captions.json final.words.json chapters.json` | median <= 0.12 s, p95 <= 0.25 s |
| 3 | A/V length | `final_gates.sh final.mp4` | within one frame |
| 4 | loudness | `final_gates.sh` | -14 +/- 1 LUFS, true peak <= -1.5 dBTP |
| 5 | colour/encode | `final_gates.sh` | yuv420p, tv range, BT.709 tags, >= 8 Mbps |
| 6 | skin luma vs source | `skin_luma_check.sh` | within 2 levels |
| 7 | first word survives | re-transcribe first 2 s | first script word present |
| 8 | contact sheet | `final_gates.sh` writes `contact.png` | you OPENED it: no pills or stickers, no caption over the mouth, logos correct, nothing private, every label inside the 4:5 crop (y 285 to 1635) |
| 9 | claims | manual | every on-screen number has a named source checked live today; false spoken lines are cut and listed |
| 10 | face first | `reel_qa.py final.mp4 --yunet yunet.onnx` | a face (box >= 15% of frame height) in at least half the frames of the first 0.3 s |
| 11 | dead air | `reel_qa.py final.mp4 --words final.words.json --joins joins.json` | no word gap > 0.25 s at a join, > 0.35 s anywhere (re-whisper of the FINAL) |
| 12 | join envelope | `reel_qa.py` (same run) | no quiet run (< -36 dBFS) > 0.25 s within 0.5 s of a join, > 0.35 s inside speech. Catches room-tone holes Whisper hides |
| 13 | dashes | `reel_qa.py --cues cues.json` | no em dash or spaced en dash in any caption |

Run gates 10 to 13 on `final.mp4` AND `final-bio.mp4`, each with its own joins file.

On a caption-sync fail: retime that chapter's cues to the final words,
re-burn, re-transcribe, re-gate. Loop until every chapter passes.

## Output

```
reel-folder/
  final.mp4        1080x1920, H.264 BT.709, AAC 48 kHz, -14 LUFS (Instagram ending)
  final-bio.mp4    same edit with the "link in my bio" ending (every other platform)
  joins.json       join times per file (joins-bio.json for final-bio.mp4)
  captions.srt     from the re-transcription of final.mp4, names spelled right
  contact.png      12-frame sheet you looked at
  QA.md            one line per gate, plus CLAIMS and any cuts of private detail
  LOG.md           written as you go
```

Example QA.md:

```
framing      12/12 PASS (head-top min 6.1%, chin max 88.4%)
face first   9/9 frames PASS   dead air max 0.21 s at joins PASS   join envelope PASS   dashes PASS
caption sync hook median 0.04 p95 0.11 PASS | body 0.05/0.14 PASS | cta 0.03/0.09 PASS
A/V          diff 0.012s PASS     loudness -14.1 LUFS, -1.8 dBTP PASS
colour       yuv420p tv bt709 13.9 Mbps PASS   skin luma diff 1.2 PASS
contact      looked: no pills, captions clear of mouth, logos official, 4:5 safe
CLAIMS       "40,000 stars": GitHub API 14:05 today = 41,212 (shown as 41K)
```

## Failure handling

- No Whisper: stop and install one (`use-local-whisper`). Never guess timings.
- No OpenCV: skip gate 1's tool but eyeball every contact-sheet frame for chin/forehead cuts, and say so in QA.md.
- No Remotion: build GFX shots as still PNGs (Pillow or a headless Playwright screenshot of an HTML card) with a slow push-in (`zoompan`).
- `make_cues.py` exits 2 (script and audio differ): fix the script to match what was said. Never burn captions that disagree with the voice.
- A gate fails three loops in a row: stop, report the numbers, ask.

## Rules that keep it from looking like AI

- No floating pills, badges, corner tags, stickers or REC chips. Ever.
- No code-generated motion-graphics sizzle. Real footage and real product screens.
- One accent colour. One caption style per shot type.
- Show, don't narrate: when the voice names a thing, that thing is on screen.
- Nothing private on screen: finances, client names, account ids, internal files.
- No sponsor text, "paid partnership" label or disclosure card burned into the video: disclosure goes in the
  post caption and the platform's paid-partnership toggle.
- No "AI clone" or "digital twin" label burned in on avatar shots: use the platform's AI-content toggle.
- No em or en dashes in scripts or captions.

Depth: `references/script-writing.md` (hooks, register, numbers),
`references/source-footage.md` (HDR, full-range cameras, clone takes, silence),
`references/edit-craft.md` (captions, screens, framing, gestures, audio, pitfalls).
