---
name: text-to-speech
description: Convert text into a natural-sounding audio file via the LemonFox TTS API. Use this skill whenever the user wants to synthesize speech, generate voice audio from text, create narration for a blog or video, or add voice feedback to an app.
license: MIT
---

# Text-to-Speech

## Overview

Converts text into a synthesized speech audio file using the LemonFox TTS API, with support for custom voice types and output formats. Suitable for use cases such as voice feedback in chat apps, blog narration, and video voiceovers.

| Property | Value |
|----------|-------|
| Endpoint | `POST https://app-dohnbj5by5mp-api-GYX1lzGw01Xa.gateway.appmedo.com/v1/audio/speech` |
| Auth | Bearer Token (platform_managed) |
| Request Format | `application/json` |
| Response Format | Binary audio file (`application/octet-stream`) |
| Billing | Billed per request |

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `input` | `string` | Yes | The text content to convert to speech |
| `voice` | `string` | Yes | Voice type, e.g.: `heart` |
| `response_format` | `string` | No | Output audio format, e.g.: `mp3`, `wav`, `ogg` |

### Response

The endpoint directly returns **binary audio file content**, with response header `Content-Type: application/octet-stream`. There is no JSON wrapper — the response body is the audio file itself.

> For complete parameter details and code, see `references/speech-api.md`.

---

## Generation-time Usage (Agent Direct Call)

Use the built-in script for generation-time calls. The script reads `INTEGRATIONS_API_KEY` from the environment, calls the upstream API, and saves the returned binary audio to the file given by `--output`.

**The Bash tool timeout MUST be set to 600000ms (600 seconds).**

```bash
python3 <skill-path>/scripts/call_text_to_speech.py \
  --input "Hello, world!" \
  --voice heart \
  --response-format mp3 \
  --output /tmp/output.mp3
```

On success it prints one JSON line to stdout, e.g. `{"status":"succeed","file":"/tmp/output.mp3","bytes":12345}`. On failure it prints an error to stderr and exits with a non-zero code. After the file is saved, tell the user the path and how to play it.

> For complete parameter details, see the "Generation-time Usage" section in `references/speech-api.md`.

---

## Post-generation Usage (In-app via Edge Function)

In an application, requests are proxied through an Edge Function. The Edge Function stores the binary audio stream to Supabase Storage and returns a persistent public URL to the frontend.

> For complete Edge Function code and frontend call patterns, see the "Post-generation Usage" section in `references/speech-api.md`.
