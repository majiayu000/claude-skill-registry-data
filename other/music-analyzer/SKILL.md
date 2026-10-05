---
name: music-analyzer
description: >
  Analyzes music files (MP3, WAV, FLAC, M4A, OGG) and produces a detailed music and lyrics
  analysis including genre recognition, mood analysis, BPM, key, instrument detection and
  lyrics interpretation. Uses HDEMUCS for vocal separation, Whisper for lyrics transcription
  and librosa for audio feature extraction with CUDA GPU acceleration.
  Use this skill when the user wants to analyze a music file, examine a song, transcribe
  lyrics, or asks questions like "analyze this song", "what genre is this", "transcribe the
  lyrics", "what mood does this song have", "what instruments do I hear", "how fast is the
  song", "what key is it in", "music analysis", "song analysis", "audio analysis",
  "detect BPM", "determine key", "detect genre", "analyze song".
---

# Music Analyzer

Comprehensive music file analysis: lyrics extraction via vocal separation + Whisper,
audio features via librosa, and Claude interprets the raw data into genre, mood,
instruments etc.

## Prerequisites

- Python 3.10+ with PyTorch, torchaudio, openai-whisper, librosa, soundfile
- ffmpeg must be in PATH
- Scripts located in: `scripts/` (relative to this skill's base directory)
- NVIDIA GPU with CUDA support recommended (works on CPU too, just slower)
- A `requirements.txt` is included in the skill's base directory

## Workflow

### Step 0: Find Python and check dependencies

The analysis script checks all dependencies on startup. If anything is missing, it returns
a JSON error with the exact install command. Run:

```bash
python "<SKILL_BASE_DIR>/scripts/analyze_music.py" --help
```

If this fails, find a working Python first:
```bash
python -c "import torch; print(torch.cuda.is_available())" 2>/dev/null || echo "FAIL"
python3 -c "import torch; print(torch.cuda.is_available())" 2>/dev/null || echo "FAIL"
```

If no Python has torch, or other packages are missing, guide the user through installation:

**Missing packages** -- the script returns JSON like:
```json
{"error": "Missing Python packages: torch, librosa, ...", "install": "pip install -r requirements.txt"}
```
Tell the user to run the install command from the JSON. For CUDA GPU support:
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
pip install -r "<SKILL_BASE_DIR>/requirements.txt"
```
For CPU-only (no NVIDIA GPU):
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install -r "<SKILL_BASE_DIR>/requirements.txt"
```

**Missing ffmpeg** -- the script returns:
```json
{"error": "ffmpeg not found in PATH", "install": "Windows: winget install Gyan.FFmpeg | Mac: brew install ffmpeg | Linux: sudo apt install ffmpeg"}
```
Tell the user the platform-specific install command.

If this fails or returns False, try common alternatives on Windows:
- `ls /c/Python3*/python.exe 2>/dev/null`

On Linux/Mac:
- `which python3.11 python3.12 python3.13 2>/dev/null`

Use the Python executable that succeeds for all subsequent commands.
Store it as `<PYTHON>` for the rest of this workflow.

### Step 1: Get input

If the user has not provided a file path, ask with AskUserQuestion:
```
"Which music file should I analyze? (Please provide the full path)"
```

Validate:
- File exists
- Format is supported: .mp3, .wav, .flac, .m4a, .ogg
- If the user only provides a filename, search with Glob in common folders:
  `~/Music/`, `~/Downloads/`, `~/Desktop/`

Optionally ask if it's an instrumental track (saves ~60s processing time).

### Step 2: Run analysis

Determine the skill base directory from the context (provided as "Base directory for this
skill" when the skill is loaded). Then run:

```bash
<PYTHON> "<SKILL_BASE_DIR>/scripts/analyze_music.py" "<AUDIO_PATH>"
```

Where `<PYTHON>` is the Python executable found in Step 0, `<SKILL_BASE_DIR>` is the base
directory of this skill, and `<AUDIO_PATH>` is the absolute path to the audio file.

Optional flags:
- `--skip-lyrics` for instrumental tracks
- `--whisper-model small` for faster (but less accurate) transcription

The script outputs JSON to stdout. Status messages appear on stderr.
**Set timeout to 600000ms (10 minutes)** -- vocal separation + Whisper need time.

### Step 3: Interpret JSON

Read the `references/genre_profiles.md` reference table from this skill's base directory.

Interpret the JSON data using the reference table and your music knowledge:

#### Genre Detection
Combine multiple signals:
1. **BPM** narrows genre families (e.g., 60-90 = R&B/Reggae/Hip-Hop, 120-140 = Dance/Rock/Pop)
2. **Spectral Centroid** indicates brightness (high = Electronic/Metal, low = Jazz/Classical)
3. **Energy (RMS)** distinguishes intense vs. gentle
4. **Key/Mode** gives genre hints (minor = Metal/Hip-Hop, major = Pop/Country)
5. **Onset Density** shows rhythmic complexity
6. **Lyrics content** confirms or corrects (rap text = Hip-Hop, love ballad = Pop/R&B)
7. **ZCR** (Zero Crossing Rate) correlates with distortion/noise
8. Assign scores from 0-100 for up to 5 genres and 5 subgenres

#### Mood Detection (Music)
- Major + fast + high energy = Energetic/Happy
- Minor + slow + low energy = Sad/Melancholic
- High dynamic range + variable energy = Dramatic/Intense
- Building energy curve = Hopeful/Triumphant
- Assign scores 0-100 for up to 5 moods

#### Instrument Detection
Derive instruments from:
- **Spectral Contrast Bands**: Low bands = Bass, mid = Guitar/Keys, high = Cymbals
- **Onset Density**: High + percussive = Drums/Percussion
- **Accompaniment Features**: Centroid and MFCCs of the accompaniment track
- **Genre Context**: Once genre is identified, typical instruments are probable
- List the most likely instruments (no scores)

#### BPM & Key
Take directly from JSON features. Format: `{BPM}BPM, {Key} {Mode}`
Example: `120BPM, E Major`

#### Vocals
Describe based on:
- `lyrics.has_vocals`: whether vocals are present
- `lyrics.vocal_rms`: vocal volume (>0.08 = strong, 0.03-0.08 = moderate, <0.03 = soft)
- `lyrics.language`: detected language
- Genre context for typical vocal characteristics
- Format: e.g., "Male vocals, mid-range, melodic" or "Female vocals, high pitch, powerful"

#### Lyrics Analysis
Use the transcribed text (`lyrics.text`) and analyze:
- **Summary**: 2-3 sentences about themes, narrative, emotional content
- **Moods**: Up to 5 moods with scores 0-100 based on text analysis
- **Themes**: Up to 5 themes with scores 0-100
- **Language**: Language from Whisper detection, in long form (e.g., "English", "German")
- **Explicit**: Check the text for profanity/explicit content -> "Yes" or "No"

If no lyrics present (instrumental):
```
Summary: Instrumental track - no vocals detected
Moods: N/A
Themes: N/A
Language: N/A
Explicit: No
```

### Step 4: Formatted output

Present the result in exactly this format. IMPORTANT: Single-value fields (Moods, Themes,
Language, Explicit, Genres, Subgenres, Instruments, BPM & Key, Vocals) go on the SAME LINE
as their label, separated by a space. Only multi-sentence text blocks (Summary, Production
Description) start on the line BELOW their label.

```
LYRICS ANALYSIS

Summary
[2-3 sentences on the next line]
Moods: [Mood1 (Score), Mood2 (Score), Mood3 (Score), Mood4 (Score), Mood5 (Score)]
Themes: [Theme1 (Score), Theme2 (Score), Theme3 (Score), Theme4 (Score), Theme5 (Score)]
Language: [Language]
Explicit: [Yes/No]

MUSIC ANALYSIS
Genres: [Genre1 (Score), Genre2 (Score), Genre3 (Score), Genre4 (Score), Genre5 (Score)]
Subgenres: [Subgenre1 (Score), Subgenre2 (Score), Subgenre3 (Score), Subgenre4 (Score), Subgenre5 (Score)]
Moods: [Mood1 (Score), Mood2 (Score), Mood3 (Score), Mood4 (Score), Mood5 (Score)]
Instruments: [Instrument1, Instrument2, Instrument3, ...]
BPM & Key: [BPM]BPM, [Key] [Mode]
Vocals: [Description]

PRODUCTION DESCRIPTION
[Detailed prose description of the production -- see below]
```

**Important:**
- Scores are always integers 0-100
- Sort by score descending
- Always exactly 5 entries for Genres, Subgenres, Moods, Themes (including Lyrics Moods)
- Instruments without scores, comma-separated list only
- No Markdown formatting in the output (no **, no #, no ```)
- NEVER include artist names, band names, album names, song titles, or direct lyrics quotes
  in the output. Describe only the musical and production characteristics generically
- Output as plain text

#### Production Description

Write a cohesive prose paragraph (3-6 sentences) describing the production in detail.
Follow this style and cover these aspects:

1. **Genre + BPM + Key** as introduction: "A [mood] [genre] production at [BPM] BPM in [Key]"
2. **Rhythm/Drums**: Describe kick pattern, hi-hats, snare character based on onset_density
   and spectral contrast in low bands
3. **Bass**: Bass character (sub-bass, warm, pulsating, dry) based on low spectral contrast
   bands and accompaniment features
4. **Harmony/Pads/Synths**: Atmospheric elements based on spectral bandwidth, energy curve
   and chroma distribution
5. **Melody Instruments**: Piano, guitar, synth leads based on mid spectral bands
6. **Vocals**: Pitch, timbre, effects, singing style based on vocal_rms, lyrics language
   and genre context. Describe expression in verse vs. chorus if segments show this
7. **Mix/Space**: Stereo width, depth, reverb character based on spectral features and
   dynamic range

Example output:
"A dreamy melancholic dream trance production at 130 BPM in F sharp minor with a soft
four-on-the-floor kick and delicate offbeat hi-hats, a deep sustained sub-bass running
warmly throughout, lush evolving pad layers creating wide cinematic atmosphere, a gentle
grand piano carrying the central melody with shimmering sustain, soft arpeggiated synth
sequences adding upper-frequency movement. Ethereal female soprano with a silvery breathy
tone, soft and intimate in the verses, soaring into sustained notes in the chorus with
layered harmonies, treated with lush hall reverb and cascading delay trails. Wide warm
immersive modern mix, sub-bass felt deep, pads filling the stereo field, piano and vocal
centered with delicate shimmer reverb creating vast nocturnal depth."

### Step 5: Show warnings

If the JSON contains `warnings`, show them at the end:
```
Notes: [warning1], [warning2]
```
