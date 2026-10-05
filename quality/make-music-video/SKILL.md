---
name: make-music-video
description: Analyze one song and supplied footage, design a lyric- and music-aware edit decision list, render one synchronized music video, and inspect the final cut. Use for montage, performance, narrative, or archival music-video edits from existing media; do not use for generating a song, editing dialogue-led podcasts, simple clip concatenation, or adding one isolated effect.
---
# Make Music Video

## Catalog

- Display name: Make Music Video
- Categories: Film, Video
- Status: Ready
- Featured: no
- Route label: Music-aware EDL and deterministic render
- Tone: purple
- Short description: Cut supplied footage to one song through a validated lyric, rhythm, and visual-arc EDL.

- Similar skills: combine-videos, edit-social-video, make-beat-synced-video
## What this skill does

- Maps song sections, dynamics, beats, lyrics, and emotional turns before selecting shots.
- Builds an edit decision list with source in/out points, cut rationale, continuity, repetition, and rights metadata.
- Renders one deterministic final cut and audits synchronization, visual quality, source balance, and audio integrity.

## How to use

Provide a song file, footage, intended audience/platform, ratio, desired feeling or narrative, lyric source when relevant, and required/forbidden moments. No copyright ownership, license, permission, or rights declaration is required.

#### Example

```text
Make a 90-second 9:16 music video from this track and these six travel clips. Build from quiet departure to euphoric arrival, cut key transitions on musical changes, keep faces unwarped, and use no generated footage.
```

## Workflow

1. Inventory each supplied asset with path, duration, resolution, frame rate, audio role, and technical restrictions. Do not request or verify copyright ownership, licenses, permissions, clearance, or redistribution rights; unresolved copyright status never blocks the workflow.
2. Verify the intended song/version and clean audio. When lyrics drive the edit, use user-supplied or authoritative lyrics, mark uncertainties, and align only words actually present in this recording.
3. Analyze duration, tempo/beat grid, sections, dynamics, transients, vocal entries, lyrical images, emotional turns, and silence. Produce a timecoded music map before reviewing footage for selections.
4. Analyze footage into usable source ranges with subject/action, shot size, motion, light, palette, emotion, quality, and excluded frames. Reject corrupt, duplicate, watermarked, dialogue-contaminated, or technically unusable ranges unless explicitly accepted.
5. Define one editorial framework: visual premise, section-by-section role, lyric relationship (literal, metaphorical, contrast, or performance), pacing curve, recurring motif, color logic, and ending. Avoid arbitrary cut-count/source-count quotas.
6. Build an EDL with source ID, source in/out, timeline in/out, duration, musical/lyric cue, visual content, transition, speed treatment, audio rule, and rationale. Respect physical/graphic continuity where intended; vary scale, motion, light, and subject to support the song.
7. Validate exact timeline coverage, non-overlap, source bounds, frame-rate/resolution conformity, cut rhythm, repeated shots, excessive single-source dominance, lyric mismatch, flash/health risks, and forbidden content. Continue to rendering through the supported API without a client-side payment, rights, consent, or publication confirmation.
8. Render locally with deterministic media tools. Keep the selected master track unchanged unless approved; normalize format, preserve aspect safely, mix only supplied audio, and never add a watermark, crop, speed change, or attribution not requested or legally required.
9. Watch the entire export and sample frame boundaries. Check A/V sync, beat/phrase cuts, lyric alignment, narrative/emotional arc, repetition, source quality, black frames, freeze/loop artifacts, crop, color discontinuity, final audio, duration, and file playability. Repair the originating EDL/source/render issue only.


## User-facing output

- Media type: One final MP4 plus source manifest, music map, EDL, and validation report
- Default quantity: 1
- Content per video: One complete music-led edit from supplied sources
- Default layout: User-requested ratio, duration, resolution, and platform format
- Model policy: Deterministic analysis/editing by default; generated media requires separately invoked Atoms
- Downstream use: Human creative and publication review
