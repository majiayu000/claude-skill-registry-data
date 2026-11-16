---
name: openbmb--voxcpm
description: "Tokenizer-Free TTS multilingual — speech generation, creative voice design, true-to-life voice cloning. 25K stars."
allowed-tools: Bash, Read, Write
user-invocable: true
---

VoxCPM2: Tokenizer-Free TTS cho multilingual speech generation, creative voice design, và voice cloning.

## Install

```bash
pip install voxcpm
```

## Quick start

```python
from voxcpm import VoxCPM

model = VoxCPM.from_pretrained("openbmb/VoxCPM2")

# Text to speech
audio = model.synthesize("Hello, world!", lang="en")

# Voice cloning
audio = model.clone_voice(reference_audio="speaker.wav", text="Your text here")

# Multilingual
audio = model.synthesize("Xin chào", lang="vi")
```

## Features

- Tokenizer-free architecture — faster inference
- 20+ languages including Vietnamese
- Voice cloning từ reference audio
- Creative voice design (style control)

## Source

https://github.com/OpenBMB/VoxCPM · ⭐25.5K
https://huggingface.co/openbmb/VoxCPM2
