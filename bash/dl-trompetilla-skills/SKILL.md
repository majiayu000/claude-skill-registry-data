---
name: dl
description: Download Video/Music from YouTube/Bilibili/X/etc.
author: guoqiao
metadata: {"openclaw":{"always":true,"emoji":"🦞","homepage":"https://clawhub.ai/guoqiao/dl","os":["darwin","linux","win32"],"requires":{"bins":["uv"]}}}
triggers:
- "/dl <url>"
- "Download this video ..."
- "Download this music ..."
---

# Media Downloader

Smartly download media (Video/Music) from URLs (YouTube, Bilibili, X, etc.) to the appropriate local folders.

- **Video:** Saves `mp4` to `~/Movies/` or `~/Videos/`.
- **Music:** Saves `m4a` to `~/Music/`.
- **Playlists:** Saves items into a subdirectory (e.g., `~/Music/<playlist_name>/`).

Designed to work with a local Media Server (e.g., Universal Media Server, Jellyfin) for instant playback on TV/devices.

## Agent Procedure

When the user provides a URL or asks to download media, **you MUST follow this exact sequence:**

1. **Acknowledge:**
   - Immediately reply to the user: "Downloading with dl skill..."

2. **Execute:**
   - Run the script:
     ```bash
     uv run --script ${baseDir}/dl.py "<url>"
     ```

3. **Capture Path:**
   - Read the script output. Look for the line: `Saved to: <filepath>`.

4. **Upload (Telegram Only):**
   - If the user is on Telegram (check context or session) AND the file is audio (mp3/m4a):
   - Use the `message` tool to send the file to the user:
     ```json
     {
       "action": "send",
       "filePath": "<filepath>",
       "caption": "Here is your music."
     }
     ```

## Usage (Manual)

Run the python script directly:
```bash
uv run --script ${baseDir}/dl.py <url>
```
The script auto-detects Video vs Music and Single vs Playlist.

## Setup (User)

This skill will be much more useful if you setup a media server on same machine to share the downloaded media in your LAN:

1. Install a DLNA/UPnP Media Server (Universal Media Server, miniDLNA, Jellyfin).
2. Share `~/Music` and `~/Movies` (or `~/Videos`) folders.
3. Downloaded media will appear automatically on your TV, with apps support DLNA/UPnP, such as VLC.

See [example script](https://github.com/guoqiao/skills/blob/main/dl/ums/ums_install.sh) to setup Universal Media Server on Mac.
