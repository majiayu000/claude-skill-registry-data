---
name: like-subscribe-overlay
description: Overlay the branded like/subscribe CTA animation — channel gem avatar + @C0BALT_CUT handle + subscribe/like/bell click choreography — for ~4 seconds WITHIN THE FIRST THIRD of a finished short (start clamped to end by the 1/3 mark, floored after the ~2.5s title card; early placement so viewers who bail never miss it). The animation source is cta.html (HTML+CSS+JS driving the pill pop-in, cursor moves, click punches, bell ring, thumb fill); build-cta.sh renders it frame-by-frame via headless Chromium (Playwright, omitBackground) and ffmpeg-encodes to assets/cta.mov (ProRes 4444 with alpha).
allowed-tools: Bash
user-invocable: true
---

# like-subscribe-overlay

Drops a hook-grabbing branded call to action into the short. A JS-driven
animation plays in the lower third for `dur` seconds starting at `pos`
fraction of the clip (default 0.15), with the start clamped so the whole
CTA lands inside the first third of the clip — where retention is highest —
while staying clear of the ~2.5s title card: a Carbon Black pill pops in carrying the channel
gem avatar (sapphire-ringed, glow breathing) and the `@C0BALT_CUT` handle
(Impact, Platinum, sapphire slashed zero) → cursor enters → clicks
SUBSCRIBE (red → dark, scale punch, expanding ring) → bell rings → cursor
glides left to the thumbs-up → clicks LIKE (thumb fills Sapphire Glow,
scale punch, expanding ring) → holds the final state.

The animation is authored in plain HTML+CSS+JS (`cta.html`) and pre-rendered
once into a transparent ProRes 4444 `.mov` asset (`assets/cta.mov`). Runtime
just composites that asset. The avatar image is `assets/channel.png` (square
crop of the channel gem); replace it and re-run `build-cta.sh` to rebrand.

## Invoke

```
.claude/skills/like-subscribe-overlay/like-subscribe-overlay.sh <input> <out> [dur=4.0] [pos=0.15]
```

- `input`: finished short (any aspect ratio; designed for 1080x1920)
- `out`: output mp4
- `dur`: total CTA duration in seconds (clamped to clip length, default 4.0)
- `pos`: fraction of the clip at which the CTA starts (default 0.15; clamped
  so the CTA ends inside the first third, starts after the ~2.5s title card,
  and never spills past the end of the clip — in that priority order)

## Output

mp4, same dimensions and duration as the input, video re-encoded
(libx264 veryfast crf18), audio re-encoded to AAC 192k. Prints the output
path to stdout. Idempotent: a `<out>.lsmeta` sidecar records the signature
(`dur|pos|asset-version`); a cache hit requires `out` newer than `input`
*and* a matching signature.

## Brand

Colors from `brand/BRAND.md`: pill in Carbon Black `#101418` with a
Sapphire Glow `#2E6BFF` edge, handle in Platinum `#E8ECF1` Impact with the
slashed zero in Sapphire Glow (same visual language as the `watermark`
renderer), liked thumb fills Sapphire Glow. The SUBSCRIBE button stays
YouTube red pre-click for instant recognition.

## Where in the pipeline

Runs after `loudnorm` and before `bg-music` / `save-local`. The overlay
lands inside the first third of the clip (after the title card), so it
composites over whatever is on screen early in the story (captions burn
beneath it for those 4 seconds — intended).

## How

1. `build-cta.sh` (one-time, or whenever `cta.html` / `assets/channel.png`
   changes): `build-cta.js` steps `cta.html`'s deterministic `window.setT(t)`
   frame-by-frame in headless Chromium (Playwright, `omitBackground`) and
   ffmpeg-encodes the transparent PNGs to `assets/cta.mov` (ProRes 4444).
2. `like-subscribe-overlay.sh` time-stretches the asset to `dur` (setpts),
   pins it to the lower third, and `enable`s it for `[start, start+dur]`
   where `start = min(pos * clip_duration, clip_duration/3 - dur)` floored
   at 3.0s (title-card clearance). The CTA overlays SILENTLY — the clip's
   source audio passes straight through (`-map 0:a`, no mix). The old
   bell-ding SFX (`make_sfx.py`) is retired; `make_sfx.py` is unused.
