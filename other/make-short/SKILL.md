---
name: make-short
description: Turn a long-form Monkey App / video-chat recording into finished captioned 9:16 shorts. Use when the user wants shorts, clips or reels cut from a long video.
---

# Make shorts from a long-form video

Details live in `long-form-to-shorts-video-editing/monkey-app-video-chat/claude.md`. Read that, not the scripts.

## Steps
1. **Get the source:** `python download_source.py <drive link>` into `input/`. Delete it after rendering, because sources are temporary.
2. **Default: let Claude pick the moments.** `python run_pipeline.py --video input/X.mp4 --auto 6` transcribes the whole call, scores every window (`find_moments.py`, borrowed from OpenShorts), and renders the global top 6 as `short_N_v1.mp4`, each starting on its hook and ending on its payoff. The ranked picks with reasons are saved to `work/<stem>_moments.json`. Show the user the scores and reasons with the renders.
3. **Manual override:** when the user names specific moments, pass `--segment a:b --segment c:d ...` instead (the keyword/face hook scan picks the start inside each segment).
4. **Gates run automatically on the new files in `output/`:** specs, black/frozen/silent stretches, loudness, face on screen, and the caption safe zone. Fix whatever fails, then re-render that segment only.
5. **Prioritise flirt moments:** keep the flirt beats, and cut or compress small talk (user feedback).
6. **Open each final render automatically** for the user (user preference).
7. **Hand off to `post-short`** once the user approves.

## Gotchas (keep this list updated)
- **`--auto` uses its own `<stem>_full_transcript.json`,** because a manual run's transcript only covers the requested segments.
- **The auto-picked hook** isn't always on the right person. The face-on-screen gate catches crop loss, but not a wrong-person opening, so check the first 3s on anything new.
- **Re-rendering one version:** every render writes `output/<name>.render.json` (video, start, duration, transcript). Re-render with `python render_short.py --video .. --start .. --duration .. --transcript .. --out output/<name>_v(N+1).mp4`, with no hook re-analysis needed.
- **Version outputs as `short_N_vK.mp4`.** Only the newest version gets checked.
- **Fixed 2026-09-26:** captions moved to `SOLO_CAPTION_Y=1500` (safe zone), and renders now get a loudnorm pass to -14 LUFS. `short_1_v32` was the first render to pass every gate.
