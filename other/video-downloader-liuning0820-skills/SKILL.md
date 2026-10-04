---
name: video-downloader
description: Download a video or audio from a URL using yt-dlp, merging video and audio into a single file with ffmpeg. Use when the user gives a media page URL (Bilibili, X/Twitter, YouTube, or any yt-dlp-supported site) and asks to download it. Saves to the user's Downloads folder by default, or to a folder the user names.
---

# Video Downloader skill

Download media from a URL with `yt-dlp`, and merge separate video+audio streams
into one file with `ffmpeg`. This is the command-line equivalent of this repo's
Chrome extension, for when the browser is not used.

## When to use

Use this skill when the user:

- gives a video/audio page URL and asks to download it, or
- asks to grab/save a video or its audio from a site, or
- names a target folder for a download.

Supported sites are everything `yt-dlp` supports (1000+): Bilibili, X/Twitter,
YouTube, and more.

## Tool

This skill is self-contained: the downloader script `download_media.py` lives
next to this file in the skill directory. Always invoke it by its **absolute
path** so it resolves no matter where the skill is installed (user level or
workspace level) and regardless of the current working directory. When the skill
is activated, the reported "Skill directory" is that absolute location — join
`download_media.py` to it:

```
python "<SKILL_DIR>/download_media.py" "<URL>" [--quality <q>] [--output "<dir>"] [--audio]
```

The script streams `yt-dlp` progress to the terminal and prints
`Done. Saved to: <dir>` on success.

### Arguments

- `URL` (required): the media page address. Always wrap it in double quotes —
  URLs often contain `?`, `&`, and `=`.
- `--quality` / `-q`: one of `best` (default), `2160`, `1440`, `1080`, `720`,
  `480`, `360`, `audio`.
- `--audio`: shortcut for `--quality audio` (audio only, no merge).
- `--output` / `-o`: target folder. Default is the current user's `Downloads`
  folder. The folder is created if it does not exist.

### Behaviour you can rely on

- Output filename uses the real media title plus the id, e.g.
  `月下煮茶 普通话版 [BV1ke5U65ECa].mp4`. Non-ASCII titles (Chinese, etc.) are
  kept; characters illegal on the OS are sanitised.
- `best` and the height presets merge the best video and audio into one `.mp4`.
  Audio-only produces a single audio file with no merge.
- `ffmpeg` is located automatically (PATH, then `~/ffmpeg/bin` and other common
  spots). Merge quality options fail with a clear message if `ffmpeg` is absent.

## How to act on a request

1. Extract the URL from the user's message. If none is present, ask for it.
2. Pick quality: default to `best`. Use `audio` only if the user asks for audio
   or music.
3. Pick output: default (Downloads) unless the user names a folder; then pass
   `--output "<that folder>"`.
4. Run the script with `execute_pwsh`, calling it by the skill directory's
   absolute path (do NOT assume a workspace-relative `.kiro/skills/...` path —
   this skill may be installed at the user level, outside any workspace).
5. Report the saved file path from the script's final `Done. Saved to:` line. On
   failure, relay the error (common causes: missing `ffmpeg`, outdated `yt-dlp`
   — suggest `yt-dlp -U`).

## Examples

In each example, `<SKILL_DIR>` is the absolute skill directory reported when the
skill is activated (e.g. `C:\Users\<you>\.kiro\skills\video-downloader` for a
user-level install, or `<workspace>\.kiro\skills\video-downloader` for a
workspace-level one).

Request: "下载 https://www.bilibili.com/video/BV1ke5U65ECa"
Run:
```
python "<SKILL_DIR>/download_media.py" "https://www.bilibili.com/video/BV1ke5U65ECa"
```

Request: "把这个视频下成 1080p 存到 D:\clips  https://x.com/i/status/123"
Run:
```
python "<SKILL_DIR>/download_media.py" "https://x.com/i/status/123" --quality 1080 --output "D:\clips"
```

Request: "只要这个视频的音频  <URL>"
Run:
```
python "<SKILL_DIR>/download_media.py" "<URL>" --audio
```

## Requirements

- `yt-dlp` on `PATH` (`yt-dlp --version`).
- `ffmpeg` reachable (on `PATH` or `~/ffmpeg/bin`) for any non-audio quality.

Both are already installed in this environment.
