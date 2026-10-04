---
name: transcribe-video
description: Use when the user asks to transcribe a YouTube video or any video URL or local video file, get a video's transcript/captions, or capture "what was said AND what was shown" (slides, codebase, diagrams). Also use when handed a youtube.com / youtu.be / shorts / embed link or a local .mp4/.mov/.mkv to write up.
---

# Transcribe Video (audio + on-screen visual)

## Overview

Capture **both streams** of a video - the **audio** (what's said) and the **visual** (what's on screen: code, slides, diagrams, UI) - then **always offer** to save a sanitized markdown summary into the KB vault. The offer in step 4 is mandatory.

There is ONE flow. Don't treat "transcript" and "video analysis" as separate tools - combine them every time so the summary reflects what was shown, not just what was said.

This skill lives next to the `watch` engine (`skills/watch` in this repo). Install both.

## Resolve the watch scripts directory

Never hardcode a home path.

1. If `CLAUDE_SKILL_DIR` is set, use `$CLAUDE_SKILL_DIR/../watch/scripts`
2. Else use the `scripts/` folder of the sibling `watch` skill next to this `transcribe-video` folder

Call that directory `<watch-scripts>` below.

## Decision: which engine to use

```
Does the user only want the spoken words (talking-head, podcast, no useful on-screen content)?
  → YES: captions-only fast path (Step 1a). Free, instant, no deps.
  → NO / unsure / video shows code, slides, demos, UI: full pipeline (Step 1b). Default.
```

When in doubt, use the full pipeline - the user has said they want on-screen info too.

## Step 1a - Captions-only fast path (optional)

Use the `mcp__youtube-transcript__get_youtube_transcript` tool if that MCP server is configured (YouTube URLs only; text captions, no visuals). If output is saved to a file, Read it. Then go to Step 3.

If that tool is not available, use Step 1b.

## Step 1b - Full pipeline (DEFAULT: audio + visual)

Drive the bundled `watch` pipeline, which downloads the video, extracts **scene-change frames** as JPEGs, and produces a **timestamped transcript** (native captions first, Whisper fallback). Works for URLs (YouTube/Vimeo/TikTok/X/...) **and local files**.

1. **Preflight** (silent on success):
   ```bash
   python3 <watch-scripts>/setup.py --check
   ```
   Needs `ffmpeg`, `yt-dlp`, and a Whisper key (Groq preferred, or OpenAI) for caption-less/local videos. On non-zero exit, run `setup.py` (no `--check`) and, if a key is missing, ask the user via `AskUserQuestion` and write it to `~/.config/watch/.env`. If they decline Whisper, add `--no-whisper` (frames-only when no captions).

2. **Run** (pass the user's reason as `--intent`):
   ```bash
   python3 <watch-scripts>/watch.py "<source>" --intent "<why they want it>"
   ```
   Useful flags: `--start/--end` to focus a section, `--max-frames N` to cap tokens, `--resolution 1024` only when on-screen **text/code must be readable**, `--whisper groq|openai`.

3. **Read the frames.** Read every frame path the script prints (parallel Read calls, single message) - the Read tool renders the JPEGs so you actually see what's on screen. Frames carry `t=MM:SS` so you can align them to the transcript.

> Note: frames cost tokens (~50-80k for 80 frames). For long videos, ask whether to focus a section with `--start/--end` before a full scan. Don't re-run the script for follow-ups in the same session - reuse what's in context.

## Step 2 - Combine the two streams

You now have **frames** (what's shown) + **transcript** (what's said). Read on-screen code/slides/diagrams from the frames and align them to the spoken explanation. This combined understanding feeds both the presentation (Step 3) and the summary (Step 5).

## Step 3 - Present

Output a readable version:
- For a captions-only run: the cleaned transcript (speaker turns if dialogue; fix obvious caption typos and note corrections).
- For a full-pipeline run: the transcript **plus** a short "On screen" pass noting key visuals (e.g. "0:42 - terminal shows `adk app`", "3:10 - slide: sequential-agent diagram", code snippets transcribed from frames).

## Step 4 - ALWAYS ask about the sanitized markdown file (MANDATORY)

**After every video, before ending your turn, ask whether to save a sanitized KB summary.** Every time - even if unprompted, even if short, even if you made one for a previous video this conversation.

Use `AskUserQuestion`, yes/no: "Save a sanitized summary to the KB (key points + on-screen content + what to learn)?" → **Yes** / **No**. Never assume the answer.

## Step 5 - If yes: write the KB summary (with on-screen content)

Write a curated summary page (NOT the raw transcript).

Resolve the vault:

- If `$WATCH_VAULT_DIR` is set and is a directory:
  - notes → `$WATCH_VAULT_DIR/wiki/notes/`
  - media → `$WATCH_VAULT_DIR/wiki/media/{slug}/`
  - update `$WATCH_VAULT_DIR/wiki/_master-index.md` and `_ingest-log.md` if those files exist
- If unset: skip the vault write. Tell the user the summary was not saved and they can set `WATCH_VAULT_DIR`. Offer to write the same markdown to a path they choose.

Other rules:

- **Filename:** descriptive kebab-case slug from the topic (not "<title>-notes"). One page per video.
- Use the template below. **Include an `## On-Screen Content` section** when the full pipeline ran (transcribe code shown, slide contents, diagrams, UI). Omit it for captions-only runs.
- **If the index/log files exist, update them:**
  - `_master-index.md` → add under `## Summaries`: `- [[slug]] — one-line hook (Speaker, YouTube)`
  - `_ingest-log.md` → append: `- <date> — \`transcribe-video\` ingest: [[slug]] — <one line>.`
- Tell the user the full path(s). If the user wants a different location, honor it and skip index/log updates.

## KB summary template

```markdown
---
title: "<Readable Title>"
type: summary
name: <kebab-slug>
date: <YYYY-MM-DD>
source: youtube-transcript | watch-pipeline
source_url: <video URL or local path>
speaker: "<Presenter / speakers>"
last_synced: <YYYY-MM-DD>
staleness: fresh
summary: "<1-2 sentence abstract for search/recall>"
tags: ["<topic>", ...]
---

# <Readable Title>

Curated key points and takeaways - not a raw transcript.
Source: <url/path> · Speaker: <name>

## Key Points
- <sanitized, deduplicated main points - cut sponsor reads, plugs, filler>

## On-Screen Content
- <code shown (transcribed), slide/diagram contents, UI/demos - with timestamps>

## What I Should Learn From This Video
1. <distilled, actionable takeaway>
2. ...
```

Cross-link related vault pages with `[[slug]]`. Use the current date for `date`/`last_synced`.

## Red Flags - you skipped a required step

- Presented a video and ended your turn without asking about the summary (Step 4).
- Used captions-only when the video clearly showed code/slides the user wanted captured (should have used the full pipeline).
- Wrote the summary without an `## On-Screen Content` section after a full-pipeline run.
- Only asked for the first video but not later ones in the same conversation.

All of these mean: go back and do the step. The ask in Step 4 happens after **every** video.
