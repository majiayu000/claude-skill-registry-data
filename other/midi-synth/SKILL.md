---
name: midi-synth
description: >
  Synthesize and render MIDI/MusicXML files to audio (WAV/MP3) and generate Strudel live-coding
  patterns for creative music manipulation. Uses analysis data (tempo, key, chords, dynamics)
  from audio-to-midi for intelligent ghost-note removal and accurate reproduction.
  Two workflows: (1) Convert MIDI/MusicXML to Strudel/TidalCycles code with note durations
  for interactive tweaking in the browser at strudel.cc, (2) Render MIDI/MusicXML to WAV/MP3
  with FluidSynth or built-in synthesis, with controls for tempo, transposition, instrument
  override, and ghost-note cleaning.
  Trigger when the user wants to: play a MIDI file, render MIDI to audio, synthesize MIDI,
  convert MIDI to Strudel code, create live-coding patterns from MIDI, change instruments,
  transpose or tempo-shift, clean ghost notes, or any MIDI playback/synthesis task.
---

# MIDI Synth

Synthesize MIDI/MusicXML to audio and generate Strudel live-coding patterns.
Uses analysis data for ghost-note cleaning, correct tempo, and key-aware filtering.

## Scripts

- **`scripts/to_strudel.py`** -- MIDI/MusicXML to Strudel patterns with duration-aware notation
- **`scripts/render.py`** -- MIDI/MusicXML to WAV/MP3 with cleaning and modifications

Both scripts auto-detect `*_analysis.json` files from audio-to-midi for tempo, key, and dynamics.

## Workflow

1. Identify input: MIDI (.mid) or MusicXML (.musicxml)
2. Auto-detect or specify the analysis JSON from audio-to-midi
3. Choose workflow:
   - **Creative:** `to_strudel.py` generates Strudel code for strudel.cc
   - **Rendering:** `render.py` produces WAV/MP3
   - **Both:** run both on the same input
4. Ghost notes are automatically cleaned using velocity, duration, and key filters

## Strudel Code Generation

```bash
# Basic (auto-detects analysis JSON next to input)
py -3.12 scripts/to_strudel.py "song.mid"

# From MusicXML
py -3.12 scripts/to_strudel.py "song.musicxml"

# Explicit analysis file
py -3.12 scripts/to_strudel.py "song.mid" --analysis "song_analysis.json"

# Stricter ghost-note filtering
py -3.12 scripts/to_strudel.py "song.mid" --min-velocity 60 --min-duration 0.1

# Open in browser
py -3.12 scripts/to_strudel.py "song.mid" --open
```

| Flag | Default | Effect |
|------|---------|--------|
| `--analysis` | auto-detect | Path to analysis JSON for tempo/key |
| `--bars` | 4 | Pattern length in bars |
| `--resolution` | 16 | Grid: 4/8/16/32 |
| `--min-velocity` | 40 | Remove notes below this velocity (0-127) |
| `--min-duration` | 0.05 | Remove notes shorter than this (seconds) |
| `--no-key-filter` | off | Disable key-based ghost note filtering |
| `--tempo` | from analysis | Override tempo BPM |
| `--open` | off | Open in strudel.cc in browser |

Note durations are encoded with `@N` notation (e.g., `c3@4` = held for 4 steps).

## Audio Rendering

```bash
# Basic (auto-detects analysis, cleans ghost notes)
py -3.12 scripts/render.py "song.mid" --mp3

# From MusicXML
py -3.12 scripts/render.py "song.musicxml" --mp3

# With SoundFont
py -3.12 scripts/render.py "song.mid" --soundfont "GeneralUser_GS.sf2" --mp3

# Aggressive cleaning
py -3.12 scripts/render.py "song.mid" --min-velocity 60 --min-duration 0.1

# Skip cleaning entirely
py -3.12 scripts/render.py "song.mid" --no-clean

# Modifications
py -3.12 scripts/render.py "song.mid" --tempo 2.0 --transpose 3 --instrument 0
```

| Flag | Default | Effect |
|------|---------|--------|
| `--analysis` | auto-detect | Analysis JSON for tempo/key-based cleaning |
| `--min-velocity` | 40 | Ghost note velocity threshold |
| `--min-duration` | 0.05 | Ghost note duration threshold (seconds) |
| `--no-clean` | off | Skip ghost note removal |
| `--no-key-filter` | off | Disable key-based filtering |
| `--soundfont` | auto-detect | .sf2 SoundFont path |
| `--tempo` | 1.0 | Tempo scale factor |
| `--transpose` | 0 | Semitones up/down |
| `--instrument` | original | Override GM program (0-127) |
| `--mp3` | off | Also produce MP3 |

## Ghost Note Cleaning

Three filter layers (applied in order):
1. **Velocity filter**: removes notes below `--min-velocity` (default: 40)
2. **Duration filter**: removes notes shorter than `--min-duration` (default: 50ms)
3. **Key filter**: if analysis provides a key, removes out-of-key notes that also have low velocity (<60)

The key filter only removes notes that are BOTH out-of-key AND below medium velocity, preserving intentional chromatic passages.

## Dependencies

Auto-installed: `pretty_midi`, `numpy`, `soundfile`.
For MusicXML input: `music21` (installed by audio-to-midi skill).
Optional: `pyfluidsynth` + `.sf2` SoundFont for high-quality rendering.
Runtime: Python 3.12 (`py -3.12`).
