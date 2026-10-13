---
name: listening-companion
description: "Act as a real-time multimodal music companion by listening to audio tracks and providing structural, stylistic, and lyrical feedback."
version: 1.0.0
author: agent-lx-music project
license: MIT
metadata:
  hermes:
    tags: [music, companion, multimodal, audio, conversation]
    related_skills: [agent-lx-music, audio-analysis]
---

# Multimodal Music Listening Companion Skill

## Overview

This skill enables AI agents with multimodal audio processing capabilities (such as Gemini 1.5 Pro) to function as a real-time, highly interactive **Music Listening Companion (听歌伴侣)**. The agent literally "hears" the audio tracks played by `alx` and combines it with lyrics and metadata to engage in rich, analytical, and emotional conversations with the user about music.

---

## Capabilities of the Multimodal Audio Companion

Large multimodal models can ingest high-quality audio files directly. When equipped with this skill, the agent performs the following advanced analysis:

1. **Acoustic & Production Analysis**: Identifies specific instruments (e.g. Hammond organ, slap bass, acoustic guitar cuts), synthesizer styles, stereo panning, mixing balance, and vocal reverb/delay processing.
2. **Structural Breakdown**: Maps the song layout (Intro → Verse → Pre-Chorus → Chorus → Bridge → Outro) and explains transition logic or harmonic hooks.
3. **Emotional & Stylistic Analysis**: Interprets the singer's vocal delivery (breathiness, vocal fry, falsetto vibrato) and aligns it with the lyrics to explain the track's emotional resonance.
4. **Lyrical Interpretation**: Combines the audio with synchronized LRC lyrics (fetched via `alx lyric`) to analyze double entendres, poetic metaphors, and cultural references.

---

## Agent Integration Workflow

When a user initiates the Listening Companion mode:

```text
                  ┌──────────────────────┐
                  │ 1. User plays music  │
                  └──────────┬───────────┘
                             ▼
                  ┌──────────────────────┐
                  │ 2. Agent downloads   │
                  │    audio clip & LRC  │
                  └──────────┬───────────┘
                             ▼
                  ┌──────────────────────┐
                  │ 3. Feed audio + LRC  │
                  │    to Multimodal LLM │
                  └──────────┬───────────┘
                             ▼
                  ┌──────────────────────┐
                  │ 4. Rich Conversation │
                  │    on style / music  │
                  └──────────────────────┘
```

### Automation Script Example

The agent can fetch the currently active song, download a 30-60 second preview or the full audio, fetch the cached lyrics, and submit them to the multimodal interface:

```bash
# Step 1: Resolve currently active song metadata
SONG_INFO=$(alx now --json)
SONG_ID=$(echo "$SONG_INFO" | jq -r '.song.song_id')

# Step 2: Download the audio file and its lyrics
alx download "$SONG_ID"
alx lyric "$SONG_ID" --save
```

---

## Sample Companion Dialogues

### Scenario 1: Analyzing Instrument and Production Choices

- **User**: "This guitar solo sounds so warm and organic. What gear or techniques are they using here?"
- **Companion (Model Listening to Audio)**: *"Ah, that's a gorgeous tone. Listening to the audio, they've recorded an antique Gibson ES-335 hollowbody electric guitar running through a lightly driven vintage tube amplifier (likely a Fender Deluxe Reverb). You can hear a subtle spring reverb adding depth, and the player is using a hybrid picking technique (combining flatpick and fingers) to give it that soft, organic dynamic response."*

### Scenario 2: Lyrical and Vocal Resonance

- **User**: "Why does this chorus hit so hard emotionally?"
- **Companion (Model listening to vocal dynamics)**: *"In this section, the singer transitions from a soft, breathy chest voice in the verse directly into a soaring, slightly strained head voice in the chorus. The model's audio captures a slight vocal fry on the words '[02:14.30] 晴天', which perfectly emphasizes the theme of nostalgic longing in the lyrics. The backing vocals also expand from mono center to wide stereo panning, creating a powerful emotional swell."*
