---
name: download-best-audio
description: Shared deterministic runtime for the site-specific Bilibili, Douyin, and YouTube audio-download skills. Use explicitly for maintenance or direct invocation; ordinary requests should route to the matching site skill.
---

# Download Best Audio

This is the shared runtime behind the three site-specific skills. Resolve the absolute path to this Skill directory before running its script. Do not put a raw URL, output path, or browser profile into a shell command. Encode every user-controlled string as UTF-8 Base64 in memory, then pass only the Base64 alphabet.

```powershell
py -3 "<skill-dir>\scripts\download_audio.py" --url-base64 "<UTF8_BASE64>" --expected-platform "<Bilibili|Douyin|YouTube>"
```

On macOS or Linux, use an available Python 3 interpreter:

```bash
python3 "<skill-dir>/scripts/download_audio.py" --url-base64 "<UTF8_BASE64>" --expected-platform "<Bilibili|Douyin|YouTube>"
```

For an explicit custom directory use `--output-dir-base64`; after per-link cookie approval use `--cookies-from-browser-base64`. The public positional interface remains available for direct non-shell callers.

## Required behavior

- Accept exactly one published-video HTTPS URL from Douyin, Bilibili, or YouTube. The script also recognizes their normal share-link domains.
- Default to the best source audio exposed by the site and yt-dlp. Preserve the source codec; a container-only remux is acceptable, but an unexpected codec change is a failure.
- Save successful files under the current user's `Downloads/Codex-Audio` directory unless the user explicitly supplies another absolute output directory.
- Treat a video URL that also contains a playlist parameter as one video. Reject a playlist-only URL, multiple URLs, and an active livestream.
- Never pass raw user data through a shell. Never bypass DRM, a paywall, account entitlement, or a region restriction. Process only content the user is authorized to download and remind them that platform terms still apply when relevant.

## Authentication boundary

Run once without browser cookies. If the script returns `authentication_required`, ask the user for permission for this URL. Only after explicit permission, Base64-encode the allowed `chrome[:profile]` value outside the shell and rerun with `--cookies-from-browser-base64 '<UTF8_BASE64>'`. Do not export cookies to a file, request a password, or persist authentication details.

## Result handling

The script writes one JSON object to stdout.

- On `downloaded` or `already_exists`, tell the user the final absolute path, title, codec/container, available bitrate/sample-rate/channel details, and whether the source codec was preserved or only remuxed.
- On `authentication_required`, ask for cookie permission without retrying automatically.
- If any result contains `recovery_path` or `previous_file_backup`, always report that absolute recovery path so the user can preserve or inspect the old file.
- For every other failure, report the safe `message` and `error_code`. Do not expose subprocess stderr, signed media URLs, cookie data, or browser-profile paths.

Do not silently install or upgrade dependencies during a download. If the script returns `dependency_missing` or `extractor_failed`, report the installed version information and ask before changing the installation.
