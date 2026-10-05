---
name: video-15s
description: Produce a single 15-second vertical short video from a text idea on the Skilyst/Beehive platform. Use when the user wants a 15s social clip (no source media) and expects a finished video file URL. Covers the shot-intent-first prompt skeleton, the cheapest acceptable render tier, and the artifact hand-off.
license: MIT
compatibility: Requires the skilyst runtime with the beehive_submit_video tool and network access to the Beehive API endpoint declared in manifest.json permission.egress.
metadata:
  skilyst.skill_id: skilyst/video-15s
  skilyst.version: "1.0.0"
---

# 15s Vertical Short Video (text-to-video)

## When to use

The user asks for a short vertical clip generated from an idea, with no source
footage and no reference image. Deliverable = one playable video URL.

## Method (order matters)

1. **Intent first.** Decide the single piece of information / emotion this shot
   carries, then the shot size (extreme wide → close-up = information dial).
   Never start from visual adjectives.
2. **One visual centre.** Exactly one dominant element per frame; everything
   else supports it. If squinting at a thumbnail gives two focal points, rewrite.
3. **Lighting with a motive.** Write the key:fill ratio explicitly and give the
   light an in-frame source (window, practical, neon).
4. **One movement per shot.** At most one camera move; lock it with "static" if
   the shot should hold.
5. **Prompt skeleton (camera first):** camera movement → subject + action →
   environment → lighting/atmosphere → style/technical.
6. **Cheapest acceptable render:** provider `minimax-h3`, `duration=15`,
   `resolution=768P` (about $1.04 per clip). Do not silently upgrade the tier;
   a higher tier is a separate, user-confirmed decision.

## Call contract

Call `beehive_submit_video` exactly once with:

| field | value |
| --- | --- |
| `prompt` | the five-part skeleton assembled above, in English |
| `duration` | `15` |
| `resolution` | `768P` |
| `ratio` | `9:16` |

## Hand-off

Report the artifact URL verbatim (`dest_video_url`) plus the job id. If the job
fails, report the platform error verbatim — never substitute a different clip or
a "closest" result.
