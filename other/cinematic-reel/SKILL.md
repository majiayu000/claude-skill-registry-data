---
name: cinematic-reel
description: Turn one raw landscape/cinematic clip (DJI Osmo Pocket, drone, phone) into a polished vertical 9:16 cinematic reel — scale/crop, color grade, beat-snapped chapter/title cards, optional ElevenLabs VO + ducked BGM — in a SINGLE ffmpeg pass (NVENC with libx264 auto-fallback), then optionally auto-schedule it across all socials via GHL MCP with a different human caption + hashtag set per platform. Distilled from a SkynetLabs sunset/landscape reel (2026-05-29). Trigger when user says "cinematic reel", "/cinematic-reel", "make a reel from this clip", "sunset/landscape reel", "cut this DJI footage", drops a single scenic .mp4 and wants a vertical cinematic cut, or wants a reel rendered AND scheduled to socials.
---

# Cinematic Reel — scenic clip → vertical cut → all-socials schedule

End-to-end for a SINGLE scenic source clip (sunset, landscape, b-roll, drone, Osmo Pocket).
Output: vertical 9:16 cinematic cut with title/chapter cards + optional VO/BGM, then optional
multi-platform GHL scheduling. **Single ffmpeg pass.**

## When to use

- One scenic/cinematic source clip → want a vertical reel with grade + text cards.
- Optionally: schedule it to FB/IG/TikTok/YT/LinkedIn/Pinterest at staggered times with per-platform copy.

Not for: talking-head/script reels (→ `reel-studio`), landscape screencast promos (→ `demo-promo`),
static social cards (→ `social-stack`).

## Pipeline

### 1. Probe + verify the arc (DO NOT skip)

`ffprobe` the source (res/fps/duration). Then extract frames across the timeline and **eyeball them** —
card text must match what's actually on screen. Numeric/agent color analysis lies (auto-exposure, artificial
lights). See `references/pipeline-notes.md`.

```
ffmpeg -ss <t> -i SRC -frames:v 1 -q:v 3 frame_<t>.jpg
```

### 2. Write the config + render (one pass)

Build a `reel.config.json` (schema in `scripts/build_cut.py` header). Snap card `t_in` to the BGM beat
grid; card at VO handoff, one before the ~50% drop-off, ~50-60s cadence. Then:

```
python -u <skill>/scripts/build_cut.py reel.config.json
```

`encoder:"auto"` tries h264_nvenc and falls back to libx264 if the GPU driver is too old. Audio comes
out 48kHz stereo, loudnorm ~-14.

### 3. QA the render

Probe streams (expect h264 WxH, aac 48000 stereo). Re-extract frames at each card `t_in` and confirm the
overlay fired over the right image. Check loudness: `ffmpeg -i OUT -af ebur128=framelog=quiet -f null -`.

### 4. (optional) Schedule to all socials via GHL MCP

1. `mcp__ghl__locations_get-location` → confirm timezone (e.g. Asia/Karachi +05:00).
2. `mcp__ghl__social-media-posting_get-account` → account IDs (cached in `references/ghl-accounts.md`).
3. Upload the rendered mp4 to GHL media → get the CDN URL (user does this, or media API).
4. Write `schedule.config.json` (one entry per platform, each with its OWN human caption + hashtags),
   then `python <skill>/scripts/make_schedule_plan.py schedule.config.json` to get the exact payloads.
5. Fire each payload with `mcp__ghl__social-media-posting_create-post`. Same-platform accounts batch in
   one call; different captions = separate calls.

## Captions (per platform, human, psychology-led)

Different hook + different hashtag set per platform. Humanizer rules: no em-dash spam, contractions,
varied sentence length, real specifics. Travel/personal = NO agency pitch; handle `@yourhandle`.
Hooks by platform: FB = nostalgia + reciprocity question · IG = identity/FOMO + save-bait · TikTok = POV +
curiosity gap · YouTube = curiosity + completion · LinkedIn = reflection + universal lesson.

## Files

- `scripts/build_cut.py` — single-pass render, config-driven, NVENC auto-fallback.
- `scripts/make_schedule_plan.py` — offline builder for the staggered GHL create-post payloads.
- `references/pipeline-notes.md` — the gotchas (read before debugging).
- `references/ghl-accounts.md` — your account ID map + per-platform create-post rules.
- `assets/fonts/` — impact.ttf, arialbd.ttf.

## Reference build

`<repo>/sunset-reel-2026-05-27/` (60s + 4min cuts, PUBLISH-PACKAGE.md).
