---
name: video-sound
description: >-
  Makes the sound of any video: ElevenLabs voiceover (one file per line, static levelling, a
  transcript gate that must hear brand names verbatim, word timings for captions), music picked
  by role and tempo from a beat-mapped library and cut to the film, sound effects from an
  analysed library of 1,277 redistributable sounds or generated, the stereo mix that ducks music
  per spoken passage with a static master to -14 LUFS, and the check that every effect is heard.
  An executor under video-studio. Use when a film needs a voice, music, effects or a mix, or when
  video-studio reaches its audio steps. Triggers: "voiceover", "voice the script", "music bed",
  "sound design", "sound effects", "mix the audio", "loudness", "install the sound library".
---

# video-sound

Everything a film sounds like. video-studio decides when sound happens in the work
(audio first, then the mix); this skill decides how. House laws on sound live in
`../video-studio/references/laws.md` (Sound section) and win over anything here.

**Input: the film's `brief.md`** (`../video-studio/references/brief.md`). It owns copy, claims, tone,
material, moments and private data; this skill owns the implementation. If the brief cannot be
met, say so to video-studio - never change it silently.

## Setup (once)

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/library.py install   # ~150 MB download, SHA-256 checked
python3 ${CLAUDE_SKILL_DIR}/scripts/library.py venv      # tools/.venv: librosa, numpy, scipy, soundfile, matplotlib
python3 ${CLAUDE_SKILL_DIR}/scripts/library.py doctor    # what is missing
PY="${VIDEO_LIBRARY:-$HOME/.local/share/marketing-agent-kit/video-library}/tools/.venv/bin/python"
```

- `ffmpeg` and `ffprobe` on PATH (every script).
- `ELEVENLABS_API_KEY` in the environment or `~/.config/marketing-agent-kit/.env`
  (`connections/elevenlabs-api.md`). Sound generation needs a paid ElevenLabs plan.
- The voice gate needs a Whisper CLI: `mlx-whisper` on Apple Silicon, `openai-whisper` elsewhere.
  `--words` needs `parakeet-mlx` (Apple Silicon only); on other machines use `--align`.

## Library

`$VIDEO_LIBRARY` (default `~/.local/share/marketing-agent-kit/video-library`), shared by every
film. 8 music tracks (5 by Sascha Ende, CC BY 4.0, credit line in its `LICENSES.md`; 3 scratch
synth beds) and 1,277 sound effects: 228 Kenney, 32 keypresses, 11 ElevenLabs-generated interface
and brand-moment sounds, and 1,006 CC0 sounds in 19 functional types from the opus-sound-layer kit
(`sfx/osl/<type>/`: hit, glitch, zap, boom, ui, pop, tick, click, riser, swish, reverse, whoosh,
thump, chime, tap, key, shimmer, transition, paper; each with its peak offset).

- `catalog/CATALOG.md` first (its "By type" table and the kit's default picks), then
  `catalog/sfx.json` and `catalog/music.json`; every `path` is relative to the library root.
- Beat cues per track in `cues/`; every file's licence in `LICENSES.md`.
- **External tracks**: four music entries carry `"external": true` - their licence does not allow
  redistribution, so only their beat grids ship. Use one only when its file is at its `path`;
  `library.py doctor` says how to get each (two are 18 s cuts that `tools/prep_bed.py` re-makes).
- New sounds or music: licence row first (`catalog/sources.json` + `LICENSES.md`), then the file,
  then analyse, then rebuild the catalogue - the library's `README.md`, "Adding your own sounds".
  The tools live in `${CLAUDE_SKILL_DIR}/library-tools/` (copied into `$VIDEO_LIBRARY/tools/` on
  install): `analyze_music_cues.py`, `music_key.py`, `analyze_sfx.py`, `build_catalog.py`,
  `prep_bed.py`, `synth_bed.py`.

## Tools

`$PY` = the library venv (Setup).

| Job | Command |
|---|---|
| Voice, one file per line | `python3 ${CLAUDE_SKILL_DIR}/scripts/gen_voice.py lines.json out_dir --must Acme[,Zoom]` (ElevenLabs; static gain to -18 LUFS; transcript gate; `--words` caption timings (parakeet, European languages); `--align` = word timings from ElevenLabs itself, any language (required for Arabic/Hebrew/CJK; Hebrew needs `--model eleven_v3`); `--speed`, `--stability`) |
| A sound the library lacks | `python3 ${CLAUDE_SKILL_DIR}/scripts/gen_sfx.py sounds.json lib_dir` (ElevenLabs; "dry" for UI; `default` = the starter set of 11 prompts), then analyse and add it to the library |
| The mix | `python3 ${CLAUDE_SKILL_DIR}/scripts/mix.py timeline.json out.wav --duck fg bg [--depth 7] [--merge 1.0]` - voice on `fg`, music on `bg`, effects flat; ducks per passage; static master to `loudness`, then an oversampled true-peak limiter at `--tp-ceiling` (-2 dBTP) with the gain re-solved to the target (-1.9 dBTP survives AAC); writes `<out>.placed.json`. Library files are written `"$VIDEO_LIBRARY/sfx/..."` |
| Put a sound ON a picture event | an event with `"cue": <s>` (or `"frame"`) and `"align": "peak"` - the sound's peak lands on the cue (2 ms envelope; the sidecar's `peak_offset_s` when there is one); `"end"` for risers and reverses. Mark `"visual": "cut\|move\|land\|appear"` (+ `"roi"`, `"hero"`) so video-check can test it against the picture |
| Level and pitch effects against the music and the voice | `$PY ${CLAUDE_SKILL_DIR}/scripts/sfxauto.py timeline.json timeline.resolved.json --duck fg bg`, then mix the resolved file. `"gain": "auto"` = lifted 3.5 dB (hero 5) over the bed in its own band, capped (2-8 kHz, peak); under a voice = texture only, -24 dB, flagged. `"pitch": "auto"` = a tonal effect moved ≤ ±3 st onto the music's key (from the catalogue) |
| Silence before the peak, a build into it | on the effect: `"stop_before": true` (music -24 dB for the 0.4 s before its cue), `"build": true` (music thins through a 300 Hz high-pass over the 2 s before) - mix.py |
| Find a sound and look at it | `$PY ${CLAUDE_SKILL_DIR}/scripts/sfxlib.py browse --type whoosh --like "fast" --max-dur 1.5 --sheet out.png [--ads]` (waveform + spectrogram + peak per pick; prints the timeline path); `sfxlib.py measure <file>` for a new sound |
| Is every effect heard | `$PY ${CLAUDE_SKILL_DIR}/scripts/sfxcheck.py timeline.json` - GAP / OVER / LOW / MASKED, ONSET and TAIL flags |
| The library itself | `python3 ${CLAUDE_SKILL_DIR}/scripts/library.py install \| venv \| path \| doctor` |
| Sounds of camera and editing moves, story-time voice | the **video-moves** skill (`../video-moves/scripts/move_audio.py`) |

The full practice - voice models and settings, ElevenLabs details, music cutting to the
beat grid, effect placement, the mix and loudness targets, what to try next:
`references/audio.md`.

## Sources

- **opus-sound-layer** (github.com/Bodila51/opus-sound-layer @52ac266, MIT): the CC0 sound kit
  (licences re-checked page by page, 38 events left out), peak-aligned placement, the true-peak
  limiter loop, the per-band gain solver (`sfxauto.py`; under a voice it only sets texture), the
  dead stop and filter build, the browse sheet (`sfxlib.py`), the shared-room recipe, and the
  sync/picture/offset check (video-check `soundqa.py`). Their word-following duck is not taken
  (the laws duck per passage). Key detection (`music_key.py`, the idea is theirs) and the whisper
  speech scan of the Freesound set (`speechSuspect` in sfx.json; `sfxlib.py --ads` skips them) are ours.
- **latent-spaces/brag** (MIT): `analyze_music_cues.py`, the Ende tracks' cue presets and the
  Kenney/keyboard analysis.
- **The shared room**: mix.py adds it to the effects by default, off under speech
  (`--room off` disables it) - a blind A/B on a camera-moves test film picked it.

## Adapt it

- **Your voices**: pick ElevenLabs voice ids per language (premade voices work in the API;
  non-English lines need a shared-library voice) and write them into your brand laws.
- **Your names**: pass your product and brand names to `--must` on every take.
- **Your music**: add tracks you hold a licence for under `music/<source>/` (row in
  `catalog/sources.json` and `LICENSES.md` first), or put the four external tracks in
  `music/external/`; then analyse and rebuild the catalogue.
- **Your sounds**: write a `sounds.json` of prompts in your product's sonic style for
  `gen_sfx.py`, and add the results to the library as a source of their own.
- **Your targets**: `"loudness"` per timeline (-14 LUFS suits YouTube, LinkedIn, ads); after your
  first film checked by ear, move `sfxcheck.py`'s 0 dB line to what your ears agreed with.
