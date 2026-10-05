---
name: lipsync-audio-refs
description: Dialogue shots on the skilyst platform — synthesize the line with TTS first, then drive the shot with that track (audio_refs plus reference images) so the mouth follows the voice and the clip ships with its own audio. Use when a shot has spoken dialogue; covers the 2-15s audio_refs bounds, the first_frame ban in audio mode, and the pacing rule that decides how long the line may be.
license: MIT
compatibility: Requires the skilyst runtime (>=0.1.0) with the tool named in manifest.json requires.nodes[].binding and network access to the skilyst API host declared in permission.egress.
metadata:
  skilyst.skill_id: skilyst/lipsync-audio-refs
  skilyst.version: "1.2.0"
---

# Dialogue shots: TTS first, then audio-driven generation

## When to use

A shot contains spoken dialogue and the mouth must match the voice. Deliverable =
one playable video URL that carries its own audio track, plus the TTS track that
drove it.

Not this skill: silent shots (`skilyst/video-15s`, `skilyst/embed-video`). Do not
"add dialogue later" by dubbing a finished clip — this pipeline is the platform's
only route to a matched mouth (the lane explicitly decided against an external
lip-sync service).

## Pipeline (order is not negotiable)

1. **TTS first** — render the line with `generate:tts-minimax-hd`
   (`text`, `voice_id`, `emotion`, `speed`); keep the mp3.
2. **Drive the shot with that track** — `audio_refs=[mp3]` plus the character
   still(s) as `reference_image`.
3. **Size the shot from the track** — `duration = ceil(audio_seconds) + tail margin`.

## Rule 1 — audio mode forbids frame roles (the 400)

`audio_refs` and `first_frame` cannot appear in the same job. Use
`image_roles=["reference_image", …]`; add `first_frame` (or `last_frame`) and the
submission is rejected — measured twice in the lane: the LIP-1 puncture run
documented *"audio 模式混传即 400"*, and the 5/5 dialogue batch reproduced the rule
(cycle-4: "不能 first_frame——与 audio 模式混传会 400"). The platform's own
validator rejects the mix at submission time for the seedance family, so the
failure is loud and free rather than a paid surprise.

**Trade-off to accept up front:** with no frame role, the composition comes from
the reference images and the prompt, not from a locked first frame. Two references
(character anchor + costume plate) drove 14/14 frames at face-similarity ≥0.78 in
the measured run — so pick reference images whose framing already matches the shot
you want, and write the identity lock (see `skilyst/prompt-craft`) instead of
relying on the picture alone.

## Rule 2 — the voice track must be 2-15 s (one clip)

`audio_refs` accepts a single clip of 2-15 s. A shorter line is refused upstream
as an invalid parameter: a 1.836 s line ("Raise your head.") was rejected, and
re-rendering the TTS at `speed=0.6` produced 2.34 s, which passed. Note where the
bound lives: the **upstream model API** enforces it — the platform's own
submission validator only enforces the mode-mixing rule of Rule 1 (see
`internal/provider/minimax_h3/runner.go`, which maps `audio_refs` straight to
`reference_audio` without a length check). So an under-length line is not caught
by local preflight; it fails on submit/run. Do not assume the speed knob is
linear either — the same batch saw `speed=0.9` have no effect on that line, so
**measure the produced duration of every line** before it becomes an input, and
pad with a beat of room tone if a line is genuinely too short.

## Rule 3 — duration = ceil(audio) + tail

The shot must outlast the voice: `duration = ceil(audio_seconds) + 0.5-1.5 s`
(integer, 4-15 s on `generate:minimax-h3`), which absorbs the start offset and
leaves a beat before the cut. Measured: a 5.076 s line at `duration=6` rendered
6.58 s, leaving ~1.5 s of tail — comfortable. A shot that ends on the last
syllable cuts the performance off.

## Rule 4 — the clip ships with its own audio (and re-synthesized timbre)

The audio-driven route re-synthesizes the speech inside the video: the rendered
clip carries an embedded AAC track, so there is no post-production mux step. The
timbre is close to, but not identical with, the TTS take (measured F0 median
82.7 Hz in the mp3 → 87.3 Hz in the clip). Two consequences: get the voice
approved before batch rendering, and keep the TTS mp3 as the record of the
intended performance.

## Rule 5 — one speaker, one line per shot

Two speakers in one shot split the mouth budget: the model spends the sync on one
of them and the other drifts. Give the second character a body reaction instead,
and cut to their own shot for their line.

## Rule 6 — pacing: ≤8 words per 3 seconds

Budget roughly 2.5 words per second. The measured failure: a 15-word line inside a
3.3 s window came in audibly too fast — **cut the line, do not speed up the
render**. Keep proper nouns and numbers out of the spoken line (put them on screen
in post): the model mispronounces them and they consume the pacing budget.

## Call contract

Bound through the tool named in the manifest
(`requires.nodes[].binding.tool` = `beehive_submit_job`):

| argument | node | value |
| --- | --- | --- |
| `text`, `voice_id`, `emotion`, `speed` | `generate:tts-minimax-hd` | the line, rendered first (2-15 s) |
| `node_id` | `generate:minimax-h3` | video node |
| `prompt` | | performance only: who speaks, how, what the body does — the mouth is driven by the track, not described |
| `images` / `image_roles` | | the character still(s), roles `["reference_image", …]` — **never** `first_frame` |
| `audio_refs` | | `[<tts mp3 URL>]` |
| `duration` | | `ceil(audio_seconds) + tail`, 4-15 |
| `resolution` / `ratio` | | `768P` / the delivered ratio |

### Runtime support (A1 phase-2)

`beehive_submit_job` forwards every argument this binding declares, under the node
field the manifest names: for the dialogue shot `prompt`, `images`, `image_roles`,
`audio_refs`, `duration`, `resolution`, `ratio`; for the TTS node `text`, `voice_id`,
`emotion`, `speed`. An argument the binding does not declare for the chosen node is
refused with the declared list, never dropped — dropping `audio_refs` would produce a
silent shot at the price of a dialogue shot. The 2-15s per-track bound is the upstream
model's rule, not the runtime's: preflight cannot see it, so size the track before
submission.

## QA gates (acceptance, not vibes)

1. **Mouth follows the voice** — the quantitative split is the test: mouth-region
   change is ~frozen during silence and active during speech (measured std 0.5 in
   silent windows vs 5.0 in speech windows). A clip with mouth activity during
   silence fails.
2. **Dialogue present in the mix** — the audio analysis must report the spoken
   line as prominent; nothing else may be.
3. **Identity** — score the animated frames against the anchor with the i2v
   thresholds in `skilyst/embed-video` (PASS ≥ 0.60), with the stricter 0.70
   reserved for the still itself.

## Cost reference

TTS is $0.042 per piece; `generate:minimax-h3` at 768P is $0.069/s, so a 6 s
dialogue shot ≈ $0.41. The measured 5-shot dialogue batch (5 videos + TTS
re-renders + visual QA) came to ≈ $2.09.

## Hand-off

Report the artifact URL (`dest_video_url`) verbatim, the job id, and the TTS mp3
that drove it. Report a rejected submission verbatim (`invalid param`, the mixing
message) — do not re-word a platform refusal into a creative choice.
