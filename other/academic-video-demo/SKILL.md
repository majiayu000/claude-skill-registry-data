---
name: academic-video-demo
description: Use when making a research demo video, an animated explainer intro followed by a recorded run of the user's prototype (conference booth loop, demo-track or supplementary video), or when re-rendering, reviewing, or narrating one. Not for slide decks, posters, GIFs, plotted data animations, or editing existing footage.
---

# Academic video demo

Make a video that explains one research idea and then shows the system doing it. The proven shape: a 60 to 70 s animated intro (title, problem, method, evidence, architecture, hand-off), then one recorded demo round per case study, then a closing card. Everything renders off screen, frame by frame: exact, reproducible, 4K, and the computer stays free.

`references/worked-example.md` describes the first video made this way (GridMind, SIGSPATIAL 2026 booth); read it at the start for the structure and the user's decisions.

## Workflow

1. **Design interview** (one question at a time): audience and setting (booth loop with a presenter talking over it, or a standalone video with audio), target length, the two or three points the video must make, the case studies to demo, sources (paper figures, poster, manuscript), what exists already.
2. **Storyboard** in `DESIGN.md` in the video folder: one table row per shot with length, content, and caption. Get the user's approval on the table before building. Record every later decision in it.
3. **Scaffold**: copy the bundled scripts and assets into the project's video folder (bare `playwright` imports resolve from the script's folder), then `npm i -D playwright` and `npx playwright install chrome` there. Python packages are the user's to install; name the package and the command.
4. **Build the intro** from `assets/scene_template.html`, one `<section>` per shot, one paused timeline. Check with `scripts/stills.mjs scene` at shot boundaries and mid-animation before every render.
5. **Write the recorders** for the live app on `scripts/recorder.mjs` and `assets/overlay.js`; read `references/live-app-recording.md` first. Verify every fact a shot shows (IDs, times, values) against the app's data with a script, not from memory.
6. **Render in segments**: `render_scene.mjs` for the HTML parts, the recorder with `--seg` for each demo segment, `--stills` for a still per shot and popup.
7. **Assemble** with `scripts/assemble.mjs` (a spec lists the parts; segments of one recording hard-cut, parts crossfade).
8. **Review** with the checklist below. Fix, re-render only the affected segment, re-assemble, review again.
9. **Narration**: write the presenter's script last, from the final timing table (see below).

Commit scripts, scenes, small assets, and docs; git-ignore renders (`*.mp4`, `frames/`).

## On-screen text

- Academic register: precise verbs ("infers", "attributes", "derived from the grid topology", "escalates"), proper names for case studies, every place with its country. No slogans, internal shorthand, or casual verbs.
- Name conditions honestly: only the proposed method is "grounding" (or the paper's own term); a baseline is named for what it does ("coordinate inference").
- Lead with the framing: the problem's principle goes in the slide heading, not in a note under the example.
- Show, don't list: an abstract set (base cells, levels, channels) gets a picture (a diagram in matching colours), never bare labels.
- One caption per shot, unique to that shot (no caption reused across shots); bottom of the frame, at most 84 % of the width and 3 lines; body text at least 29 px and captions about 44 px at 1080p.
- Follow the user's writing rules (no em dashes, no "·" separators, term choices recorded in memory).

## Visual rules

- Parallel parts look and move the same: if one case-study transition highlights its card, every one does; same caption positions, same pacing.
- Nothing covers content: a popup or panel that does not fit its space is replaced by another example or skipped.
- No flashes, no loading states, no cursor jumps; the video ends on a frame that loops into the first.
- Use the app's defaults; switch extra layers on for their shot only.
- Reuse the paper's figures and the poster's colours; draw a diagram yourself when no figure explains the idea (a canvas drawn from `t` inside `seek`, checked against the reference library or data).

## Review checklist (before every hand-off)

Run all of it; the user should not find what this list finds.

1. Contact sheet of the intro at every shot boundary and mid-transition (`stills.mjs scene`); read every tile.
2. Every recorder still and popup still: nothing covered, clipped, or overlapping; captions clear of panels.
3. `flashscan.mjs` on every rendered segment and the final video: 0 hits.
4. Frames either side of every hard cut and every crossfade in the final video (`stills.mjs video`).
5. Parallel parts side by side (both demos, both transitions, all captions): consistent.
6. Facts on screen against the data; captions against the storyboard.
7. Total length matches the timing table; the narration's times match the final cut.

Report what was checked and the numbers (length, flash hits), with the stills you looked at.

## Narration

When a presenter talks over the video, write `NARRATION.md`: a one-line pitch for visitors who arrive mid-video, then one section per part headed with its time range (`## Intro (0:00 to 1:08)`). Inside, each beat is a line `**Cue: <what is on screen>.**` followed by the lines to say as a `>` quote. Conversational in transitions ("Let's start with", "So", "Now look at"), precise in technical terms (no "works out", "figures out"). Regenerate the section times whenever a part's length changes.

## Bundled resources

- `scripts/render_scene.mjs`: HTML scene to MP4 (seek per frame, Playwright screenshot, ffmpeg). `node render_scene.mjs intro.html 69 frames/A_intro.mp4`
- `scripts/recorder.mjs`: live-app recorder core (virtual clock, capture after data arrives, segments, stills, eased mouse, captions).
- `scripts/stills.mjs`: contact sheet from a scene or a video at given times.
- `scripts/assemble.mjs`: parts and segments to the final MP4 from a JSON spec; prints where each part starts.
- `scripts/flashscan.mjs`: transient bright frames.
- `scripts/ffmpeg.mjs`: ffmpeg/ffprobe lookup (PATH, then WinGet) and `duration()`.
- `assets/scene_template.html`, `assets/gsap.min.js`: intro scene skeleton with theme tokens, captions, and the seek contract.
- `assets/overlay.js`: recording-time captions, highlight, cursor, and fetch counter for a live app.

These are starting points. Change them freely, or use other tools when the video needs it (a voice-over, a desktop app, real screen capture); the workflow, text rules, and review checklist still apply.
