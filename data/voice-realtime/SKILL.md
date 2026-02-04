---
name: voice-realtime
description: Real-time voice AI knowledge including STT and TTS providers, LiveKit Agents plugins, and voice pipeline patterns. Use when working with speech-to-text, text-to-speech, voice agents, LiveKit, or any voice-related infrastructure.
---

# Real-time Voice AI

Knowledge for building real-time voice agents with STT/TTS providers and LiveKit Agents.

## Provider Selection

See [stt-providers.md](stt-providers.md) for speech-to-text comparison.

See [tts-providers.md](tts-providers.md) for text-to-speech comparison.

## LiveKit Integration

See [livekit-plugins.md](livekit-plugins.md) for plugin usage and code patterns.

## Quick Decision Matrix

| Requirement | STT | TTS |
|-------------|-----|-----|
| Korean + Accuracy | OpenAI gpt-4o-transcribe | Google Cloud TTS |
| Korean + Low latency | Deepgram Nova-3 | ElevenLabs |
| Korean specialty | CLOVA | Google Cloud TTS |
| Cost-sensitive | Deepgram Nova-3 | Google Cloud TTS |
| Best quality | OpenAI gpt-4o-transcribe | ElevenLabs |
| Lowest latency | Deepgram Nova-3 | Cartesia |
