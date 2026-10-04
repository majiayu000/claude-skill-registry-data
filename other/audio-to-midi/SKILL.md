---
name: audio-to-midi
description: >
  Convert MP3/WAV/FLAC audio files to MIDI (.mid) and MusicXML (.musicxml) with full music analysis.
  Two engines: Basic Pitch (general-purpose polyphonic) and Piano Model (high-accuracy piano, 96.7% F1).
  Optional Demucs stem separation. Use --engine piano for piano/keyboard music for best results.
  Trigger when the user wants to: transcribe audio to MIDI, convert music to sheet music/notes,
  extract notes from audio, get MusicXML from a recording, analyze tempo/key/chords of a song,
  separate stems (vocals/drums/bass) and transcribe each, or any audio-to-notation task.
  Also triggers for requests like "convert this MP3 to MIDI", "get the notes from this song",
  "what key is this song in", "transcribe this audio", "separate and transcribe stems".
---

# Audio-to-MIDI Transcription

Convert audio files to MIDI and MusicXML with full music analysis (tempo, key, chords, dynamics, instruments).

## Tool

**Script:** `scripts/transcribe.py` -- wraps Basic Pitch, Demucs, librosa, and music21. Auto-installs dependencies.

## Workflow

1. Identify the input audio file (MP3, WAV, FLAC, OGG, M4A)
2. Determine options:
   - **Stems?** Add `--stems` to separate vocals/drums/bass/other with Demucs first
   - **Output dir?** Use `-o path` or default to input file's directory
   - **Skip analysis?** Add `--no-analysis` if only MIDI/MusicXML needed
   - **Skip MusicXML?** Add `--no-musicxml` if only MIDI needed
3. Run the transcription script
4. Report output files and analysis summary to user

## Engines

| Engine | Flag | Best for | Accuracy |
|--------|------|----------|----------|
| Basic Pitch | `--engine basic-pitch` (default) | Mixed/polyphonic music | Good |
| **Piano Model** | `--engine piano` | Piano/keyboard music | **96.7% F1** |

For piano or keyboard music, always use `--engine piano` — it captures sustain/pedal, has far fewer ghost notes, and produces much more accurate MIDI.

## Usage

```bash
# Piano music (recommended for piano/keyboard)
py -3.12 scripts/transcribe.py "piano.mp3" --engine piano

# General music (default engine: Basic Pitch)
py -3.12 scripts/transcribe.py "song.mp3"

# With stem separation (Demucs): each stem gets its own MIDI + MusicXML
py -3.12 scripts/transcribe.py "song.wav" --stems

# Custom output directory
py -3.12 scripts/transcribe.py "song.mp3" -o ./output --engine piano

# Tuning Basic Pitch sensitivity
py -3.12 scripts/transcribe.py "song.mp3" --onset-threshold 0.6 --frame-threshold 0.4

# MIDI only (skip MusicXML)
py -3.12 scripts/transcribe.py "song.mp3" --no-musicxml

# MIDI + MusicXML without analysis
py -3.12 scripts/transcribe.py "song.mp3" --no-analysis
```

## Output Files

For input `song.mp3`:
- `song.mid` -- MIDI file (for DAWs, notation software)
- `song.musicxml` -- MusicXML (for MuseScore, Finale, Sibelius, Dorico)
- `song_analysis.json` -- Full analysis (tempo, key, chords, dynamics, spectral)

With `--stems`, each stem produces its own MIDI + MusicXML:
- `vocals.mid`, `vocals.musicxml`
- `drums.mid`, `drums.musicxml`
- `bass.mid`, `bass.musicxml`
- `other.mid`, `other.musicxml`

## Analysis Output

The `_analysis.json` contains:
- **tempo_bpm**: Detected BPM
- **key**: Detected key and mode (e.g. "A minor")
- **key_confidence**: 0-1 confidence score
- **chords**: Time-stamped chord progression
- **unique_chords**: Deduplicated chord list
- **dynamics**: Mean/max/min dB, dynamic range
- **spectral**: Centroid, bandwidth, rolloff, ZCR
- **instrument_hints**: Detected instrument categories

## Tuning Parameters

| Flag | Default | Effect |
|------|---------|--------|
| `--onset-threshold` | 0.5 | Higher = fewer ghost notes, may miss quiet notes |
| `--frame-threshold` | 0.3 | Higher = stricter note detection |
| `--min-note-length` | 58 | Minimum note duration in ms |

For clean recordings (piano, guitar): defaults work well.
For complex mixes: use `--stems` for best results.
For percussive music: lower onset threshold to 0.3-0.4.

## Dependencies

Auto-installed on first run: `basic-pitch`, `librosa`, `music21`, `pretty_midi`, `numpy`, `onnxruntime`.
With `--stems`: also installs `demucs` (includes PyTorch).
Requires: Python 3.12 (`py -3.12`), ffmpeg (for MP3 decoding).

**Important:** Use `py -3.12` (not `python`) to run the script. Python 3.14 has compatibility issues with ML packages. The script auto-selects the ONNX backend for Basic Pitch (most compatible).

## Supported Input Formats

MP3, WAV, FLAC, OGG, M4A, AAC, WMA
