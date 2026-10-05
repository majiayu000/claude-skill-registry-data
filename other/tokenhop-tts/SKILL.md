---
name: tokenhop-tts
description: Text-to-speech via tokenhop /v1/audio/speech using OpenAI / ElevenLabs / Deepgram / Edge TTS / Google TTS / Hyperbolic / Inworld voices. Use when the user wants to convert text to speech, generate audio, voiceover, narrate, or read text aloud.
---

# tokenhop — Text-to-Speech

Requires `TOKENHOP_URL` (and `TOKENHOP_KEY` if auth enabled). See <https://raw.githubusercontent.com/tokenhop/tokenhop/refs/heads/master/skills/tokenhop/SKILL.md> for setup.

If they are unset, use the legacy `NINEROUTER_URL` / `NINEROUTER_KEY` instead. <!-- legacy(9router): remove in v2 -->

## Discover

```bash
# 1) List models
curl $TOKENHOP_URL/v1/models/tts | jq '.data[].id'
# 2) Per-model metadata (params, voicesUrl if voice-by-id)
curl "$TOKENHOP_URL/v1/models/info?id=el/eleven_multilingual_v2"
# 3) List voices (elevenlabs, edge-tts, deepgram, inworld, local-device). Optional ?lang=vi
curl "$TOKENHOP_URL/v1/audio/voices?provider=edge-tts&lang=vi" | jq '.data[].model'
```

`model` field in `/v1/audio/speech` = voice ID directly (e.g. `edge-tts/vi-VN-HoaiMyNeural`, `el/<voice_id>`, or `openai/tts-1` model+default voice).

## Endpoint

`POST $TOKENHOP_URL/v1/audio/speech`

| Field             | Required | Notes                                                                                                       |
| ----------------- | -------- | ----------------------------------------------------------------------------------------------------------- |
| `model`           | yes      | voice ID from `/v1/models/tts`                                                                              |
| `input`           | yes      | text to speak                                                                                               |
| `voice`           | no       | used only when `model` has no voice (`openai`, `selfhosted-tts`)                                            |
| `response_format` | no       | audio codec `mp3`, `opus`, `aac`, `flac`, `wav`, `pcm` (`openai`, `selfhosted-tts`); anything else is a 400 |

The query `?response_format=mp3` (the default, raw bytes) or `?response_format=json` (`{audio: base64, format}`) picks the response envelope. The body `response_format` picks the codec.

## Examples

Save MP3:

```bash
curl -X POST "$TOKENHOP_URL/v1/audio/speech" \
  -H "Authorization: Bearer $TOKENHOP_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"openai/tts-1","input":"Hello world"}' \
  --output speech.mp3
```

JS (save file):

```js
import { writeFile } from "node:fs/promises";
const r = await fetch(`${process.env.TOKENHOP_URL}/v1/audio/speech`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.TOKENHOP_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ model: "el/eleven_multilingual_v2", input: "Xin chào" }),
});
await writeFile("speech.mp3", Buffer.from(await r.arrayBuffer()));
```

## Response shape

Default → raw audio bytes (Content-Type `audio/mp3`).

`?response_format=json`:

```json
{ "audio": "SUQzBAAAA...", "format": "mp3" }
```

## Provider quirks (model format)

| Provider                                  | `model` format                                         | Notes                                                       |
| ----------------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------- |
| `openai`                                  | `tts-1/alloy`, `tts-1` (+ body `voice`), or just voice | Default model `gpt-4o-mini-tts`                             |
| `elevenlabs`                              | `<model_id>/<voice_id>` or `<voice_id>`                | Default model `eleven_flash_v2_5`; list voices in Dashboard |
| `openrouter`                              | `openai/gpt-4o-mini-tts[/alloy]` (+ body `voice`)      | Or bare voice; streamed via chat-completions audio          |
| `edge-tts`                                | voice id e.g. `vi-VN-HoaiMyNeural`                     | **noAuth**; default `vi-VN-HoaiMyNeural`                    |
| `google-tts`                              | language code e.g. `en`, `vi`                          | **noAuth**                                                  |
| `local-device`                            | OS voice name (`say -v ?` / SAPI)                      | **noAuth**; needs `ffmpeg`                                  |
| `deepgram`                                | `aura-asteria-en` etc                                  | Token auth                                                  |
| `nvidia`, `inworld`, `cartesia`, `playht` | `model/voice`                                          | Provider-specific auth header                               |
| `coqui`, `tortoise`                       | speaker / voice id                                     | Localhost noAuth                                            |
| `hyperbolic`                              | model id                                               | Body = `{text}` only                                        |
