---
name: video-editor
description: "Edit videos from the command line with FFmpeg: trim/cut, resize for platforms, recompress, adjust audio, extract clips and subtitles. Use for video post-production tasks."
---

# Video Editor (FFmpeg workflows)

Common edit tasks as reliable FFmpeg recipes.

## Recipes
- **Trim** — `ffmpeg -ss 00:01:10 -to 00:02:00 -i in.mp4 -c copy out.mp4` (re-encode if frame accuracy glitches).
- **Cut list** — concat filter with per-segment `select`, or split + `concat demuxer` (`file list.txt`).
- **Platform resize** — 9:16: `-vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"`; 1:1: 1080x1080.
- **Compress** — `-c:v libx264 -crf 23 -preset slow -c:a aac -b:a 128k` (crf 18 near-lossless, 28 small).
- **Audio** — normalize: `-af loudnorm=I=-16:TP=-1.5:LRA=11`; boost x1.5: `-af volume=1.5`; strip: `-an`; extract: `-vn -c:a copy`.
- **Captions** — burn SRT: `-vf subtitles=subs.srt:force_style='FontSize=22,OutlineColour=&H80000000,BorderStyle=3'` or soft-mux `-c:s mov_text`.
- **Clips → GIF/frames** — palettegen/paletteuse two-pass GIF; `fps=1/10` for thumbnails.
- **Speed** — `setpts=0.5*PTS` (2x) with `atempo=2.0` for audio.

## Workflow
1. Probe first: `ffprobe -hide_banner in.mp4` (streams, fps, duration, resolution).
2. Always preview a 10s sample before full render.
3. Deliver final commands + explain flags used.

## Output
ffmpeg/ffprobe command set + sample-test instruction + quality notes.
