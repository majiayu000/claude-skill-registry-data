---
name: manim-architect
version: 1.2.0
description: Manim Community 0.22 explainer scenes for formal objects that change shape — graphs explored, formulas built piece by piece, tables filled in, traces unrolled — with LaTeX formulas fitted to the frame, a base class that times scenes from the narration and writes a sections file, a cue helper, a teaching-helper package, audio muxed per scene, 1080p review renders and the traps that waste hours (morphing text, a failing formula failing the whole render, unredirected output). Use when writing, structuring, rendering or reviewing Manim scenes, alone or as a companion to a Remotion video.
---

# Manim Architect

Targets **Manim Community 0.22** on Python 3.13+, run with `uv`. Produces scene code and render scripts. What to teach and in which order is [explainer-designer](../../frontend/explainer-designer/SKILL.md); the words and the speech rate are [narration-writer](../../frontend/narration-writer/SKILL.md); a Remotion frame that embeds a clip or owns the final timing is [remotion-architect](../remotion-architect/SKILL.md). Code patterns are in [RECIPES.md](RECIPES.md); objects kept across scenes, a worked number before a formula, a squared quantity drawn as a square and the draft sweep are in [TRAPS.md](TRAPS.md); pinned versions and system packages in [STACK.md](STACK.md); the library's scene classes, animation families, built-in sections and sound, and CLI flags in [FRAMEWORK.md](FRAMEWORK.md).

## 1. When Manim, when not

- **Use Manim** where a formal object changes shape: a graph being explored, a formula built from parts, a table that fills in, a state sequence unrolled.
- **Do not use it** for the frame around a scene (badges, source lists, final timing, transitions between videos) when a Remotion video already owns them: render the clip silent and embed it, or render the whole edition in Manim and mux the audio.
- Manim is not frame-deterministic in the way Remotion is: a scene is a script that plays animations in order. Treat the script as the timeline.

## 2. Structure

- **One chapter = one `Scene` subclass** that extends a small base class. The base class reads the content file and the narration file, draws the frame of each scene, and writes the start and end of every scene to a **sections file** (`id`, `start`, `end`, `seconds`). The audio step and the review step read that file. Pattern in [RECIPES.md](RECIPES.md#1-the-base-class).
- **Scene length** is `max(animation time, words / rate + lead-in + tail)` before audio exists, with a measured rate (narration-writer). Once audio exists it is `lead-in + measured voice + tail + hold` from the audio manifest, and cues are resolved against the measured length ([RECIPES.md](RECIPES.md#7-timing-from-the-audio)). A clip with several parts gets one audio per part.
- **Cue drawings to narration phrases** with a `cue(scene, phrase)` helper that waits until the voice would reach the phrase, and raises when the phrase is not in the narration ([RECIPES.md](RECIPES.md#2-the-cue-helper)).
- **Teaching helpers live in a package, one module per family** (a formula built from pieces, a token that walks a path, a wave that fills a table, a stamp, a slider, a chain of states). Chapter files stay thin and call helpers; parallel work then touches different files, and a helper is fixed once.
- **A registry file** lists the editions (id, module, class) so one command renders any of them, or all.

## 3. Drawing rules

- **Morph shapes, not text.** Morphing one label into another turns the glyphs to noise mid-transition. Fade the new label in after the shape has moved.
- **Formulas are LaTeX** through one helper that uses a minimal template and scales a wide formula down to a maximum width (about 12.6 units on a 16:9 frame 8 units high). A mixed line of words and formulas uses a second helper, so words stay in the text font.
- **A formula that fails to compile fails the whole render.** Render after every edit that touches one, at draft quality; do not batch edits and render at the end.
- **Build a formula from pieces** and point each piece at the part of the drawing it describes, so the viewer sees where every symbol comes from. Colour the piece and its target the same.
- **Colours and fonts come from one token file** shared with the other tools (CSS custom properties parsed once), so Manim and the web side cannot drift. Register fonts in a context manager around the scene.
- **Layout is a budget.** A frame is 8 units high; keep a title band, a drawing band, a summary band and a footer band, and a measured gap between them. Dense text on one side and an empty side is a layout bug.
- **Teach a formula with one real case first** (pick an item by a stated rule, show its numbers, then apply to all); see [TRAPS.md](TRAPS.md#2-a-worked-number-before-the-general-formula).
- **Every scene is closed to the same state**: everything fades out in a fixed time, and the last frame of a scene is the finished drawing.

## 4. Rendering

- **Draft first:** `-ql` (480p15) for iteration, `-qh` at 1920x1080 and 30 fps for review and delivery. Judge the look only at final size.
- **Always redirect Manim's output to a log file** (`> render.log 2>&1`): it prints a progress line per animation and floods a session. Read the tail on failure.
- **Fast reruns:** keep the media directory stable so the partial-movie cache is reused, and clear it when a helper changes in a way the cache cannot see.
- **No unseeded randomness** in scenes: a seeded generator, or fixed coordinates, so two renders are the same.
- **Parallel renders** need separate media directories (and separate working trees if the code differs).
- **Audio** is placed in a separate step: read the sections file, delay each scene's audio to its start plus the lead-in with `adelay`, mix with `amix=normalize=0`, copy the video stream. Generated audio never enters the Manim code ([RECIPES.md](RECIPES.md#3-muxing-the-audio)).
- **Review** with one contact sheet per version: `python3 scripts/contact_sheet.py video.mp4 video.sections.json` writes `video.sheet.png`, a labelled frame at 85% of every scene, so a version is judged without playing it (explainer-designer, section 6, says what to look for). Keep the sheets of v1 and v2 side by side; open the dense scenes at full size.

## 5. Anti-patterns

- Animating a `Transform` between two text labels.
- A formula edit that was not rendered before the next edit.
- Scene times from a hard-coded constant instead of the narration file, or from the planned rate after audio exists.
- Scene code that calls a speech engine, or audio that is part of the scene.
- Output of the render printed into the session.
- Colours or fonts typed into scenes instead of read from the token file.
- Page-wide formulas that overflow the frame because nothing scaled them.
- A kept drawing that disappears or sits on the wrong layer because only top-level mobjects were compared, or a group left at `z_index` 0 ([TRAPS.md](TRAPS.md#1-objects-that-stay-on-screen-across-scenes)).
- A `Scene.wait()` with no reason; a pause either holds a finished drawing or waits for a cue.

## 6. Review checklist

- [ ] Every formula compiles; each one was rendered right after it was written.
- [ ] Scene lengths come from the narration file and its measured rate; the sections file is written.
- [ ] Cues point at phrases and raise when a phrase is gone.
- [ ] No label is morphed into another label.
- [ ] Colours and fonts come from the shared token file.
- [ ] A 1080p render was reviewed with its contact sheet (one per version) and full-size frames of the dense scenes.
- [ ] Audio is muxed in a separate step and no audio runs past its scene.
- [ ] Render output goes to a log, not to the session.
