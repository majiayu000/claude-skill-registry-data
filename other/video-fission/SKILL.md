---
name: video-fission
description: >
  Create controlled variants from one owner-authorized source video. Use when
  the user explicitly asks for video fission, multiple video variants,
  controlled variations, or several hypotheses from the same clip. Analyze the
  source first, then resolve what should vary before proposing any generation.
metadata:
  author: renoise
  version: 0.2.2
  category: video-production
  tags: [video, fission, variants, experimentation, portable]
---

# Video Fission

Create a controlled batch of variants from one source video. This is an experiment, not a multi-shot production workflow: vary one axis, or at most two, and lock everything else.

## Runtime Boundary

Use only capabilities exposed by the current host. The source must be one conversation attachment, material, task result, or other video that the host identifies as owner-authorized. Never invent a source, request a host filesystem path, or use more than one source video.

Live model capabilities are authoritative for availability, roles, role combinations, limits, duration, ratio, resolution, and audio controls. Inspect them for every fission run; model names below are routing preferences, not permission to assume a capability.

## Hard Gates

1. **Analyze before resolving the direction.** Once the source is available, use the host's video-analysis capability before finalizing what to vary. If analysis is unavailable or fails, stop. Analysis creates no generation task.
2. **Clarify only when blocked.** If the initial request already names a usable, safe experimental axis, use it after analysis without restating it for text confirmation. Ask one focused question only when the axis is absent, unsafe, or ambiguous; allow a second axis only when the user explicitly needs it.
3. **Default the count.** Use **4 outputs** when no count is supplied; do not ask merely to confirm that default. Four is not a hard cap: accept another reasonable count of at least two, constrained only by live service limits, the total estimate, and the user's budget.
4. **Use one logical batch.** Hand the complete disclosed experiment to the active host execution workflow. Use a native batch primitive when the host exposes one; otherwise follow its documented ordered execution path. Do not invent tool names or execution interfaces.

## 1. Analyze the Source

Report the analysis in the user's language, including:

- subject, setting, actions, camera, composition, lighting, style, pacing/edit structure, duration, aspect ratio, and audio/dialogue;
- dimensions that appear fixed and plausible dimensions to vary;
- uncertain or inferred details as warnings.

Do not resolve an unstated direction until this report exists. If the request already supplies a usable axis, disclose how the analysis maps to it and proceed. Otherwise ask one focused question:

> Which direction should the variants explore? I recommend one axis from this clip's analysis; we can use at most two. The default is 4 outputs, or name another reasonable count.

Offer only source-relevant directions, such as action/motion, camera treatment, pacing, atmosphere/lighting, performance, or transformation. Do not preselect an absent direction for the user.

## 2. Use the Source Video Directly

This workflow has one generation path:

1. Select MiniMax H3 Max (`hailuo-h3-max`) only if the live capability advertises `reference_video`.
2. Use the exact owner-authorized source analyzed in Step 1 as every variant's sole `reference_video` input. If the source reference changes, analyze the replacement before continuing.
3. Refer to that source as `Video 1` in every generation prompt.

Do not extract or upload a frame, and do not replace the source with a `first_frame`. Before handing off paid execution, compare the analyzed source with the live capability's reference-video duration and count limits. If the source exceeds a duration limit, report its measured duration and the live limit when available, ask the user to shorten it below that limit with an editor available to them, then require the shortened source to be referenced and analyzed again. If H3 Max reference-video generation is not live or another source limit is violated, stop and explain the incompatibility. Do not assume a particular host editor, invent another mode, or silently route to another model.

## 3. Design the Experiment

Before submission, show a compact variant matrix in the user's language:

| Variant | Axis value(s) | Distinct hypothesis | Locked dimensions |
|---|---|---|---|
| V1 | ... | If ..., then ... because ... | ... |

Rules:

- Use one axis by default and never more than two.
- Give every variant a genuinely distinct, testable hypothesis; do not use cosmetic synonyms.
- Lock all unselected dimensions across every variant, including model, source video, subject identity, composition, duration, ratio, resolution, audio mode, dialogue, and output controls unless one is the selected axis.
- Keep the same prompt skeleton and change only the clauses that implement the selected axis values.
- If two axes are used, choose intentional combinations; do not create an unrequested Cartesian product.
- Derive every parameter and material role from the selected model's live capability.

## Dialogue and Language

Use the user's language for analysis, questions, matrices, plan text, and results. Prompts are English by default only when they contain no speech.

If any variant contains dialogue, voiceover, or narration, use the explicitly requested or safely inferable spoken language; clarify it only when ambiguous. Keep every spoken line verbatim in that language; never translate it. For dialogue-dense variants, keep the whole prompt in the spoken language. Unless dialogue is the selected axis, lock its text, speaker, delivery, and spoken language across all variants.

## 4. Hand Off One Logical Batch

After the direction, count, hypotheses, prompts, and any spoken language are resolved, hand the complete variant plan to the active host execution workflow. Pass the source aspect ratio, or the closest ratio supported by H3 Max. Preserve any source provenance handle exposed by the host so outputs remain linked to their source where supported.

The execution handoff must:

- keep the whole experiment reviewable as one disclosed plan;
- provide the actual parameters needed for per-variant and total estimation;
- submit the source video directly as every task's `reference_video`;
- follow the host's approval, concurrency, idempotency, and task-tracking rules;
- preserve variant order and never repeat paid execution after interruption.

For revisions, ask which axis value or failed variant to change only when the request is ambiguous, preserve accepted outputs, and hand only the revised experiment back to the host.
