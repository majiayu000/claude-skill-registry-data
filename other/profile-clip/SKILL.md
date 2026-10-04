---
name: profile-clip
description: Sidecar-free style analyzer — reduce ANY finished vertical short (ours in output/ OR a downloaded Group C exemplar) into a versioned Style Profile JSON using ONLY pixels + audio, never our internal edit plans. Deterministic tier (ffmpeg scene-detect for cut rhythm, silencedetect + RMS for speech/SFX/music, MediaPipe face sampling for cutaway fraction, Canny caption-band density) fills every quantitative field; ONE optional Claude vision call on a director-pass contact sheet fills the enumerated judgment fields (broll_mode, caption_style, production_class, hook_device). The shared organ of the style-replication loop — style-corpus profiles Group C exemplars with it and style-gate profiles our span 0 with it, so comparison is fair (delivered pixels vs delivered pixels). Non-fatal, idempotent (.ppmeta). PROFILE_VISION=0 skips the vision call.
---

# profile-clip

```bash
bash .claude/skills/profile-clip/profile-clip.sh <clip.mp4> <out.styleprofile.json> [--no-vision] [--pane <p>]
```

Output: `<out>.styleprofile.json`, `style_profile_version: 1` per
`SPEC-style-replication.md` — `duration_sec`, `cuts{cuts_per_min, median_shot_sec,
p90_shot_sec, longest_static_gap}`, `speech{words_per_min, max_silence_sec,
speech_fraction}` (words_per_min via local whisper when available, else absent),
`visual{face_fraction, cutaway_fraction, cutaway_count, opens_on_face}`,
`captions{present_fraction, band}`, `audio{onsets_per_min, music_floor_db,
music_present}`, `hook{first_cut_sec, title_overlay_open}`, `vision{broll_mode,
caption_style, production_class, hook_device, confidence}`, `meta{needs_vision}`.

Routing (UniRoute principle): the cheap tier decides everything it can and lists
what it can't in `meta.needs_vision`; exactly one vision round-trip fires only
when that list is non-empty and `PROFILE_VISION=1`. Vision failure → the
deterministic profile ships with `vision:{}` (the match gate only reads
deterministic levered fields, so the gate still works).

Env: `PROFILE_VISION` (1), `PROFILE_FRAMES` (12), `PROFILE_SAMPLES` (16 sampled
frames for face/caption stats), `PROFILE_SCENE` (0.3), `PROFILE_TRANSCRIPT`
(pre-existing transcript json to skip whisper), `PROFILE_MUSIC_DB` (-48).
