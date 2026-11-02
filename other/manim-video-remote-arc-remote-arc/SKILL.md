---
name: manim-video
description: Make local mathematical, geometric, algorithm and data-explanation animations with Manim. Use when the film needs a precise visual derivation or transformation.
priority: P1
category: media
status: builtin-guidance
---

# Manim Video

Choose Manim for a proof unfolding on screen, geometric construction, calculus/linear-algebra explanation, algorithm walkthrough or a chart whose changing values explain a mechanism. Use Remotion for a broader film/UI/data composition, HyperFrames for HTML/SVG motion, and Blender MCP for modeled objects, physical materials and spatial lighting. Engines may contribute shots to the same finished film.

## Device and permission gates

Run Python and rendering on the authorized user computer, inside its allowed task directory. Prepare ordinary missing dependencies there as part of the requested media task, with their source, destination and approximate size disclosed. No model API, cloud rendering or media upload is required. Qwen TTS/ACE-Step still require the existing size-aware approval before installation.

## Prepare and render

Arc prepare_skill stages this package. Connect read_skill provides hashed files in bounded path/offset chunks. The scripts directory includes local-creative.mjs and its sibling local-media.mjs; retrieve both exactly and verify their SHA-256 before use.

    node "<skill>/scripts/local-creative.mjs" ensure --workspace "<workspace>" --engine manim

This prepares a task-local Python environment with Manim 0.22.0, plus FFmpeg when missing. It reuses Python 3.11–3.13 or prepares portable Python through pinned uv. Keep the returned Python path and requirements.lock.txt. A source build may need existing OS Cairo/Pango development libraries; report the actual missing dependency if preparation fails. Do not use administrator privileges or call failed setup ready.

Write an original Python Scene, then render through the same environment:

    node "<skill>/scripts/local-creative.mjs" render-manim --workspace "<workspace>" --source "<scene.py>" --scene Main --output "<new film>.mp4"

The helper renders 1280×720 at 30 fps using Cairo, preserves existing outputs, checks the video stream, decodes the MP4 and records an artifact hash. Use the process manager for long rendering jobs and wait for actual completion. Adjust a render with the returned Python directly when the brief calls for another resolution or frame rate, then verify the resulting file.

## Explain through transformations

- Establish the quantities and units, show one meaningful change, then connect the result to the initial question. The animated state must agree with the stated mathematics.
- Use Scene/MovingCameraScene, ValueTracker, updaters, object transforms, axes and named visual groups. Remove temporary updaters when their role ends. Animate measured changes rather than arbitrary numbers.
- Use readable text, font checks and geometric primitives for the first render. Text supports Chinese/Unicode through Pango. MathTex/Tex requires a TeX installation; do not claim the ordinary bootstrap includes it. Use the requested notation and prepare its actual typesetting dependency when needed, or an appropriate supported text/Typst route.
- Match the user's language, duration, narration and music. Reuse authorized audio; synchronize labels and edits with the actual rendered timeline.

## Verify and deliver

Inspect rendered stills before a long render. Check formulas, geometry, labels, object overlap and the transition into the final conclusion. Verify duration, resolution, frame count and audio where applicable. Decode success does not establish mathematical correctness.

Deliver the playable MP4 and editable Scene source, with absolute local paths and the checks actually performed. Keep videos out of the code repository; publish only to a destination the user requested.

Official method/API reference: https://docs.manim.community/en/stable/
