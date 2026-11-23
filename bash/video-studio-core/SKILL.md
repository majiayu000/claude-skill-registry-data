---
name: video-studio-core
description: Shared engine and editor brain for the Video Studio skills. Transcribes and cuts raw footage like a professional editor (smart pause/filler/retake cuts, J/L cuts), assembles multi-clip timelines with real transitions and speed ramps, reframes to any aspect ratio by following faces, grades colour on the footage (auto correction, log to Rec.709, 50+ looks), renders motion-graphics overlays frame by frame, mixes sound to platform loudness, then delivers platform exports with subtitles, chapters, thumbnails and QC. Use it directly for a plain professional edit, or through any Video Studio genre skill (wedding-highlight, podcast-episode, retention-reel...) or style skin (halo-cut, depth-type...).
license: MIT
---

# Video Studio Core (v2)

The engine and the editor's judgement every Video Studio skill runs on. Raw footage in, finished and delivered edit out, all on the user's own computer, free.

**Genre skills** decide *how it is cut* (structure, pacing, transitions, sound, deliverables). **Style skills** are *skins* (the look of captions and graphics). Run any genre with any skin.

## Setup (once)

```bash
pip install faster-whisper playwright numpy pillow opencv-python mediapipe
python -m playwright install chromium
# plus FFmpeg (full build) on PATH: brew install ffmpeg | winget install ffmpeg | sudo apt install ffmpeg
python scripts/check_env.py      # prints exact fixes; also lists optional add-ons (kokoro voice-over, demucs stems...)
```

## Paths

- `CORE` = this skill's folder (`scripts/`, `runtime/`, `references/`, `luts/`).
- `SKIN` = a style skill folder next to it (holds `theme.json` + `theme.css`), e.g. `~/.claude/skills/halo-cut`.
- Each job gets its own work folder next to the user's footage (`./edit-name/`). Never write inside skill folders.

## The pipeline

```bash
# one clip, cut like an editor, stop at the plan so you can refine it
python CORE/scripts/run.py clip.mp4 --style SKIN --genre reel-talking-head --smart-cuts --retakes --work edit-x --stop-after plan
python CORE/scripts/editor.py review edit-x/plan.json --genre reel-talking-head --fix   # the editor's review + safe fixes
python CORE/scripts/render.py edit-x/plan.json --frames 1,4,8,12                      # contact sheet: LOOK at it
python CORE/scripts/render.py edit-x/plan.json                                         # overlays + composite (+ colour on footage)
python CORE/scripts/finish.py edit-x/plan.json --platform reels                        # texture, legal levels, mix, loudness
python CORE/scripts/deliver.py edit-x/plan.json --to reels,tiktok,shorts               # platform exports, SRT/VTT, thumbnails
python CORE/scripts/qc.py edit-x/final.mp4 --plan edit-x/plan.json                     # automated QC report
```

`run.py` options (all optional): `--genre`, `--clips A B C` / `--timeline spec.json` / `--auto montage|story|highlights` (multi-clip), `--music`, `--reframe 9:16`, `--stabilize`, `--denoise light|strong`, `--deflicker` (prep clean-up), `--smart-cuts`, `--retakes`, `--broll DIR`, `--platform`, `--deliver youtube,reels`, `--format`, `--model`, `--language`, `--stop-after STEP`. See `python CORE/scripts/run.py --help`.

| script | does | reference |
| --- | --- | --- |
| `prep.py` / `transcribe.py` | normalise footage (+ `--stabilize` vidstab, `--denoise light` or `strong`, `--deflicker`); faster-whisper word timestamps (`--model`, `--language`, `--prompt` for names; split tokens like "$10,000" merged) | |
| `autocut.py` | pauses, fillers (en + hi basics), retakes, quietest-point cuts, breaths, `--jcut`, `--genre` | craft.md |
| `selects.py` / `story.py` | selects + paper edit from long footage; outline, hook candidates, reorder (Frankenbite flags) | craft.md |
| `timeline.py` | multi-clip build/auto: 58 transitions, J/L cuts, speed ramps, freeze, reverse, Ken Burns, beat montage | timeline.md |
| `scenes.py` / `track.py` | shot/black/flash detection; face tracking, active speaker, auto-reframe, stack2 podcasts | timeline.md |
| `broll.py` | place B-roll from a folder on matching words, covering jump cuts first | timeline.md |
| `make_plan.py` | draft plan from transcript + skin theme + genre preset (+ beats, face track, peaks) | plan-schema.md |
| `editor.py` | Rule-of-Six cut scoring, pacing, retention, overlay discipline, captions cps; `--fix` | craft.md |
| `render.py` | HTML overlays (deterministic) + composite; colour on the footage first; `blurs` (privacy), face-aimed `speaker.zooms` | plan-schema.md, motion.md, color.md |
| `color.py` / `luts.py` | analysis, auto correction, log→709, 52 looks (skin-protected), matching, scopes, QC | color.md |
| `finish.py` | texture (grain, halation, letterbox...), legal levels, dialogue chain, SFX, music duck, loudness | audio.md |
| `audio_chain.py` / `beats.py` / `music_fit.py` / `tts.py` / `stems.py` | mix graph, 49 synthesized SFX, beats, music cut to length, offline voice-over, stems | audio.md |
| `deliver.py` / `export_edl.py` / `qc.py` | platform presets, subtitles, chapters, thumbnails, post pack; EDL/FCPXML/OTIO; QC | delivery.md |
| `director.py` | reads any footage and recommends genre skill, skin, format, platform and the run.py command (used by the video-director skill) | |
| `clip_candidates.py` / `multicam.py` | best moments in long video; switch cameras by who talks | |

Genre presets: `python CORE/scripts/editor.py genres` (pacing, cut rules, captions, loudness, deliverables per genre).

## Think like the editor (read references/craft.md)

1. **Story first.** Find the strongest line (`story.py outline`). Hook in the first 1–3 s, payoff before the end, CTA last 2 s.
2. **Cut for emotion and story before continuity** (Rule of Six). Cut at the end of a thought, in the quietest gap, keep natural breaths.
3. **Cover every jump cut** with B-roll, a punch-in or a cutaway — or make it deliberate.
4. **Split edits** (J/L) for dialogue; hard cuts by default; one transition grammar per video, used with restraint.
5. **Pacing has a target and varies.** Something changes every 1.5–3 s in reels, 4–8 s in long-form.
6. **Overlays:** enter 0.05–0.1 s before the word, ≥0.6 s on screen, ≤2 at once in reels, inside safe zones (10–85% height, clear of the right 12% in 9:16), never over the face.
7. **Colour:** correct first, match shots second, look last — on the footage, not the graphics. Protect skin.
8. **Sound is half the picture:** clean dialogue, music under it (ducked), SFX on motion, silence before a drop, platform loudness (-14 LUFS social, -16 podcast, -23/-24 broadcast).
9. **Deliver completely:** every platform size, captions file, thumbnail, chapters — then QC.

## Refine the plan (where the edit gets good)

`make_plan.py` is a draft. Read `words.json` and improve `plan.json`: rewrite the hook (≤7 words), pick key words that carry meaning, one idea per element, numbers become counters/charts, spoken lists become cards with `items[].at`, then run `editor.py review --fix`. Element and field references: `references/plan-schema.md` (base), `references/motion.md` (v2 motion, captions presets, 28 components, transitions), `references/color.md` (`"color"` block), `references/audio.md` (`"audio"`, `"music"`, `"sfx"`).

## QC before you hand it over

- Contact sheet (`render.py --frames`): text readable, nothing cut off, nothing over the face, safe zones.
- `qc.py`: duration, loudness/true peak, black/flash frames, illegal levels, caption cps, overlay rules.
- Report to the user: what was cut (seconds), structure, look, loudness, deliverables and file paths.

## Troubleshooting

- Fonts: Google Fonts need internet; otherwise fallbacks are used.
- Matte jumpy: `matte.py --smooth 0.7`; harsh hair: `--feather 5`; wrong person: `--backend rembg`.
- Slow: `--model base`, `render.py --workers 4`; minterpolate slow-mo is slow by nature.
- Captions wrong: fix words in `words.json` (keep times) and re-run `make_plan.py`.
- No face found (reframe): small/profile faces are missed; use `--mode locked` or a manual crop.
- Shaky, noisy or flickering footage: `run.py ... --stabilize --denoise light --deflicker` (single input). For
  multi-clip specs, clean a clip first with `prep.py clip.mp4 --work fix/c1 --stabilize` and use `fix/c1/source.mp4`.
- Podcast audio file: `qc.py final_podcast-mp3.mp3 --platform podcast` (audio-only checks).
