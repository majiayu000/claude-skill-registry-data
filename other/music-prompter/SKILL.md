---
name: music-prompter
description: MUST read this skill BEFORE entering generate mode for music tasks. Covers
  prompt crafting framework, structure syntax, and multi-clip strategy.
---

# Music Generation Prompt Guide

When crafting music generation prompts, adopt the mindset of a **world-class music arranger and producer**. Think holistically about the entire piece — its emotional arc, sonic palette, and structural flow — before writing the prompt. Your goal is to translate the user's vision into a single, cohesive musical blueprint that the model can execute in one take whenever possible.

## 1. Duration Awareness

Each call to the music generation tool produces a single audio file with a maximum duration of **~184 seconds (approx. 3 minutes)**.

The decision to use single-call vs multi-clip is based **SOLELY on duration**:
- If the requested duration is **≤ 180 seconds (3 minutes)**: **MUST use a single call**, regardless of song structure complexity. Pack all sections (verse, chorus, bridge, outro, etc.) into one prompt using the Standard Prompt Structure (Section 3).
- If the requested duration is **> 180 seconds**: Use the Multi-Clip Continuity Strategy described in Section 7.

## 2. The 9-Dimension Framework

Good prompts are descriptive and clear. The prompt must be a single, continuous text string. Construct your prompt by combining the following 9 dimensions. Be descriptive and specific, using adjectives and adverbs to paint a clear sonic picture.

1. **Genre & Style**: The primary musical category and stylistic characteristics.
   - *Examples*: `electronic dance`, `classical`, `jazz`, `ambient`, `8-bit`, `cinematic`, `lo-fi`
2. **Tempo & Rhythm**: The pace and rhythmic character.
   - *Examples*: `fast tempo`, `slow ballad`, `120 BPM`, `driving beat`, `syncopated rhythm`, `gentle waltz`
3. **Key & Scale**: The harmonic foundation.
   - *Examples*: `in D minor key`, `in the key of C major`
4. **Mood & Emotion**: The desired feeling the music should evoke.
   - *Examples*: `energetic`, `melancholy`, `peaceful`, `tense`
5. **Instrumentation**: Key instruments you want to hear.
   - *Examples*: `piano`, `synthesizer`, `acoustic guitar`, `string orchestra`, `electronic drums`
6. **Density & Brightness**: The thickness of the arrangement and tonal color.
   - *Examples*: `sparse arrangement`, `dense layers`, `warm dark tones`, `bright crisp tones`
7. **Arrangement/Structure**: How the music progresses or layers over time (e.g., `starts with a solo piano, then strings enter`, `crescendo into a powerful chorus`). For more precise control, you can optionally use **timestamp cues** `[mm:ss - mm:ss]` and **Intensity** parameters `Intensity: X/10 (Level)` — see the Detailed Structure Example below.
   - *Examples*: `starts with a solo piano, then strings enter at the halfway point`, `solo piano from 0-8s, strings enter at 8s, drums join at 16s`
8. **Soundscape/Ambiance & Space**: Background sounds, overall sonic environment, and spatial characteristics such as reverb type, stereo width, and perceived distance.
   - *Examples*: `rain falling`, `city nightlife`, `underwater feel`, `large hall reverb`, `tight room reverb`, `wide stereo image`, `intimate close-mic feel`, `distant and far away, as if playing in the next room`
9. **Production Quality**: Desired audio fidelity, recording style, and spatial production choices.
   - *Examples*: `high-quality production`, `clean mix`, `vintage recording`, `raw demo feel`, `studio dry sound`, `live concert hall recording`, `outdoor open-air feel`

*Note on Vocals*: The model supports vocal generation for songs. If the user explicitly wants background music without vocals, you MUST append `Instrumental only, no vocals` to the prompt.

## 3. Standard Prompt Structure

To ensure the model accurately follows your instructions, especially regarding duration, always structure your prompt in this specific order:

1. **Global Directives (CRITICAL for Duration)**: Explicitly state the total duration, BPM, and vocal preferences at the very beginning of the prompt.
   - *Example*: `Instrumental only, no vocals. Create a 60-second track at 80 BPM.`
2. **Core DNA**: Describe the Genre, Mood, Instrumentation, Density, Soundscape, and Production Quality. This establishes the overall sonic picture.
   - *Example*: `The feeling is nostalgic, introspective, and atmospheric. The sound should be centered around a warm Fender Rhodes...`
3. **Arrangement Breakdown (Optional)**: If you need precise control, provide a chronological breakdown. **CRITICAL**: If you use timestamps, the final timestamp MUST exactly match the total duration declared in step 1.
   - *Example*: `[0:00 - 0:12] Intro... [0:48 - 1:00] Outro...`

## 4. Detailed Structure Example

When the user requests a specific structure or duration, use the Arrangement/Structure dimension to write a detailed script using timestamps and intensity markers.

*Example*:
```text
Instrumental only, no vocals. Create a 60-second track at 80 BPM. The feeling is nostalgic, introspective, and atmospheric - a warm, comforting melancholy with a soft, minor-key feel. The sound should be centered around a warm, slightly overdriven Fender Rhodes and soft, ethereal synth pads. The rhythm is a minimalist, laid-back drum beat with a relaxed, human feel. Weave subtle atmospheric textures, like soft static or room tone, through the entire track for texture.

[0:00 - 0:12] Intro: Begin atmospherically with just the Fender Rhodes playing soft, hazy chords. Drench it in warm reverb and introduce a light atmospheric texture. The mood is like a memory coming into focus. Intensity: 1/10 (Very Low)

[0:12 - 0:24] Verse 1: The laid-back drum beat enters with a simple kick and snare. A soft, ethereal synth pad swells in the background. A clean, subtle sub-bass joins, adding depth. The Rhodes melody becomes slightly more defined, following a simple, melancholic progression. Intensity: 3/10 (Low)

[0:24 - 0:36] Build: The groove deepens as a gentle, syncopated hi-hat is added. A simple, memorable lead melody appears, played on a warm, rounded synth. This section should feel like the gentle peak of the track's focus, with a chord progression that builds a sense of hopeful tension. Intensity: 5/10 (Medium)

[0:36 - 0:48] Chorus: Gracefully pull back the intensity. The synth lead melody fades out, returning focus to the core Rhodes groove and the drums. This gives the track space to breathe, resolving the tension from the build. Intensity: 4/10 (Medium-Low)

[0:48 - 1:00] Outro: The drums and bass drop out completely. The track fades out leaving only the Rhodes playing spacious chords, the lingering synth pad, and the persistent atmospheric texture. Intensity: 2/10 (Very Low)
```

## 5. In-Text Negative Prompting

To specify elements to exclude from the music, describe what you want to discourage the model from generating directly in your main prompt using explicit negative phrasing.

- **Instead of**: a hypothetical `negative_prompt: "drums, fast tempo"`
- **Write**: `"Ensure there are no drums or percussion. Avoid fast tempos."` or `"A drumless, percussion-free ambient track..."`

Categories of elements commonly excluded:
- **Instruments**: `no drums, no percussion, no vocals`
- **Behaviors**: `no complex melodies, no sudden dynamic changes, no fast runs`
- **Moods**: `avoid dark mood, avoid aggressive energy`

## 6. Emulating Advanced Controls

To emulate specific parameter controls, use these prompt translations:
- **Low Density**: `sparse arrangement, minimal layers, lots of space between notes`
- **High Density**: `dense, busy arrangement with many overlapping layers and fills`
- **High Brightness**: `bright, crisp tones, emphasizing high frequencies and presence`
- **Mute Drums**: Add `Ensure there are no drums, no percussion, no beat, no rhythm section` to the prompt
- **Bass & Drums Only**: Add `Only bass and drums, rhythm section only. No melody, no chords, no harmony, no piano, no guitar, no strings, no synth pads.`

## 7. Multi-Clip Continuity Strategy (Duration > 184s)

When the user's request exceeds the single-call limit (~184 seconds), generate multiple independent clips and concatenate them. Think like a professional arranger to make them sound like a cohesive song: **Plan the entire song structure first, then write prompts for each clip.**

### Step 1: The Arrangement Plan
Plan the song's progression (e.g., Intro → Verse → Chorus → Bridge → Outro). Determine which musical elements define the song's core identity (DNA) and which elements drive the narrative forward. Divide the total duration into logical chunks of up to ~180s each.

### Step 2: Categorize the 9 Dimensions

**Category A: Always Lock (Identical across all clips)**
These elements are the song's DNA. Changing them will cause jarring transitions.
- **Genre & Style**: The fundamental musical category.
- **Tempo & Rhythm**: The BPM and rhythmic feel. Essential for seamless beat-matching.
- **Production Quality**: The recording fidelity.

**Category B: Default Lock, Intentional Vary**
These elements are usually locked, but can be changed if the arrangement plan specifically calls for it.
- **Key & Scale**: Default to identical. *Exception*: Intentional modulations (e.g., upward modulation in the final chorus).
- **Core Instrumentation**: The sonic palette is locked, but you can add/remove layers (e.g., adding drums in the chorus, stripping back to piano solo in the bridge).
- **Soundscape/Ambiance**: Default to identical, but can be tweaked (e.g., from "intimate" to "spacious").

**Category C: Should Vary (Different across clips)**
These elements drive the song's narrative.
- **Mood & Emotion**: Shift slightly within the same emotional spectrum (e.g., from "introspective" to "uplifting").
- **Arrangement/Structure**: Use **timestamp cues** and **Intensity** to precisely script the arrangement within each clip.
- **Density & Brightness**: Adjust according to the arrangement state.

### Step 3: Clip Transition Design (Precise State Alignment)

The core principle is **Precise State Alignment**: use timestamp cues to ensure the musical state at the **end** of one clip exactly matches the musical state at the **beginning** of the next clip. This means matching instrumentation, energy level, and dynamic intensity.

**Avoiding Instrumentation & Loudness Jumps:**
- **Gradual Instrumentation Changes**: Never jump from 2 instruments to 5 between adjacent clips. Add or remove instruments incrementally across clips. If the arrangement plan requires a large instrumentation change, insert a transitional clip in between.
- **Loudness Consistency**: Use density and arrangement state descriptions to indirectly control loudness across clips (e.g., `intimate, gentle arrangement` vs `full, powerful arrangement`).

**Prompt design rules for each clip type:**
- **First Clip (Intro)**: Script the arc from low energy to the target state using timestamps. The state at the end must match the 0s state of the next clip.
- **Middle Clips**: Script the arrangement using timestamps. The state at 0s must match the ending state of the previous clip. The state at the end must match the beginning state of the next clip.
- **Last Clip (Outro)**: Script the decay from the current energy level using timestamps. The state at 0s must match the ending state of the previous clip.

### Step 4: Post-Processing
Use `ffmpeg` via the shell tool to apply crossfades between the clips. With precise state alignment via timestamps, shorter crossfades (0.5-1s) are usually sufficient. Calculate the crossfade duration to align with the beat grid based on the BPM (e.g., at 120 BPM, 1 beat = 0.5s, so a 2-beat crossfade = 1.0s).
