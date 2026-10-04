---
name: video-dubbing
description: "Reference for the studio/dubbing service — the Kurdish Sorani to Iraqi Arabic video dubbing pipeline. Use this for any task involving audio/video processing, Demucs, transcription, translation prompts, TTS providers, or FFmpeg reassembly. Covers which TTS providers are licensed for client work and which are not."
---

# Video Dubbing Pipeline — Kurdish Sorani → Iraqi Arabic

## Pipeline Overview

```
Original video
  → 0. Demucs: separate vocals from background music/SFX
  → 1. Gemini: transcribe Sorani vocals, chunked by sentence/pause, with timestamps
  → 2. MiniMax (LLM): translate each chunk to Iraqi Arabic dialect, per the spec below
  → 3. TTS: generate Iraqi Arabic speech per chunk (MiniMax now, Chatterbox later)
  → 4. FFmpeg: align dubbed speech to original timestamps, remix with the
       preserved background track from step 0, optionally burn in Arabic SRT
```

Base/reference implementation: fork `pyvideotrans` (github: jianchang512/pyvideotrans) and run it in CLI/headless mode — no dashboard needed. It already has Claude and MiniMax integrations and handles the FFmpeg reassembly. Steps 0–2 below are largely custom and replace its default ASR/translation.

## Step 0 — Audio Separation (Demucs)

Run BEFORE transcription. Splits the original audio into:
- `vocals.wav` — speech only → goes through steps 1–3
- `background.wav` — music/SFX/ambience → preserved untouched, mixed back in at step 4

Without this step, the final dub loses all original music/ambience because the whole audio track gets replaced. This is the single highest-impact addition to the pipeline.

## Step 1 — Transcription (Gemini)

- Input: `vocals.wav`
- Whisper's Kurdish Sorani support is weak — Gemini's broader multilingual exposure tends to do better on low-resource languages
- **Chunk by natural sentence/pause boundaries, not fixed time windows.** Ask Gemini to return segments as `{ text, start_time, end_time }` at natural breaks. Fixed-interval chunking cuts mid-sentence and degrades both translation quality and dub timing.
- A custom Sorani ASR model is in development separately — when ready, it slots in here as a drop-in replacement for this step (same input/output contract: vocals.wav → list of timestamped chunks).

## Step 2 — Translation (MiniMax LLM)

- Input: each chunk's Sorani text + its duration (start_time/end_time)
- Output: Iraqi Arabic (عربي عراقي) text for that chunk
- System prompt must specify:
  - Target dialect: Iraqi Arabic, not MSA
  - Match the tone/register of the source (casual vs formal)
  - Keep translated text roughly speakable within the original chunk's duration (TTS timing depends on this)
- **This is the highest-leverage step in the entire pipeline** — every downstream step inherits translation quality, and no model was trained specifically for Sorani→Iraqi Arabic. Use `memory/` (see subagent memory) to record which prompt phrasings produced good vs bad translations for specific content types (casual dialogue vs narration vs product descriptions), and refine the system prompt over time.
- For new content types, consider spot-checking a sample chunk through Claude as well — Claude tends to be strong on dialect/register nuance — and compare against MiniMax's output to calibrate the MiniMax prompt.

## Step 3 — Text to Speech

| Provider | Status | When to use |
|---|---|---|
| **MiniMax TTS** | ✅ Use now | Same account as translation (step 2), zero new setup, commercially licensed for client work. Default for launch. |
| **Chatterbox (Resemble AI)** | Self-host later | Permissive license, ElevenLabs-tier quality, supports Arabic, voice cloning. Ships with its own Gradio UI — that Gradio UI is your "dashboard." Use once volume justifies the self-hosting effort, to cut per-minute TTS costs. |
| **Fish Audio / Fish Speech** | ❌ Do not use for this project | Fish Audio's Research License covers research and non-commercial use only — commercial use (including any client work) requires a separate license from `business@fish.audio`. Self-hosting and rebranding does NOT change this — it remains a license violation regardless of branding. Do not build any part of this pipeline around Fish unless/until a commercial license is actually obtained. |

Both MiniMax and Chatterbox sit behind the AI Gateway's `/ai/tts` endpoint (see `ai-gateway` skill) — switching between them is a one-line config change, not a code change.

## Step 4 — Reassembly (FFmpeg)

- Concatenate/align the per-chunk TTS audio to the original chunk timestamps
- Mix the aligned dubbed-vocals track with `background.wav` from step 0
- Replace the original video's audio with this mixed track
- Optionally burn in Arabic subtitles (SRT generated from step 2's translated text + timestamps)
- Use `fluent-ffmpeg` (npm) if calling from Node, or `ffmpeg-python` if the dubbing service itself is Python (it is — FastAPI)

## Lip Sync — Explicitly Deferred

Not part of the current pipeline. Most dubbed content ships without it. If revisited later: Wav2Lip (free, open source, needs GPU) or HeyGen API (paid, easier). Do not let this block the audio pipeline.

## Job Tracking

Each dubbing job corresponds to a row in the `dubbing_jobs` table (Supabase) with status (`queued`, `separating`, `transcribing`, `translating`, `synthesizing`, `assembling`, `done`, `failed`) and a `dubbing_chunks` table for per-chunk progress — this lets the upload UI show real progress and lets a failed job resume from the last completed chunk rather than restarting.
