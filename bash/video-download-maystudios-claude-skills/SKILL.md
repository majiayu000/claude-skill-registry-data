---
name: video-download
description: >
  Download videos from Instagram, YouTube, TikTok, Twitter/X, Facebook, and
  1000+ other platforms as MP4 files using yt-dlp. Auto-recovers from YouTube
  bot detection ("Sign in to confirm you're not a bot", LOGIN_REQUIRED) by
  rotating through browser cookies and cookie files without manual
  intervention. Use this skill when the user wants to download, save, or grab
  one or more videos from any social media or video platform URL. Supports
  single videos or full playlists, configurable resolution, and saving to a
  specified target folder.
---

# Video Download Skill

Wraps yt-dlp with automatic recovery for YouTube anti-bot challenges.

## Tool

`scripts/download.py` — installs yt-dlp on first run, merges video+audio to MP4,
auto-rotates strategies on bot detection, uses a download-archive for safe resume.

## Workflow

1. Collect all URLs from the user's request.
2. Determine output directory (current working directory if unspecified).
3. Decide single-video vs playlist mode:
   - User says "this video" / single URL → leave default (single-video).
   - User says "playlist" / "all videos" / passes a `playlist?list=` URL → add `--playlist`.
4. Run the script. If YouTube bot detection hits, the script auto-rotates strategies.
5. Report which files were saved and which strategy worked.

## Usage

```bash
# Single video, current directory
python scripts/download.py "https://www.youtube.com/watch?v=..."

# Multiple URLs to a folder
python scripts/download.py "URL1" "URL2" -o "/path/to/output"

# Full playlist as 720p MP4
python scripts/download.py "https://www.youtube.com/playlist?list=..." --playlist -o "./out"

# Force a specific browser for cookies (skips auto-rotation)
python scripts/download.py "URL" --cookies-from-browser chrome

# Force a manual cookies.txt file
python scripts/download.py "URL" --cookies "~/Downloads/www.youtube.com_cookies.txt"

# Higher quality
python scripts/download.py "URL" --max-height 1080
```

## Flags

| Flag | Default | Notes |
|---|---|---|
| `-o`, `--output` | cwd | Output directory |
| `--max-height` | 720 | Max video height (e.g. 1080, 480) |
| `--playlist` | off | Download full playlist; default is single-video |
| `--cookies-from-browser` | auto | Force one browser; skips auto-rotation |
| `--cookies` | auto | Force one cookies.txt file; skips auto-rotation |
| `--no-archive` | off | Disable `.download-archive.txt` resume tracking |

## Auto-Recovery Strategy Chain

When a request fails with bot-detection markers (`Sign in to confirm`,
`LOGIN_REQUIRED`), the script automatically advances through these strategies
**in order**, stopping at the first one that succeeds:

1. **No auth + throttle** — Default. Sleep intervals between requests.
2. **Player client rotation** — `default,tv,mweb,web_safari`. Bypasses softer blocks.
3. **Browser cookies rotation** — Tries `chrome → edge → firefox → brave → vivaldi → opera`,
   only browsers actually installed on the system.
4. **Cookies file discovery** — Picks the newest valid cookies file from
   `~/Downloads/www.youtube.com_cookies.txt`, `youtube*cookies*.txt`,
   `cookies.txt` (< 7 days old to be considered fresh).

If all 4 strategies fail, the script prints a context-aware recovery walkthrough
(see "Recovery instructions for the user" below).

If the user explicitly passes `--cookies-from-browser` or `--cookies`, the chain
is skipped and only that source is used (useful when the user already knows
what works).

## Recovery instructions for the user

When all strategies fail, the script auto-prints a step-by-step guide. **Surface
the most relevant subset to the user verbatim** — it is concrete and actionable.

The guide branches based on what the script saw:

- **Cookies file found but rejected** (file is stale): tell the user to
  re-export cookies *right now*, since YouTube invalidates cookies aggressively
  once a bot-block triggers.
- **No cookies file found**: walk the user through the first-time export.
- **Otherwise**: just list alternatives (close browser, change network, wait).

### Cookie export walkthrough (the part the user will likely need)

1. Install a cookie export browser extension:
   - **Chrome / Edge / Brave / Vivaldi / Opera**: "Get cookies.txt LOCALLY" —
     <https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc>
   - **Firefox**: "cookies.txt" —
     <https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/>

2. Open <https://www.youtube.com> in that browser, signed in to a Google
   account.

3. Click the extension's toolbar icon:
   - "Get cookies.txt LOCALLY" → "Export As" → Netscape format → use the
     "Current Site" option so only `youtube.com` cookies are included.
   - Firefox "cookies.txt" → "Current Site" → Save.

4. Save the file to the OS default Downloads folder. Any of these names work
   (auto-detected, newest wins):
   - `www.youtube.com_cookies.txt` (extension default — easiest)
   - `youtube.com_cookies.txt`
   - `cookies.txt`

5. Re-run the same download command. Strategy 4 picks the file up
   automatically.

### When to recommend each alternative

- **Close the browser** (Chrome / Edge): fastest fix on Windows, where
  App-Bound Encryption locks the cookie database while the browser runs. Costs
  the user their open tabs unless "Continue where you left off" is enabled.
- **Different network** (mobile hotspot, VPN): bypasses an IP-level block.
  Fastest if the user already has a VPN.
- **Wait it out**: YouTube IP blocks lift on their own, usually within 24 h.
  Recommend only if no other option fits.

## Resume / Re-Run Safety

`--download-archive .download-archive.txt` is enabled by default. Already-downloaded
videos are skipped on re-runs, so it's safe to re-run after partial failure or
when adding more URLs to the same folder. Pass `--no-archive` to disable.

## Output Filename Pattern

- Single video: `{title} [{id}].mp4`
- Playlist: `{NNN} - {title} [{id}].mp4` (zero-padded index keeps order in file managers)

`--windows-filenames` is always on, so files are safe across OSes.

## Authentication Notes

- Auto-rotation handles most cases without user input.
- `--cookies-from-browser chrome` requires Chrome **closed** on Windows
  (App-Bound Encryption locks the cookie DB while Chrome is running).
- If Chrome must stay open, recommend the user export cookies via the
  "Get cookies.txt LOCALLY" Chrome extension and drop the file in `~/Downloads/`.
  The script picks it up automatically on next run.

## Supported Platforms

YouTube (single + playlists), Instagram, TikTok, Twitter/X, Facebook, Vimeo,
Reddit, and 1000+ more via yt-dlp.
