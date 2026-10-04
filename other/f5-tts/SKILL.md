---
name: f5-tts
description: Use the local F5TTS-FASTAPI service for voice-cloned text-to-speech, voice discovery, and direct synthesis. Trigger when working with the user's local F5 TTS Docker service, listing available voice profiles, validating health or auth, generating speech in a specific cloned voice, or using the F5 API independently of Hermes' built-in text_to_speech provider.
metadata:
  hermes:
    tags: [TTS, F5, Voice Cloning, FastAPI, Audio]
---

# f5-tts

Use this skill when the task is specifically about the user's local F5 TTS server or when you need to choose a voice profile directly instead of relying on Hermes' default `text_to_speech` configuration.

## Core workflow

1. Check the service first with `GET /health`.
2. Read the base URL from `tts.f5.base_url` in `~/.hermes/config.yaml` when available. Default to `http://localhost:8081`.
3. Use the already-loaded environment variable `F5TTS_SECRET_KEY` when you need to authenticate directly.
4. Generate a short-lived HS256 bearer token from that env value.
5. Call `GET /api/v1/voices/list` to discover valid `voice_profile` names instead of guessing.
6. Call `POST /api/v1/tts/synthesize` with exact user text plus the selected `voice_profile`.
7. Save the returned WAV bytes to disk and return the file path or `MEDIA:` tag as needed.

## Preferred behavior

- Prefer the built-in Hermes `text_to_speech` tool when the user simply wants speech output and the configured default voice is fine.
- Prefer direct F5 API use when the user wants to inspect voices, pick a specific cloned voice, debug the local TTS service, or bypass Hermes' default provider selection.
- Preserve the user's text exactly unless they asked for rewriting.
- For long text, keep the FastAPI request body within the service limit by chunking and stitching rather than relaxing validation.
- Do not ask the user for the secret key if `F5TTS_SECRET_KEY` is already present in the environment.

## Long text

- The local F5 FastAPI endpoint accepts `text` up to 1000 characters per request.
- For text longer than that, split on sentence boundaries when possible.
- If a sentence still exceeds the limit, split on whitespace, then hard-split only as a last resort.
- Synthesize each chunk separately and concatenate the WAV files in order.
- For Telegram voice bubbles, convert the final WAV to OGG Opus after stitching.

## Failure handling

- If `/health` fails, report that the local F5 container is unavailable before trying anything else.
- If auth fails, first check whether `F5TTS_SECRET_KEY` is already present in the environment and use it before asking the user for anything.
- If auth still fails after using the env var, verify `F5TTS_SECRET_KEY` matches the FastAPI container `SECRET_KEY`.
- If a requested voice is missing, list available voices from `/api/v1/voices/list`.
- If synthesis fails on long text, retry with shorter chunks instead of sending a larger single request.

## Reference file

- Load `references/api.md` when you need exact endpoint shapes, token generation snippets, or direct request examples.
