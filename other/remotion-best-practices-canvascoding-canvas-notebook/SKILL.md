---
name: remotion-best-practices
description: "Use this Canvas-owned clean-room skill when working with Remotion or React-based video generation. Trigger for Remotion projects, compositions, sequences, frame-based animation, rendering, captions, audio, video assets, templates, and debugging programmatic video output."
compatibility: "Requires a project with Remotion dependencies installed or a task that is explicitly planning a Remotion implementation."
license: "Canvas Notebook Sustainable Use License"
---

# Remotion Best Practices

This skill guides Remotion work in Canvas Notebook. It is a clean-room Canvas
skill; do not copy vendor skill material, hidden prompts, or proprietary rule
packs into this folder.

## Core Contract

- Use Remotion's frame-based model for animation. Avoid CSS animations and
  transitions for timeline-critical motion because renders must be deterministic
  by frame.
- Keep compositions editable React components. Avoid baking the whole video into
  a single prerendered asset unless the user asks for that.
- Put local media in the project's public asset path and reference it through
  Remotion-compatible asset helpers.
- Make dimensions, FPS, duration, and default props explicit in composition
  registration.
- Verify representative frames or short renders before delivering meaningful
  video changes.

## Workflow

1. Inspect the project: package scripts, Remotion version, composition registry,
   asset folders, styling system, and render command.
2. Choose the task mode: new composition, targeted edit, asset integration,
   captions/subtitles, audio/video timing, render debugging, or export.
3. Implement motion with frame-driven values and deterministic interpolation.
4. Keep timing centralized: FPS, durations, sequence offsets, and transitions
   should be easy to audit.
5. Render a still frame or short segment that covers the changed area. Inspect
   for blank frames, clipping, wrong asset paths, bad timing, text overflow, and
   audio/caption sync issues.

## Implementation Rules

- Use `useCurrentFrame` and video config values for time-based calculations.
- Use sequences for staged entrances, exits, and scene timing.
- Clamp interpolations where values should stop changing.
- Avoid viewport-dependent typography that can shift between preview and render.
- Prefer reusable components for repeated lower thirds, captions, cards, charts,
  and scene shells.
- Keep text within safe margins and test the longest expected copy.
- Use official Remotion documentation for version-specific APIs when uncertain.

## Media And Captions

- Confirm asset paths and dimensions before wiring media into a composition.
- For captions, parse source timing data once, normalize it, and render from a
  structured caption model.
- For audio, verify duration and align visual beats to frame boundaries.
- For transparent or alpha workflows, confirm the target codec/container
  supports the requested output.

## Final Checks

- Composition renders at the intended size, FPS, and duration.
- Representative frames are not blank and have correct framing.
- Text is readable and does not overflow.
- Assets load without broken paths.
- Audio, captions, and transitions line up with the timeline.
- Any skipped render verification is clearly reported.
