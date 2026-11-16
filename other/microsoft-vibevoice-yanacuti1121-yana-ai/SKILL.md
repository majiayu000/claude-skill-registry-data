---
name: microsoft--vibevoice
description: "Microsoft VibeVoice — open-source Voice AI: ASR 7B (60-min audio 1 pass, 50+ ngôn ngữ), TTS 1.5B (90-min, 4 speakers), Realtime 0.5B (300ms latency). HuggingFace."
allowed-tools: Bash, Read, Write
user-invocable: true
---

VibeVoice: bộ 3 model voice AI open-source của Microsoft Research — ASR dài hạn, TTS đa người nói, Realtime streaming.

## 3 Models

```
VibeVoice-ASR (7B)
  - 60-minute long-form audio trong 1 pass
  - Speaker identification + timestamps
  - 50+ languages + custom hotwords

VibeVoice-TTS (1.5B)
  - 90-minute speech synthesis
  - Tối đa 4 distinct speakers
  - English, Chinese, multilingual

VibeVoice-Realtime (0.5B)
  - Streaming với ~300ms latency
  - Robust lên đến 10 phút
  - Lightweight deployment
```

## Architecture

```
Continuous Speech Tokenizers
  Acoustic tokenizer  — audio quality preservation
  Semantic tokenizer  — contextual understanding
  Frame rate: 7.5 Hz  — ultra-low, efficient cho long sequences

Generation:
  LLM — understand text context + dialogue flow
  Diffusion head — generate high-fidelity acoustic details
```

## Access

```python
# HuggingFace
from transformers import pipeline

# ASR
asr = pipeline("automatic-speech-recognition",
               model="microsoft/VibeVoice-ASR-7B")
result = asr("long_audio.wav")

# TTS
tts = pipeline("text-to-speech",
               model="microsoft/VibeVoice-TTS-1.5B")
audio = tts("Hello, this is VibeVoice.")
```

## Playgrounds

- ASR: aka.ms/vibevoice-asr
- Colab notebooks: HuggingFace model pages
- Interactive demo: HuggingFace Spaces

## Khi nào dùng

- Transcribe meeting/podcast dài (>30 min) với speaker diarization
- TTS multi-speaker cho audiobook, dialog synthesis
- Real-time voice interface với latency thấp
- Alternative cho Whisper khi cần long-form hoặc multi-speaker

## Source

https://github.com/microsoft/VibeVoice · MIT · +216⭐ today
