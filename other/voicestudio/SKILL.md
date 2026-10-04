---
name: voicestudio
description: Neural TTS voice cloning, design, and audio DSP
---

# VoiceStudio

Operates the user's running [VoiceStudio](https://github.com/Osama-Alzahrani-UQU/Voice-Studio-TTS) / [debpalash VoiceStudio](https://github.com/debpalash/VoiceStudio) suite powered by k2-fsa OmniVoice and Coqui XTTS v2.

## Capabilities & Workspaces
- **Speech Synthesis**: 600+ languages with neural diffusion and broadcast DSP mastering (`broadcast`, `podcast`, `warm`, `bright`, `raw`).
- **Voice Design**: Interactive attribute prompt generation (gender, age bracket, pitch, style, accent).
- **Voice Cloning**: Zero-shot reference voice conditioning from clean 3-10s audio samples.
- **Model Context Protocol (MCP)**: Native tools for AI agents mounted on stdio or HTTP/SSE port `3900`.
- **Desktop Application**: Bidirectional GUI in `E:\Projects_D\LocalTTS_App\main.py`.

## Quick Execution via CLI
```sh
# OmniVoice 600+ languages with broadcast mastering
python E:/Projects_D/LocalTTS_App/cli_synthesizer.py --text "Hello world" --engine omnivoice --output out.wav

# Arabic speech synthesis
python E:/Projects_D/LocalTTS_App/cli_synthesizer.py --text "مرحباً بكم في استوديو الصوت" --lang ar --output arabic.wav
```

## MCP Tools Exposed
- `synthesize_speech(text, engine, language, speaker_or_instruct, speed, dsp_preset)`
- `clone_voice(ref_audio_path, speaker_id, text, engine)`
- `list_voices(engine)`
- `list_dsp_presets()`
- `check_system_status()`

## Attribution
Built on research and open-source foundations from Palash Deb (`debpalash/VoiceStudio`), k2-fsa (`k2-fsa/OmniVoice`), Coqui AI (`coqui-ai/TTS`), and maintained by Osama Alzahrani.
