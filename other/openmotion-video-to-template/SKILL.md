---
name: openmotion-video-to-template
description: Rebuild a reference video (pure motion graphics or mixed media with products, people, or audio) into a reusable editable OpenMotion template with source files, assets, preview, editing guide, and folder or ZIP delivery. Use only when a reusable template is requested; use openmotion-recreate for a single film recreation, openmotion-template-to-video for adapting an existing template, and openmotion-director for original videos.
---

# OpenMotion Video to Template

This is the openmotion-video-to-template production entry, selected for a requested reusable template. Read [shared context](../openmotion-production/references/context.md) for the current scope and reuse available bodies without returning to the router. MCP-only clients use resources/read `openmotion://workflow/video-to-template/start` for this same file; follow supporting references only when needed. Revisions to an existing template draft use the [shared edit workflow](../openmotion-production/references/edit.md). A request to recreate a finished video without a reusable-template deliverable stays with [openmotion-recreate](../openmotion-recreate/SKILL.md).

Deliver a reusable native HyperFrames project with local assets and an actual preview. Keep controlled text, brand overlays, graphics and timing editable. When reference footage, product imagery or sound carries part of the film, reconstruct that role as a separate, replaceable asset in the same timeline.

Closely match the reference's pictures, composition, motion and pacing while preserving editability. Reproduce texture, depth and lighting present in the reference; do not add decorative effects merely to make it look more polished.

When a reference comes with change requests, deliver the faithful template first and apply those changes separately through `openmotion-template-to-video`; do not mix a remix into the faithful baseline.

Follow the [shared material policy](../openmotion-production/references/materials.md). Use the [mixed-media workflow](references/rebuild.md#rebuild-mixed-media-shots) only when images, footage or audio need to be sourced or recreated. Code-only Motion never enters provider setup or generation.

## Understand the requested result

Obtain and read the whole reference through the shared [reference reading and measurement](../openmotion-production/references/reference-video.md) method before choosing implementation. Use its local sound checks when the active model's audio input is unavailable or unknown. Preserve the link's URL and the local copy's checksum.

Preserve the reference's content, wording, brand, composition and motion as they are; do not pre-substitute them. Content replacement happens later with `openmotion-template-to-video`.

Work independently on ordinary creative decisions. Where the reference is ambiguous, choose the most faithful reasonable option and record the choice and trade-off in `TEMPLATE.md`. If generation needs spend consent not covered by the task, follow the media Skill for the planned batch. If an input cannot be obtained or decoded, report the specific blocker.

## Choose an editable representation

Apply the shared [editable representation](../openmotion-production/references/reference-video.md#choose-an-editable-representation) and [text and fonts](../openmotion-production/references/reference-video.md#text-and-fonts) rules. A template's content stays editable for later replacement: keep wording, brand, images and named objects easy to locate, declare common edits as root variables, and make distinctive lettering settable for new words. Record font substitutions and other approximations in `TEMPLATE.md`.

## Make and check the work

Read the pinned native authoring guide and [runtime adapter](../openmotion-production/references/production.md). For a portable folder, create a separate working directory and use the pinned native CLI; this requires host filesystem/shell capabilities. For a managed project, reuse its projectId or create a carrier with `openmotion_create_project`: use projectType=reference_video with an actual HTTP(S) referenceUrl or known referenceVideoId; for a local video use projectType=natural_language and record the local reference/checksum in requirements. Include requestId, title and requirements. Creation records the source but does not analyze or recreate the video. Read sources/current versions with `openmotion_get_project`, import supplied local files with `openmotion_import_assets` or adopt a selected workspace asset version as described by the [media Skill](../openmotion-media/SKILL.md), and save native text through `openmotion_edit_project` with projectId, requestId, expectedRevision and expectedVersionId. Read the new version after imports or GUI changes. Do not assume a catalog ID exists, write reserved metadata, or bypass managed-project version protection with direct filesystem writes.

Use the shared [runtime and media-tool paths](../openmotion-production/references/reference-video.md#locate-the-pinned-cli-and-media-tools) to read the guide and locate the CLI. Do not call `openmotion_open_preview` just to obtain paths: it runs lint and selects an existing project in Studio. Initial template packaging can run in the background; follow-up content edits apply the shared [continuing-edit preview rules](../openmotion-production/references/native.md#continuing-edits), with explicit background requests taking precedence. Use host capabilities to obtain and analyze video, make the comparison, and package an independent folder. Report a concrete capability gap if any of these steps is unavailable.

Use the shared [measurements](../openmotion-production/references/reference-video.md#measure-specific-questions) for questions that need exact timing, dimensions or layout, and [record them](references/measure.md) in `TEMPLATE.md`. Use [rebuild guidance](references/rebuild.md) for grouping, media and edit dependencies. For an unfamiliar or difficult visual system, a short representative segment can establish a useful approach before expanding the film; this is advice, not a mandatory extra stage.

Compare actual frames with the reference while developing, and apply the shared [fidelity checks](../openmotion-production/references/reference-video.md#check-fidelity-and-edit-dependencies): bounded repair, hard cuts and edit dependencies. Record an issue that bounded repair does not resolve in `TEMPLATE.md` and move on.

Finish with [technical checks and packaging](references/verify.md) and the [portable project contract](../openmotion-production/references/portable-project.md). Deliver the complete folder/ZIP, preview and cover, with one `TEMPLATE.md` inside. Do not require registration, a template ID or a custom content schema. Keep the reply short and in the user's words: absolute-path links to the preview, the template and the original-versus-template comparison; what can be changed; and where it still differs from the original. Technical check results stay in `TEMPLATE.md`; mention one in the reply only when it affects the user, such as a silent tail or a substituted font. Humans decide visual acceptance. Do not reject or repeatedly rework a deliverable solely because of a similarity score or your own taste.

Keep two checks separate: reference-to-rebuild uses diagnostics and human visual judgment; the package check confirms the unpacked ZIP renders elsewhere without missing files or creator-machine paths, with the frame rate, frame count and duration of `preview.mp4`. It is not a pixel comparison; do not spend repair rounds on invisible differences.

[Guidance sources](references/rule-sources.md) separates reviewed material, observed evidence and advice. Do not treat one sample or another product's documentation as a universal effect guarantee.
