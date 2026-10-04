---
name: qwen3-tts
description: Adapt voice cues into Qwen3 TTS custom-voice, voice-design, or voice-clone inputs, preserving exact dialogue, language, character voice identity, delivery instruction, and reusable clone references.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Qwen3 TTS Prompting

## Choose mode

### CustomVoice

Use a supported predefined speaker plus optional natural-language `instruct` control for delivery.

Required fields: `text`, `language`, `speaker`. Optional: `instruct`.

### VoiceDesign

Use the 1.7B VoiceDesign model to create a new voice from a natural-language description.

Required fields: `text`, `language`, `instruct`.

The instruction should describe audible traits such as approximate vocal age, register, timbre, cadence, articulation, breath, accent only when decided, and delivery behavior. Avoid visual personality traits that cannot be heard.

### VoiceClone

Use a Base model with reference audio. For highest identity consistency, provide `ref_audio` and accurate `ref_text`. Speaker-vector-only mode can work without reference text but may reduce cloning fidelity.

For an invented recurring character, a practical pipeline is:

1. VoiceDesign a clean short reference.
2. Save the exact reference transcript.
3. Build a reusable clone prompt from that reference.
4. Generate later lines from the reusable clone identity.

## Output

Save one JSON object per cue under `04_generation/prompts/qwen3-tts/` or a JSONL batch with exact screenplay text.

## Rules

- Never paraphrase a screenplay line without updating the screenplay.
- State language explicitly when known.
- Keep delivery instructions playable and audible.
- Preserve one `VOICE-###` mapping per recurring character.

## Done

Every output contains enough information to reproduce the intended speaker identity and exact line without reading the screenplay again.
