---
name: GIF
slug: gif
version: 1.0.1
description: Find, search, and create GIFs with proper optimization and accessibility.
homepage: https://clawic.com/skills/gif
changelog: Declare required binary (ffmpeg), document optional deps (gifsicle, API keys)
metadata:
  clawdbot:
    emoji: 🎞️
    requires:
      bins:
      - ffmpeg
    os:
    - linux
    - darwin
    - win32
    displayName: GIF
---

## Requirements

**Required for creating GIFs:**
- `ffmpeg` — video to GIF conversion

**Optional:**
- `gifsicle` — post-optimization (reduces size 30-50%)
- `GIPHY_API_KEY` — for Giphy search API
- `TENOR_API_KEY` — for Tenor search API

## Where to Find GIFs

| Site | Best for | API |
|------|----------|-----|
| **Giphy** | General, trending | Yes (key required) |
| **Tenor** | Messaging apps | Yes (key required) |
| **Imgur** | Viral/community | Yes |
| **Reddit r/gifs** | Niche, unique | No |

## Creating GIFs with FFmpeg

**Always use palettegen (without it, colors look washed out):**
```bash
ffmpeg -ss 0 -t 5 -i input.mp4 \
  -filter_complex "fps=10,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse" \
  output.gif
```

| Setting | Value | Why |
|---------|-------|-----|
| fps | 8-12 | Higher = much larger file |
| scale | 320-480 | 1080p GIFs are massive |
| lanczos | Always | Best scaling quality |

## Post-Optimization

If `gifsicle` is available:
```bash
gifsicle -O3 --lossy=80 --colors 128 input.gif -o output.gif
```

Reduces size 30-50% with minimal quality loss.

## Video Alternative

For web, use video instead of large GIFs (80-90% smaller):

```html
<video autoplay muted loop playsinline>
  <source src="animation.webm" type="video/webm">
  <source src="animation.mp4" type="video/mp4">
</video>
```

## Accessibility

- **WCAG 2.2.2:** Loops >5s need pause control
- **prefers-reduced-motion:** Show static image instead
- **Alt text:** Describe the action ("Cat jumping off table")
- **Three flashes:** Nothing >3 flashes/second (seizure risk)

## Common Mistakes

- No `palettegen` in FFmpeg — colors look terrible
- FPS >15 — file size explodes for no visual benefit
- No lazy loading on web — blocks page load
- Using huge GIF where video would work — 10x larger

## API Quick Reference

**Giphy search:**
```bash
curl "https://api.giphy.com/v1/gifs/search?api_key=$GIPHY_API_KEY&q=thumbs+up&limit=10"
```

**Tenor search:**
```bash
curl "https://tenor.googleapis.com/v2/search?key=$TENOR_API_KEY&q=thumbs+up&limit=10"
```
