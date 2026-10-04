---
name: video-downloader
description: Download a video from YouTube, Instagram, TikTok, Twitter/X, Facebook, Vimeo (and 1000+ yt-dlp sites) to local disk, and optionally transcribe it. Standalone utility for repurposing and analysis — not part of the static publishing pipeline.
allowed-tools: Read, Bash
area: Productivity
use_for: "Download a video from a URL (YouTube/IG/TikTok/X/FB/Vimeo/+) to local disk and optionally transcribe it — a standalone repurposing/analysis utility"
deps:
  files: []
  env: []
---

## Maintenance

| Agent | Version | Last Changed |
|---|---|---|
| Link | v1.0.1 | May 28, 2026 |

**Description:** Download a video from a URL to local disk and optionally transcribe it — standalone utility.

### Change Log

**v1.0.1** — May 28, 2026
- **Removed the bundled `scripts/download_video.py` + `$CLAUDE_PLUGIN_ROOT` path.** Cowork (not Claude Code) is the runtime and doesn't expose `CLAUDE_PLUGIN_ROOT`, and link-skills has no bundled-runtime-script convention. Reworked to run yt-dlp **inline** (`python3 -m pip install yt-dlp` → `python3 -m yt_dlp`) in the skill's Bash block — the same local-glue pattern content-generator uses for its inline Python. No plugin-relative paths, no shipped `.py`.

**v1.0.0** — May 28, 2026
- New standalone utility (yt-dlp + optional Whisper transcription). Not wired into the static publishing pipeline; transcripts can feed `meeting-analyzer`. No brand context required.

---

# SKILL.md — Video Downloader

A standalone utility — no brand context, no Notion, no dashboard logging. Use it whenever a video URL needs to come down to local disk for repurposing (clip → static post), analysis (transcribe → summarize), or archiving. Everything runs **inline in the Cowork bash sandbox** — there is no bundled script and no gateway tool (yt-dlp is a local binary; the serverless gateway can't run it).

## When to use

- "Download this video: [URL]"
- "Get this reel / short / clip: [URL]"
- "Transcribe this video: [URL]" (download + transcribe)

Do **not** use this for the static social pipeline (`social-calendar` → `content-creation` → `creative-designer` → `social-publisher`). It stands alone.

## Step 1 — Download (inline yt-dlp)

`yt-dlp` is a Python package — install it on demand and run it as a module (no PATH dependency, no bundled file). Substitute the real URL and (optionally) `OUT`:

```bash
OUT="${OUTPUT_DIR:-/tmp/downloads}"; mkdir -p "$OUT"
python3 -m pip install --quiet --upgrade yt-dlp 2>/dev/null || pip install --quiet --upgrade yt-dlp

# Best-quality MP4 (merges video+audio when ffmpeg is present)
python3 -m yt_dlp -f "bestvideo[ext=mp4]+bestaudio/best[ext=mp4]/best" --merge-output-format mp4 \
  --no-playlist --no-warnings -o "$OUT/%(title).80s.%(ext)s" "VIDEO_URL"
```

Variants:

| Need | Tweak |
|---|---|
| Cap quality (e.g. 720p) | `-f "bestvideo[height<=720][ext=mp4]+bestaudio/best[height<=720]"` |
| Audio only (MP3) | `-x --audio-format mp3` (drop the `-f` / `--merge-output-format` flags) |
| Output directory | set `OUT` (default `/tmp/downloads`) |

**If the merge step fails** (no `ffmpeg` in the sandbox), retry with a single-file format that needs no merge:

```bash
python3 -m yt_dlp -f "best[ext=mp4]/best" --no-playlist --no-warnings -o "$OUT/%(title).80s.%(ext)s" "VIDEO_URL"
```

Report the resulting file path (most recent file in `$OUT`):

```bash
ls -t "$OUT" | head -1
```

Supported: YouTube, Instagram, TikTok, Twitter/X, Facebook, Vimeo, and 1000+ other yt-dlp sites. If `pip`/network is unavailable in the sandbox, say so rather than failing silently.

## Step 2 — Transcribe (optional)

Only when a transcript is wanted, and only if `ffmpeg` + `whisper` are available (both are heavy — guard for them):

```bash
command -v ffmpeg >/dev/null || { echo "ffmpeg not available here — cannot transcribe"; exit 0; }
ffmpeg -i "/path/to/video.mp4" -ar 16000 -ac 1 -y /tmp/video-audio.wav
python3 -m pip install --quiet --upgrade openai-whisper 2>/dev/null
python3 -c "import whisper; print(whisper.load_model('base').transcribe('/tmp/video-audio.wav')['text'])"
```

Save the transcript next to the video (`<basename>.txt`) or print it. A transcript can feed `meeting-analyzer` (action items) or `content-creation` (repurposing into posts).

## Step 3 — Cleanup

`rm -f /tmp/video-audio.wav` when done. Leave the downloaded video unless the user asked for transcript-only.

## Notes

- Respect copyright and platform ToS — download only content the user is authorized to use (their own, licensed, or fair-use analysis).
- Local-only by design: no gateway tool (yt-dlp/ffmpeg/whisper can't run in the serverless gateway) and no bundled script (Cowork has no `CLAUDE_PLUGIN_ROOT`). If `pip` / network / `ffmpeg` aren't available in the sandbox, report the limitation rather than failing silently.
