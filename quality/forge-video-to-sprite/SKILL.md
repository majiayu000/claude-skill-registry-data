---
name: forge-video-to-sprite
description: "Use when existing, MiniMax Hailuo, Jimeng, optional local ComfyUI MiniMax H3 video must become a validated 2D Sprite animation."
---

# Forge Video to Sprite

Use this Skill for a local MP4, MOV, WebM, or an explicitly selected generated
motion clip that must become game-ready Sprite frames. Keep the repository root
and shared `src/` package available; the launcher is
`skills/forge-video-to-sprite/scripts/run.py`.

## Standard interaction

1. Extract the character, action, view, camera, loop, start/end pose,
   background, frame densities, outputs, anchor, canvas, processing mode, and
   engine notes from the request and conversation.
2. Ask one consolidated creative/delivery confirmation for missing or
   contradictory fields. Do not preflight a provider or create a paid task
   before this confirmation.
3. Route explicitly to `existing-file`, `comfyui-h3`, `minimax`, or `jimeng`.
   `comfyui-h3` uses the conditional `comfy-mcp` backend. Hosted generation
   asks for `api` or `cli` in the same route choice. Detection reports
   availability; it never chooses or switches a route or backend.
4. For `comfyui-h3`, require the H3 Prompt Writing Skill and Comfy MCP. For a
   local H3 2D game-character or Sprite animation, also read
   [`references/h3-character-quality-profile.md`](references/h3-character-quality-profile.md)
   before writing the prompt. Merge its quality and identity blocks into the
   H3-required `integrated_multimodal_description`; do not apply it to
   unrelated video, map, audio, existing-file, or hosted-provider requests.
   Use the prompt Skill for the selected H3 mode, then preflight and validate
   the local workflow. Bind the prompt, references, workflow, model, duration,
   resolution, and their hashes before execution. Inspect the graph for Cloud
   or partner nodes; obtain explicit spend confirmation when it can consume
   credits or the billing boundary is unverified. A fully local graph needs no
   paid confirmation.
5. Run a confirmed ComfyUI graph once, persist its `prompt_id`, and recover it
   through the Comfy MCP job/status and output-fetch tools. Never rerun an
   uncertain graph automatically. Fetch one immutable video before local ingest.
6. For MiniMax Hailuo or Jimeng, refresh the provider model snapshot, show provider,
   backend, region, model, mode, references and hashes, duration, resolution,
   billing context, estimate status, and request fingerprint. Ask for one
   paid-submit confirmation. An unverified estimate is labelled unverified and
   must be acknowledged explicitly. The current MiniMax-H3 V2 profile and its
   exact duration, resolution, ratio, and reference limits are visible; a
   discovered-unprofiled model is shown but cannot be submitted through API.
7. Submit exactly once after the confirmation is persisted. Query or download
   an existing task when recovering; never resubmit `submission_unknown`.
8. Ingest the immutable video, sample by presentation timestamp, clean and
   align frames, export the requested densities, and run deterministic checks.
   For game Sprite output, use the strict `canvas_policy` by default and use
   `safe_frame_margin: 0` unless an optional positive guard band is desired;
   the complete character and every moving
   prop must remain inside that safe frame at every requested density.
9. Present source interval, timestamped contact sheet, transparent GIF,
   motion-difference image, anchor diagnostic, strips, and sheets for the final
   motion review. Only a current approved review allows publication.

Existing-video work never invokes a provider. Local processing changes reuse the
same source video and do not create a new paid task.

- Provider subprocesses use binary UTF-8 JSON, and chroma delivery must pass the all-density residue gate before publication.

## Canvas containment contract

Game Sprite delivery is governed by a geometric frame contract in addition to
the visual review. `canvas_policy` defaults to `strict`; use `report-only` only
when a preserved-background or non-game run cannot produce a foreground mask.
`safe_frame_margin` is an optional normalized inset (default `0`) applied to
each side of the delivery canvas. A zero margin means the full canvas is the
allowed area; being close to or exactly on an edge is acceptable. The report
records per-frame `frame_bounds`, the half-open safe rectangle, `swept_bounds`
for the union of all visible frames, `minimum_margin`,
`edge_contact_frames`, `out_of_safe_frame_frames`, and
`source_edge_contact_frames` captured before `tight` trimming.

In strict mode, a visible foreground or defining weapon that leaves the safe
frame is a deterministic failure and cannot be published, even when a manual
review is approved. Exact edge contact is not itself a violation; it is
recorded as `needs_attention` for manual clipping and equipment-completeness
review. A preserved opaque background is explicitly
`foreground_evaluable=false` and is also a deterministic failure under strict
policy; choose `report-only` only when manual review is intentionally allowed.
It is never silently claimed to be contained. Tight layout must not erase
source-edge evidence by recentering a cropped weapon; source-edge evidence is a
review warning, not an automatic margin failure.

Manual review must include the exact checks `no-canvas-clipping` and
`equipment-in-safe-frame`. Inspect the anchor diagnostic's safe rectangle and
swept bounds before approving an attack, projectile, shield, or other moving
prop. Reject any candidate that needs a camera pan, zoom, crop, or out-of-frame
weapon tip to complete the action.

## Local H3 game-character profile

Use this profile for a stationary character attack whose body must stay on one
tower or platform while a bow, arrow, staff, or other prop extends beyond the
body:

1. Use `i2v-first-tail` / FL2VA and connect the same ready-pose image to both
   the H3 `first_frame` and `last_frame` inputs. A prompt that merely says
   "return to the start" is not an end-frame condition.
2. Use a fixed seed and a valid H3 `17k + 5` length (124 frames is the default
   five-second baseline). Describe the complete duration, including the final
   return and hold; select the shorter gameplay interval later by presentation
   timestamp. I2VA/FL2VA selection remains action-specific: use FL2VA when an
   exact first and last pose are required, and use I2VA when the approved
   opening frame should develop forward without an exact final keyframe. The
   mode must be justified by end-pose requirements and visual review, not
   treated as a universal sharpness switch. The fixed seed supports provenance
   and reproducibility; it does not promise equal clarity across prompt,
   model, software, hardware, or other changes.
3. For a no-motion idle, use one static source image. Do not generate an H3
   video solely to simulate a standing idle.
4. Set the request `layout_mode` to `reference-locked`. This uses the first
   frame's scale and feet anchor for every frame, so an extending weapon cannot
   move or resize the character. The default `tight` layout remains unchanged
   for ordinary clips.
5. Set `canvas_policy: strict`; use the default `safe_frame_margin: 0` unless
   the reference composition benefits from an optional positive guard band.
   Keep the complete body, shield, weapon, projectile origin, and farthest
   point of the full attack sweep inside that safe frame with a locked camera.
   Edge contact is acceptable but must be manually reviewed; the quality report
   must have no out-of-safe-frame `swept_bounds`, and any
   `source_edge_contact_frames` must be explained by complete visible
   equipment.
6. Treat a flying projectile as runtime-owned after the release frame. Reject
   the clip if the held arrow becomes a duplicated, symmetric, malformed, or
   anatomically attached projectile.

Before a local H3 run, inspect the graph with:

```powershell
python skills/forge-video-to-sprite/scripts/run.py video sprite inspect-h3 --workflow inputs/video_minimax_h3_i2v_sageattention.json --out runs/h3/workflow-report.json
```

The report must show one H3 node, connected first and last frames from the same
source, a fixed seed, a valid length, and local-only nodes. This check is
read-only and does not update ComfyUI, install nodes, download models, or run a
generation.

## Conditional prerequisites

The `comfyui-h3` route requires both dependencies below. If a prerequisite is absent during ordinary asset work, report it and stop the selected route. Do not install it. Only when the user explicitly asks to install or enable a workflow, hand off to the repository Agent installation guide. That guide must ask whether to enable ComfyUI MiniMax H3, inspect first, display the missing-component plan, and obtain installation confirmation before installing Comfy MCP or `h3-prompt-writing`.

- [Comfy MCP official installation](https://docs.comfy.org/agent-tools/mcp#installation)
- [MiniMax H3 Prompt Writing Skill official installation](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/README.md#installation)
- [Unified repository installation guide](../../install/README.md)

Other routes remain available when these conditional dependencies are absent.

## Commands

```powershell
python skills/forge-video-to-sprite/scripts/run.py video sprite plan --request inputs/video-request.json --out-dir runs/video --now 2026-08-09T00:00:00Z
python skills/forge-video-to-sprite/scripts/run.py video sprite route --request inputs/video-request.json --out runs/video/source-decision.json --state runs/video/job-state.json --now 2026-08-09T00:00:00Z
python skills/forge-video-to-sprite/scripts/run.py video sprite route --request inputs/comfyui-h3-request.json --selection comfyui-h3 --backend comfy-mcp --available runs/video/comfyui-availability.json --out runs/video/source-decision.json --state runs/video/job-state.json --now 2026-08-09T00:00:00Z
python skills/forge-video-to-sprite/scripts/run.py video sprite ingest --request inputs/video-request.json --video inputs/source.mp4 --repo-root . --out runs/video/video-source-record.json --state runs/video/job-state.json --now 2026-08-09T00:00:00Z
python skills/forge-video-to-sprite/scripts/run.py video sprite process --request inputs/video-request.json --source runs/video/video-source-record.json --repo-root . --out-dir runs/video --state runs/video/job-state.json --now 2026-08-09T00:00:00Z
python skills/forge-video-to-sprite/scripts/run.py video sprite record-review --request inputs/video-request.json --source runs/video/video-source-record.json --processing-result runs/video/processing-result.json --repo-root . --quality-report runs/video/video-quality-report.json --out runs/video/video-motion-review.json --checks runs/video/review-checks.json --now 2026-08-09T00:00:00Z
python skills/forge-video-to-sprite/scripts/run.py video sprite validate --request inputs/video-request.json --source runs/video/video-source-record.json --processing-result runs/video/processing-result.json --review runs/video/video-motion-review.json --quality-report runs/video/video-quality-report.json --repo-root . --final-dir outputs/video --now 2026-08-09T00:00:00Z
```

Provider adapter commands are documented in
[`references/provider-workflow.md`](references/provider-workflow.md). Local
sampling, cleanup, output, and quality details are in
[`references/processing-and-quality.md`](references/processing-and-quality.md).

The hosted-provider command surface is `video provider models`, `preflight`,
`estimate`, `submit`, `query`, and `download`. Local source work uses FFmpeg
and FFprobe without modifying the source video. ComfyUI execution is performed
through Comfy MCP rather than the hosted-provider command surface.

## Safety rules

- Never install FFmpeg, `mmx`, `dreamina`, Comfy MCP, the H3 Prompt Writing
  Skill, Python extras, models, or credentials.
- Never write credentials, authorization headers, Base64 media, signed URLs, or
  raw provider responses to repository artifacts.
- Bind a local first-frame PNG by repository-relative path and SHA-256; create
  any provider Data URI only in memory immediately before the confirmed submit.
- Never retry a paid request automatically, and never switch API/CLI after a
  task has been created.
- Never rerun a ComfyUI graph automatically after an unknown submission result;
  recover the persisted `prompt_id` or inspect the existing queue/history first.
- Treat automatic metrics as review evidence, not proof of identity, anatomy,
  action semantics, or loop quality.
