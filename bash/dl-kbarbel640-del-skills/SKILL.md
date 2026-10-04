---
name: dl
description: Download media, smart and to the point.
metadata: {"openclaw":{"always":true,"emoji":"🦞","homepage":"https://github.com/guoqiao/skills/blob/main/dl/dl/SKILL.md","os":["darwin","linux","win32"],"requires":{"bins":["uv"]}}}
triggers:
- "Download this video ..."
- "Download this music ..."
---

# Media Downloader

Download media with yt-dlp, with sane options, to expected locations.

Recommended Extra Setup:
- Install a DLNA/UPnP Media Server on this machine, e.g.: miniDLNA, Universal Media Server, Jellyfin, etc.
- Add the ~/Movies and ~/Music folders to the media server to share over LAN.
- Downloaded media with this skill, which will be shared automatically in LAN.
- Play the media on other devices via the media server.

# Usage

Just run this python uv script:
```
uv run --script ${baseDir}/dl.py $url
```
Which will auto detect Video/Music and Single/Playlist info from the url, and save to corresponding locations.

Or, you can still use following shell cmds:

Download Single Video, save into ~/Movies as mp4:
```
uvx yt-dlp@latest --js-runtime node --remote-components ejs:github \
    -f "bestvideo[vcodec^=avc1]+bestaudio/best" --merge-output-format=mp4 --max-filesize=2000M \
    -P "$HOME/Movies" \
    -o "%(title).240B.%(ext)s" --no-playlist \
    ${url}
```

Download Video Playlist, save into ~/Movies/<playlist>/ as mp4:
```
uvx yt-dlp@latest --js-runtime node --remote-components ejs:github \
    -f "bestvideo[vcodec^=avc1]+bestaudio/best" --merge-output-format=mp4 --max-filesize=2000M \
    -P "$HOME/Movies" \
    -o "%(playlist_title)s/%(title).240B.%(ext)s" --max-downloads=30 \
    ${url}
```

Download Single Music, save into ~/Music as m4a:
```
uvx yt-dlp@latest --js-runtime node --remote-components ejs:github \
    -f "bestaudio/best" --extract-audio --audio-format=m4a --audio-quality=0 --max-filesize=30M \
    -P "$HOME/Music" \
    -o "%(title).240B.%(ext)s" --no-playlist \
    ${url}
```

Download Music Playlist, save into ~/Music/<playlist>/ as m4a:
```
uvx yt-dlp@latest --js-runtime node --remote-components ejs:github \
    -f "bestaudio/best" --extract-audio --audio-format=m4a --audio-quality=0 --max-filesize=30M \
    -P "$HOME/Music" \
    -o "%(playlist_title)s/%(title).240B.%(ext)s" --max-downloads=30 \
    ${url}
```

Tips:
- `%(title).240B`: limite filename to 240 chars in output template, to avoid `file name too long` errors.
- `--max-filesize=2000M`: limit single file max size to 2G, to avoid huge file download.
- `--max-downloads=30`: limit max playlist item to 30, to avoid huage list download.
- `--no-playlist`: avoid downloading playlist unexpectedly for single item url like `https://www.youtube.com/watch?v=UVCa8...&list=PL...`
- macOS defaults `~/Movies` and `~/Music` are used here.
- `uvx yt-dlp@latest` will ensure `yt-dlp` is always up to date.
- `yt-dlp` will be blocked quickly if the host machine is in Cloud/DataCenter, use a residential IP if you can.

Adjust the cmds when needed.
