---
name: localise-dub
description: "Localisation and dubbing editor for Claude: takes a finished video and makes a version in another language: transcript, translation, subtitles per language (SRT/VTT/TTML), and an offline TTS voice-over dub time-fitted to the original lines and mixed over the music and effects. Honest about limits: translation needs Claude or an optional local model, voices depend on installed TTS, and lip-sync is not done locally. Use when the user says 'dub this into Hindi', 'translate my video', 'Spanish subtitles', 'make a Tamil version', 'localise for Brazil', 'voice-over in another language', 'add subtitles in three languages'. Runs on video-studio-core (transcribe, tts, stems, finish, deliver, QC)."
license: MIT
---

# Localise and Dub

Same edit, new language: subtitles you can trust, and a dub that lands on the original timing.

- **Best for:** explainers, tutorials, courses, product demos, talks, short documentaries, faceless channels
- **Inputs:** the finished video (or its work folder), the target language(s), a glossary of names and product terms
- **Default skin:** `dual-subs` (bilingual captions) · alternatives `minimal-mono`, `news-desk`, `chapter-pro`
- **Formats:** whatever the original is; each language gets its own master + subtitle files
- **Durations:** unchanged from the original (dub lines are fitted to it)
- **Genre preset:** `--genre localise-dub` (see `python CORE/scripts/editor.py genre localise-dub`)

## Before you start

- This skill needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run on a machine: `python CORE/scripts/check_env.py` and fix what it reports.
- **What runs locally and what does not:**

| step | local? | how |
| --- | --- | --- |
| speech to text | yes | `transcribe.py` (faster-whisper), any Whisper language |
| translation | partly | Claude translates the transcript text in the conversation (default), or an optional local model: Opus-MT / MarianMT (`pip install transformers sentencepiece torch`, one model per language pair, CC-BY weights). NLLB and Seamless weights are non-commercial. Not installed by default |
| subtitles | yes | `deliver.py` writes SRT/VTT/TTML from a words file |
| voice-over | yes, voice-limited | `tts.py`: kokoro (if installed; English plus a few other languages, voice prefix sets the language), Windows SAPI (only the voices installed in Windows Speech settings), macOS `say`, espeak-ng (robotic, many languages) |
| music + effects bed | optional | `stems.py` needs `pip install demucs` (slow on CPU); or the original M&E stem from the user |
| voice cloning | no | XTTS/F5 weights are non-commercial and not part of this pack |
| lip-sync | no | needs heavy optional models (LatentSync, Wav2Lip = non-commercial); say so, offer a voice-over style dub instead |

- Get the user's OK on: the target languages, formal or informal register, and who reviews the translation.
  Machine translation of names, numbers, legal or medical claims must be checked by a fluent speaker.
- Only dub content the user owns or has rights to translate. A synthetic voice is not the original speaker: label it
  ("AI voice-over") where the platform or the audience expects it, and never present it as the person's own voice.

## How a pro cuts this

**Structure.** The original structure stays 100%. Localisation changes words and voices, not the edit.

**Pacing and timing.** Each translated line must fit the time the original line had. Translations run 10-30% longer
(German, Spanish, Hindi) or shorter (Chinese). Fit in this order: rewrite shorter (best), adjust TTS `--rate` within
0.85-1.15 (about +-15%), let the line borrow up to 0.3 s of the following pause, and only then extend the shot
(a freeze or slower B-roll in a re-edit). Never speed a voice above 1.15: it sounds rushed.

**Cut rules.** No new cuts. Keep the original J/L timing: the dub line starts where the original line started
(+-0.1 s), so on-screen actions and graphics still match the words.

**Transition grammar.** Unchanged from the original.

**Music and sound.** Dub over the music-and-effects bed (no original voice). If there is no M&E, either separate it
(`stems.py`) or keep the original voice ducked ~18 dB under the dub ("UN-style" voice-over), which is honest and
common for interviews. Same loudness as the original (-14 LUFS / -1 dBTP for web).

**Colour.** Untouched. Re-use the original grade.

**Captions.** Target-language subtitles, sentence case, <= 42 chars per line, <= 17-20 cps (Netflix-style rules
built into `deliver.py`). Burned-in creator captions in the new language only if the original had them.
Translated on-screen text (titles, lower thirds, cards) must be edited in the plan too.

**What the client judges.** Natural sound, timing, translation accuracy, and that names and terms are consistent.

**Common mistakes.** Literal translation that overruns the line; speeding TTS to 1.4x; original voice bleeding under
the dub; untranslated graphics; subtitles that still follow the source sentence breaks; promising lip-sync.

## Make the edit

The original work folder `W` (with `plan.json`, `words.json`, `cut.mp4`, `final.mp4`) is the best starting point.
From a finished file only, make one with the genre preset (no cutting):

```bash
python CORE/scripts/run.py video.mp4 --style SKILLS/dual-subs --genre localise-dub --format 16:9 --no-cut --model small --work W --stop-after plan
```

1. **Transcript in segments.** `W/transcript.json` (source words) and `W/words.json` (cut timeline) exist. Group the
   words into sentences with their start/end and write `W/loc/es/lines.json`:
   `[{"id": 1, "start": 0.42, "end": 3.10, "src": "Here are three mistakes.", "text": ""}]`.
2. **Translate** each `src` into `text` (Claude in the conversation, or Opus-MT if installed), keeping the glossary.
   Aim for the same length; mark lines that are > 15% longer and shorten them.
3. **Voice each line** and fit it:

```bash
python CORE/scripts/tts.py --list-voices
python CORE/scripts/tts.py --text "Aquí tienes tres errores." --out W/loc/es/l001.wav --voice "Microsoft Helena Desktop" --rate 1.0
```

   Compare each WAV's length (ffprobe) with `end - start`; re-run with `--rate` = tts length / slot length, clamped to
   0.85-1.15. Still too long: shorten the text.
4. **Bed without the original voice** (optional, needs demucs):

```bash
python CORE/scripts/stems.py W/cut.mp4 --out W/stems
```

   Then make a copy of the picture with the bed as its audio (plain FFmpeg, no filters):
   `ffmpeg -i W/cut.mp4 -i W/stems/music.wav -map 0:v -map 1:a -c:v copy -c:a aac -shortest W/cut_me.mp4`.

## Refine the plan

Copy the plan per language: `W/plan_es.json` (same folder, so relative paths still work). Then:

- **Source with the bed:** `"source": "cut_me.mp4"` and `"audio": {"platform": "youtube", "voice": false}` (do not run
  the dialogue chain on music). Voice-over style without an M&E: make a copy with the original sound about 18 dB down,
  `ffmpeg -i W/cut.mp4 -map 0 -c:v copy -af volume=0.12 W/cut_vo.mp4`, and use `"source": "cut_vo.mp4"` with the same
  `"voice": false`.
- **Dub lines** as timed audio files: `"sfx": [{"t": 0.42, "file": "loc/es/l001.wav", "gain": 1.0}, {"t": 3.55, "file": "loc/es/l002.wav", "gain": 1.0}]`.
- **Words for subtitles:** write `W/loc/es/words.json` = `{"language": "es", "words": [{"w": "Aquí", "start": 0.42, "end": 0.70}, ...]}`
  by spreading each line's words over its slot by character count (or run `tts.py --words` per line and offset the
  times by the line's `t`). Put the same list in the plan's `"words"` so captions and ducking follow the dub.
- **Translate on-screen text:** every `text`, `headline`, `card`, `lowerthird`, `titlecard` field in `elements`.
  Check fonts cover the script (`theme.fontsUrl`, e.g. Noto Sans Devanagari for Hindi).
- **Bilingual captions:** with the `dual-subs` skin follow its notes for the second line.
- `"outputFile": "final_es.mp4"`, then `python CORE/scripts/render.py W/plan_es.json --frames 2,10,20` and
  `python CORE/scripts/render.py W/plan_es.json`, `python CORE/scripts/finish.py W/plan_es.json --platform youtube`.

## Deliver

`deliver.py` takes words from the plan when you give it a plan; to attach a specific language's subtitles, give it
the video and `--words`:

```bash
python CORE/scripts/deliver.py W/final_es.mp4 --to youtube --words W/loc/es/words.json --out-dir W/deliver_es --burn no
python CORE/scripts/deliver.py W/final.mp4 --to youtube --words W/loc/hi/words.json --out-dir W/subs_hi --burn no --no-thumbs --no-post
python CORE/scripts/qc.py W/deliver_es/final_es_youtube.mp4 --plan W/plan_es.json --platform youtube
```

The second line makes Hindi subtitles for the original-language video (upload `captions.srt` as an extra track).
Deliver per language: dubbed master, `.srt/.vtt/.ttml`, the untouched original master, and the M&E/no-vocals stem.

## Check before delivering

- A fluent speaker has read the translation (names, numbers, units, claims). Note who checked it.
- Every dub line starts within 0.1 s of the original line; no overlaps between lines (`qc.py` silence and loudness pass).
- No original voice audible under the dub (unless the voice-over style was chosen on purpose).
- Subtitles parse, <= 42 chars per line, reading speed within limits (`qc.py` caption checks).
- On-screen text translated and rendered with a font that has the script.
- Tell the user plainly: voice is synthetic, no lip-sync, which steps were machine translation.

## Example requests

- "Make a Hindi version of this tutorial with a voice-over and Hindi subtitles."
- "Add Spanish and Portuguese subtitles to my video, no dub."
- "Dub this product demo into German, keep the music, and tell me which lines you had to shorten."
