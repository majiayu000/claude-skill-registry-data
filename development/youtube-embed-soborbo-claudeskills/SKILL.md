---
name: youtube-embed
description: YouTube video facade pattern for performance. Lazy-load iframe on click, poster images, GA4 tracking, Schema.org markup.
---

# YouTube Embed Skill

## Purpose

Embed YouTube videos without loading YouTube scripts until user clicks. Massive performance win.

## Core Rules

1. **Facade pattern** — Poster + play button, no iframe until click
2. **Local posters** — Download and optimize thumbnails locally
3. **Privacy-enhanced** — Use `youtube-nocookie.com` only
4. **Track engagement** — GA4 `video_play` event on click
5. **Schema.org** — VideoObject markup for rich snippets

## Flow

```
Click before: Poster image + Play button (no YouTube)
Click after:  Replace with iframe + GA4 event + autoplay
```

## Poster Images

1. Download: `https://i.ytimg.com/vi/{VIDEO_ID}/maxresdefault.jpg`
2. Fallback: `sddefault.jpg` if maxres unavailable
3. Convert: Use Picture skill (avif, webp, jpg)
4. Store: `src/assets/videos/{slug}.jpg`

## References

- [Component](references/component.md) — Full VideoFacade.astro code
- [Schema](references/schema.md) — VideoObject markup

## Forbidden

- ❌ YouTube iframe/script before click
- ❌ `youtube.com` (must use `youtube-nocookie.com`)
- ❌ `fetchpriority="high"` on video facades
- ❌ YouTube logo as play button (trademark)
- ❌ Remote poster images (always local)
- ❌ Missing poster or title

## Definition of Done

- [ ] VideoFacade component created
- [ ] Poster images downloaded and optimized
- [ ] Click triggers iframe swap + autoplay
- [ ] GA4 video_play event firing
- [ ] VideoObject schema on pages with videos
- [ ] Keyboard accessible (Enter/Space)
