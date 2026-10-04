---
name: tool-youtube-transcript
description: Fetch the transcript/captions of a YouTube video by URL or video id. Use when the user pastes a YouTube link and wants the contents summarised, quoted, or searched — WebFetch on youtube.com only returns navigation chrome, not the transcript. Supports `youtube.com/watch?v=...`, `youtu.be/...`, `/shorts/`, `/embed/`, or a bare 11-char id. Output is plain text by default; pass `--with-timestamps` for `[hh:mm:ss]` prefixes, `--out PATH` to write to a file (useful for long videos to keep context small). NOT for filing the video as a vault note (use vault-yt-digest, which wraps this) and NOT for a local video file.
---

# YouTube Transcript Skill

Pulls captions (manual or auto-generated) for a YouTube video. The video must have captions available — most do.

## Setup (one-time)

```bash
pip install youtube-transcript-api
```

## Usage

```bash
# Print transcript to stdout
python "skills/tool-youtube-transcript/youtube_transcript.py" "https://www.youtube.com/watch?v=v4F1gFy-hqg"

# With timestamps
python "skills/tool-youtube-transcript/youtube_transcript.py" v4F1gFy-hqg --with-timestamps

# Save to file (recommended for long videos to keep context small)
python "skills/tool-youtube-transcript/youtube_transcript.py" <url> --out /tmp/transcript.txt

# Specific language
python "skills/tool-youtube-transcript/youtube_transcript.py" <url> --lang zh-Hans
```

## Workflow when user pastes a YouTube link

1. Run the script, piping to file if the video is >~20 min: `--out /tmp/yt-<id>.txt`.
2. Read the file with the Read tool (using `limit`/`offset` if huge).
3. Summarize / answer the user's question against the transcript.

## Notes

- `WebFetch` on a YouTube watch page returns only the page chrome, not the transcript — always prefer this skill.
- If a video has no captions in any language, the API raises an error. There's no fallback to audio transcription here; for that, use `yt-dlp` to download audio and Whisper to transcribe.
- The script accepts either a full URL or a bare 11-character video id.
