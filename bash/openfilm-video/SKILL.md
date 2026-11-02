---
name: openfilm-video
description: Assemble and render local code-driven shots and media tracks with OpenFilm. Use for clip-based editing, transitions, product sequences and reusable shot pages.
priority: P0
category: media
status: builtin-guidance
---

# OpenFilm Video

Use OpenFilm for a shot-based timeline combining owned footage, local audio and code-driven pages. For React/Three.js scene composition use remotion-video; for HTML/SVG/GSAP motion use hyperframes-video when that better fits the task.

## Device and permission gates

Render on an authorized user computer in a task workspace. Follow video-creator for source handling, ordinary automatic dependency preparation and finished-file checks. Announce download source, size and destination. Do not request another permission merely because ordinary OpenFilm, Chromium or FFmpeg is missing. Qwen TTS and ACE-Step installation retains its explicit large-download approval gate. Publishing or paid APIs require authorization covering that action.

## Execute and verify

Materialize the packaged scripts/local-media.mjs through Arc prepare_skill or Connect's chunked, hashed resources.

    node "<skill>/scripts/local-media.mjs" ensure --workspace "<workspace>" --components openfilm
    node "<skill>/scripts/local-media.mjs" render --workspace "<workspace>" --engine openfilm --project "<project>" --output "<new film>.mp4"

Read the installed CLI manual before authoring. Give each code page a deterministic window.film duration/frame(t) interface. Compose tracks in film.html, keep audio on the composition timeline, and load scripts, fonts and images from local assets. Preserve OPENFILM_NO_BROWSER=1 and OPENFILM_NO_UPDATE_CHECK=1 for unattended rendering; do not open a visible progress browser without a user need.

Use meaningful scene actions and transitions; avoid filling the duration with title cards. If music timing is requested, align significant edits to the recording and retain readable captions. Verify contact sheets, transition frames, actual stream duration, audio coverage and complete decoding. Deliver the MP4 and editable shot sources.
