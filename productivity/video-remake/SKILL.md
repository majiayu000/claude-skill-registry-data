---
name: video-remake
description: >
  Recreate or remix one supplied reference video with replacement characters,
  products, branding, props, or scenes. Use when the user asks to replicate a
  video, remake a clip, 复刻视频, 剪同款, 换脸, or make a version of a supplied
  video with controlled replacements. The source video must remain attached.
metadata:
  author: renoise
  version: 0.1.1
  category: video-production
  tags: [video, remake, replication, replacement, portable]
---

# Reference Video Remake / 复刻视频 / 剪同款

This workflow resolves replacement slots before final generation. The current host owns authorized media analysis, materials, live capabilities, costs, spending approvals, and tasks. This skill owns slot matching, creative decisions, and resumable plan state kept in the conversation.

## Runtime Boundary

Use only capabilities and references exposed by the current host. Do not invoke local executables, request filesystem paths, or emulate missing analysis/material/task operations. Before selecting a model or writing prompts, read `../model-routing/SKILL.md` and inspect live capabilities.

Use the user's language for analysis, plans, approvals, and results. If retained or replacement content contains dialogue, voiceover, or narration, use the explicitly requested or safely inferable spoken language; clarify only when ambiguous, and keep every spoken line verbatim in that language.

## Non-Negotiable Source Policy

The source video is always attached to final generation through a compatible video role advertised by the selected model.

Before planning replacements:

1. Query live video-model capabilities.
2. Select a model that advertises both a compatible source/reference-video role and every image role needed by replacement slots.
3. Check guidance, reference counts, duration, ratio, audio behavior, and role combinations.
4. If no model supports the complete source-video + replacement-image combination, stop and explain. Never omit the source video or invent a role.

The final prompt must state that the source video supplies timing, camera motion, composition, transitions, effects, pacing, and emotional beats. Replacement materials supply identity, product, wardrobe, props, and other slotted content. This text reduces accidental copying but is not a security boundary; normal moderation rules still apply.

## Phase 1 — Analyze and Build a Remake Plan

Use the host's media-analysis capability in template/video mode on the authorized source. If that capability is unavailable, stop; do not request a local command or fall back to copied model code.

The result should contain:

- factual analysis: summary, timeline, composition, style, subjects, and audio;
- a model-neutral prompt with `{{slot_id}}` placeholders;
- slots: each replaceable character/product/object/scene/style plus a reference-image prompt;
- warnings: inferred or uncertain details.

Maintain this plan in the conversation so retries resume known task/material IDs instead of recreating charges:

```json
{
  "version": "v1",
  "source": {
    "authorizedRef": "host reference",
    "materialId": null,
    "role": null
  },
  "analysis": "structured analysis result",
  "videoModel": null,
  "imageModel": null,
  "prompt": "template containing {{slot_id}} placeholders",
  "slots": [
    {
      "id": "subject_1",
      "type": "character",
      "description": "replacement lead",
      "prompt": "English reference-image prompt",
      "source": "user|library|generated|missing",
      "materialId": null,
      "materialName": null,
      "role": null,
      "taskId": null
    }
  ],
  "videoTaskId": null
}
```

Do not store API keys, signed URLs, credential contents, or arbitrary host paths.

## Phase 2 — Fill Replacement Slots

Use this priority:

1. User-provided host-authorized material that clearly matches the slot.
2. Existing owner-scoped Renoise material confirmed by the user.
3. Generate a replacement image from the slot prompt through the active host execution workflow.

Never let filename similarity alone choose a character or product. Show the proposed mapping with source, description, and intended role.

### Slot Plan and Cost

Present in the user's language:

- source-video summary and warnings;
- extracted timeline/style at useful density;
- every replacement slot and proposed source;
- selected image/video models from live capabilities;
- live estimated cost for missing slot images;
- the fact that the source video will be attached to final generation.

If a proposed slot mapping is ambiguous, ask the user to resolve that mapping. Otherwise, hand each requested missing slot and its complete parameters to the active host execution workflow.

For every generated slot:

1. Follow the host's execution, estimate, and approval policy.
2. Record any task identifier returned by the host immediately.
3. Resume that task after a wait interruption; never repeat paid execution blindly.
4. Register the approved result as a reusable material only once.

For user-provided references, register the authorized item once. Record the returned material ID and full server filename. Prompt mentions must use that complete filename, including extension.

Show generated slot images and let the user replace/regenerate individual slots. Do not proceed until all required slots are approved.

## Phase 3 — Prepare Final Generation

Inspect the selected video model again immediately before generation. Then:

1. Register the source video once.
2. Assign it a compatible advertised source/reference-video role.
3. Assign every approved slot a compatible advertised image role.
4. Verify combined reference counts and role combinations.
5. Replace every `{{slot_id}}` with the corresponding exact `@material:{id}` token returned for its registered replacement material.
6. Add an explicit source lock: source video controls motion/editing/style; slot materials control identities and replaceable content.
7. Preserve source dialogue only when the user explicitly wants it and spoken language has been confirmed.

The final prompt must contain no unresolved placeholder.

Request a live estimate with actual duration, resolution, output controls, and full material set; also read the live balance.

### Final Prompt, Assets, and Video Cost

Present in the user's language:

- full final prompt;
- source video → exact material ID and role;
- every slot → exact filename, material ID, and role;
- generation parameters;
- final estimated cost and account balance.

Hand these complete arguments to the active host execution workflow; do not assume a particular tool, command, card, or approval interface.

## Phase 4 — Generate and Resume Safely

Execute through the active host workflow and record any returned task identifier immediately. Resume that same task after interruption or timeout; never repeat paid execution blindly.

Return the result URL, task ID, source/slot mapping, and warnings. For revisions, keep approved slot materials and change only the identified prompt dimension unless the user asks to replace an asset.

## Failure Rules

Do not pre-screen the source, replacement materials, or prompts. Continue normally unless the host returns an explicit content-review error.

| Failure | Action |
|---|---|
| Media analysis unavailable | Stop and explain; do not fall back to a command or copied model code. |
| No model supports source video + slot images | Stop; do not omit the source or invent roles. |
| Source video exceeds supported limits | Ask for/approve a shorter source; do not silently clamp it. |
| Slot generation fails | Keep successful slots and retry only the failed slot after approval. |
| Wait times out | Resume the recorded task ID. |
| Host returns `INPUT_*` / `OUTPUT_*` content-review error | Report the actual error and stop; do not retry paid create or suggest bypasses. |
| Output copies source identity despite slots | Strengthen the source lock or replace the conflicting source; never claim text guarantees isolation. |
