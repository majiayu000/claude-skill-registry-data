---
name: xai_tts
description: Use when the user asks to generate speech, text-to-speech, audio narration, voice output, or TTS with xAI/Grok through a Grok-connected xAI TTS tool.
---

# xAI TTS

Use this skill to generate speech audio through the Grok-connected xAI TTS tool.

## Preferred Grok Tool Flow

1. Use `search_tool` to discover the available tool schema first:

```json
{
  "query": "xai tts"
}
```

2. Call the returned xAI TTS MCP tool with the schema it reports. A typical payload is:

```json
{
  "input": "Hello from Grok.",
  "voice_id": "eve",
  "language": "auto",
  "codec": "mp3"
}
```

## Options

- `input`: required text to speak.
- `voice_id`: optional voice, commonly `eve` when supported.
- `language`: optional language, commonly `auto` when supported.
- `codec`: optional output codec.

Return the content type and explain where the audio artifact or base64 payload appears in the tool output.

## Credential Safety

Use existing Grok/xAI credentials exposed by the host or MCP server. Never print, quote, summarize, or store OAuth tokens, refresh tokens, bearer tokens, or API keys.
