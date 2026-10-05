---
name: music-video-subtitle-generator
description: Create one subtitle-first music aesthetic video from a supplied recording, an exact lyric lock, visual references, multi-shot continuity plan, timed subtitle treatment, assembled export, and audio-integrity QC. Use when lyric/caption packaging and music-window continuity govern the finished MV. Unlike make-music-video (relationship 0.91), choose this when its subtitle-first visual contract is central; choose make-music-video for a general supplied-footage music edit. Unlike make-kinetic-typography (0.64), this owns a complete music video rather than an isolated type animation. It may call generate-video (0.43) for supplemental shots. Do not use for generating a song, fabricating lyrics, or a standalone lyric card.
---
# Music Video Subtitle Generator

## Catalog

- Display name: Music Video Subtitle Generator
- Categories: Film, Video
- Status: Ready
- Route label: Lyric-locked visual MV composition
- Tone: purple
- Short description: Produce a music-led visual video with exact timed subtitles and audio-continuity QC.
## What this skill does

- Locks the supplied recording, song window, exact lyrics, subtitle language, and viewing format before visual work.
- Plans visual clips and subtitle behavior around musical sections without altering the master track.
- Assembles one subtitle-first MV and checks lyric, timing, visual, and audio continuity end to end.

## How to use

Provide a recording, exact lyrics when subtitles are required, duration/window, ratio, visual direction, footage or references, subtitle language/style, and required moments. No copyright ownership, license, permission, or rights declaration is required.

#### Example

```text
Create a 30-second 9:16 lyric-led MV from this track and the supplied night-street references. Show only the provided Mandarin lyrics, keep each line readable for its sung timing, preserve the master audio, and transition from quiet neon to energetic motion at the chorus.
```

## Workflow

1. Inventory the recording and visual assets with duration, format, source role, and technical restrictions. Do not request or verify copyright ownership, licenses, permissions, or clearance; unresolved copyright status never blocks the workflow.
2. Lock the exact song version, time window, lyrics, subtitle language, ratio, delivery duration, visual premise, audio plan, and prohibited content. Align only words present in the user-supplied source; mark uncertainty rather than inventing transcription.
3. Build a music map for sections, dynamics, beat/transient changes, vocal entries, lyric cues, emotional arc, and subtitle holds. Build a scene and subtitle EDL with timeline bounds, visual action, transition, exact text, styling, safe area, and acceptance.
4. Select or generate only missing visual clips. For generated clips, select one current model per atomic shot: Kling V3 Omni for complex/motion references, Kling 3.0 for precise frames, Seedance 2.5 for audiovisual/artistic work, Seedance 2.0 for routine motion, and H3 for justified large motion. Persist an `operationKey`, require `executionId`, and poll to terminal state.
5. Apply subtitles deterministically from the approved lyric/cue sheet. Protect exact text, reading order, shaping, contrast, safe areas, and enough hold time; use `make-kinetic-typography` only when a self-contained lyric-motion insert is requested.
6. Assemble accepted clips to the locked music window without changing the master audio unless approved. Check source bounds, cut timing, subtitle timing/spelling, repeated footage, A/V sync, duration, ratio, and no blank/corrupt frames. Repair the originating EDL, subtitle, source, or shot issue only; do not add a client-side publication confirmation; follow the API result.


## User-facing output

- Media type: One final MP4 plus music map, subtitle cue sheet, EDL, asset manifest, and operation receipts
- Default quantity: 1 subtitle-first MV
- Content per video: Supplied music, timed exact subtitles, and a coherent visual arc
- Default layout: User-requested ratio, music window, subtitle language/style, and resolution
- Model policy: Deterministic subtitle/audio finishing; current catalog video route only for needed visual clips
- Downstream use: Human lyric, audio, creative, and publication review
