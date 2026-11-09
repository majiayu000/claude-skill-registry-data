---
name: cut-list
description: Turn a transcript, footage log or beat sheet into an edit plan (cut list) with in/out points, durations, transitions and pacing notes, with an optional EDL. Use when the user is planning a rough cut, tightening an edit, hitting a target runtime, or building a vertical short-form edit.
license: MIT
metadata:
  author: Benjamin Leleu
  version: "1.0.0"
---

# Cut List

Produce an edit plan an editor can follow in Premiere, DaVinci Resolve or any NLE.

## Inputs to collect

Ask only for what is missing:

1. Source material: transcript with timecodes, footage log, or a beat sheet (required)
2. Target runtime and platform (e.g. 60 s vertical, 5 min YouTube, 90 s trailer)
3. Frame rate of the project (needed for any timecode math and the EDL)
4. Tone and rhythm references

## Process

1. Define the **structure** first: hook, build, payoff (adapt to format). For short-form vertical, the **hook must land in the first 1-2 seconds**.
2. Do the **runtime math**: sum durations and compare to target. If over, say what to cut and why, and propose the first cuts rather than leaving it vague.
3. Choose cuts by **purpose**: each clip must advance information, emotion or rhythm. Flag clips that do none.
4. Plan **rhythm**: alternate long and short, put the strongest moment at the climax, avoid three similar-length shots in a row unless intentional.
5. Specify **transitions** only where they have a job (match cut, J/L cut for dialogue, impact cut on a sound hit). Default to straight cuts.
6. Note **audio**: where music hits land, dialogue overlaps, room tone needs.

## Output format

Start with a one-line **edit concept** and the **runtime math** (current total, target, delta).

### Cut table

| # | Source / clip | In | Out | Duration | Purpose | Transition | Audio / notes |
|---|---------------|----|-----|----------|---------|------------|---------------|

Use `HH:MM:SS:FF` timecode at the stated frame rate. If the source has no timecodes, use clip names and estimated durations and say so.

### Pacing notes
Three to five bullets: where the edit speeds up, where it breathes, where it risks dragging.

### Trim candidates (if over runtime)
Ordered list of what to cut first, with the cost of each cut.

### Optional: EDL (CMX3600)
Only if the user asks, or if all in/out points are real timecodes. Format:

```
TITLE: PROJECT_NAME
FCM: NON-DROP FRAME

001  CLIP01   V     C        01:00:00:00 01:00:02:12 01:00:00:00 01:00:02:12
* FROM CLIP NAME: clip_name.mov
```

Always tell the user to import the EDL into a test project and check the first events before trusting the rest, since reel names and drop-frame settings vary by NLE.

## Rules

- Never invent footage, dialogue or timecodes. If something is missing, ask or mark it as an estimate.
- Be explicit about what is a creative suggestion and what follows from the numbers.
- For vertical edits: respect safe zones for captions and keep key action centered.
