---
name: video-notes
description: Use when the user shares a YouTube link or lecture video and wants notes, a summary, or slides from it
---

# /video-notes: turn any lecture or video into a note with its slides

1. Gather (free, local):
   `python3 ~/.ecx/watch-notes/wn_gather.py <url> --label <short-name> --out-dir <vault>/notes`
   It downloads the video (yt-dlp), keeps only frames that change (perceptual hash), fetches the transcript, and prints a JSON manifest.
2. Read the manifest, the transcript and the key frames.
3. Write the note in the vault: sections that follow the video, the key slides embedded where they belong, timestamps, and a 5-line recap at the top.

Uses your Claude plan for the writing, so no paid vision API is needed. Requires `yt-dlp` and `ffmpeg`.
