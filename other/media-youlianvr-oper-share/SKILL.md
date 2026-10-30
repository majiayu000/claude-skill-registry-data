---
name: media
description: >-
  Audio, image and video work: text-to-speech through an OpenAI-compatible
  endpoint (with a Russian fallback), audio/video transcription, image generation
  and editing, quick ffmpeg screenshot demo videos (while HyperFrames handles
  motion graphics and promos), YouTube transcript/content extraction, and the
  4-stage novel-* short-drama pipeline.
---

# media — speech, image, video, and story production

> Home branch in Memora: `root/skill/media`.
>
> For motion graphics, animated explainers, and product promos, use the
> `hyperframes` skill first; use `parts/demo-video/` here when you need a fast
> `ffmpeg` stitch of existing screenshots with TTS narration.

## Choosing a part

| Task | Part |
|---|---|
| Russian & multilingual TTS fallback (`edge-tts` / local pipeline, default voice path) | `parts/ru-tts-fallback/` |
| Speech synthesis via an OpenAI-compatible `/v1/audio/speech` endpoint | `parts/speech/` |
| Audio/video transcription to text | `parts/transcribe/` |
| Generate or edit images via `scripts/generate.py` (a local gateway or provider keys from the root `.env`) | `parts/image-generation/` |
| Fast `ffmpeg` + `edge-tts` video stitch from HTML scenes or screenshots | `parts/demo-video/` |
| Extract transcripts from YouTube videos | `parts/youtube-transcripts/` |
| Extract full structured content from YouTube videos | `parts/youtube-full/` |
| Short-drama stage 1: adaptation brief, cast, hook/beat table → `outline.json` | `parts/novel-outline/` |
| Short-drama stage 2: character profiles, image/voice prompts, character sheets | `parts/novel-characters/` |
| Short-drama stage 3: scene sets, consistency anchors, lighting variants | `parts/novel-art/` |
| Short-drama stage 4: timed screenplay with dialogue and beat flows → `script.json` | `parts/novel-script/` |

## Rules

- Walk `root/skill/media` in Memora before starting; record working voice/image models and pipeline parameters as nodes.
- Route TTS and image calls through the OpenAI-compatible base URL in the root
  `.env` (`OPENAI_API_BASE` and its key). Never pay or create an external account
  without the owner's approval through the host's question channel.
- Save generated images, audio, and video inside the target project's directory, and open the deliverable for the owner with `reveal_file`.

## Related

`ai-image-prompts-skill` (prompt engineering and style libraries), `decks` (slide presentations), `design` (visual composition).
