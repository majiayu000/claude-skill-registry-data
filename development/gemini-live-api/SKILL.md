---
name: gemini-live-api
description: Expert developer skill for implementing real-time voice and video interactions using the Google Gemini Live API. This skill should be used when implementing bidirectional audio streaming, voice conversations with interruption handling, real-time transcription, function calling in live sessions, session management, or voice customization.
---

# Gemini Live API Developer Skill

## Overview

The Gemini Live API enables low-latency, real-time voice and video interactions with Gemini models. This skill provides comprehensive guidance for implementing natural voice conversations, handling interruptions, integrating tools and function calling, managing sessions, and customizing voice output.

## When to Use This Skill

Use this skill when:
- Implementing real-time two-way voice conversations between AI and users
- Building voice agents that can be interrupted naturally mid-response
- Adding function calling and real-time web search to live voice sessions
- Implementing text-to-speech with natural cadence and tone
- Debugging audio streaming issues or session management problems
- Customizing voice characteristics (cadence, tone, style, language)
- Managing WebSocket connections, session resumption, or context compression
- Implementing ephemeral tokens for client-side authentication

## Core Capabilities Covered

- **Bidirectional Audio Streaming**: 16kHz PCM input, 24kHz output with real-time processing
- **Voice Activity Detection (VAD)**: Automatic or manual speech detection with interruption handling
- **Function Calling**: Tool integration with async execution and scheduling parameters
- **Session Management**: Connection lifecycle, resumption tokens, context compression
- **Voice Customization**: Multiple voices, speech configuration, natural prosody
- **Audio Processing**: PCM encoding/decoding, sample rate conversion, queue management
- **Security**: Ephemeral tokens for production client-to-server implementations

## How to Use This Skill

### For Quick Reference

Start with `references/api-overview.md` for endpoints, authentication, models, and limitations.

### For Specific Implementation Tasks

**Implementing Voice Conversations:**
1. Review `references/audio-handling.md` for audio specifications and streaming strategies
2. Use `scripts/audio_utils.py` for PCM encoding/decoding utilities
3. Reference `references/architecture-patterns.md` for complete implementation approaches

**Handling Interruptions:**
Check `references/audio-handling.md` for VAD configuration and interruption patterns.

**Adding Function Calling:**
See `references/function-calling.md` for tool declarations, response handling, and async execution patterns.

**Customizing Voices:**
`references/voice-customization.md` provides comprehensive guidance on:
- Available voices and their personalities
- Making voices sound natural
- Adjusting cadence, pitch, and tone
- Language and multilingual support

**Managing Sessions:**
Review `references/session-management.md` for lifecycle management, resumption tokens, and graceful shutdown.

**Production Best Practices:**
Check `references/best-practices.md` for error handling, optimization, and common pitfalls.

### Audio Utilities

The `scripts/audio_utils.py` module provides reusable functions for:
- Converting between numpy arrays, bytes, and base64 for PCM audio
- Sample rate conversion (16kHz input ↔ 24kHz output)
- Audio chunk management for gap-free playback
- Format conversions for different Python audio libraries (pyaudio, sounddevice)

Import and use these utilities in your implementation to avoid rewriting common audio processing code.

### Working Example

For a complete working implementation, reference the ai-news-app repository which demonstrates:
- Bidirectional audio streaming with interruption handling
- Real-time transcription display
- Audio playback scheduling without gaps
- Session management and cleanup
- Browser-based implementation using the JavaScript SDK

## Key Technical Considerations

**Audio Format Requirements:**
- Input: 16-bit PCM, 16kHz, mono (`audio/pcm;rate=16000`)
- Output: 24kHz sample rate
- Real-time processing with minimal latency

**Session Limits:**
- Audio-only: 15 minutes without compression (unlimited with compression)
- Audio+video: 2 minutes without compression
- WebSocket connections: ~10 minutes maximum
- Context window: 128k tokens (native audio), 32k (half-cascade)

**Response Modalities:**
Can only set ONE modality per session - either TEXT or AUDIO, not both simultaneously.

**Production Security:**
Always use ephemeral tokens for client-to-server implementations. Never expose API keys in client-side code.

## Reference Documentation

All reference files contain detailed technical information with code examples in both Python and JavaScript:

- `api-overview.md` - Endpoints, authentication, models, limitations
- `audio-handling.md` - Audio specs, VAD, interruptions, streaming
- `function-calling.md` - Tool integration and async execution
- `session-management.md` - Lifecycle, resumption, compression
- `voice-customization.md` - Voices, speech config, natural prosody
- `best-practices.md` - Production patterns and optimization
- `architecture-patterns.md` - Implementation approaches with examples

## Additional Resources

- Official Documentation: https://ai.google.dev/gemini-api/docs/live
- Python SDK: `google-genai` package
- JavaScript SDK: `@google/genai` package
- Interactive Demo: Google AI Studio
- Example Implementation: ai-news-app repository
