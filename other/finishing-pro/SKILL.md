---
name: finishing-pro
description: "Finishing editor for Claude: takes any locked Video Studio edit (or any finished video with a plan) through the finishing department: colour correction and shot matching, a creative look with protected skin, dialogue clean-up, music and SFX mix to the delivery loudness, legal levels, then platform encodes, captions, chapters, thumbnails and an automated QC report. Use when the user says 'finish this edit', 'grade and mix it', 'make it broadcast-ready', 'final polish', 'fix the colour and sound', 'loudness for YouTube / podcast / broadcast', 'QC my video', 'online and deliver'. Runs on video-studio-core (color.py, finish.py, audio_chain.py, deliver.py, qc.py)."
license: MIT
---

# Finishing Pro

Picture is locked; now make it look right, sound right, measure right and arrive in every format, with a QC report to prove it.

- **Works on:** any work folder with `plan.json` (from any genre or style skill) after `render.py`, or a finished video
- **Makes:** graded + mixed `final.mp4`, platform encodes, `captions.*`, `chapters.txt`, thumbnails, `deliver_report.md`, `qc_report`
- **Order (never change it):** lock, correct, match, look, texture, mix, loudness, legalise, encode, QC

## Before you start

- Needs **video-studio-core** in the same skills folder (`CORE`). First run: `python CORE/scripts/check_env.py`.
- Confirm **picture lock** with the user. Any timing change after finishing means redoing captions, mix and QC.
- Ask the delivery targets up front (platforms, broadcaster spec, LMS, cinema) because loudness differs:
  web -14 LUFS / -1 dBTP, podcast -16, EBU R128 -23, ATSC A/85 -24 LKFS / -2 dBTP.
- Never grade a vertical cut and the 16:9 master differently; finish one master and derive the rest.

## 1. Colour (on the camera footage only; graphics keep their colours)

```bash
python CORE/scripts/color.py analyze W/source.mp4 --work W            # W/color.json: cast, levels, skin, likely_log
python CORE/scripts/color.py scopes W/source.mp4 --t 3 --out W/scopes.png
python CORE/scripts/color.py looks-sheet W/source.mp4 --t 3 --correct --out W/looks.png
python CORE/scripts/color.py preview W/source.mp4 --look portra --intensity 0.6 --correct --t 3 --out W/look_portra.png
```

Open the PNGs with the Read tool. Then set the plan:

```json
"color": {"auto": true, "wb_strength": 0.85, "look": "portra", "intensity": 0.6},
"finish": {"grain": 4, "vignette": 0.3, "legal": "strict"}
```

- **Correct first, look second.** `auto` fixes white balance, levels and saturation; add `exposure`/`contrast` only if the
  scopes say so. Log footage: `"log": "slog3"` etc. only when you know the camera; prefer the official `"lut"`.
- **Match cameras:** export a hero still and set `"match": "hero.png"` (Reinhard Lab match, after correction).
- **Look by genre:** corporate/interviews 0.4-0.6 (`cool-corporate`, `documentary-natural`, `portra`); social/brand
  0.7-0.85 (`clean-commercial`, `teal-orange-pro`, `kodak-2383`); weddings `wedding-pastel`, `indian-wedding`; food
  `food-pop`; property `real-estate-bright`; music videos up to 1.0. Faces on screen: use a skin-protected look.
- Texture belongs in `finish` (grain, halation, letterbox `2.39`), and the legal limiter is always last (`"legal": "strict"`).

## 2. Sound

```json
"audio": {"platform": "youtube", "voice": {"denoise": "light", "eq": "clear", "deess": true, "voice": "female"}},
"roomTone": true,
"music": {"src": "bed.wav", "under": 20, "duck": "speech-aware", "fitTo": "beats", "endButton": true},
"sfx": [{"t": 4.6, "kind": "whoosh", "gain": 0.5}]
```

- Dialogue chain order is fixed (HPF, de-hum, de-click, de-noise, EQ, de-ess, gate, compressor, limiter). Too much
  `denoise` sounds underwater: A/B with `python CORE/scripts/audio_chain.py voice in.wav out.wav --cfg '{"denoise":"light"}'`.
- `roomTone: true` fills autocut joins with matched room tone (needs `W/cutlist.json`).
- Music under dialogue: `under` 18-24 LU; music-led edits (montage, wedding, travel): `"voice": false` so the song is not
  run through the dialogue chain.
- One sound per idea; most of the video dry. Lists: `python CORE/scripts/audio_chain.py list-sfx`.
- **The plan's `audio.platform` wins over `finish.py --platform`.** Set the loudness target in one place.

## 3. Render the finish

```bash
python CORE/scripts/render.py W/plan.json --frames 1,4,8,12          # look at W/contact_sheet.png
python CORE/scripts/render.py W/plan.json
python CORE/scripts/finish.py W/plan.json --platform youtube
python CORE/scripts/audio_chain.py measure W/final.mp4 --platform youtube
python CORE/scripts/color.py qc W/final.mp4
```

Contact sheets (`render.py --frames`) show `cutaways` and `blurs`; to check the finished texture and grade, grab a frame
of `final.mp4` (`ffmpeg -ss 8 -i W/final.mp4 -frames:v 1 W/check_8s.png`, then Read it). For another target than the plan's, use
`finish.py --lufs -23` or set `audio.lufs`.

## 4. Deliver

```bash
python CORE/scripts/deliver.py --list
python CORE/scripts/deliver.py W/plan.json --to youtube,reels,tiktok,prores-422hq,audio-wav --out-dir W/deliver
python CORE/scripts/deliver.py W/plan.json --to broadcast-xdcam --out-dir W/deliver_tv --burn no
```

- Web presets re-normalise loudness per platform (two-pass, true-peak limited); ProRes, DNxHR and WAV keep the mix untouched.
- Vertical presets from a 16:9 master use a face-centred crop if `W/track.json` exists (`python CORE/scripts/track.py analyze W/cut.mp4 --work W`),
  else a centre crop or blurred fill. For a real vertical edit re-render the plan at 9:16.
- `--burn auto` burns captions only on muted-autoplay feeds and only if the plan has no captions element; YouTube gets sidecars.
- Chapters: `--chapters "0:00 Intro; 1:20 Setup"` or plan `chapters`; YouTube needs >= 3, first at 0:00, each >= 10 s.
- Thumbnails: Read `thumb_*.png` before handing over; headline from `--headline` or the first sentence.
- `broadcast-xdcam` is "XDCAM-like" (not AS-11 checked), SCC captions are not produced, HDR is not produced: say so.

## 5. QC

```bash
python CORE/scripts/qc.py W/deliver/final_youtube.mp4 --plan W/plan.json --platform youtube --out-dir W/qc --strict
python CORE/scripts/qc.py W/deliver/final_reels.mp4 --plan W/plan.json --platform reels --out-dir W/qc_reels --strict
```

> Tested: `qc.py --plan` compares a **reframed** output (e.g. 9:16 from a 16:9 plan) with the plan's own frame and
> overlay positions, so it reports false FAILs (`resolution_vs_plan`, `safe_zone_vertical`, `max_overlays_at_once`).
> For files whose aspect differs from the plan, run `qc.py FILE --platform NAME` without `--plan`, and check overlays on a still.

Read the Markdown report. FAIL = fix and re-run; WARN = look, decide, and write down the decision. Then do one full
watch-down with headphones: lip-sync at start/middle/end, clicks at joins, music ending, captions vs. audio.

## Check before delivering

- Skin on the skin line (vectorscope in `scopes.png`), whites neutral, no clipped faces, cameras matched.
- Loudness within ±1 LU of target, true peak at or under the ceiling, no clipping, no digital-silence holes.
- No black or flash frames, < 3 flashes per second, legal levels (BRNG < 1%), BT.709 tags.
- Text in safe zones per platform; captions <= 42 chars x 2 lines, <= 20 cps; names and numbers checked.
- File names `client_project_v003_16x9.mp4`; hand over files + `deliver_report.md` + QC reports, and list what you decided on each WARN.

## Example requests

- "The cut is locked. Grade it, mix it to YouTube loudness and give me every social version."
- "My two cameras don't match and the voice is muddy, finish it properly."
- "QC this video for broadcast and tell me what fails."
