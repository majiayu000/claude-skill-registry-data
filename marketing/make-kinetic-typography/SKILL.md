---
name: make-kinetic-typography
description: Create one polished, accessible kinetic-typography animation from supplied copy and brand direction, with readable static typography, intentional split/reveal motion, deterministic frame review, and a runnable or rendered deliverable. Use for animated headlines, title cards, lyric or caption-led pieces, variable-font motion, and text-on-path animation; do not use for ordinary subtitles, a full product promo, static posters, or inaccessible character splitting.
---
# Make Kinetic Typography

## Catalog

- Display name: Make Kinetic Typography
- Categories: Video
- Status: Ready
- Route label: Accessible animated typography
- Tone: blue
- Short description: Turn approved copy into one readable, verified typography animation.

## What this skill does

- Locks copy, hierarchy, line breaks, fonts, and contrast before motion.
- Selects one motion grammar that supports meaning and reading order.
- Produces a deterministic deliverable and verifies representative frames plus playback.

## How to use

Provide exact copy and language, destination/format, dimensions, duration, brand direction, supplied fonts, audio or cue timestamps, and whether the result must run on the web or render to video.

#### Example

```text
Animate this exact six-word headline as a five-second 16:9 title card using this variable font. Reveal by word on the supplied beats, keep the final frame readable for two seconds, and include reduced-motion behavior.
```

## Workflow

1. Freeze exact copy, punctuation, reading order, language shaping needs, brand constraints, output dimensions, duration, and font choice. Do not require copyright or font-license authorization. Preserve supplied lyrics or quotations unless the user requests an edit.
2. Design the final static frame first: hierarchy, type scale, width, line breaks, tracking, line height, alignment, contrast, safe area, and fallback fonts. Confirm the type remains readable without motion.
3. Choose the least fragmented split that achieves the effect: line for calm hierarchy, word for rhythmic emphasis, character only for short copy. Preserve a complete accessible text node or label and hide visual fragments from assistive technology.
4. Define one primary reveal grammar—mask, directional wipe, opacity/blur, stagger, variable axis, path, or stroke—and only supporting accents. Match timing to semantic emphasis or supplied audio cues; avoid constant motion and hazardous flashing.
5. Implement with one deterministic animation driver suitable for the requested destination. Wait for fonts before measuring or splitting. Provide reduced-motion behavior that exposes the complete final text.
6. Create a reproducible review harness or render. Inspect start, key midpoints, and end for exact copy, glyph shaping, clipped ascenders/descenders, line-wrap changes, masks, contrast, font fallback, and final-state completeness.
7. Review normal-speed playback for cadence, reading time, audio sync, easing, motion sickness, and dropped frames. Repair the smallest failing layer; do not mix animation systems to hide timing defects.
8. Deliver the runnable source or rendered video, font/dependency notes, duration, dimensions, cue map, and verification frames. State any font substitution or browser/render limitation.


## User-facing output

- Media type: Runnable or rendered animated typography
- Default quantity: One animation
- Content per artifact: Exact approved copy with one coherent motion system
- Default layout: Destination-specific with safe-area protection
- Model policy: Deterministic code or motion tooling; no paid media generation
- Downstream use: Title cards, lyric/caption pieces, social video, web hero, or editorial motion
