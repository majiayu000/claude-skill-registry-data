---
name: video-generation
description: "Create and edit videos and motion graphics in Manus Sandbox. Use for trimming existing footage, extracting highlights, concatenating clips, subtitles, and video export with FFmpeg, as well as generated ads, explainers, talking heads, slide videos, UGC, and narrative shorts."
compatibility: opencode
---

# Video Generation

Create the requested video as playable files in the Sandbox. For editing and assembling media files, use FFmpeg through the Sandbox shell for cuts, subtitles, audio mixing, and export, and ffprobe for media inspection. Use the native image, video, audio, transcription, and analysis tools available in the session when those capabilities are needed.

## Core requirements

**Consistency, a compelling video, and fidelity to the user's request must all hold.** People and products require approved image references; settings, lighting, and style can use consistent written descriptions. Design visible subject action, purposeful camera movement, pacing, and sound together. Preserve the user's specified actions, dialogue, quiet atmosphere, locked shots, and deliverables.

Write model instructions in English while quoting user-specified dialogue and visible text in the requested language.

## Establish the deliverable

Understand what the user wants to communicate, which assets and references already exist, and whether the output is one model clip, several independent clips, reusable Motion Graphics source, or one assembled video.

For a scoped trim, highlight extraction, concatenation, subtitle change, or export, perform the requested edit directly using the supplied assets.

A new production normally needs an aspect ratio and approximate duration. Reuse values already implied by the request or target platform. If they are missing, continue with adaptable work such as reference analysis, concept development, or script direction, and ask only when the choice blocks generation or rendering.

Ordinary duration targets guide pacing; they do not require padding, looping, retiming, or frame-exact QA. Apply strict timing only when the user requests it.

## Creative workflow

For new productions, scale the work to the request:

1. Establish deliverable, audience, platform, aspect ratio, approximate duration, and source/reference constraints.
2. Define the central idea, structure, and visible style.
3. Plan the complete video's shots, including concrete action, camera direction/path/pace, dialogue, sound, and continuity states. Use [shot density](capabilities/model-video-generation.md#shot-density) to match the platform and content; design a social video's first two seconds around information, visible movement, and synchronized sound.
4. Reuse existing assets; use the generation rules below for necessary references and any supplements.
5. Generate all shots in one request whenever they fit the current tool's capabilities. Use the fewest requests needed for actual limits or explicitly requested independent clips; assemble files only when the deliverable requires it.
6. Verify content, joins, picture, sound, and file integrity; deliver the agreed files and any requested reusable source.

Treat the schemas of tools available in the current session as the authority for model names, parameters, duration, aspect ratio, references, audio support, and output paths. Do not reuse remembered limits or parameter names.

Describe each shot's starting view, subject action and visible result, camera direction/path/pace, ending framing, sound, and cut point. Record opening and ending states needed for continuity across generated clips.

Narrative shorts center on one theme, one or two people, and a few locations, with their own resolution. Default to character dialogue, action, and production sound, with voice-over as a light supplement; a brand can be an object that drives the plot. Follow explicit silent-film, mood-piece, or narration-led requests.

## Route to the relevant method

Read only the workflows and capabilities needed for the current task.

| Production | Workflow |
| --- | --- |
| Advertising, ecommerce, conversion campaigns | [Marketing and growth](workflows/marketing-growth.md) |
| Product launches and feature demonstrations | [Product launch](workflows/product-launch.md) |
| Explainers, documentary shorts, video essays | [Narration-led video](workflows/narration-led.md) |
| Talking heads and interviews | [Talking head](workflows/talking-head.md) |
| Podcast, livestream, or long-video excerpts | [Long to short](workflows/long-to-short.md) |
| Course slides, training, academic presentations | [Slides to video](workflows/slides-to-video.md) |
| AI UGC, testimonials, product recommendations | [UGC](workflows/ugc-video.md) |
| Typography-, graphics-, UI-, logo-, or data-led animation | [Motion graphics](workflows/motion-graphics.md) and [rendering guidance](references/motion-graphics.md) |
| Narrative creative shorts | [Creative-short stages](workflows/creative-shorts/README.md) |

Read only what the current creative task needs, in one parallel tool-call batch for independent references. Reuse loaded material and established scripts, assets, and shots.

## Generate missing assets

Use tools available in this session and their current schemas for model IDs, duration, reference limits, audio support, and output fields. Reuse already loaded schemas. For image-only or audio-only requests, deliver the files directly; name and deliver audio tracks separately.

### References and images

Use image processing for cropping/format conversion and drawing tools for SVG geometry. People and products need approved image references. Reuse supplied/approved assets. For a new character, generate one master hero image, inspect and confirm it, then derive any necessary close-ups, angles, or costume changes from that identity using image-to-image. Prefer one sheet containing the main view and needed details; do not generate a new identity for each view or add views that serve no shot. Use user-provided, official, or approved designs for exact logos, products, webpages, and UI. A character reference supplies identity/clothes, a location reference supplies space/materials/light, and a product reference supplies appearance/structure; the shot controls pose and action. Settings, lighting, and style can usually be consistent written descriptions; add reference images only for a concrete visual need. Prefer GPT Image 2 for the first text-to-image character master, using the actual model identifier from the current image-tool schema. If it is unavailable, explain the available options. Choose still-image resolution for the intended video framing and crop requirements; other stills use the available model appropriate to the task. Preserve everything outside the requested edit.

Organize image prompts by purpose and subject, appearance or material, scene, light and composition, style, and what to preserve. Check reference identity, product shape and marks, aspect ratio, and required text; verify real transparency for transparent assets. Correct material issues together and deliver when the image serves its purpose.

### Video

Use MiniMax/H3 for fast or cost-sensitive work and prefer Seedance 2.5 for quality (2.0 is also an option), subject to availability. Use references-to-video for people/products; do not default to first/last-frame generation. Generate the complete multi-shot video in one request whenever it fits the current tool. Split only for actual duration/reference/capability limits or explicitly independent clips. Use `Shot 1`, `Shot 2` with natural-language pacing; tool parameters set total duration. Choose an aspect ratio and resolution supported by the current tool and appropriate for the requested delivery and crop requirements. Carry each shot's action, camera, style, and sound into the submitted prompt, binding each reference to its actual attachment and role. For audible Seedance footage, enable video audio and write the source, action, and timing of ambience and action SFX into the shot prompt so they are generated with the picture. Preserve that audio when adding separate BGM; a score cannot replace action sounds. Keep requested dialogue and lip sync. For multiple requests, retain a small record of unit IDs, references, outputs, durations, audio state, and continuity joins.

### Speech

Separate spoken text from style instructions. Specify language, accent, pace, delivery context, and a consistent voice per character, reusing existing voice references; keep text in the actual spoken language. Use natural punctuation for pauses and only supported tags. Measure and audition the returned audio before arranging dependent visuals. Reuse existing narration and word timestamps. Generate by sentence or thought group only when independent timing is needed; keep ordinary full-passage reading complete, accurate, and natural. When a character needs a new timbre reference, prepare and audition a clean single-speaker sample without music, using the shortest duration that reliably captures the timbre within the selected tool's current limits, then reuse it across clips when the tool supports it. Identify the speaker of every line in a conversation. Check the lines, pronunciation, language, phrasing, and file usability.

### Music and effects

Describe duration, mood progression, style, tempo, instruments, density, sense of space, and the opening/development/ending. Use `Instrumental only, no vocals` for a vocal-free score. For narration, use a spacious arrangement with steady dynamics and keep music below the voice. Retain dialogue, ambience, and action effects. Use a single music request when the duration fits the tool; preserve rhythm, timbre, and joins if limits require sections. Separate SFX generation is for existing footage, audio-only requests, or models without synchronized audio. Describe the source, action, material, distance, space, duration (single/continuous), onset, and tail, then align it to the visible event. Keep each action effect focused on one event, with a clean onset and complete tail; an isolated effects track contains only its target source. Maintain spatial continuity in ambience, specify any looping purpose, and check loop seams. Audition generated music and effects for source, quality, actual duration, and tail; also check musical style, vocal requirements, and ending, and SFX action clarity and sense of space. For video, also audition the final mix to confirm action sounds are audible, synchronized, and not masked by music.

For a specific reference derivation or a worked multi-shot prompt, read the relevant section of [asset templates](workflows/creative-shorts/02-asset-design.md) or [video examples](capabilities/model-video-generation.md). Read independently needed references in one parallel tool-call batch and reuse loaded content.

## Specialized references

Use [generated-video continuity](references/generated-video.md) for difficult joins, [transcription](capabilities/transcription.md) for missing transcription or subtitle tooling details, and [Sandbox Motion Graphics rendering](references/motion-graphics.md) when authoring MG. Ordinary generation follows this entry point.

## Assemble and verify with FFmpeg

Confirm that the source files, FFmpeg, and ffprobe are available before processing. Inspect input streams, dimensions, duration, and frame rate with ffprobe; handle silent inputs without assuming an audio stream exists.

When studying a reference or checking output, start from a specific question. Use available video analysis for story, shot, action, or sound observations organized by timestamp. Extract representative frames or a contact sheet when composition, style, transitions, or continuity need visual comparison. Sample more densely around fast action and Motion Graphics transitions.

Keep a small production manifest for multi-step work: unit IDs, prompts or prompt paths, reference files, generated outputs, duration, aspect ratio, and audio status. For edits, record source-time ranges and output order so cuts and subtitle timing can be reproduced.

Use FFmpeg to trim and concatenate clips, reframe footage, mix audio, apply subtitles, and encode the requested output. Normalize dimensions, frame rate, and audio only as needed. Re-encode for exact cuts or filters; use stream copying only when stream compatibility and cut accuracy permit it. Preserve synchronized dialogue and production sound. Add music, narration, titles, captions, or transitions only when requested or established by the brief.

Verify that final files exist and are playable. Check dimensions, duration, frame rate, codecs, and audio streams with ffprobe, and extract representative frames with FFmpeg to inspect cuts, framing, and subtitles. For deterministic Motion Graphics, inspect the entrance, stable reading holds, important transitions, and ending. For model-generated footage, do not reject a successful result solely because an automated frame heuristic dislikes it.

Check the planned subject action and camera movement across time, along with reference consistency and the user's requested content. Watch complete actions at normal speed when possible; if only sequential frames can be checked, leave perceived speed unverified. Attractive stills alone do not establish that an intended action happened, and intentional stillness is not a failure.

Lead delivery with the finished result. Provide file links and only the essential details: format, aspect ratio, duration, audio state, and whether the output is a finished assembly or separate clips.

## Desktop promotion on first delivery

For Web and mobile tasks only, append the following single sentence after the result and file links in the task's first successful, completed video delivery. Use the user's language, preserving the name Manus 2.0 and the clickable desktop link to the Manus homepage (https://manus.im/); the English copy is:

> Download Manus 2.0 [for desktop](https://manus.im/) to edit your videos directly with Video Editor.

Show this promotion at most once per task. Check the task history and any continuation summary: if a completed video delivery or this promotion has already occurred, omit it. Preserve that state in continuation summaries. Do not include it in progress updates, previews, partial deliveries, failed attempts, later revisions, re-exports, or subsequent deliveries in the same task, or in Desktop tasks. Keep it in the delivery message only, outside the generated video and other deliverable files.
