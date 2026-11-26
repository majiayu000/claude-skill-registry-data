---
name: openmotion-recreate
description: >-
  Recreate a reference video (a link or file) as the user's own film with OpenMotion: rebuild it as an
  editable OpenMotion project and hand it over open in the editor, keeping the original content or
  swapping in the user's copy, brand and assets. This includes small edits to
  the user's own finished video when no editable project for it exists. "Make one like this" and "I
  want this feel" both count as recreation. In a workspace with the user's product material, a bare
  link alone means "make one like this for us". References that also contain portraits, product
  photography, live-action or AI footage, narration or music are in scope: those parts use configured
  media generation while the structure stays editable. Not for only analysing or discussing a video. Use
  openmotion-director when the reference is only inspiration for an original film,
  openmotion-template-to-video for an existing template, openmotion-production for edits to an existing
  editable OpenMotion project, and openmotion-video-to-template for a reusable template package.
---

# OpenMotion Recreate — reference video → the user's own film

For generated shot or audio needs, apply the [generation boundary](../openmotion-production/references/materials.md#generation-boundary) and [generation timing ladder](../openmotion-production/references/materials.md#generation-timing-ladder) before using [openmotion-media](../openmotion-media/SKILL.md).

## Role and goal

Deliver an editable OpenMotion project of the user's version of the reference video, open in the editor. Default creation reads the reference, builds the complete film, makes one focused preview comparison at up to four representative moments, fixes clear defects in at most one batch, exports with automatic technical verification and hands over the result. Detailed frame comparisons, scoring and extended visual revision follow an explicit request. Follow shared [reference reading and measurement](../openmotion-production/references/reference-video.md), [Rebuild](references/rebuild.md), [difficult visual reconstruction](references/reconstruction.md) when needed, and [Export and requested review](references/verify.md) for delivery scope. Use only the Tools actually returned by `tools/list`.

Rebuild everything native code can carry: text, UI, charts, logos, captions, shapes, camera and layer motion. Parts native code cannot rebuild (portraits, product photography, live-action or AI shots, narration, music) become media in the same editable project through [openmotion-media](../openmotion-media/SKILL.md), supplied assets or the reference soundtrack. Apply the shared [replacement rules](../openmotion-production/references/materials.md#replacing-existing-shots), [cross-shot consistency](../openmotion-production/references/materials.md#cross-shot-consistency) (for any subject spanning multiple shots) and [mixed-media recreation boundaries](../openmotion-production/references/materials.md#mixed-media-recreation-boundaries); keep text, logos and UI as native layers above generated plates. Keep the reference's story, shot order, motion, holds and cuts around generated media: do not add native decoration or re-cut to beats unless the reference or user asks, and a footage-led shot need not stand alone with its media hidden. Without a usable media provider, state plainly which parts cannot be produced, finish the rest natively, and offer adding a provider in Model providers, supplying own footage/images, or accepting a native approximation. State limits as workflow facts; never mention, quote or link this Skill or its files in replies.

## 0. Shared context

A catalog template ID, whether an accepted onboarding recommendation or a library selection without editable project files, is read through `openmotion_get_template`; use its instructions and motionDocument as the shared [reference reading](../openmotion-production/references/reference-video.md#obtain-the-reference) describes. An accepted onboarding recommendation also follows [accepted template selection](../openmotion-production/references/templates.md#accepted-template-selection). An accepted sample experience retains the reference's content and motion unless the user requests adaptation; incidental workspace branding does not restart intake or change the template. Preserve the ID and source in project working notes and recovery. Its first successful delivery follows the shared [first-run delivery](../openmotion-production/references/templates.md#first-run-delivery) for the reply, next-step invitation and failure rules.

Read the [shared context](../openmotion-production/references/context.md) before working; it lists the references a recreation needs and how to reuse documents already read. When the work changes an existing draft or project, also apply the [shared edit workflow](../openmotion-production/references/edit.md). If the reference turns out to be only loose inspiration for an original film, switch to [openmotion-director](../openmotion-director/SKILL.md).

## 1. Read the user's context before anything else

Before asking anything, look in the current workspace for the user's own material: README and docs, product or marketing copy, brand files, logos, screenshots, colour or font definitions, package or site metadata. Read what is there. This is the user's brand, product and latest features; use it as the content of the film.

Then read the reference as the shared [reference reading](../openmotion-production/references/reference-video.md#obtain-the-reference) describes: a local decodable copy, its URL and checksum, the whole video and consecutive frames around important changes.

## 2. Decide what the user wants

Work out the film the user wants from everything available: their words, whose film the reference is, what the workspace holds and the conversation so far. Short requests often mean more than they say. A bare link in a workspace with product material usually asks for a film like this about that product; "do this for our new feature" or "I want this feel" usually asks for the reference's craft carrying the user's story; an explicit list of changes asks for exactly those changes.

Whether the reference's brand stays or becomes the user's is your judgement from the request and context, not a fixed rule. When a wrong guess would change the whole film, such as "make one identical" while the workspace holds the user's own brand, put it in the single question below; otherwise decide and state the assumption at delivery.

Parts the request does not cover keep the original. Requested changes are in scope without restriction: wording, brand, images, colours, typography, pacing, duration, adding or removing scenes.

## 3. Ask at most once

Ask only when the workspace and the request together still lack something only the user can supply (brand, product, claims, numbers, prices, logos, images), or when an ambiguity would materially change the result. With usable material in the workspace, do not ask who the film is for. Offer "you decide" where it fits. When selecting, obtaining or replacing an image, clip or sound, apply the [shared material policy](../openmotion-production/references/materials.md) within this workflow's supported media scope. Ask for a material gap only when it cannot be resolved within the current scope, available sources and authorization. When parts need generated media, plan them during this step and put the media cost-consent question from [openmotion-media](../openmotion-media/SKILL.md) (planned assets, count, provider/model, what the key cannot make) into this same single batch. If nothing else is missing, that consent is the only question.

Ask all of it in one batch through the host's question interface, in the user's language. If nothing is missing, do not ask. Do not ask about technical choices, intermediate approval or storyboards. After the answers, work through to the finished film without stopping.

## 4. Create the project

Follow the [runtime adapter](../openmotion-production/references/production.md) and [Native authoring](../openmotion-production/references/native.md). A continued recreation reuses its projectId. Otherwise create one project with `openmotion_create_project` and a stable requestId: `projectType: "reference_video"` with `referenceUrl` for a link, or `projectType: "natural_language"` for a local file, with the file path and the agreed brief in `requirements`.

Read `openmotion_get_project({projectId})` for the directory, revision, current version, `hyperframesCli` and `authoringGuide`; read the pinned engine guide before writing source. Commands you run yourself (`node <hyperframesCli>`, this Skill's measurer, `ffmpeg`) locate Node and FFmpeg through the shared [runtime paths](../openmotion-production/references/reference-video.md#locate-the-pinned-cli-and-media-tools).

## 5. Rebuild, then change

For detailed moving material, scrolling text or textured breakup, use the [reusable rendering code](references/rendering.md). It supplies complete-texture transport, source-coloured sprites, release masks and motion exposure. Use its optional source observer when existing source views leave a concrete mark-size, brightness or transition question unresolved; batch those observations and sprite preparation. Read that reference for the applicable mechanism and save the rendering helper with the editable project.

Follow [rebuild](references/rebuild.md) and the shared [editable representation](../openmotion-production/references/reference-video.md#choose-an-editable-representation) to choose the representation from source observations and build the user's version directly. Resolve appearance-bearing materials, visible bounds, motion controls and event timing together before writing the complete implementation. Carry observed texture and mark-size distributions through motion, exposure and breakup. Reuse suitable supplied implementations and the pinned engine's supported capabilities with their coordinate and timing contracts. For dense multi-shot work, use the [segment reconstruction process](references/reconstruction.md), delegate independent units when available and authorized, and integrate their source. Keep source observations, representation decisions, timed controls and known gaps in existing working notes. Default creation follows the focused preview pass and delivery below.

Before grouping reference regions into materials, inspect each proposed material region through time and inventory its independently changing contents, including small changes within stationary boundaries. Connect those changes to source controls in the reconstruction.

When the reference is the user's own finished film and the request changes only a few details (a year, a line of copy, a logo) while everything else stays, the project may keep the original video as its base layer: import it, cover only the changed areas with clean patches and set the new text or logo as editable native elements that follow the original's timing and motion. Fit each patch to its surroundings, including edges and underlying texture. This is still the editor project and delivery below; never deliver an MP4 edited outside the project. Otherwise, placing the whole original video on the timeline is not a recreation, and an unrelated built-in template is not a substitute.

New content must keep the reference's craft, not just its palette. Match its visual density (a screen full of tiles stays full), camera and 3D motion (a tilted orbit stays tilted), type scale and type character (the closest available face of the same kind, such as a pixel, mono or wide display face, instead of a generic system font), and its background layers (line drawings, grids, textures). A line, label or headline that is clearly visible in the reference must be equally visible in the remix, and the remix must not be darker or lower-contrast than the reference. Preserve the density and spatial relationships of dense and 3D passages in the implementation.

Apply the changes with care: fit longer text with related layout and reading-time changes, update every relevant appearance of a replaced brand or object, keep unrelated content and motion, never invent facts, and check audio timing when changes shift pictures.

Sound: when the reference has sound, the remix has sound. Keep the reference soundtrack by default (extract it as AAC `.m4a` and import it) and re-time it to the new cut. A voiceover that names the reference's brand or product is replaced with the user's lines in the reference's language, delivery and timing when speech generation is available and consented. An unanswered consent question stays pending; do not remove or replace the narration to get around it. If generation is unavailable or declined, follow the audio alternative the user chose; if the narration cannot be separated from the music, say so. When the reference carries captions or the film needs readable subtitles synced to kept or newly generated narration (without duplicating synchronized on-screen display typography), manage them as an editable native caption layer via [the shared caption-sync contract](../openmotion-production/references/sound.md#配音与可编辑字幕协同). Deliver a silent film only when the user asks or the reference is silent.

When the final video is ready, open the editor through the [editable preview handoff](../openmotion-production/references/native.md#editable-preview-handoff); export and delivery follow §6 and §7.

## 6. Export and requested review

Follow the single focused preview pass in [delivery](references/verify.md#1-default-delivery), then export the current version and use that job's automatic technical verification. Recover concrete render, asset-loading or file-integrity failures from their reported cause, then hand over the result.

Numeric reference comparisons, full playback-review sessions, reviewer delegation and extended visual repair follow an explicit review, evaluation or visual-change request. A review-only or evaluation-only request returns findings for the inspected version. Apply visual fixes when the user requests revision, covering the affected interval and dependent appearances. Report known visual gaps and distinguish technical export success from visual acceptance.

## 7. Deliver

Deliver the editable project in the editor and present the same version's verified final video once through the [shared final-video delivery workflow](../openmotion-production/references/production.md#final-video-delivery). That workflow also governs host-native embedding without a download request; supplementary copies and download links follow explicit user requests or its plain-link timeout fallback. Playback recovery reuses the completed export.

Reply briefly in the user's language. Give the `previewUrl` returned by `openmotion_open_preview` and say the editor is open only after confirming visible latest content through the shared handoff; otherwise state the display failure or confirmed inactive-chat deferral, even if the MP4 exported successfully. Say in one or two sentences what changed, which assumptions you made from the workspace material, and any limitation the user would notice. When the reference, analysis or tools fall short, name the specific gap and its effect; never claim a faithful result that was not achieved.

## 8. Follow-up requests

Apply follow-ups to the same project with the shared edit workflow. Use §6 for export and review scope, and validate requested changes over their affected intervals and dependencies. Never start over. `openmotion_list_versions` and `openmotion_restore_version` bring back an earlier version as a new one. When the user is unhappy without saying why ("not satisfied", "第一版不太满意"), ask at most three multiple-choice questions in one batch, for example: follow the reference's story or tell our own; which feature is the hero; size and duration. Offer "you decide" as an option. Then revise the existing project.
