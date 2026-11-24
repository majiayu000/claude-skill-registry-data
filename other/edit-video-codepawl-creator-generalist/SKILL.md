---
name: edit-video
description: "Edit video in the tool the user has: DaVinci Resolve (Edit, Fusion, Color, Deliver, scripting), CapCut, Premiere Pro and After Effects, Kdenlive, Shotcut or FFmpeg. Covers cutting Shorts and long videos, pacing, beat sync, captions, transitions, speed ramps, titles, grade, loudness, export per platform and a map from paid plugins to free tools. Use for any editing step, \"edit this video\", \"cut a Short\", \"speed ramp\", \"color grade\", \"burn captions\", \"Fusion macro\" (\"edit video\")."
license: MIT
---

# Edit Video

A tool skill. The generalist skills (`2d-generalist`, `3d-generalist`) decide the story, the look and the order of
work. This skill says how to cut, time, finish and export the video in the editor the user has, by exact UI path,
by script or by command.

## When to use

- Cutting footage or renders into a piece, a Short or a reel, with captions, music, transitions and effects.
- A retime, title, grade, composite or export in any editor, or a batch job with FFmpeg.
- Not for building video in code (Remotion) and not for designing sound. Mix levels here, design sound elsewhere.

## Pick the editor

Use the editor the user already has. When nothing decides it: DaVinci Resolve for a full edit with effects and grade
(the free edition covers most work); CapCut for a fast phone-first Short with auto captions; FFmpeg for batch,
scripted or headless jobs; Kdenlive or Shotcut when the user wants open source; Premiere and After Effects when the
user already pays for them. Ask before suggesting a paid tool.

## Routing

| The task is | Read |
| --- | --- |
| Cutting craft in any editor: hook, pacing, J and L cuts, which joins Shorts really use (hard cuts, no crossfades), beat sync, captions, safe zones, platform export | `references/editing-craft.md` |
| Any Resolve step: free vs Studio, rules, scripting, checks | `references/resolve-basics.md` first |
| Resolve Anim Curves, splines, beat sync, markers, scene cut detection | `references/edit-page-and-keyframes.md` |
| Resolve transitions, stingers, zooms, wipes on adjustment clips | `references/transitions.md` |
| Resolve shakes, twitches, punch, camera shake | `references/shakes-and-camera.md` |
| Resolve optical flow retime, speed ramps | `references/retime-and-speed.md` |
| Resolve Fusion effects, masks, keying, macros | `references/fusion-effects.md` |
| Resolve titles, Text+, 3D text, morphs, subtitles | `references/text-and-typography.md` |
| Resolve grade, film look, overlays, hue tricks | `references/color.md` |
| Resolve hotkeys, cache, settings, packs, troubleshooting | `references/workflow-and-settings.md` |
| CapCut desktop or mobile | `references/capcut.md` |
| Premiere Pro or After Effects | `references/premiere-and-after-effects.md` |
| Kdenlive or Shotcut | `references/open-source-editors.md` |
| FFmpeg: trim, join, reframe to 9:16, burn captions, loudness, speed, encode | `references/ffmpeg.md` |
| An After Effects, Premiere, Twixtor, Saber or Element 3D look in a free tool | `references/paid-to-free.md` |
| After Effects expressions (wiggle, loopOut, time*N) in Fusion, Blender or code; an AE effect to free-tool map; AE hotkeys, render settings, free resources | `references/after-effects-motion-design.md` |

Long references open with a reading map. Find the exact entry, then read the whole entry with its steps and source.

## How to work

1. Read the brief from the calling skill. When the user called this skill directly, ask about platform, length,
   aspect and look first (at most 4 questions, each with options and a recommended default).
2. Set the timeline to the delivery format first: 1080x1920 for vertical Shorts, 1920x1080 for landscape, and the
   frame rate of the footage.
3. Cut the story before effects: rough cut, then timing to the voice or the beat, then transitions, titles, grade,
   captions and the mix.
4. Keep effects on adjustment layers or clips so the cut can still change.
5. Export a low quality preview of the whole piece first. Export full quality only after the user signs off.

## Checks before handing off

- Extract frames at each cut, at the peak of each effect and at the end, and look at them. Check that text fits
  inside the platform safe zone, edges show no ghosting, and speed ramps land on the beat.
- No eyebrow or helper text: no small muted line under or above a title (taglines, "humans: X / agents: Y",
  "paste into ..."), and no corner caption naming the shot, step or tool. The voice carries it; text on screen is
  only what the viewer must read (the title itself, code, a command).
- Run `scripts/check_blended_cuts.py` on the export: it lists crossfades and dissolves between shots, which read as a
  slideshow; replace each with a hard cut or one of the joins in `references/editing-craft.md`.
- Measure the loudness of the export (`references/ffmpeg.md`, "Measure loudness") against the platform target.
- Check duration, resolution, frame rate and codec with `ffprobe` against the platform limits.
- Say which paid or Studio-only features were used and which free fallback replaced them.
