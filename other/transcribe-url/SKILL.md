---
name: transcribe-url
description: "Download and transcribe any video from a social/web URL using yt-dlp and faster-whisper locally. Outputs a markdown file with metadata plus plain and timestamped transcript. Triggers: transcribe this link, transcribe this url, transcribe this reel, pull transcript from, what does this video say, get the transcript of this video, transcribe-url."
---

> **Video Studio:** this skill lives in `engines/content-os` (Content OS, inside this repo). Before running anything from it, `cd engines/content-os` and use that folder's copy (`.claude/skills/transcribe-url/`), which has its scripts and reference files. Every path below is relative to that folder. This copy only lets Claude find the skill from the Video Studio folder.


# Transcribe URL — yt-dlp + faster-whisper

Pulls audio from any public video URL and transcribes it locally. Zero API cost, runs on the user's local machine. Built for fast research lookups — "what's this competitor reel actually saying?"

## How to Trigger

- **"transcribe this link <url>"** → grab + transcribe + show the transcript
- **"transcribe <url>"** → same
- **"what's this reel saying <url>"** → same, but lead the reply with the gist
- Any social media URL works: YouTube, Instagram Reels/posts, TikTok, X/Twitter, Vimeo, Facebook, LinkedIn, etc.

## The Pipeline (one script, no orchestration)

```bash
bash .claude/skills/transcribe-url/scripts/transcribe-url.sh "<url>"
```

Optional second arg: output directory (defaults to `transcripts/url/`).

That script path is relative to the repo root. If the skill is installed globally (`~/.claude/skills/transcribe-url/`), call `bash ~/.claude/skills/transcribe-url/scripts/transcribe-url.sh "<url>"` instead.

The script picks one of two paths automatically:

**Fast path (YouTube only):** Pulls YouTube's auto-generated captions via `yt-dlp --write-auto-sub --skip-download`. No audio download, no whisper. Finishes in ~2s regardless of video length.

**Fallback (everything else, or YouTube without captions):**
1. Downloads audio only via `yt-dlp -x --audio-format mp3`
2. Transcribes with faster-whisper `small.en` (override with `WHISPER_MODEL=medium.en` env var)
3. Writes `transcripts/url/<slug>_<date>.md` (a same-day repeat of the same title gets a `_2`, `_3`, ... suffix; nothing is overwritten)

Returns the absolute output path on stdout.

## Run It

Step 0, dedupe: `grep -rl "<url or video id>" transcripts/url/ transcripts/local/`. If it hits, read that file instead of re-running.

Run from the repo root, or pass an absolute output dir as arg 2 (`"$PWD/transcripts/url"`): the default output dir is cwd-relative, and background runs are where cwd drift bites.

YouTube URLs finish in ~2s — always synchronous. For non-YouTube short reels (<3 min), still synchronous (~10-30s). For long non-YouTube videos (10+ min), run in background.

After it completes:
1. Read the output file
2. Show the user the transcript inline (or summarize if it's long)
3. Mention the saved path in case they want to reference it later

## Output Shape

```markdown
# <video title>

- **Source:** <canonical URL>
- **Uploader:** <handle>
- **Uploaded:** YYYY-MM-DD
- **Duration:** M:SS
- **Detected language:** en (p=0.99)   # whisper path only
- **Model:** small.en                   # whisper path only
- **Method:** YouTube captions ...      # fast path only

## Transcript

<full plain text, one block>

## Timestamped

`[00:00]` first segment
`[00:04]` second segment
...
```

## Model Choice

(Only relevant for the whisper fallback. The YouTube fast path doesn't run whisper.)

- **`small.en`** (default) — ~5-10x realtime on a modern laptop, good enough for most spoken content. Quick research lookups, competitor reels, captioned content.
- **`medium.en`** — better with mumbling, music-heavy backgrounds, accents. Override: `WHISPER_MODEL=medium.en bash .../transcribe-url.sh <url>`
- **`large-v3`** — best quality, slowest. Use only when small/medium got it wrong.

First run downloads the model (~250MB for small, ~1.5GB for medium, ~3GB for large) and caches it under `~/.cache/`. Subsequent runs are instant.

## Gotchas

- **YouTube without auto-captions** — extremely rare (YouTube auto-generates for almost everything), but if no `.vtt` is published we fall back to whisper automatically. No action needed.
- **Login-walled content** (private IG, restricted YouTube, TikTok login walls) — yt-dlp will error out. If it fails, retry with browser cookies via the env switch: `YTDLP_COOKIES_BROWSER=chrome bash .claude/skills/transcribe-url/scripts/transcribe-url.sh "<url>"` (any browser yt-dlp supports: chrome, firefox, safari, ...). Don't set it by default: slower, and unnecessary for public content.
- **Music-heavy or no-speech videos** — Whisper may hallucinate lyrics. If the transcript looks like nonsense, that's why. Note it in the report rather than passing the garbage along.
- **Title is used for the filename slug** — exotic Unicode titles get stripped to `transcript_<date>.md`. That's fine.
- **Placement & naming are fixed** — always `transcripts/url/<title-slug>_<YYYY-MM-DD>.md`. Never save to the top level, and never name by video ID (the canonical URL lives inside the file). Local-file transcripts go in `transcripts/local/`. Full convention: `transcripts/README.md`.
- **Don't re-transcribe** — if the same URL was already saved (step 0 grep in Run It), just read the existing file. Whisper isn't deterministic enough that re-running adds value.
- **Language** — script lets faster-whisper auto-detect language. The `small.en` model is English-only; if the user needs another language, switch to `small` (no `.en`) via the env var.

## Handoff

This skill produces transcripts. It does NOT summarize, pull viral hooks, or write scripts. After transcribing:
- For script ideas → hand the transcript to the `scriptwriter` skill (don't improvise scripts inline)
- For competitor analysis at scale → use `ig-competitor-research` instead (handles many accounts at once)
- For raw clips already on disk → `bash .claude/skills/voice-corpus-builder/scripts/transcribe-file.sh <file> transcripts/local/<slug>_<date>.md` (same shared whisper venv, plain-text output; the `transcripts/README.md` naming convention still applies); this skill is URL-only.
