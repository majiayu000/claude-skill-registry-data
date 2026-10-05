---
name: embed-video
description: Image-to-video craft on the skilyst platform — animate a locked still (first-frame anchor) into a 4-15s clip that keeps the identity of that still, and cut several such clips together without a visible jump. Use when the user has a locked image (or needs one) and wants controlled motion from it, instead of a free text-to-video render.
license: MIT
compatibility: Requires the skilyst runtime (>=0.1.0) with the tool named in manifest.json requires.nodes[].binding and network access to the skilyst API host declared in permission.egress.
metadata:
  skilyst.skill_id: skilyst/embed-video
  skilyst.version: "1.2.0"
---

# Image-to-video: lock the still, animate the change

## When to use

The user has a locked image (or approves generating one) and wants motion from
it: a character shot, a product beat, a shot that must match a neighbouring shot.
Deliverable = one playable video URL per shot, plus the still that anchors it.

Not this skill: a clip with no source image (`skilyst/video-15s`) or a shot whose
motion is driven by a voice track (`skilyst/lipsync-audio-refs`).

## Rule 1 — pick ONE mode per job, never mix (this is the expensive one)

Two modes exist on the video nodes, and they cannot coexist inside one job:

| mode | how it is declared | what the model does |
| --- | --- | --- |
| **frame mode** | `image_roles[0] = first_frame` (optionally `last_frame`) | animates *from* the locked still(s) toward the described end state |
| **reference mode** | `image_roles = [reference_image, …]` (optionally + `video_refs` / `audio_refs`) | treats the image(s) as style/identity reference while generating freely |

Mixing them is rejected upstream with *"first/last frame content cannot be mixed
with reference image, video, or audio"*. That is not a theoretical risk: the
platform's own 30-day failed-node distribution carried 17 jobs killed by exactly
this message, our lane's first i2v attempt was rejected the same way (then a
plain `first_frame` run succeeded for $0.414 at 6s/768P), and the audio-driven
route hits it again (see `skilyst/lipsync-audio-refs`).

The implicit form counts too: **a frame role anywhere makes every other image a
reference** (un-roled images get no role and the upstream reads them as
`reference_image`). So `images=[still, style_ref]` with
`image_roles=[first_frame]` is the same forbidden mix — N images need N frame
roles or the job will be refused. The runtime validator
(`internal/api/validation/seedance_mode.go`) enforces this at submission time for
the seedance family, so the failure is caught before money is spent; do not
"try it and see".

The runtime side of the same rule: `video_refs` and `audio_refs` are mapped
unconditionally to the reference roles (`reference_video` / `reference_audio`) —
"video / audio refs are always reference mode" (`internal/provider/minimax_h3/runner.go`)
— which is why they can never be combined with a frame role in the first place.

## Rule 2 — the first frame carries identity, so build it before you animate

Because frame mode forbids a `reference_image`, identity has to be baked into the
still *before* the animation step: generate the still from the character anchor
(or the approved asset), inspect it, then animate it. *Why: in reference mode a
picture alone is read as a style image — the lane measured identity drift on
batches that handed over an image with no written lock; the fix is either the
frame-mode chain below, or the five-part reference-lock syntax documented in
`skilyst/prompt-craft`.*

When the user has no still yet, generate it with the declared optional image
node (`generate:nb2-image`, fallbacks `generate:nb2-lite-image`,
`generate:gpt-image-2`) and get it approved before animating — an animation of a
still nobody approved is a wasted render.

## Rule 3 — write only the change (I2V prompts are not T2V prompts)

The still already says who/what/where. The prompt spends its budget on motion:

- 15-40 words; camera move + subject motion + environmental micro-motion only;
  never re-describe what is already visible.
- One primary action per shot; environmental motion (steam, drifting mist,
  background passers-by) supports it and must not compete with it.
- **Always give the end state** — `…then settles back into place`, `…comes to
  rest`. *Why: without an end state the shot stalls or keeps drifting at the tail
  of the clip; the tail is exactly where a splice lands.*

## Rule 4 — duration and resolution are mode-dependent

| node | duration | resolution | note |
| --- | --- | --- | --- |
| `generate:minimax-h3` | 4-15 s integer | `768P` (ratio 1.0) / `2K` (×1.6) | primary node; no auto length; 768P at 14 s ≈ $0.97, 6 s ≈ $0.41 |
| `generate:byteplus-seedance-2.0` | 4-15 s in text/image/frame modes; **4-30 s only when `video_refs` is present** (r2v); `-1` = auto | `480p` / `720p` / `1080p` / `4k` | declared fallback; pricing is per second, resolution and model multipliers stack |

A single job cannot exceed the frame-mode cap, so anything longer than 15 s is
several jobs spliced in post. Do not reach for `video_refs` just to unlock 30 s:
that switches the job into reference mode (Rule 1) and changes the price.

## Rule 5 — splice craft for multi-shot sequences

Independently generated clips cut together read as different people unless the
chain is built and verified:

1. Derive the next shot's still **from the previous shot's tail frame** (or a
   frame of it), so the chain is continuous.
2. In frame mode that tail frame becomes the next shot's `first_frame`. In
   reference mode the same craft is expressed as `reference_image` — never carry
   it as `reference_image` while a frame role is present (Rule 1).
3. QA the splice on three elements — shoulder line, camera pitch, light ratio —
   and regenerate the later shot when any of them mismatches. This is a measured
   cost decision: the lane's three-clip trailer had to specify these three at the
   splice or the cut was visible.

## Rule 6 — identity QA thresholds differ for i2v

Sampled frames of an i2v output score lower than a static image, purely from
motion blur and intermediate-frame warping. Measured across 8 shots × 7 frames
(min distribution 0.47-0.75, ±0.03 within a shot, no visible drift): use
**PASS ≥ 0.60, GRAY 0.50-0.60, regenerate below 0.50** on animated frames, and
keep the stricter **0.70** for the still image itself. Applying the static
threshold to i2v frames manufactures false failures.

## Call contract

Bound through the tool named in the manifest
(`requires.nodes[].binding.tool` = `beehive_submit_job`):

| argument | value |
| --- | --- |
| `node_id` | `generate:minimax-h3` |
| `prompt` | motion-only prompt (Rule 3) |
| `images` | `[<locked still URL>]` |
| `image_roles` | `["first_frame"]` (or `["reference_image", …]` in reference mode — not both) |
| `duration` | integer 4-15 |
| `resolution` | `768P` unless a higher tier was approved |
| `ratio` | `9:16` / `16:9` as delivered |

### Runtime support (A1 phase-2)

`beehive_submit_job` forwards every argument this binding declares, under the node
field the manifest names: `prompt`, `images`, `image_roles`, `duration`,
`resolution`, `ratio` (for the still: `prompt`, `images`, `ratio` → the node's
`aspect_ratio`). An argument that is *not* declared here is refused with the declared
list rather than dropped — a dropped image would silently turn an i2v render into a
text-to-video render, at the same price. `images` and `image_roles` are validated as
positionally paired before submission, so the frame/reference mix that the platform
rejects is caught before the job is paid for.

## Hand-off

Report `dest_video_url` verbatim plus the job id, and name the still that anchored
the shot (path or URL) so the sequence can be rebuilt. Report platform errors
verbatim; never substitute a neighbouring take.
