---
name: manimgx
description: Plan and render mathematical or educational animations with ManimGX. Use for new Manim videos, scene storyboards, and migrations from Manim CE or ManimGL. Includes layout inspection before video rendering.
---

# ManimGX

Use ManimGX for new animations. For existing projects, identify the engine from imports and dependencies before editing.
Keep the project's engine when the user requests maintenance without migration.

## Load only what the task needs

- For multi-scene planning, read [Storyboards](references/storyboards.md).
- For existing CE or GL scenes, read [Migration](references/migration.md).
- For an unfamiliar API, fetch the relevant page from https://manimgx.academa.ai/llms.txt.
  Load specific pages; use the full reference only when focused pages cannot answer the question.

## Prepare the runtime

Check `manimgx --version`. ManimGX requires Python 3.13 or 3.14 for the reviewed release.
If missing, use an existing `uv` installation:

```sh
uv tool install --python 3.14 manimgx
manimgx --version
```

For a temporary run, replace `manimgx` with `uvx --python 3.14 manimgx`.
For project dependencies, install into the project's Python environment.
Do not install Manim CE, LaTeX, or system FFmpeg for this workflow.
The wheels include text rendering, fonts, and video encoding.
Linux wheels include a CPU rendering fallback for machines without a GPU.

## Plan the scene

Infer audience, duration, language, and aspect ratio from the request.
Ask only when a missing choice changes the animation substantially.
Give each scene one teaching goal. Start with a concrete example, then introduce notation.
Reveal objects in stages, transform recurring objects, and pause after important changes.
Use consistent colors for the same quantities across scenes.
For a short request, proceed directly to code; write `scenes.md` when a plan is requested or multiple scenes need coordination.

## Write Python

Use `import manimgx as m` and public names such as `m.Scene`, `m.Circle`, and `m.Create`.
Start from [the runnable example](assets/quickstart.py) when useful.
Time advances through `self.play(...)` and `self.wait(seconds)`.
Use raw strings for `m.MathTex(r"...")`. Typst renders its supported LaTeX subset.
Keep labels readable and leave margins inside the frame.
Derive updater state from time or other objects; avoid frame-count-dependent motion.

When ty is available, check scene code in the environment containing ManimGX before rendering.
Types catch unknown keywords that runtime objects may silently ignore.
Do not add a checker or editor extension unless the task needs it.

## Inspect, render, and review

Run these from the scene directory. Supply the class name when a file defines multiple scenes.

```sh
manimgx inspect scene.py MyScene
manimgx render scene.py MyScene -r 1280x720 --fps 30
```

Read the timeline and open every generated storyboard sheet with an image-capable tool.
Fix unintended clipping, text collisions, and unreadable labels, then inspect the affected moments again.
Exit code 1 indicates layout problems. Check mid-animation states with `inspect scene.py MyScene -t 0.5,end` when motion can cause collisions.
Inspection checks sampled times only. For 3D scenes, it produces pictures and a timeline but skips layout checks.

Review the rendered video or extracted frames for timing, motion, and visual correctness.
Use `preview` for interactive playback when a display is available.
For final output, honor the requested resolution and frame rate; otherwise use render defaults: 1920×1080 at 60 fps.
For vertical output, use `-r 1080x1920`. Match inspection dimensions through `m.config` in the scene.
Outputs appear beside the source file; `-o` selects another path.
Deliver the source and video paths, plus subtitles when produced.
Open the result when the user requests playback and the environment supports it.

## Additional features

Use `self.next_section()` and `manimgx present scene.py` for slides.
Read the sound-and-voice reference before adding narration; voice services can require credentials and paid requests.
Browser playback uses WebGPU. The reviewed browser release lacks CJK text and boolean shape operations.
Use native rendering when those features are required.

Provenance and reviewed versions: [Sources](SOURCES.md).
