---
name: moneyprinter
description: >
  Generate short videos automatically from a topic or custom script.
  Uses MoneyPrinterTurbo to write scripts, select B-roll footage, synthesize TTS audio, and render subtitles.
version: 1.0.0
author: harry0703
triggers:
  - generate video
  - create a short video
  - make a TikTok
  - video script generation
  - money printer turbo
capabilities:
  - video-generation
  - video-scripting
  - subtitle-rendering
  - B-roll-retrieval
---

# MoneyPrinterTurbo Skill

This skill allows the agent to generate AI-synthesized short videos based on user topics or custom scripts using `MoneyPrinterTurbo`.

## Invocation

Run `python cli.py` inside the `MoneyPrinterTurbo` module path.

### Command Example

```bash
python apps/statenour/lib/ai/moneyprinter/cli.py --video-subject "Why Exercise is Important" --video-aspect "9:16"
```

## Options
*   `--video-subject` (required): The topic/keyword of the video.
*   `--video-script` (optional): Custom script text. Bypass AI script generation.
*   `--video-aspect` (optional): Aspect ratio, e.g., `"9:16"` (portrait) or `"16:9"` (landscape). Defaults to `"9:16"`.
*   `--video-language` (optional): Script language code, e.g., `"en"` or `"zh"`.
*   `--video-source` (optional): B-roll material source, e.g., `"pexels"`, `"pixabay"`, `"coverr"`, `"local"`. Defaults to `"pexels"`.
*   `--paragraph-number` (optional): Paragraph count (1-10) for script segment generation.
*   `--video-clip-duration` (optional): Duration of B-roll clips in seconds.
