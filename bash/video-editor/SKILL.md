---
name: video-editor
description: Cinematic video post-production for TeamDay. Extract reference frames, compose multi-scene sequences with per-scene colour grading + text overlays + xfade transitions, append TeamDay logo endcards, mux music. Pattern ported from Jam/SuperScale's Seedance 2.0 pipeline. Use after Seedance/Kling/Wan generation to assemble a final branded film.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Video Editor Skill

Post-production pipeline for AI-generated video clips. Takes raw 720p/1080p clips (typically from Seedance 2.0 or Kling) and produces a branded cinematic film.

Every script lives at `.claude/skills/video-editor/scripts/`. Reference material from Jam's SuperScale work is in `reference/`. Brand assets (TeamDay logo, Inter fonts) are in `assets/`.

## Core capabilities

| Script | What it does |
|---|---|
| `extract_frames.py` | Pull N frames/sec (or N samples) from a reference video for vision analysis — how to reverse-engineer Jam's or any competitor's cinematic style |
| `compose_scenes.py` | Jam-style multi-scene composer — per-scene colour grade (`eq`/`curves`), text PNG overlays with fade in/out, xfade transitions. Library + CLI |
| `append_endcard.py` | Render TeamDay logo endcard (logo + wordmark + rule + tagline + URL) and append to any video with fadeblack transition |
| `mux_audio.py` | Fade-in/out audio mux without re-encoding video. For adding ElevenLabs Music or voiceover |

## Typical workflow

```
1. Generate raw clips          → seedance-specialist / ai-video-creator agent
2. (Optional) Analyse a ref    → extract_frames.py  (get 1fps PNGs, read w/ vision)
3. Compose + grade + overlay   → compose_scenes.py  (Jam premium pattern)
4. Append branded endcard      → append_endcard.py  (default TeamDay logo)
5. Mux orchestral score        → mux_audio.py       (fade in/out, preserve video)
```

## Reverse-engineering an existing video

When asked "recreate this video in our style" or "match Jam's orchestra video":

```bash
# 1. Extract 1 frame/sec (or N samples) as PNGs
python3 .claude/skills/video-editor/scripts/extract_frames.py \
    reference.mp4 --fps 1 --out /tmp/ref_frames --size 1280x-1

# 2. Read each frame via the Read tool to vision-analyse composition,
#    lighting, camera direction, subject, colour grade. Use that to
#    draft new Seedance keyframe prompts matching the style.

# 3. Generate new keyframes + clips (delegate to ai-image-creator +
#    seedance-specialist).

# 4. Compose using compose_scenes.py with scene configs that mirror
#    the reference's grade (contrast/sat/curves) — borrow from
#    reference/compose_premium.py for proven values.
```

## Start-to-end motion (Seedance first_frame + last_frame)

For "here's the start, here's the end, do the motion between":

- Use the **seedance-specialist** agent (not this skill) — Seedance 2.0's
  `imageToVideo` accepts `first_frame` + `last_frame` content roles. The
  specialist agent knows the API.
- Pass it the two PNGs + a motion prompt. You receive one MP4 back.
- Then use **this skill** for post: `compose_scenes.py` to grade/overlay,
  then `append_endcard.py` to brand.

## Jam's proven colour grade presets (from compose_premium.py)

Each scene in Jam's premium showcase used these values. Useful starting points:

| Mood | contrast | sat | bright | r_curve | g_curve | b_curve |
|---|---|---|---|---|---|---|
| **Warm anticipation** (amber-heavy, low exposure) | 1.35 | 1.20 | -0.04 | `0/0 0.4/0.32 1/0.88` | `0/0 0.45/0.48 1/0.92` | `0/0.05 0.35/0.45 0.75/0.9 1/0.98` |
| **Teal-amber reveal** (complementary split) | 1.40 | 1.35 | -0.02 | `0/0.02 0.5/0.5 1/0.94` | `0/0 0.5/0.5 1/0.92` | `0/0.08 0.45/0.6 1/1` |
| **Balanced warm-cool** (harmony scenes) | 1.30 | 1.40 | 0.00 | `0/0 0.55/0.48 1/0.86` | `0/0 0.5/0.52 1/0.93` | `0/0.06 0.45/0.62 1/1` |
| **Golden hero** (warm, high exposure, vignette) | 1.25 | 1.30 | 0.02 | `0/0.02 0.5/0.6 1/1` | `0/0 0.5/0.5 1/0.9` | `0/0 0.5/0.35 1/0.76` |
| **High-tech cool** (dashboards, cyan accent) | 1.35 | 1.20 | 0.00 | `0/0 0.6/0.5 1/0.82` | `0/0 0.5/0.52 1/0.95` | `0/0.06 0.4/0.65 1/1` |

## Compose config (JSON for CLI)

```json
{
  "out": "final.mp4",
  "endcard": "endcard.mp4",
  "dur": 4.0,
  "xfade": 0.45,
  "fps": 24,
  "W": 1920,
  "H": 1080,
  "transitions": ["fade", "dissolve", "fade", "dissolve", "fadeblack"],
  "scenes": [
    {
      "video": "raw/s1.mp4",
      "title": "Your team",
      "subtitle": "is always on.",
      "contrast": 1.35, "sat": 1.20, "bright": -0.04,
      "r_curve": "0/0 0.4/0.32 1/0.88",
      "g_curve": "0/0 0.45/0.48 1/0.92",
      "b_curve": "0/0.05 0.35/0.45 0.75/0.9 1/0.98",
      "vignette": true
    }
  ]
}
```

Run: `python3 compose_scenes.py config.json`

## Library usage (Python)

```python
import sys
sys.path.insert(0, '.claude/skills/video-editor/scripts')
from compose_scenes import Scene, compose

scenes = [
    Scene('raw/s1.mp4', title='Your AI team', subtitle='is always on.',
          contrast=1.35, sat=1.2, bright=-0.04, vignette=True),
    # ... more scenes
]
compose(scenes, out='final.mp4', dur=4.0, W=1920, H=1080)
```

## TeamDay branding (non-negotiable)

- **Logo** — `.claude/skills/video-editor/assets/teamday_logo.png` (Vector-3 "Y" emblem from `docs/brand/A_4/`). This is the ONLY approved logo. Do not substitute.
- **Fonts** — Inter Bold / Medium / Regular, shipped with this skill.
- **Endcard tagline variants** (pick or remix):
  - `Your AI workforce.`
  - `The team behind every great team.`
  - `Always on. Never tired.`
- **Never use** — the word "conductor" in copy (deprecated framing per 2026-04-18 feedback — founders lead; AI works *alongside*, not *under*, them).

## Related agents

- **ai-video-creator** — generates raw clips via Kling/Wan (no Seedance)
- **seedance-specialist** — generates raw clips via Seedance 2.0 (first+last frame, text-to-video, editing, extension)
- **ai-image-creator** — generates keyframes via Flux/Grok/Gemini/OpenAI

This skill runs *after* those generate raw footage. It is the branding/post-production layer.

## Provenance

Pipeline pattern lifted from `reference/compose_premium.py` — Jam Alinson's
SuperScale premium showcase compositor (4-scene cinematic with xfade + grade
+ text overlays). Kept as a reference for future tuning; adapted into a
reusable library in `scripts/compose_scenes.py`.
