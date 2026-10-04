---
name: video-fetch-and-summarize
description: >
  Downloads videos from URLs and generates a Markdown summary for each one using the Gemini API.
  Supports custom prompts to extract specific information instead of the default summary.
  Each video is saved in its own subfolder containing the MP4 file and a summary.md.
  Use this skill when the user provides video URLs directly, or a file (Markdown, TXT, or any
  text file) containing video URLs, and wants both the video downloaded and summarized.
  Triggers on requests like "download and summarize these videos", "fetch these links and summarize",
  "process this list of video links", "extract X from these videos", or when given a file with
  URLs and asked for summaries. Supports Instagram, YouTube, TikTok, Twitter/X, Facebook, and
  1000+ other platforms. Requires GEMINI_API_KEY environment variable.
---

# Video Fetch & Summarize

Downloads videos from URLs and generates a Markdown summary per video via Gemini. Fully self-contained — no other skills required.

## Output Structure

```
<output_dir>/
  <Video_Title>/
      <uploader>_<id>.mp4
      summary.md
```

## Prerequisites

- `GEMINI_API_KEY` env var set
- `yt-dlp` and `google-genai` — **auto-installed** on first run if missing
- Python available as `py` (Windows) or `python3`

## Script

`scripts/fetch_and_summarize.py`

## Usage

```bash
# Direct URLs — default summary
py scripts/fetch_and_summarize.py "https://..." "https://..." -o ./output

# File containing URLs (TXT, Markdown, or any text file)
py scripts/fetch_and_summarize.py links.txt -o ./output

# Custom prompt (inline) — replaces default summary format
py scripts/fetch_and_summarize.py "https://..." --prompt "Extract all mentioned tools and prices"

# Custom prompt (from file) — replaces default summary format
py scripts/fetch_and_summarize.py links.txt --prompt-file my-prompt.txt

# With browser cookies (for private/login-required content)
py scripts/fetch_and_summarize.py links.txt --cookies-from-browser chrome
```

## How Claude should handle user arguments

When the user invokes this skill:

1. If the user specifies a **custom prompt or extraction goal** (e.g., "extract all tools mentioned",
   "summarize focusing on pricing", "list action items"), pass it via `--prompt "..."`.
2. If the user provides a **prompt file path**, pass it via `--prompt-file path/to/file.txt`.
3. If the user gives **no specific instructions**, run without `--prompt` to use the default format.
4. A custom prompt **completely replaces** the default — it does not add to it.

## Workflow

1. Extract all URLs from provided arguments and/or files (regex-based, works with any text format)
2. For each URL:
   a. Fetch video metadata via `yt-dlp --dump-json` to get the title for the folder name
   b. Download the video as best-quality MP4 into `<output>/<Title>/`
   c. Upload MP4 to the Gemini Files API, wait for ACTIVE state
   d. Generate Markdown summary (using custom or default prompt), delete file from Gemini storage
   e. Save summary as `<output>/<Title>/summary.md`
3. Skip videos where both MP4 and summary.md already exist (idempotent re-runs)

## Download Details (yt-dlp)

- Format: `bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best` — best quality, always MP4
- Filename pattern: `{uploader}_{video_id}.mp4` — e.g. `DesignMotion_DUf3nehjIg7.mp4`
- `--no-playlist` is set by default (single videos only)
- Supported platforms: YouTube, Instagram (posts/reels), TikTok, Twitter/X, Facebook, Vimeo, Reddit, and 1000+ more

### Authentication for private/login-required content

```bash
py scripts/fetch_and_summarize.py links.txt --cookies-from-browser chrome
# also works with: firefox, edge, safari
```

The user must be logged in to the platform in the specified browser.

## Summarization Details (Gemini)

- Model: `gemini-3-flash-preview`
- Upload via Gemini Files API (supports large video files)
- Uploaded files are auto-deleted from Gemini storage after generation (48h max limit anyway)
- Summary language matches the language spoken/shown in the video

### Default output format (when no custom prompt is given)

```markdown
# [Video Title]

## Summary
[2-3 sentence description of the video and its main topic]

## Key Points
- key point 1
- key point 2
- ...

## Core Content & Takeaways
[Central message and most important insight, 2-4 sentences]

---
*Auto-generated with Gemini API*
```

## Notes

- Output directory defaults to the current working directory
- Folder names are sanitized from the video title (max 80 chars, special chars replaced)
- Already-processed videos are skipped on re-runs
- If the Gemini API returns 503 (overloaded), re-run the script — already-done videos are skipped automatically
