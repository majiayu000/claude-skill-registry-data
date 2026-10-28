---
name: course-kinetic-text-video
description: Use this skill to create course-style talking-head video edits with big lower-third kinetic text, champagne/gold highlight strips, circled emphasis words, face punch-ins, slow push-ins, flash transitions, and SFX cues in Remotion/Agent Zero workflows.
---

# Course Kinetic Text Video

Use this skill when the user asks for a course-style text edit, kinetic typography edit, text course style, circled emphasis words, or a blendable text-animation render for long-form talking-head video.

Do not use this as the default luxury overlay-card workflow. This is a separate text-animation lane.

## Core Rules

- Render full videos on the server/Hostinger worker, not locally.
- Do not commit or archive source videos, final MP4s, `.env`, API keys, SSH keys, or private transcripts in public repos.
- Use selective emphasis moments across the transcript, not full subtitles.
- Aim for one text emphasis about every 8-14 seconds, placed on idea boundaries.
- Use face/camera punch-ins when a word is circled. Do not zoom into the word itself.
- Add 1-3 slow push-ins in a long-form video for motion variety.
- Pair SFX with text hits, circled words, punch-ins, and flashes.

## Files To Use

- Remotion component kit: `assets/remotion/CourseOverlayKit.tsx`
- Remotion composition: `assets/remotion/CourseStyleEdit.tsx`
- Props builder: `scripts/build-course-props.mjs`
- Moment-plan example: `examples/moment-plan.example.json`
- Style reference: `references/style-spec.md`
- Render workflow: `references/hostinger-render-workflow.md`
- SFX sourcing: `references/sfx-sources.md`

## Workflow

1. Verify source metadata with `ffprobe`.
2. Transcribe the video.
3. Pick 8-14 second idea-boundary moments from the transcript.
4. Write a moment plan:
   - `start`
   - `duration`
   - `lines`
   - `circleWord`
   - `zoom`
   - optional `flash`
5. Generate Remotion props with:
   `node scripts/build-course-props.mjs examples/moment-plan.example.json props/course-props.json`
6. Render proof PNGs first.
7. Inspect text size, lower-third placement, circle position, face zoom, and SFX timing.
8. Render full MP4 on Hostinger only.
9. Download final MP4, preview PNGs, render logs, props, and transcript.
10. Save a process log so the successful render can be restored.

## Visual Defaults

- Text: bold white, lower third.
- Highlight: champagne/gold, slightly rotated.
- Circle: pale gold SVG stroke reveal.
- Shade: black bottom gradient for readability.
- Punch zoom: `1.07-1.085`.
- Slow push-in: about 5 seconds, `1.04-1.06`.
- Flash: 10 frames, white or cool wash.

## SFX Defaults

- `course-pop.mp3`: text entrance.
- `course-ding.mp3`: circled word plus face punch.
- `course-whoosh.mp3`: flash or slow push-in.

If SFX files are missing, do not block the edit. Use placeholders or generate props with empty `sfxCues`, then add SFX later.
