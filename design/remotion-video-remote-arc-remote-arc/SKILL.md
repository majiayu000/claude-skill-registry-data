---
name: remotion-video
description: RA core local filmmaking with Remotion, React and optional Three.js. Use for programmable scenes, cinematic camera work, explainers, data animation and music-timed edits.
priority: P0
category: media
status: builtin-guidance
---

# Remotion Video

Use Remotion as a core RA video option when React components, reusable scenes, synchronized data, three-dimensional camera work or precise frame control fit the brief. HyperFrames is another option for HTML/SVG/GSAP motion; OpenFilm fits shot and clip assembly. Match the user's chosen engine and outcome.

## Device and permission gates

Render on an authorized user computer, inside its Trusted Write Locations. The media request authorizes ordinary task-local Node/npm, Chromium, FFmpeg and Remotion dependencies under the existing device permissions. Disclose their source, destination and approximate download size, then prepare them as needed without a second installation question. Do not upload footage or render in the cloud unless requested.

Qwen TTS and ACE-Step need explicit size-aware approval before downloading their multi-GB runtimes or weights. Reuse an already installed compatible model or a prior approval covering the same installation. Narration or music requests alone do not authorize those downloads. Read video-creator for local audio alternatives and the consent boundary.

Remotion has its own software license: https://www.remotion.dev/license. Follow the terms applicable to the user's use; do not describe it as universally free or buy a license on the user's behalf. RA's workflow is original guidance and does not redistribute the separate upstream agent-skills repository.

## Prepare and render

The package includes scripts/local-media.mjs, identical to the helper used by video-creator. In Arc use prepare_skill with this skill ID, deviceId and workspace. In Connect read_skill lists hashed resources; retrieve the helper by path/offset through the final chunk and verify its SHA-256 before writing it locally.

    node "<skill>/scripts/local-media.mjs" ensure --workspace "<workspace>" --components remotion

This prepares pinned Remotion 4.0.538, React, Three.js/React Three Fiber, local fonts support, Chromium and FFmpeg when needed. Initial downloads can be hundreds of MB. Keep project package versions aligned with the pinned helper and use the returned module directory, browser path and CLI rather than global npx/latest. Dependency readiness is not a finished video.

Create a separate project with a registered Composition and local public assets. For the reusable cache's npm dependencies, link or resolve project modules to the returned engine directory within the authorized workspace, or install the same pinned dependencies in the project. Preserve existing project files and lockfiles.

    node "<skill>/scripts/local-media.mjs" render --workspace "<workspace>" --engine remotion --project "<project>" --entry src/index.tsx --composition Main --output "<new film>.mp4"

The helper passes the verified local browser path and a bounded concurrency, renders a real MP4, checks streams/duration, decodes it and saves an artifact receipt. Run long jobs in the device process manager and read their completion status and logs. Never equate starting a render with success.

## Authoring decisions that matter

- Derive visual state from useCurrentFrame and useVideoConfig. Do not use wall clocks, unseeded randomness or independent CSS animation for rendered motion.
- Use separate scene components and purposeful cuts, camera changes or transformations. When comparing engines, design different visual treatments rather than relabeling identical frames.
- For Three.js use ThreeCanvas from @remotion/three, frame-driven transforms, actual lighting and locally generated or authorized textures. Wait for fonts before screen textures are drawn; release the font hold only after the canvas has mounted. preserveDrawingBuffer:true may be needed for reliable WebGL capture. Check actual rendered stills: a successful render can still contain a blank canvas. Prefer deterministic sprite/particle halos if a postprocessing chain does not advance reliably.
- For requested beat edits, analyze the chosen local music, align scene/action anchors to detected transients at the chosen frame rate, and keep enough time for subtitles. Retiming the visuals must also update the subtitle file and chapter markers. Inspect actual output cuts with audio, not just a timeline diagram.
- User-specified language, duration, narration and music take priority. Keep the recording's original attribution; do not claim that supplied music is original or royalty-free.

## Verify and deliver

Inspect rendered keyframes and transitions, especially small text, the longest caption, first/last frames, and three-dimensional canvas content. Check actual duration, resolution, frame count, audio coverage and full decode; review speech/subtitle alignment where applicable. Keep numeric event counters consistent with the explained events instead of tweening them into fictitious transactions.

Deliver the playable file and its absolute local path, with editable sources and checks that actually ran. A temporary Remote Arc file resource is an expiring download, not permanent hosting. Publish only to a destination the user requested.
