---
name: video-15s
description: Produce a single 15-second vertical short video from a text idea on the skilyst platform. Use when the user wants a 15s social clip (no source media) and expects a finished video file URL. Covers the shot-intent-first prompt skeleton, the cheapest acceptable render tier, and the artifact hand-off.
license: MIT
compatibility: Requires the skilyst runtime (>=0.1.0) with the tool named in manifest.json requires.nodes[].binding and network access to the skilyst API host declared in permission.egress.
metadata:
  skilyst.skill_id: skilyst/video-15s
  skilyst.version: "1.2.0"
---

# 15s Vertical Short Video (text-to-video)

## When to use

The user asks for a short vertical clip generated from an idea, with no source
footage, no reference image and no dialogue track. Deliverable = one playable
video URL.

Not this skill: anything driven by media — a locked still, a voice track, a
reference character — belongs to `skilyst/embed-video` or
`skilyst/lipsync-audio-refs`. The two modes cannot be mixed inside one job (see
the failure modes in those skills).

## Method (order matters)

1. **Intent first.** Decide the single piece of information / emotion this shot
   carries, then the shot size (extreme wide → close-up = information dial).
   Never start from visual adjectives. *What this buys you: the shot size is the
   only framing lever that reliably survives a 15s budget, and adjective-first
   prompts read as a mood board — the model then picks the framing for you.*
2. **One visual centre.** Exactly one dominant element per frame; everything
   else supports it. If squinting at a thumbnail gives two focal points, rewrite.
3. **Lighting with a motive.** Write the key:fill ratio explicitly and give the
   light an in-frame source (window, practical, neon).
4. **One movement per shot.** At most one camera move; lock it with "static" if
   the shot should hold.
5. **Prompt skeleton (camera first):** camera movement → subject + action →
   environment → lighting/atmosphere → style/technical. The full craft rules —
   per-model deltas, reference-lock syntax, dialogue pacing — live in the
   `skilyst/prompt-craft` skill.
6. **Cheapest acceptable render:** provider `minimax-h3`, `duration=15`,
   `resolution=768P` — about $1.04 per clip (69000 µUSD/s × 15s; the 768P
   dimension ratio is 1.0, 2K is 1.6). Do not silently upgrade the tier; a
   higher tier is a separate, user-confirmed decision.

## Call contract

Submit exactly once per run through the tool named in the manifest
(`requires.nodes[].binding.tool` = `beehive_submit_job`) with the bound node id:

| argument | value |
| --- | --- |
| `node_id` | `generate:minimax-h3` |
| `prompt` | the five-part skeleton assembled above, in English |
| `duration` | `15` |
| `resolution` | `768P` |
| `ratio` | `9:16` |

Omitted arguments are filled from `manifest.plan`. The runtime refuses a
`node_id` this skill does not declare, and refuses a second paid job in the same
run — a second render is a new run or an explicit budget decision, never a
retry you take on your own.

## Failure handling (declared, never implicit)

If the cluster does not register `generate:minimax-h3`, preflight blocks the run
and names the declared fallbacks `generate:byteplus-seedance-2.0` and
`generate:drawnow`. Taking a fallback means a different model, price and look,
so it requires the operator's explicit `--allow-fallback`; silently switching
would be the "quiet tier downgrade" the manifest forbids.

## Hand-off

Report the artifact URL verbatim (`dest_video_url`) plus the job id. The video
node also returns `dest_first_frame_url` / `dest_last_frame_url` — auto-extracted
previews, useful for frame-accurate review, not deliverables. If the job fails,
report the platform error verbatim — never substitute a different clip or a
"closest" result.

## Platform constraints this skill depends on

- `generate:minimax-h3`: `duration` 4-15 s, `resolution` ∈ {768P, 2K},
  `ratio` ∈ {21:9, 16:9, 4:3, 1:1, 3:4, 9:16}, RPM gate 100.
- Text mode has no length extension: anything longer than 15 s is several jobs
  cut together in post — see `skilyst/embed-video` for the frame-chain craft
  that keeps such a splice seamless.
