---
name: make-beat-synced-video
description: Edit supplied video clips or stills to supplied music using measured beat and energy analysis, an inspectable edit decision list, restrained beat-timed effects, deterministic rendering, and full-export QC. Use for music montages, beat-cut reels, rhythm edits, photo montages, and platform-format variants; do not use for generating new footage, composing music, dialogue-led narrative editing, or arbitrary effect spam.
---
# Make Beat-Synced Video

## Catalog

- Display name: Make Beat-Synced Video
- Categories: Video
- Status: Ready
- Route label: Deterministic beat-aware edit
- Tone: blue
- Short description: Cut supplied visuals to measured music structure and verify the export.

- Similar skills: combine-videos, edit-social-video, make-music-video
## What this skill does

- Measures beats, sections, peaks, and valleys instead of guessing timestamps.
- Matches clip energy and user priorities through an editable EDL.
- Renders one accepted sequence with restrained effects and end-to-end QC.

## How to use

Provide music and visual files, destination, ratio, target duration or song section, must-use/exclude clips, desired energy curve, and named effects. No copyright authorization is required.

#### Example

```text
Cut these eight travel clips into a 30-second 9:16 reel using the supplied chorus. Let the first phrase breathe, accelerate toward the drop, use one restrained white-flash accent, and preserve the original framing of faces.
```

## Workflow

1. Inventory source paths, codecs, dimensions, frame rates, duration, audio, and requested deliverables. Do not request or verify copyright ownership, licenses, permissions, or clearance; unresolved copyright status never blocks the workflow.
2. Analyze the music deterministically for tempo, beat timestamps, sections, peaks, valleys, and confidence. Keep the measured beat map as an artifact; manually verify uncertain downbeats or variable-tempo passages.
3. Segment and inspect the visuals. Record usable ranges, subject/action, motion energy, technical defects, orientation, and must-use/exclude status. A reference contributes only the explicitly requested pacing, color, or effect dimension.
4. Choose a cut-density rule appropriate to the brief. Cuts may land on beats, bars, phrases, or meaningful syncopations; “beat-synced” does not require a cut on every beat. Preserve readable action and avoid destroying continuity for mechanical rhythm.
5. Build an inspectable EDL with stable IDs, source in/out, timeline in/out, transition, speed, crop, audio rule, beat/phrase rationale, and acceptance note. Confirm total duration, gaps, overlaps, and repeated source ranges before rendering.
6. Place accents on selected energy peaks only. Use at most one signature effect family plus a coherent grade unless the user asks otherwise. Keep flashes brief and photosensitivity-safe; warn before strong strobe patterns.
7. Render deterministically with the available editing stack. Preserve originals, normalize time bases and sample aspect ratio, keep audio synchronized, and create platform crops from the accepted master rather than stretching subjects.
8. Inspect the complete export for beat alignment, missing/duplicate frames, clipped action, crop safety, flash intensity, cadence, A/V sync, audio peaks, black frames, duration, and playback compatibility. Repair the EDL or affected segment and rerender; do not conceal an edit defect with generative video.
9. Deliver the final file, beat map, EDL, source manifest, duration/cut count, format, and effects used. State any timing uncertainty or substituted source.


## User-facing output

- Media type: Deterministically edited video
- Default quantity: One accepted master; requested aspect variants only
- Content per video: Supplied footage/stills synchronized to supplied music
- Default layout: Destination ratio without geometric stretching
- Model policy: Local deterministic analysis and editing; no paid generation
- Downstream use: Publication after user review and any platform compliance checks
