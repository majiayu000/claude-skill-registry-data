---
name: callesnikov-youtube-preserver
description: Preserve YouTube videos and audio locally with a robust yt-dlp wrapper. Use when the user asks Codex to download, save, grab, archive, preserve, or extract audio from YouTube links, including MP4/WebM/MKV video, MP3/M4A/OPUS/WAV/FLAC audio, thumbnails, subtitles, metadata JSON, single-video default behavior, playlist opt-in, and retry-safe downloads.
---

# Callesnikov Youtube Preserver

Use this skill to save YouTube media through `yt-dlp` without global package installation side effects. Prefer single-video downloads unless the user explicitly asks for a playlist.

## Runtime Rule

Use the bundled wrapper script:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-youtube-preserver\scripts\download_video.py" "https://www.youtube.com/watch?v=VIDEO_ID"
```

The script uses `yt-dlp` from PATH or `python -m yt_dlp` if available. It intentionally does not run global `pip install`.

Default output:

```text
<current working directory>\downloads\youtube-preserver\
```

Always report the saved file paths after a successful run.

## Intent Navigator

| User wording | Command |
|---|---|
| "скачай видео", "сохрани ролик", "архивируй" | default video download, MP4 best |
| "только аудио", "скачай аудиоряд", "MP3" | add `-a --audio-format mp3` |
| "без пережатия аудио", "лучше m4a/opus" | `-a --audio-format m4a` or `opus` |
| "720p/1080p/4K" | add `-q 720p`, `-q 1080p`, or `-q 2160p` |
| "webm/mkv" | add `-f webm` or `-f mkv` |
| "с субтитрами" | add `--write-subs`; set `--sub-langs` if language is known |
| "с обложкой/метаданными" | add `--write-thumbnail --write-info-json` |
| "плейлист" | add `--playlist`; otherwise playlists stay blocked |
| "не перезаписывай" | add `--no-overwrites` |
| "нужно авторизованное/возрастное" | ask before using `--cookies-from-browser chrome/firefox` |

## Commands

Best MP4 video:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-youtube-preserver\scripts\download_video.py" "URL"
```

Specific quality:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-youtube-preserver\scripts\download_video.py" "URL" -q 1080p
```

Audio MP3:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-youtube-preserver\scripts\download_video.py" "URL" -a --audio-format mp3
```

Archive-style save with metadata:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-youtube-preserver\scripts\download_video.py" "URL" --write-info-json --write-thumbnail --write-subs
```

Custom output directory:

```powershell
python "C:\Users\User333\.codex\skills\callesnikov-youtube-preserver\scripts\download_video.py" "URL" -o "C:\path\to\output"
```

## Reliability Rules

- Do not use `/mnt/user-data/outputs` on Windows.
- Do not auto-install `yt-dlp` globally.
- Keep `--no-playlist` behavior unless the user explicitly asks for playlist download.
- Use retries and fragment retries from the script defaults before declaring failure.
- If download fails, report the URL, selected mode, output directory, and relevant stderr.
- If extraction to MP3 fails, check whether `ffmpeg` is available before retrying.
- If YouTube blocks anonymous access, ask before using browser cookies.
- Use `--no-overwrites` when preserving an existing archive.

## Output Rules

Use Windows-safe filenames. The script enables safe filename flags and appends the YouTube video id to avoid collisions:

```text
%(title).200B [%(id)s].%(ext)s
```

For user-facing replies, give the exact saved path and mention any companion files such as `.info.json`, thumbnails, or subtitles.
