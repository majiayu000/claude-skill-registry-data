---
name: youtube-transcript
description: Use when an agent needs to extract a verbatim transcript from a public YouTube video or YouTube Shorts URL. Provides a Gemini-based transcript retrieval workflow, secure API-key handling pattern, output format, troubleshooting, and verification steps.
version: 1.0.0
author: Tony Semana
license: MIT
metadata:
  hermes:
    tags: [research, youtube, transcript, gemini, video]
    related_skills: []
---

# YouTube Transcript

## Overview

Extract verbatim transcripts from YouTube videos, including Shorts, using the Google Gemini API. This skill is intended for research workflows where a user provides a YouTube URL and wants the video content converted into markdown text with lightweight source metadata.

The bundled script sends the YouTube URL to Gemini as a video URI and asks for transcript text only. It can print to stdout, write to an explicit file, or auto-save a markdown transcript to an output directory.

## When to Use

Use this when:
- The user asks to “get a YouTube transcript,” “transcribe this YouTube video,” or “get the transcript of this video.”
- The user provides a YouTube or YouTube Shorts URL and wants its spoken content as text.
- The desired output is a research/reference transcript, not a polished summary.

Do not use this when:
- The user wants a summary rather than a transcript. Get the transcript first, then summarize separately.
- The video is private, unavailable, age-restricted, or otherwise inaccessible to Gemini.
- The content is sensitive and should not be sent to a hosted model provider.

## Prerequisites

Required:
- Python 3.10+.
- `google-genai` Python package.
- A Gemini API key available as `GEMINI_API_KEY`.

Recommended local setup from this skill directory:

```bash
python3 -m venv .venv
.venv/bin/pip install google-genai
```

For secret injection, use your environment's normal secure secret manager. A generic Varlock template is included at `templates/env.schema.example`; copy or adapt it locally if your Hermes setup uses Varlock:

```bash
cp templates/env.schema.example .env.schema
# edit .env.schema for your secret manager
```

Do not commit a populated `.env`, local `.env.schema` with private account paths, API keys, OAuth tokens, or credential dumps.

## Usage

From this skill directory:

```bash
GEMINI_API_KEY="$GEMINI_API_KEY" .venv/bin/python3 scripts/get_transcript.py "YOUTUBE_URL"
```

With Varlock, after creating a local `.env.schema`:

```bash
varlock run -- .venv/bin/python3 scripts/get_transcript.py "YOUTUBE_URL"
```

### Options

| Flag | Description |
|---|---|
| `--model MODEL` | Gemini model to use. Defaults to `GEMINI_MODEL` or `gemini-2.5-flash`. |
| `-o FILE`, `--output FILE` | Save transcript to a specific file path. |
| `--stdout` | Print transcript to stdout instead of saving to file. |

### Default output behavior

When neither `--output` nor `--stdout` is specified, the transcript is auto-saved to:

```text
~/transcripts/youtube/YYYYMMDD_VIDEOID.md
```

Override this with:

```bash
TRANSCRIPT_OUTPUT_DIR=/path/to/transcripts .venv/bin/python3 scripts/get_transcript.py "YOUTUBE_URL"
```

## Output Format

The script writes markdown with YAML frontmatter:

```markdown
---
source: https://www.youtube.com/watch?v=...
model: gemini-2.5-flash
date: 2026-03-22T12:00:00Z
---

Verbatim transcript text here.
```

## Procedure

When a user provides a YouTube URL and asks for a transcript:

1. Confirm the URL is a YouTube or YouTube Shorts URL.
2. Work from this skill directory so relative paths resolve correctly.
3. Ensure `google-genai` is installed in `.venv` or the active Python environment.
4. Ensure `GEMINI_API_KEY` is present through environment variables or secure secret injection.
5. Run `scripts/get_transcript.py` with the URL.
6. Use `--stdout` if the user wants the transcript in the chat, `-o` if they provided a target path, or the default auto-save behavior for normal research capture.
7. If the API call fails, consult `references/troubleshooting.md`.
8. Report the output path and model used. Do not print secret values.

## Common Pitfalls

1. **Publishing local credential wiring.** Keep local `.env`, machine-specific `.env.schema`, Keychain item names, and 1Password paths out of the repo. Use `templates/env.schema.example` as a generic starter only.
2. **Assuming every YouTube URL is accessible.** Private, deleted, age-restricted, geo-blocked, or very long videos may fail through Gemini.
3. **Overwriting transcripts accidentally.** Auto-saved filenames include the current date and video ID, but explicit `--output` paths overwrite by design.
4. **Treating Gemini output as legally perfect caption extraction.** This workflow asks Gemini to produce a verbatim transcript from the video. For regulated or legal work, verify against source media.
5. **Using a hosted model for sensitive content.** YouTube URLs and extracted content are sent to Gemini. Do not use this path for sensitive, private, or proprietary recordings.

## Verification Checklist

- [ ] `SKILL.md` has lowercase `name: youtube-transcript` and valid frontmatter.
- [ ] `scripts/get_transcript.py` runs with `--help`.
- [ ] No `.venv`, `.git`, `.DS_Store`, `.env`, local `.env.schema`, raw chat logs, or credentials are included in the published skill directory.
- [ ] `python3 scripts/validate_skills.py` passes from the repo root.
- [ ] A known public YouTube URL can produce either stdout output or a markdown file when `GEMINI_API_KEY` is configured.
