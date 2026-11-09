---
name: openvids
description: Make a product-launch motion-graphics video (Claude Code launch-video style) with Remotion, a procedural soundtrack, and a fan-out of scene, sound, and design subagents. Use when the user asks for a launch video, feature announcement video, promo, explainer, or motion graphics about a product.
---

# openvids

You direct the film. Subagents build it. The output is an MP4 at 1920x1080, 30 fps, with a soundtrack synthesized in code, plus an X/LinkedIn caption and a cost receipt.

`{skillDir}` below means the directory that holds this file. The tools need Node 24 or later (the scripts import `src/timeline.ts` with Node's type stripping), ffmpeg and ffprobe on `PATH`, and Python 3.10 or later with numpy and scipy.

## The data shape

Everything hangs off one contract in the film project:

- `src/timeline.ts` has `durations` (id, name, dur in frames), the derived `SCENES` (adds `from`) and `TOTAL_FRAMES`, and `CUES` (the scene-local frame of every visual event). The picture and the soundtrack both read it. Cues never move once the sound is built.
- `HANDOFF.md` has the boundary table. The last frame of scene N equals frame 0 of scene N+1, because both render the same shared component with default props.
- `src/theme.ts` and `src/components.tsx` are the design system. Only the director and the art director edit them.
- Each scene file `src/scenes/S<n>.tsx` has exactly one owner at a time.

## Workflow

1. **Research the facts.** Fetch the product's pricing, docs, benchmarks, and announcements. Put only verified claims on screen. Date-stamp benchmark claims. Never invent numbers for competitors. Save the facts with their source URLs in `FACTS.md`.
2. **Ask only what you cannot observe.** Length, aspect ratio, palette, and audio preferences are the user's call. Ask them once, together.
3. **Storyboard.** Follow `references/storyboard.md`. Write the scene table with seconds, picture, hero moment, transition out, and cues. Every transition must be motivated by an object already on screen.
4. **Scaffold.** Copy `{skillDir}/template` to the project directory and run `npm install`. Fill in the brand object in `src/theme.ts`, then write `durations`, `CUES`, and the boundary table. Replace the demo scenes with one stub per scene in `src/scenes/S<n>.tsx` that renders its frame-0 boundary component, and register every scene in `SCENE_COMPONENTS` in `src/Film.tsx`. Replace the demo events in `<project>/audio/score.py` with an empty `EVENTS` list. `npx tsc -p .` must pass. Run `npm run timeline` (it writes `public/timeline.json` for the audio engine) and a test still before you fan out.
5. **Fan out the first draft.** Send one scene builder per scene pair and one sound designer, all in parallel, using `references/briefs.md`. The sound designer edits `<project>/audio/score.py` and renders it with `python {skillDir}/audio/render.py <project> <project>/audio/score.py`.
6. **Render and sheet.** Run `npx remotion render src/index.ts Film out/draft.mp4 --scale=0.5 --muted`, then `python {skillDir}/scripts/contact_sheet.py out/draft.mp4 out/sheets`. Look at every sheet yourself.
7. **Art direction.** Send one art director with your notes from the sheets. It writes `DIRECTION.md` and applies the global changes.
8. **Polish.** Send one polish designer per scene pair, in parallel, on the strongest design model.
9. **QA.** Render the release candidate with audio. Send one QA director with `motion_scan.py` and `check_boundaries.py` results and your own list of issues.
10. **Receipt.** If the film shows its own cost, run `python {skillDir}/scripts/droid_usage.py --out <project>/src/usage.json` from the directory where the Droid session started, or pass `--session <uuid>`. Re-render after that, because the numbers exist only after the work.
11. **Final render and verify.** Run `npx remotion render src/index.ts Film out/<name>.mp4 --codec=h264 --crf=16 --audio-bitrate=320k`. Then check it:
    - `ffprobe` shows the expected duration, 1920x1080, 30 fps, and AAC 48 kHz stereo.
    - `ebur128` reads near -14 LUFS.
    - `python {skillDir}/scripts/check_boundaries.py <project>` passes.
    - `python {skillDir}/scripts/motion_scan.py out/<name>.mp4 --allow <holds>` passes, with only the designated holds allowed.
    - You looked at the poster frame and the receipt frame.
12. **Deliver.** Give the path, a scene list, the validation results, the usage table if requested, and a caption written like a person posting it.

## Model routing

Route by role, not by habit:

- Scene builders and scripts go to a strong code model.
- The sound designer goes to the strongest code model available. The DSP is the hardest code in the film.
- The art director, polish designers, and QA director go to the strongest design model. On Droid at the time of writing, that is Claude Opus 5.5.

If the user names a model for a role, that choice wins.

## Rules that keep it from looking generated

The full list is in `references/design-system.md`. These five decide most outcomes:

- One accent color, and it always means the product.
- Nothing below 24 px on screen. Lines are 2 px.
- Every element enters through a mask or from an object already on screen. No crossfades between scenes.
- Use expo-out for entrances, ease-in for exits, and ease-in-out for morphs. Nothing bounces.
- No frame sits still for more than 12 frames unless it is a designated hold.

## Sound

Read `references/sound.md` before you brief the sound designer. Score with foley and tuned hits, not music loops. Use one quiet harmonic bed that changes only at scene boundaries, and use silence on purpose.

## Files

- `template/` is the brand-neutral Remotion starter: three demo scenes, the design system, and the handoff contract.
- `audio/synth.py` holds the sound primitives. `audio/render.py` is the score engine. `audio/scores/` holds example score specs.
- `scripts/` holds the checks and tools: `timeline_json.mjs`, `contact_sheet.py`, `check_boundaries.py`, `motion_scan.py`, `droid_usage.py`, and `prices.json`.
- `references/` holds `storyboard.md`, `design-system.md`, `sound.md`, and `briefs.md`.
- `examples/droid-launch/` is a finished 75-second film made with this workflow.
