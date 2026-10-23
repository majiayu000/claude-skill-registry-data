---
name: video-build
description: >-
  Builds HyperFrames compositions for any code-built video - the project scaffold
  (hyperframes.json, pinned CLI, a build.py that emits the composition from measured timings),
  building from a real product UI (capture the real app, compose from its own classes, a measure
  pass), word-highlight captions in any language including Arabic and Hebrew, real footage with
  frame-exact windows, rendering, and a catalogue of HyperFrames, GSAP and render traps. A layer
  over the upstream hyperframes skills and an executor under video-studio. Use when video-studio
  reaches the build step of a code-built film. Triggers: "build the composition", "HyperFrames",
  "render the video", "add captions", "word-by-word captions", "put this footage in the video".
---

# video-build

How a code-built film is put together in HyperFrames. video-studio decides what the film
is and when it is built; this skill decides how. The upstream `hyperframes`,
`hyperframes-core`, `hyperframes-animation`, `hyperframes-cli` skills are the base
(heygen-com, used as they are); this is what was learned on top of them.

**Input: the film's `brief.md`** (`../video-studio/references/brief.md`). It owns copy, claims,
tone, material, moments and private data; this skill owns the implementation. If the brief
cannot be met, say so to video-studio - never change it silently.

**Setup.** Node.js 22+, FFmpeg, the HyperFrames CLI and its skills (the kit's
`connections/hyperframes-cli.md`; `npx hyperframes doctor` checks the toolchain). Python 3 for
`build.py` and `scripts/footage_proxy.py` (standard library only).

## Start a project

`references/scaffold.md`: the files (`hyperframes.json`, `package.json` pinning the CLI,
`build.py`, `assets/`, `audio/`, `timing.json`, `renders/`), the `build.py` pattern (one
source, everything timed from `timing.json`, so the picture never drifts from the audio),
the stylesheet head, trimming identity PNGs, commands, and inspecting a render without
watching it.

## Build from a real product UI

`references/product-ui.md`: get the real UI, compose from its own classes, measure instead
of guessing, captions word by word from the take's word timings.

## Captions

`node ${CLAUDE_SKILL_DIR}/scripts/captions.mjs film.json --font "Family=path"` →
`captions.cues.json` + `captions.html` (paste inside the root, call `mountCaptions(tl)`):
word-highlight captions in any language and direction, cue breaks chosen so every cue passes
readcheck. Rules, RTL, fonts, checks: `references/captions.md`.

## Before writing composition HTML

`references/hyperframes-gotchas.md` - every trap that cost a render: layout, text reveals,
media, checking, rendering, the visibility leak, overlap markers, clip-path on SVG, fonts,
encoding; real footage (`<video>`): exact-double times, in-points from the rendered file, priming
for the live player.

## Real footage

`python3 ${CLAUDE_SKILL_DIR}/scripts/footage_proxy.py CLIP --in A --out B --at T [--split] [--raw]`:
`<video>` windows with exact-double times and the cut list from the file you render, optionally
via a 30 fps proxy that matches the engine (VFR, sparse keyframes, many windows). Rules:
`references/hyperframes-gotchas.md`, "Real footage".

## Related executors

- Camera and editing moves, the render(t) rig, story time: **video-moves**.
- Sound for the film: **video-sound**. Gates and review: **video-check**.
- Generated people and scenes to assemble here: **video-generated**.
- Real 3D (three.js objects, globes, particles): **video-3d**.

## Adapt it

- Keep your brand tokens (colours, fonts) in one `brand-tokens.css` and your trimmed logo
  lockups in one folder; every project copies them in (`references/scaffold.md`).
- Save your first finished film as the reference project - the next one starts as a copy of it.
- Pin the HyperFrames version you tested in `package.json`; bump it only after a test render.
- Add every new trap you hit to `references/hyperframes-gotchas.md` under a dated heading.
- Set the caption colours from each film's own palette (`--cap-*` variables), never one default.
