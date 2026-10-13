---
name: audio-analysis
description: "Inspect downloaded track waves or query APIs to analyze audio parameters like BPM, Key, Energy, and Valence."
version: 1.0.0
author: agent-lx-music project
license: MIT
metadata:
  hermes:
    tags: [music, analysis, bpm, key, signal-processing]
    related_skills: [agent-lx-music]
---

# Audio & Music Analysis Skill

## Overview

This skill guides AI agents in performing deep signal-processing analysis or metadata lookups on music tracks. By analyzing audio parameters such as **BPM (Beats Per Minute)**, **Musical Key / Scale (e.g. C Major, A Minor)**, and **energy metrics**, the agent can help users categorize playlists, match tempos for workouts or DJ sets, and explore composition structures.

---

## Technical Analysis Approaches

### Approach 1: Audio Metadata API Integration

Agents can query open music repositories (such as AcousticBrainz, Spotify Audio Features, or MusicBrainz) using song metadata to fetch precise pre-computed acoustic features.

```json
{
  "title": "晴天",
  "singer": "周杰伦",
  "bpm": 84,
  "key": "G Major",
  "valence": 0.52,
  "energy": 0.48,
  "danceability": 0.58,
  "time_signature": "4/4"
}
```

### Approach 2: Native Audio Waveform Extraction (CLI Signal Processing)

When the track is downloaded locally via `alx download <id>`, the agent can run local CLI signal processing tools (such as `aubio`, `ffmpeg`, or custom scripts using `librosa` / `essentia` / `madmom` models) to analyze the audio file.

#### 1. BPM / Tempo Detection

Identify the rhythmic rate of the song:

```bash
# Using aubio CLI tool to detect tempo (BPM) on downloaded track
aubiopitch -i "/path/to/song.mp3"
aubiotempo -i "/path/to/song.mp3"
```

#### 2. Key & Scale Detection

Analyze spectral pitch classes (chroma) to determine the tonic key:

```python
# Conceptual ESSENTIA key extractor Python script
import essentia.standard as es
loader = es.MonoLoader(filename="song.flac")
audio = loader()
key_extractor = es.KeyExtractor()
key, scale, strength = key_extractor(audio)
print(f"Key: {key} {scale} (Strength: {strength})")
```

---

## Agent Usage Patterns

### Pattern 1: Automatic Tempo-Matched Playlist

Build a playlist with songs matching a target BPM range (e.g. 120-130 BPM for jogging):

1. Query search cache or local music files.
2. Filter tracks matching the desired tempo.
3. Automatically load them into a running queue:

```bash
# Retrieve track metadata and filter for workout tempo (e.g. 125 BPM)
alx search "workout hits" --json | jq -r '.list[] | select(.bpm >= 120 and .bpm <= 130) | .id' | while read id; do
    alx queue add "$id"
done
```

### Pattern 2: Harmonious Transition Analysis

Advise the user on key matches (Camelot Wheel / Circle of Fifths) for smooth playlist progression:

- Track A (G Major / 9B) transitions harmoniously into Track B (D Major / 10B, C Major / 8B, or E Minor / 9A).
