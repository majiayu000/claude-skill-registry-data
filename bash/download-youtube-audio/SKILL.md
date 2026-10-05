---
name: download-youtube-audio
description: Download the highest available source-quality audio from one YouTube link only when the user explicitly asks to 提取音频, 下载音频, extract audio, or download audio and the link belongs to youtube.com, youtu.be, or youtube-nocookie.com. Do not activate for a bare YouTube link that the user only wants opened, read, summarized, or discussed.
---

# Download YouTube Audio

Use this Skill's wrapper for the shared deterministic downloader. Accept exactly one published-video URL whose normalized hostname is `youtube.com`, `youtu.be`, or `youtube-nocookie.com`, or one of their subdomains.

## Run

- Resolve the absolute path to this Skill directory. Encode the complete URL as UTF-8 Base64 in memory before composing the command. Never place the raw URL in a shell command or pass it as a positional argument.
- Run this Skill's `scripts/run.py`; the wrapper applies the fixed YouTube platform guard:

```powershell
py -3 "<skill-dir>\scripts\run.py" --url-base64 "<UTF8_BASE64>"
```

On macOS or Linux, use `python3 "<skill-dir>/scripts/run.py" --url-base64 "<UTF8_BASE64>"`.

- If the user explicitly supplies another output directory, Base64-encode it outside the shell and append `--output-dir-base64 '<UTF8_BASE64>'`.
- The wrapper keeps `--expected-platform YouTube` fixed. Reject a mismatched platform, multiple URLs, a playlist-only URL, or an active livestream.
- Preserve the best source audio codec exposed by YouTube and yt-dlp. A container-only remux is acceptable; an unexpected codec change is a failure.

## Authentication and safety

- Always attempt the public download first, without browser cookies.
- Only if the JSON result is `authentication_required`, ask for permission to use Chrome cookies for this exact URL. After explicit permission, Base64-encode the allowed `chrome[:profile]` value outside the shell and add `--cookies-from-browser-base64 '<UTF8_BASE64>'`.
- Never export or persist cookies, request a password, or bypass DRM, paid access, account entitlement, or a region restriction. Process only content the user is authorized to download; platform terms still apply.
- Do not silently install or upgrade dependencies.

## Results

The downloader emits one JSON object. On `downloaded` or `already_exists`, report the final absolute path, title, codec/container, available bitrate/sample-rate/channel details, and codec-preservation status. On `authentication_required`, stop and request URL-specific cookie permission. If any result contains `recovery_path` or `previous_file_backup`, always report that absolute recovery path. For other failures, report only the safe `message` and `error_code`; do not expose subprocess stderr, signed media URLs, cookie data, or browser-profile paths.
