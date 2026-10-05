---
name: previs-rerender
description: Requires OFOX_API_KEY — create one at https://app.ofox.ai, plus a publicly reachable reference video the user is authorized to use. Use when a user has a rough 3D white-model, clay, wireframe, blockout, previs, or animatic clip and wants a finished visual treatment that preserves its shot order, cut timing, camera framing, spatial layout, and motion directions. Distinguishes that structure-preserving job from a continuation beginning at the reference's final state. Do not use for two still endpoints (keyframe-animation), for appending and locally joining a new ending (video-extend-edit), or when still-image references must be combined with the video in one request — first/last-frame anchors conflict with video references in the shipped core, while mixed image/video references are untested.
license: MIT
version: "1.0.0"
homepage: https://github.com/ofoxai/skills/tree/main/skills/previs-rerender
metadata:
  author: ofoxai
  version: "1.0.0"
  openclaw:
    requires:
      env: [OFOX_API_KEY]
      bins: [curl, jq]
    primaryEnv: OFOX_API_KEY
    envVars:
      - name: OFOX_API_KEY
        required: true
        description: Ofox API key. Create one at https://app.ofox.ai (Settings -> API Keys). The same key works across every Ofox skill.
    emoji: "🏗️"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/previs-rerender
---

# previs-rerender: turn a locked rough cut into a finished treatment

Use a rough video as the structural reference for a new clip. The reference
already decides the shot sequence, camera positions, edit rhythm, spatial
relationships, and motion directions; the prompt changes the visual treatment
without casually redesigning that structure.

This is a scenario layer over
[`ofox-video-core`](../ofox-video-core/SKILL.md). It owns the choice between a
structure-preserving rerender and a continuation, the prompt contract, and the
artifact review. The core owns credentials, request construction, pricing,
submission, polling, download, error mapping, and the no-resubmit rule. Read
the core's safety contract and
[`approval-gate.md`](../ofox-video-core/references/approval-gate.md) before a
real run.

## Safety and input contract

- Use only footage the user owns or is authorized to transform. Do not upload
  or make a local clip public merely because this route needs a URL; obtain
  explicit authorization for that external write.
- Never print or persist `OFOX_API_KEY`. The core reads it from the environment
  and never needs it inside a prompt, URL, JSON payload, or output file.
- A video reference must be a publicly reachable web URL. A
  `data:video/mp4` URI reached the client payload but the current route rejected
  it before job creation with `reference_video must be provided as a web url`.
- A temporary or signed URL must remain valid until the upstream fetches it.
  Do not paste a signed URL or a payload containing it into chat or logs. A
  completed Ofox job's `unsigned_urls` entry can work, but it may expire within
  about 24 hours.
- The shipped core rejects first/last-frame `frame_images` together with
  `input_references` as `references_conflict`, before estimate or submission.
  Therefore this skill cannot use a previs video with first- or last-frame
  anchors in one job. Material or character images represented as `image_url`
  elements inside `input_references` are a different mixed-reference shape:
  the core can carry it, but this repo has not tested whether the server
  honours it. This v1 workflow does not offer that unmeasured combination.
- One video reference is the documented ceiling. Do not imply that several
  reference videos can be blended.

## Find the execution layer

Resolve the core once, from this skill's directory:

```bash
for d in ../ofox-video-core \
         ../ofoxai-skills-ofox-video-core \
         ~/.agents/skills/ofox-video-core \
         ~/.agents/skills/ofoxai-skills-ofox-video-core \
         ~/.claude/skills/ofox-video-core; do
  [ -f "$d/references/ofox-video.sh" ] && echo "$d" && break
done
```

Examples below use `../ofox-video-core/...`. Substitute the path the probe
found. If nothing is found, tell the user that `ofox-video-core` is missing and
offer this narrow install command for the user to run; do not run an installer
without permission:

```bash
npx skills add ofoxai/skills --skill ofox-video-core
```

This skill needs `ofox-video-core` 2.0.0 or newer because every paid command
below relies on its `--approved` guard.

Run the availability check once per session:

```bash
bash ../ofox-video-core/references/ofox-video.sh check
```

A missing key does not block planning or a dry-run quote. It blocks only the
real submission.

## Choose the intent before writing the prompt

These are two different jobs that use the same request field. Do not mix their
instructions.

| Intent | What the reference means | Output contract |
|---|---|---|
| **Structure-preserving rerender** | The whole clip is a shot and motion blueprint | Replay its sequence in a new visual treatment; same order, boundaries, framing, layout, and motion directions |
| **Continuation** | The clip is preceding footage | Begin from its final state, do not replay earlier layouts, then reveal new action or space |

If the user wants the original and a generated continuation joined into one
file, use `video-extend-edit` for the extraction/join workflow. This skill's
continuation route produces a new standalone segment; it does not append the
source clip.

## Settle the brief

Read the reference description and the user's request first. Ask only for
information that is still missing:

- **Required:** a public video URL, confirmation that the user may transform
  it, and whether the job is rerender or continuation.
- **For rerender:** the target material, lighting, environment, and subject
  treatment; the source duration or intended output duration; target
  resolution and aspect ratio when they are not already stated.
- **For continuation:** what must happen after the final state, what earlier
  material must not replay, and where the new segment should settle.

Do not ask the user to redescribe camera moves already legible in the previs.
Do name the structural cues that will be checked afterward: shot count and
order, cut times, framing or layout per shot, and each important motion
direction.

## Prompt contracts

### Structure-preserving rerender

Write observable constraints, not the vague phrase “follow the reference”:

```text
Treat the reference video as exact previs. Preserve its <N>-shot order, cut
timing, camera framing and movement, spatial layout, subject positions, and
each named motion direction: <cue list>. Replace only the visual treatment
with <materials, lighting, environment, subject finish>. Do not add, remove,
merge, reorder, or extend shots. Do not invent new camera moves or reverse a
motion direction.
```

Keep “take” and “ignore” separate: the video supplies structure and motion;
its rough materials, grid, placeholder geometry, labels, and unfinished
lighting are not appearance targets.

### Continuation

Anchor the opening to the final state and prohibit replay explicitly:

```text
The reference video is preceding footage, not a shot list to replay. Start
from its final composition: <final-state description>. Do not replay <earlier
layouts or actions>. Continue with <new action and camera move>, reveal <new
space or state>, then settle on <new endpoint>.
```

The measured continuation evidence is narrow: one 4-second, 480p Seedance 2.5
job on `byteplus`. It opened on the reference's final right-bay state, moved
the yellow object out to the right, revealed further bays, and did not replay
the earlier three layouts. Do not generalize that one result to every model,
duration, composition, or provider.

## Build and inspect the request for free

Keep the URL in a shell variable. Verify that an unauthenticated ranged read
works; this accepts either a normal `200` or a ranged `206` response and saves
nothing:

```bash
curl --silent --show-error --fail --range 0-0 --output /dev/null "$VIDEO_URL"
```

Build the short JSON value with `jq` and assert its shape locally:

```bash
EXTRA="$(jq -cn --arg u "$VIDEO_URL" \
  '{input_references:[{type:"video_url",video_url:{url:$u}}]}')"
printf '%s' "$EXTRA" | jq -e \
  '.input_references | length == 1 and .[0].type == "video_url"' >/dev/null
```

Then dry-run the exact job. Use the source duration for a structure-preserving
rerender unless the user explicitly wants different timing. Pass the intended
aspect ratio explicitly rather than relying on a default:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate \
  --dry-run --print-payload \
  --model bytedance/seedance-2.5 --provider byteplus \
  --prompt "$PROMPT" --duration "$DURATION" \
  --resolution "$RESOLUTION" --aspect-ratio "$ASPECT_RATIO" \
  --generate-audio false --extra-json "$EXTRA" \
  --out-dir "$OUT_DIR" --name "$NAME"
```

Inspect the printed payload locally and confirm it contains exactly one
`video_url` reference. If the URL is signed, redact its query before relaying
any payload excerpt. The estimate must identify the request as v2v. Do not
replace the script's live quote with a remembered rate.

The measured anchor is only this pair: two Seedance 2.5 jobs, each 4 seconds at
480p on `byteplus`, were quoted at 56 cents and billed 56 cents. Other
durations, resolutions, models, providers, and future prices require their own
dry run.

Show the full approval table from the shared approval reference, including the
single-job and total maximum. Stop here until the user explicitly approves
that spend.

## Submit once after approval

Re-run the same command without `--dry-run --print-payload` and with
`--approved`:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --approved \
  --model bytedance/seedance-2.5 --provider byteplus \
  --prompt "$PROMPT" --duration "$DURATION" \
  --resolution "$RESOLUTION" --aspect-ratio "$ASPECT_RATIO" \
  --generate-audio false --extra-json "$EXTRA" \
  --out-dir "$OUT_DIR" --name "$NAME"
```

`OUT_DIR` must be an absolute path, and the delivered `VIDEO_PATH` must be
reported as an absolute path. If a create response is ambiguous, stop and
check account/job state. If a job id exists, recover with `poll`; never create
the job again because polling or downloading failed.

## Judge the artifact, not `STATUS completed`

For a structure-preserving rerender, compare the source and result manually:

1. List every source composition in order and locate it in the result.
2. Check every named motion direction, not merely that something moved.
3. Inspect frames on both sides of every source cut and measure whether each
   boundary moved.
4. Record any added, missing, merged, or reordered beat.
5. Separately judge whether the requested visual treatment replaced the rough
   one.

A scene detector can suggest candidate boundaries, but it cannot decide the
verdict. On the four-cut control used for this skill, high thresholds missed
all or some true cuts and the lowest tested threshold added a false positive.

For continuation, inspect the opening half-second, then answer three concrete
questions: does it begin from the source's final state, are earlier layouts
absent, and does the requested new action/space appear? If those signatures
are not readable, report the result as inconclusive rather than inventing a
mechanism.

## Evidence boundary

Two paid jobs establish the current guidance, both on
`bytedance/seedance-2.5`, `byteplus`, 4 seconds, 480p, audio off:

- Structure-preserving rerender, job `30c3e3e0-ec28-4988-91a2-95b440a24629`:
  all four compositions stayed in order, all motion directions survived, and
  hard boundaries remained at 1.0, 2.0, and 3.0 seconds.
- Continuation, job `e15cdaef-c1b3-4a23-9ebc-4484be926a1b`: the opening used
  the final reference state, continued rightward into newly revealed bays,
  and did not replay the first three layouts.

This does not establish performance on photoreal footage, longer clips,
1080p, another model or provider, simultaneous appearance images, or several
video references. Treat the first attempt outside the measured pair as an
experiment and say which boundary is untested before the approval table.
