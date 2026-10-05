---
name: easton-reel
description: >
  Turn a raw vertical talking-head clip into an "Easton" finance-bro / hustle
  style reel — kinetic ONE-WORD red-serif punch captions snapped to speech
  (big Times-bold, red glow, scale-in punch), cinematic crushed-black warm
  grade, 9:16 1080x1920, single ffmpeg pass with NVENC→libx264 fallback.
  Word timestamps via faster-whisper (local, $0). Optional yellow CapCut-style
  sub track for b-roll lines.
  Trigger when user says "easton reel", "/easton-reel", "finance bro reel",
  "red kinetic caption reel", "one-word punch captions", "make my talking-head
  clip look like easton/hamza/hustle reels", or drops a vertical talking-head
  .mp4 and wants big red one-word-at-a-time captions.
---

# easton-reel

Decoded from the "this is a message to all finance bros" (Easton) reel format.
Produces the signature look: **one word at a time, huge red Times-Bold, red
glow, punch-scaled to the beat of speech**, over a dim crushed-black warm grade.

## Genre anatomy (what makes it read as "Easton / finance-bro")

1. **War-room shot** — dim room, key-light face only, authority props behind
   (US map, Steve Jobs poster, monitors). Subject does the alpha finger-pinch.
2. **Red-serif kinetic caption** — ONE word per beat, Times/Trajan bold caps,
   red fill + red outer glow, punched (scale 78→100%) on the stressed syllable,
   upper-third. Hook + name-drop in this style.
3. **B-roll cutaways** — Rolex wrist, eye macro, prop gag (cup-noodles
   "I'm gambling"). Money-aesthetic vs broke-reality contrast = the joke.
4. **Clean white-cyc outro** — full body, yellow CapCut sans subs, CTA "tune in".
5. **Format** = hook → name-brand → story/joke → CTA. Trending audio low under VO.

The script does #2 and #3 (grade) automatically from a raw clip. #1/#4/#5 are
shooting/scripting choices — see "Shoot checklist" below.

## Pipeline (one command)

```
python easton_reel.py INPUT.mp4 [-o OUT.mp4] [options]
```

Steps: faster-whisper word timestamps → build `.ass` (one-word red-serif punch)
→ ffmpeg cover-crop 9:16 → grade → burn subs → encode.

### Options

- `--text "..."` **manual caption mode** — skips transcription, distributes the
  words one-per-beat evenly across the clip. Use for SILENT b-roll / timelapse
  (no audio to transcribe). `|` inserts a pause beat. Audio track auto-dropped
  when the source has none.
- `--model tiny|base|small|medium` whisper size. Default `small` (good CPU
  accuracy). Use `tiny`/`base` for speed, `medium` for noisy audio.
- `--size N` caption font px (default 110).
- `--style red` Easton red-serif glow (default). `--style yellow` =
  CapCut yellow-sans (use for b-roll / second pass).
- `--upper` force caption into top third (auto-on for red style).
- `--marginv N` vertical offset from top when `--upper` (default 430).
- `--no-grade` skip the cinematic colour grade (keep source look).
- `--keep` keep the generated `.ass` (hand-tweak then re-burn).

### Examples

```
# default Easton red punch caption + grade
python easton_reel.py "raw_talkinghead.mp4" --upper

# faster draft
python easton_reel.py raw.mp4 --model base

# b-roll line in yellow CapCut style, no grade
python easton_reel.py broll.mp4 --style yellow --no-grade
```

## House rules / gotchas (hard-won on this machine)

- **NVENC is broken here** — GPU driver exposes nvenc API 12.2 but ffmpeg 8
  needs 13.0 → `h264_nvenc` fails. Script auto-falls back to `libx264 -crf 20`.
  Don't "fix" the nvenc path; the fallback is the working path until the GPU
  driver is updated. (Matches the SkynetLabs video deploy gotcha: NVENC-broken
  → libx264.)
- **Events `Format:` line MUST list `Name`** — the V4+ Events column order is
  `Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text`.
  Omit `Name` and every Dialogue row (which carries the empty Name field
  `E,,0,0,0,,`) mis-parses — libass leaks a phantom **leading comma into the
  text** (`,YOU`). Symptom: clean `.ass` text but a red comma renders before
  every word. Fix = add `Name` to the Format line. Don't strip the comma in
  code — fix the header.
- **Force `-pix_fmt yuv420p`** — the filter chain (`eq`/`curves`/`subtitles`)
  promotes output to `yuv444p` (profile High 4:4:4), which Windows Media Player /
  Photos refuse with **0x80004005 "unsupported encoding settings"**. Both encode
  paths pin `-pix_fmt yuv420p` → profile High, universally playable. Don't ship
  without it.
- **Strip punctuation** — whisper emits `,BROS.`; build_ass strips leading/
  trailing `.,!?;:"()[]—-` so words render clean (`BROS`). Apostrophes kept
  (`I'M`, `EASTON'S`).
- **ASS colour is &HAABBGGRR** (alpha,blue,green,red) — red fill = `&H000000FF&`.
  Don't swap for RRGGBB.
- **Windows path escaping** — the `subtitles=` filter needs the drive colon
  escaped (`C\:/...`); handled in code. Don't pass a raw Windows path.
- Fonts used: **Times New Roman** (red) / **Arial** (yellow) — both ship with
  Windows. Swap to Cinzel/Trajan/Playfair in `STYLES` for a more "luxury" serif.
- Output is always **1080x1920** cover-crop (no letterbox). Feed vertical or
  near-vertical source; very wide source loses the sides.

## Tuning the look (edit `STYLES` / `build_ass` in easton_reel.py)

- Bigger glow → raise `blur` (red style, default 9) and `border` (4).
- Slower/snappier punch → change `\t(0,90,...)` ms and the `\fscx78` start scale.
- Hold each word longer/shorter → words hold from their start to the _next_
  word's start (always one on screen). For gap-punches instead, end at `b`.
- Two-track look (red hook + yellow b-roll): run twice — pass 1 `--style red`
  on the hook clip, pass 2 `--style yellow --no-grade` on the b-roll clip,
  then concat.

## Shoot checklist (to feed this skill the right raw clip)

- Phone vertical 1080×1920, 30fps. Lock exposure on face.
- Key light on face only; kill background light → crushed-black look the grade
  leans into.
- Authority backdrop (map / poster / monitors). Sit centred, mid-frame.
- Script: punchy hook in first ~1.5s, drop your NAME early (brand), payoff/joke,
  CTA "follow + tune in". Keep it <40s.
- Shoot b-roll separately (watch, eyes, prop gag) for cutaways.

## Verified

Tested 2026-06-09: (1) 6s speech trim — faster-whisper word timestamps OK.
(2) Full run on a silent DJI laptop timelapse (2688×1512 landscape, no audio)
via `--text` manual mode → cover-cropped 9:16, graded, red-serif glow punch
words snapped to beats, audio auto-dropped, nvenc→libx264 fallback. Output
clean after fixing the missing-`Name`-column comma bug. Functional, shipped a
real reel (`easton_laptop.mp4`).
