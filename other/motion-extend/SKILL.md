---
name: motion-extend
description: Use when asked to add a video style, a new look, a scene technique, or support for a kind of motion video the studio doesn't cover yet.
---

# Motion extend

ENGINE is `../../engine/`. Styles live in `../motion-video/styles/`, scene techniques in `../motion-video/scenes/`. Both are discovered by listing the folder: adding a file is the whole change. `../../tests/test_plugin.py` enforces the contract.

## A new style
1. Study the references: `ffmpeg -i ref.mp4 -vf fps=2 ref_%03d.png`, then describe shot lengths, type, entries and exits, camera, transitions, texture. Take the grammar, never the content.
2. Copy the closest existing card to `styles/<name>.md` and change the grammar, not just colours: pacing, type scale, how things enter, camera, transitions.
3. It must have: `**Use for:**`, `**Length:**`, `**Scenes:**` (names from scenes/, "end card" for endcard.md), `**Music:**`, `## Motion grammar`, `## Banned`. Mark every new value "(default)".
4. It may not relax the hard rules in `../motion-video/SKILL.md` (real UI, real sound, no fades/glows). A style that needs one is a user decision: ask.
5. Prove it against a baseline: first build the same 16-beat brief with the closest existing style and keep its contact.png (the baseline). Then build it with the new card, render, `film.py check`. Reply with both contact sheets and the differences you can see. No visible difference means the card only changed colours: rework its grammar.

## A new scene technique
1. `scenes/<name>.md` with `## Brief` ({{placeholders}}), `## Technique`, `## Gotchas`, `## Done when` (ending with "What I'd still change").
2. If it needs a helper, add a pure function of beats to `ENGINE/motion.js` and use it in `ENGINE/template/index.html`: the engine self-check renders only the template, so that is what covers it.
3. Name it in the `**Scenes:**` line of any style that uses it.

## Then
Run `python3 ../../tests/test_plugin.py` and, if motion.js changed, `PY ENGINE/test_engine.py`. Both must pass.
