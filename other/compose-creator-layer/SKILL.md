---
name: compose-creator-layer
description: Composite a generated creator track into a product layer, per beat — in the creator's zone on split beats (either side of a seam), full frame on creator beats, hidden on product beats — with the creator's voice as the audio (loudness -14 LUFS) and an optional ducked music bed, or a music-only or silent master for voiceless formats. Free, local ffmpeg. Pairs with footage-cutlist (the layer) and create-creator-takes-h3 (the creator). Use for split-screen, screen-insert and any creator-over-product format.
status: active
---

# compose-creator-layer

## Run

```bash
python compose.py --layer layer.mp4 --beats cutlist.aligned.json --creator creator.mp4 \
    --out reel.mp4 [--music bed.mp3 --music-db -20] [--head 0.30]
```

- `--layer`: `footage-cutlist` `cut.py` output rendered from the **same** cut list as
  `--beats` (re-render it after `align_beats.py`). `--draft` layers are refused.
- `--creator`: `create-creator-takes-h3` `join_takes.py` output, reel time from 0.
- `--audio creator|music|none`: the voice (+ ducked `--music`), the `--music` bed alone
  (voiceless paid ads), or a silent master (organic posts: the track is added in-platform
  at upload, which is licensed for organic use only).
- The creator track may be shorter than the reel (a 2.3s reaction hook): it only shows
  during its own `creator` beats.
- `--head`: where the crop sits vertically when the creator is scaled to cover an area
  (0 keeps the top, 0.5 centres). 0.30 keeps the head in the upper third.

## Rules

1. **Crop from the take's real size**, never a hard-coded height. A hard-coded 1080 once
   cropped the top half of an upscaled take and blew it up.
2. **No grade.** Chasing a saturation or warmth reading was tried twice and both looked
   wrong. The take goes in as generated.
3. **The voice leads.** A music bed is ducked under the voice (sidechain); the mix is
   normalised to -14 LUFS.
4. **Captions come after this** (`caption-burn`, transcribed from this output).
